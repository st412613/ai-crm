import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

// HCP APIs
export const fetchHCPs = (search = '') => api.get(`/hcps?search=${search}`);
export const createHCP = (data) => api.post('/hcps', data);

// Interaction APIs
export const fetchInteractions = (hcpId = null, search = '') => {
  let url = '/interactions?';
  if (hcpId) url += `hcp_id=${hcpId}&`;
  if (search) url += `search=${search}`;
  return api.get(url);
};
export const createInteraction = (data) => api.post('/interactions', data);
export const updateInteraction = (id, data) => api.put(`/interactions/${id}`, data);
export const deleteInteraction = (id) => api.delete(`/interactions/${id}`);

// Chat API
export const sendChatMessage = (message, conversationHistory = []) =>
  api.post('/chat', {
    message,
    conversation_history: conversationHistory,
  });

// Follow-up APIs
export const fetchFollowUps = (interactionId = null) => {
  let url = '/follow-ups?';
  if (interactionId) url += `interaction_id=${interactionId}`;
  return api.get(url);
};
export const createFollowUp = (data) => api.post('/follow-ups', data);

export default api;
