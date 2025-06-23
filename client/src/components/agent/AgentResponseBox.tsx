import React from 'react';
import './AgentResponseBox.css';

interface AgentResponseBoxProps {
  title: string;
  responseContent: string | null;
  metadata?: {
    total_tasks?: number;
    completed_tasks?: number;
    pending_tasks?: number;
    completion_rate?: number;
    high_priority_tasks?: number;
    overdue_tasks?: number;
  };
  generatedAt?: string;
  isLoading: boolean;
  error: string | null;
  onClose: () => void;
}

const AgentResponseBox: React.FC<AgentResponseBoxProps> = ({
  title,
  responseContent,
  metadata,
  generatedAt,
  isLoading,
  error,
  onClose,
}) => {
  // Format the timestamp nicely
  const formatTimestamp = (timestamp: string) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <div className="agent-response-overlay">
      <div className="agent-response-box">
        <div className="agent-response-header">
          <h2>{title}</h2>
          <button className="agent-response-close" onClick={onClose}>
            ×
          </button>
        </div>
        
        <div className="agent-response-content">
          {isLoading ? (
            <div className="agent-response-loading">
              <div className="agent-response-spinner"></div>
              <p>AI is thinking...</p>
            </div>
          ) : error ? (
            <div className="agent-response-error">
              <p>Error: {error}</p>
            </div>
          ) : (
            <>
              <div className="agent-response-text">
                {responseContent && responseContent.split('\n').map((line, index) => (
                  <React.Fragment key={index}>
                    {line}
                    <br />
                  </React.Fragment>
                ))}
              </div>

              {metadata && (
                <div className="agent-response-metadata">
                  <h3>Stats:</h3>
                  <ul>
                    {metadata.total_tasks !== undefined && (
                      <li>Total Tasks: {metadata.total_tasks}</li>
                    )}
                    {metadata.completed_tasks !== undefined && (
                      <li>Completed Tasks: {metadata.completed_tasks}</li>
                    )}
                    {metadata.pending_tasks !== undefined && (
                      <li>Pending Tasks: {metadata.pending_tasks}</li>
                    )}
                    {metadata.completion_rate !== undefined && (
                      <li>Completion Rate: {metadata.completion_rate}%</li>
                    )}
                    {metadata.high_priority_tasks !== undefined && (
                      <li>High Priority Tasks: {metadata.high_priority_tasks}</li>
                    )}
                    {metadata.overdue_tasks !== undefined && (
                      <li>Overdue Tasks: {metadata.overdue_tasks}</li>
                    )}
                  </ul>
                </div>
              )}

              {generatedAt && (
                <div className="agent-response-footer">
                  Generated: {formatTimestamp(generatedAt)}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default AgentResponseBox;
