import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { fetchHCPs } from '../api';

export const loadHCPs = createAsyncThunk('hcps/load', async (search = '') => {
  const res = await fetchHCPs(search);
  return res.data;
});

const hcpSlice = createSlice({
  name: 'hcps',
  initialState: {
    items: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(loadHCPs.pending, (state) => { state.loading = true; })
      .addCase(loadHCPs.fulfilled, (state, action) => { state.loading = false; state.items = action.payload; })
      .addCase(loadHCPs.rejected, (state, action) => { state.loading = false; state.error = action.error.message; });
  },
});

export default hcpSlice.reducer;
