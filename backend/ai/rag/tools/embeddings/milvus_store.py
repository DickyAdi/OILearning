from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from datetime import datetime

COLLECTION_NAME = "dokumen_rag"
DIMENSION = 1024  # Sesuaikan dengan model embedding kamu

def init_collection():
    # 1) Connect
    connections.connect("default", host="localhost", port="19530")

    # 2) Create collection if not exists
    if not utility.has_collection(COLLECTION_NAME):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="filename", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="timestamp", dtype=DataType.VARCHAR, max_length=100),
        ]
        schema = CollectionSchema(fields, description="RAG Document Collection")

        collection = Collection(COLLECTION_NAME, schema)

        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128},
        }
        collection.create_index("embedding", index_params)
    else:
        collection = Collection(COLLECTION_NAME)

    collection.load()
    return collection


def insert_embeddings(collection, embeddings, texts, filename):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = [
        embeddings,
        texts,
        [filename] * len(texts),
        [timestamp] * len(texts),
    ]

    collection.insert(data)
    collection.flush()
