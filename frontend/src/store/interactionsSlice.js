import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { fetchInteractions, createInteraction, updateInteraction, deleteInteraction } from '../api';

export const loadInteractions = createAsyncThunk('interactions/load', async ({ hcpId, search } = {}) => {
  const res = await fetchInteractions(hcpId, search);
  return res.data;
});

export const addInteraction = createAsyncThunk('interactions/add', async (data) => {
  const res = await createInteraction(data);
  return res.data;
});

export const editInteraction = createAsyncThunk('interactions/edit', async ({ id, data }) => {
  const res = await updateInteraction(id, data);
  return res.data;
});

export const removeInteraction = createAsyncThunk('interactions/remove', async (id) => {
  await deleteInteraction(id);
  return id;
});

const interactionsSlice = createSlice({
  name: 'interactions',
  initialState: {
    items: [],
    loading: false,
    error: null,
    selectedId: null,
  },
  reducers: {
    selectInteraction: (state, action) => {
      state.selectedId = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loadInteractions.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(loadInteractions.fulfilled, (state, action) => { state.loading = false; state.items = action.payload; })
      .addCase(loadInteractions.rejected, (state, action) => { state.loading = false; state.error = action.error.message; })
      .addCase(addInteraction.fulfilled, (state, action) => { state.items.unshift(action.payload); })
      .addCase(editInteraction.fulfilled, (state, action) => {
        const idx = state.items.findIndex(i => i.id === action.payload.id);
        if (idx >= 0) state.items[idx] = action.payload;
      })
      .addCase(removeInteraction.fulfilled, (state, action) => {
        state.items = state.items.filter(i => i.id !== action.payload);
      });
  },
});

export const { selectInteraction } = interactionsSlice.actions;
export default interactionsSlice.reducer;
