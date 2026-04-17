import { useState, useEffect, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { sendMessage, addUserMessage, clearChat } from '../store/chatSlice';
import './ChatInterface.css';

function ChatInterface({ onExtractedData }) {
  const [input, setInput] = useState('');
  const dispatch = useDispatch();
  const { messages, loading, extractedData, lastToolUsed } = useSelector(s => s.chat);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (extractedData && onExtractedData) {
      onExtractedData(extractedData);
    }
  }, [extractedData]);

  const handleSend = () => {
    if (!input.trim() || loading) return;
    const msg = input.trim();
    setInput('');
    dispatch(addUserMessage(msg));
    const history = messages.map(m => ({ role: m.role, content: m.content }));
    dispatch(sendMessage({ message: msg, history }));
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const getToolBadge = (tool) => {
    const labels = {
      log_interaction: '📝 Logged',
      edit_interaction: '✏️ Edited',
      search_hcp_history: '🔍 Searched',
      schedule_follow_up: '📅 Scheduled',
      generate_interaction_report: '📊 Report',
    };
    return labels[tool] || tool;
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="chat-header-icon">🤖</div>
        <div className="chat-header-text">
          <h3>AI Assistant</h3>
          <p>Log interaction details here via chat</p>
        </div>
      </div>

      <div className="chat-messages">
        <div className="chat-bubble system">
          <p>Log interaction details here (e.g., "Met Dr. Smith, discussed Prodo-X efficacy, positive sentiment, shared brochure") or ask for help.</p>
        </div>

        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-bubble ${msg.role}`}>
            {msg.role === 'assistant' && lastToolUsed && idx === messages.length - 1 && (
              <span className="tool-badge">{getToolBadge(lastToolUsed)}</span>
            )}
            <p>{msg.content}</p>
          </div>
        ))}

        {loading && (
          <div className="chat-bubble assistant typing">
            <div className="typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <div className="chat-input-wrapper">
          <textarea
            id="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe Interaction..."
            rows={1}
            disabled={loading}
          />
          <button
            id="chat-send-btn"
            className="chat-send-btn"
            onClick={handleSend}
            disabled={!input.trim() || loading}
          >
            <span className="send-icon">A</span>
            Log
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatInterface;
