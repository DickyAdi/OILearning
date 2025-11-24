import { create } from "zustand";
import ChatMessageType from "../type/chat_message";

interface MessageStoreState {
  messages: ChatMessageType[];
  appendMessage: ({
    role,
    message,
  }: {
    role: "assistant" | "user";
    message: string;
  }) => void;
}

export const messageStore = create<MessageStoreState>((set) => ({
  messages: [],
  appendMessage: ({
    role,
    message,
  }: {
    role: "assistant" | "user";
    message: string;
  }) =>
    set((state) => {
      const new_message: ChatMessageType = {
        id: crypto.randomUUID(),
        role: role,
        message: message,
      };
      return {
        messages: [...state.messages, new_message],
      };
    }),
}));
