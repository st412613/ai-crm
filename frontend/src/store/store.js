import { configureStore } from '@reduxjs/toolkit';
import interactionsReducer from './interactionsSlice';
import chatReducer from './chatSlice';
import hcpReducer from './hcpSlice';

export const store = configureStore({
  reducer: {
    interactions: interactionsReducer,
    chat: chatReducer,
    hcps: hcpReducer,
  },
});

export default store;
