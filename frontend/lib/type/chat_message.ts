export default interface ChatMessageType {
  id: string;
  role: "assistant" | "user";
  message: string;
}
