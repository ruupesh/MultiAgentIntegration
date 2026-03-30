import { baseApi } from "./baseApi";
import type { ChatClearResponse, ChatRequest, ChatResponse } from "@/lib/types";

export const chatApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    sendMessage: builder.mutation<ChatResponse, ChatRequest>({
      query: (body) => ({
        url: "/chat",
        method: "POST",
        body,
      }),
    }),
    clearSession: builder.mutation<ChatClearResponse, string>({
      query: (sessionId) => ({
        url: `/chat/session/${sessionId}`,
        method: "DELETE",
      }),
    }),
  }),
});

export const { useSendMessageMutation, useClearSessionMutation } = chatApi;
