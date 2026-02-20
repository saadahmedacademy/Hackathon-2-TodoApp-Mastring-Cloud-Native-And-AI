'use client';

import { createContext, useContext } from 'react';

interface ChatContextType {
  openChat: () => void;
}

export const ChatContext = createContext<ChatContextType>({ openChat: () => {} });

export function useChatContext() {
  return useContext(ChatContext);
}
