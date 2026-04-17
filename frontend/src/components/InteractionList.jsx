import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { loadInteractions } from '../store/interactionsSlice';
import './InteractionList.css';

function InteractionList() {
  const dispatch = useDispatch();
  const { items, loading } = useSelector(s => s.interactions);

  useEffect(() => {
    dispatch(loadInteractions({}));
  }, [dispatch]);

  const getSentimentIcon = (sentiment) => {
    if (sentiment === 'Positive') return '😊';
    if (sentiment === 'Negative') return '😟';
    return '😐';
  };

  const getTypeIcon = (type) => {
    const icons = { Meeting: '🤝', Call: '📞', Email: '📧', Visit: '🏥', Conference: '🎤' };
    return icons[type] || '📋';
  };

  if (loading && items.length === 0) {
    return (
      <div className="interaction-list">
        <h3 className="list-title">Recent Interactions</h3>
        <div className="list-loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="interaction-list">
      <div className="list-header">
        <h3 className="list-title">Recent Interactions</h3>
        <span className="list-count">{items.length} logged</span>
      </div>

      {items.length === 0 ? (
        <div className="list-empty">
          <p>No interactions yet. Log your first one!</p>
        </div>
      ) : (
        <div className="list-items">
          {items.map(item => (
            <div key={item.id} className="list-item" id={`interaction-${item.id}`}>
              <div className="item-header">
                <span className="item-type">{getTypeIcon(item.interaction_type)} {item.interaction_type}</span>
                <span className="item-sentiment">{getSentimentIcon(item.sentiment)}</span>
              </div>
              <div className="item-hcp">{item.hcp_name || 'Unknown HCP'}</div>
              <div className="item-date">{item.date} {item.time && `at ${item.time}`}</div>
              {item.topics_discussed && (
                <div className="item-topics">{item.topics_discussed.substring(0, 80)}{item.topics_discussed.length > 80 ? '...' : ''}</div>
              )}
              {item.materials_shared && (
                <div className="item-materials">📎 {item.materials_shared}</div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default InteractionList;
