"use client";

import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import DeleteSweepIcon from "@mui/icons-material/DeleteSweepOutlined";
import ChatWindow from "@/components/chat/ChatWindow";
import ChatInput from "@/components/chat/ChatInput";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { clearMessages } from "@/store/slices/chatSlice";
import { useClearSessionMutation } from "@/store/api/chatApi";

export default function ChatPage() {
  const dispatch = useAppDispatch();
  const { sessionId } = useAppSelector((state) => state.chat);
  const [clearSession] = useClearSessionMutation();

  const handleClearConversation = async () => {
    try {
      await clearSession(sessionId).unwrap();
    } catch {
      // Always clear local UI state even if backend session cleanup fails.
    } finally {
      dispatch(clearMessages());
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
      }}
    >
      {/* Header */}
      <Box
        sx={{
          px: 3,
          py: 1.5,
          borderBottom: "1px solid rgba(255,255,255,0.08)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <Typography variant="h6" sx={{ fontSize: 16 }}>
          Chat
        </Typography>
        <IconButton
          size="small"
          title="Clear conversation"
          onClick={handleClearConversation}
        >
          <DeleteSweepIcon fontSize="small" />
        </IconButton>
      </Box>

      <ChatWindow />
      <ChatInput />
    </Box>
  );
}
