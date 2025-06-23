import React from 'react';
import './SortControls.css';

export type SortField = 'due_date' | 'priority' | 'title';
export type SortDirection = 'asc' | 'desc';

interface SortControlsProps {
  sortField: SortField;
  sortDirection: SortDirection;
  onSortChange: (field: SortField, direction: SortDirection) => void;
}

const SortControls: React.FC<SortControlsProps> = ({ 
  sortField, 
  sortDirection, 
  onSortChange 
}) => {
  return (
    <div className="sort-controls">
      <span className="sort-label">Sort by:</span>
      <select 
        className="sort-select"
        value={sortField}
        onChange={(e) => onSortChange(e.target.value as SortField, sortDirection)}
      >
        <option value="due_date">Due Date</option>
        <option value="priority">Priority</option>
        <option value="title">Title</option>
      </select>
      
      <div className="sort-direction">
        <button 
          className={`sort-direction-btn ${sortDirection === 'asc' ? 'active' : ''}`}
          onClick={() => onSortChange(sortField, 'asc')}
          title="Ascending order"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
          </svg>
        </button>
        <button 
          className={`sort-direction-btn ${sortDirection === 'desc' ? 'active' : ''}`}
          onClick={() => onSortChange(sortField, 'desc')}
          title="Descending order"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l2.293-2.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default SortControls;
