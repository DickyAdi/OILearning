import { create } from "zustand";
import { ChatConversationType } from "../type/conversation";

interface ConversationStoreState {
  conversations: ChatConversationType[];
  currentConversationId: string | null;
  createConversation: (title: string) => void;
  switchConversation: (id: string) => void;
}

export const conversationStore = create<ConversationStoreState>((set) => ({
  conversations: [],
  currentConversationId: null,
  createConversation: (title: string) => {
    set((state) => {
      const today = new Date();
      const new_conv: ChatConversationType = {
        id: crypto.randomUUID(),
        title: title,
        createdAt: today.toISOString(),
      };
      return {
        conversations: [new_conv, ...state.conversations],
        currentConversationId: new_conv.id,
      };
    });
  },
  switchConversation: (id: string) => set({ currentConversationId: id }),
}));
