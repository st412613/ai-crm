import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { loadHCPs } from '../store/hcpSlice';
import { addInteraction } from '../store/interactionsSlice';
import './InteractionForm.css';

function InteractionForm({ extractedData, onClearExtracted }) {
  const dispatch = useDispatch();
  const { items: hcps } = useSelector(s => s.hcps);
  const [hcpSearch, setHcpSearch] = useState('');
  const [showHcpDropdown, setShowHcpDropdown] = useState(false);
  const [success, setSuccess] = useState(false);

  const initialFormState = {
    hcp_id: '',
    hcp_name: '',
    interaction_type: 'Meeting',
    date: new Date().toISOString().split('T')[0],
    time: new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }), // Use 24h format for <input type="time">
    attendees: '',
    topics_discussed: '',
    notes: '',
    sentiment: 'Positive',
    outcomes: '',
    materials_shared: '',
    samples_distributed: '',
    follow_up_actions: '',
  };

  const [form, setForm] = useState(initialFormState);

  useEffect(() => {
    dispatch(loadHCPs());
  }, [dispatch]);

  // Auto-fill from AI chat
  useEffect(() => {
    if (extractedData) {
      if (extractedData.clear_form) {
        setForm(initialFormState);
        setHcpSearch('');
        if (onClearExtracted) onClearExtracted();
        return;
      }
      
      setForm(prev => {
        const updated = { ...prev };
        if (extractedData.hcp_name !== undefined && extractedData.hcp_name !== null) {
          updated.hcp_name = extractedData.hcp_name;
          const searchName = extractedData.hcp_name.toLowerCase();
          const found = hcps.find(h => h.name.toLowerCase().includes(searchName));
          if (found) {
            updated.hcp_id = found.id;
          } else if (extractedData.hcp_name === '') {
            updated.hcp_id = '';
          }
        }
        if (extractedData.interaction_type !== undefined) updated.interaction_type = extractedData.interaction_type || 'Meeting';
        if (extractedData.date !== undefined) updated.date = extractedData.date;
        if (extractedData.time !== undefined) updated.time = extractedData.time;
        if (extractedData.attendees !== undefined) updated.attendees = extractedData.attendees;
        if (extractedData.topics_discussed !== undefined) updated.topics_discussed = extractedData.topics_discussed;
        if (extractedData.sentiment !== undefined) updated.sentiment = extractedData.sentiment || 'Neutral';
        if (extractedData.outcomes !== undefined) updated.outcomes = extractedData.outcomes;
        if (extractedData.materials_shared !== undefined) updated.materials_shared = extractedData.materials_shared;
        if (extractedData.samples_distributed !== undefined) updated.samples_distributed = extractedData.samples_distributed;
        if (extractedData.follow_up_actions !== undefined) updated.follow_up_actions = extractedData.follow_up_actions;
        if (extractedData.notes !== undefined) updated.notes = extractedData.notes;
        return updated;
      });

      if (extractedData.hcp_name !== undefined) {
        setHcpSearch(extractedData.hcp_name);
      }

      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
      
      // Clear extraction data from parent
      if (onClearExtracted) onClearExtracted();
    }
  }, [extractedData, hcps, onClearExtracted]);

  const handleChange = (field, value) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  const handleHcpSelect = (hcp) => {
    setForm(prev => ({ ...prev, hcp_id: hcp.id, hcp_name: hcp.name }));
    setHcpSearch(hcp.name);
    setShowHcpDropdown(false);
  };

  const handleHcpSearch = (val) => {
    setHcpSearch(val);
    setShowHcpDropdown(true);
    dispatch(loadHCPs(val));
  };

  const resetForm = () => {
    setForm(initialFormState);
    setHcpSearch('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.hcp_id) {
      alert('Please select an HCP');
      return;
    }
    dispatch(addInteraction({
      hcp_id: form.hcp_id,
      interaction_type: form.interaction_type,
      date: form.date,
      time: form.time,
      attendees: form.attendees,
      topics_discussed: form.topics_discussed,
      notes: form.notes,
      sentiment: form.sentiment,
      outcomes: form.outcomes,
      materials_shared: form.materials_shared,
      samples_distributed: form.samples_distributed,
      follow_up_actions: form.follow_up_actions,
    }));
    setSuccess(true);
    setTimeout(() => setSuccess(false), 3000);
    resetForm();
  };

  const filteredHcps = (hcps || []).filter(h =>
    h.name.toLowerCase().includes((hcpSearch || '').toLowerCase())
  );

  return (
    <form className="interaction-form" onSubmit={handleSubmit}>
      <h2 className="form-title">Log HCP Interaction</h2>

      {success && (
        <div className="success-banner">
          ✅ Interaction logged successfully!
        </div>
      )}

      <div className="form-section">
        <h4 className="section-label">Interaction Details</h4>

        <div className="form-row">
          <div className="form-group hcp-search-group">
            <label>HCP Name</label>
            <input
              id="hcp-name-input"
              type="text"
              value={hcpSearch}
              onChange={(e) => handleHcpSearch(e.target.value)}
              onFocus={() => setShowHcpDropdown(true)}
              onBlur={() => setTimeout(() => setShowHcpDropdown(false), 200)}
              placeholder="Search or select HCP..."
              autoComplete="off"
            />
            {showHcpDropdown && filteredHcps.length > 0 && (
              <div className="hcp-dropdown">
                {filteredHcps.map(hcp => (
                  <div
                    key={hcp.id}
                    className="hcp-dropdown-item"
                    onMouseDown={() => handleHcpSelect(hcp)}
                  >
                    <span className="hcp-name">{hcp.name}</span>
                    <span className="hcp-specialty">{hcp.specialty}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="form-group">
            <label>Interaction Type</label>
            <select
              id="interaction-type-select"
              value={form.interaction_type}
              onChange={(e) => handleChange('interaction_type', e.target.value)}
            >
              <option value="Meeting">Meeting</option>
              <option value="Call">Call</option>
              <option value="Email">Email</option>
              <option value="Visit">Visit</option>
              <option value="Conference">Conference</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Date</label>
            <input
              id="date-input"
              type="date"
              value={form.date}
              onChange={(e) => handleChange('date', e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Time</label>
            <input
              id="time-input"
              type="time"
              value={form.time}
              onChange={(e) => handleChange('time', e.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="form-section">
        <div className="form-group">
          <label>Attendees</label>
          <input
            id="attendees-input"
            type="text"
            value={form.attendees}
            onChange={(e) => handleChange('attendees', e.target.value)}
            placeholder="Enter names or search..."
          />
        </div>
      </div>

      <div className="form-section">
        <div className="form-group">
          <label>Topics Discussed</label>
          <textarea
            id="topics-input"
            value={form.topics_discussed}
            onChange={(e) => handleChange('topics_discussed', e.target.value)}
            placeholder="Enter key discussion points..."
            rows={3}
          />
        </div>
        <a className="voice-link" href="#" onClick={(e) => e.preventDefault()}>
          🎙️ Summarize from Voice Note (Requires Consent)
        </a>
      </div>

      <div className="form-section">
        <h4 className="section-label">Materials Shared / Samples Distributed</h4>
        <div className="form-group">
          <label>Materials Shared</label>
          <div className="chip-input-wrapper">
            <input
              id="materials-input"
              type="text"
              value={form.materials_shared}
              onChange={(e) => handleChange('materials_shared', e.target.value)}
              placeholder="No materials added."
            />
            <button type="button" className="chip-btn">🔍 Search/Add</button>
          </div>
        </div>

        <div className="form-group">
          <label>Samples Distributed</label>
          <div className="chip-input-wrapper">
            <input
              id="samples-input"
              type="text"
              value={form.samples_distributed}
              onChange={(e) => handleChange('samples_distributed', e.target.value)}
              placeholder="No samples added."
            />
            <button type="button" className="chip-btn">+ Add Sample</button>
          </div>
        </div>
      </div>

      <div className="form-section">
        <div className="form-group">
          <label>Observed/Inferred HCP Sentiment</label>
          <div className="sentiment-radio-group">
            {['Positive', 'Neutral', 'Negative'].map(s => (
              <label key={s} className={`sentiment-option ${form.sentiment === s ? 'active' : ''}`}>
                <input
                  type="radio"
                  name="sentiment"
                  value={s}
                  checked={form.sentiment === s}
                  onChange={() => handleChange('sentiment', s)}
                />
                <span className={`sentiment-emoji ${s.toLowerCase()}`}>
                  {s === 'Positive' ? '😊' : s === 'Neutral' ? '😐' : '😟'}
                </span>
                {s}
              </label>
            ))}
          </div>
        </div>
      </div>

      <div className="form-section">
        <div className="form-group">
          <label>Outcomes</label>
          <textarea
            id="outcomes-input"
            value={form.outcomes}
            onChange={(e) => handleChange('outcomes', e.target.value)}
            placeholder="Key outcomes or agreements..."
            rows={3}
          />
        </div>
      </div>

      <div className="form-section">
        <div className="form-group">
          <label>Follow-up Actions</label>
          <textarea
            id="followup-input"
            value={form.follow_up_actions}
            onChange={(e) => handleChange('follow_up_actions', e.target.value)}
            placeholder="Planned follow-up actions..."
            rows={2}
          />
        </div>
      </div>

      <div className="form-actions">
        <button type="submit" id="submit-form-btn" className="submit-btn">
          💾 Save Interaction
        </button>
      </div>
    </form>
  );
}

export default InteractionForm;
