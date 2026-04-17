import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { sendChatMessage } from '../api';

export const sendMessage = createAsyncThunk('chat/send', async ({ message, history }) => {
  const res = await sendChatMessage(message, history);
  return res.data;
});

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [],
    loading: false,
    error: null,
    extractedData: null,
    lastInteractionId: null,
    lastToolUsed: null,
  },
  reducers: {
    addUserMessage: (state, action) => {
      state.messages.push({ role: 'user', content: action.payload });
    },
    clearChat: (state) => {
      state.messages = [];
      state.extractedData = null;
      state.lastInteractionId = null;
      state.lastToolUsed = null;
    },
    clearExtractedData: (state) => {
      state.extractedData = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.loading = false;
        state.messages.push({ role: 'assistant', content: action.payload.response });
        state.extractedData = action.payload.extracted_data;
        state.lastInteractionId = action.payload.interaction_id;
        state.lastToolUsed = action.payload.tool_used;
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
        state.messages.push({ role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' });
      });
  },
});

export const { addUserMessage, clearChat, clearExtractedData } = chatSlice.actions;
export default chatSlice.reducer;
