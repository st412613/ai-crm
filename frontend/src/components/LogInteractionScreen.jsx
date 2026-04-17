import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { clearExtractedData } from '../store/chatSlice';
import { loadInteractions } from '../store/interactionsSlice';
import InteractionForm from './InteractionForm';
import ChatInterface from './ChatInterface';
import './LogInteractionScreen.css';

function LogInteractionScreen() {
  const [extractedData, setExtractedData] = useState(null);
  const [isChatOpen, setIsChatOpen] = useState(true);
  const dispatch = useDispatch();

  const handleExtractedData = (data) => {
    setExtractedData(data);
    dispatch(clearExtractedData());
    if (!data.clear_form) {
      setIsChatOpen(false); // Close chat after successfully logging and extracting data
    }
    // Refresh interaction list
    setTimeout(() => dispatch(loadInteractions({})), 500);
  };

  const handleClearExtracted = () => {
    setExtractedData(null);
  };

  return (
    <div className="log-interaction-screen">
      <header className="app-header">
        <div className="header-left">
          <div className="header-logo">
            <span className="logo-icon">💊</span>
            <h1>CRM<span className="logo-accent">HCP</span></h1>
          </div>
          <span className="header-subtitle">AI-First Healthcare CRM</span>
        </div>
        <div className="header-right">
          <span className="user-badge">Field Rep</span>
        </div>
      </header>

      <div className="screen-content">
        <div className="main-panel">
          <div className="form-chat-container">
            <div className="form-panel">
              {!isChatOpen && (
                <div style={{ marginBottom: 15, display: 'flex', justifyContent: 'flex-end' }}>
                  <button onClick={() => setIsChatOpen(true)} className="chip-btn" style={{ background: 'var(--accent)', color: 'white', border: 'none' }}>
                    💬 Open AI Assistant
                  </button>
                </div>
              )}
              <InteractionForm
                extractedData={extractedData}
                onClearExtracted={handleClearExtracted}
              />
            </div>
            {isChatOpen && (
              <div className="chat-panel" style={{ position: 'relative' }}>
                <button 
                  onClick={() => setIsChatOpen(false)}
                  style={{ position: 'absolute', top: 12, right: 16, background: 'transparent', border: 'none', fontSize: 18, cursor: 'pointer', color: 'var(--text-secondary)', zIndex: 10 }}
                >
                  ✕
                </button>
                <ChatInterface onExtractedData={handleExtractedData} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default LogInteractionScreen;
