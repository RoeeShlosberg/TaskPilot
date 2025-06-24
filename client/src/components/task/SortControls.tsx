import React, { useState } from 'react';
import './SortControls.css';

export type SortField = 'due_date' | 'priority' | 'title';
export type SortDirection = 'asc' | 'desc';

interface SortControlsProps {
  sortField: SortField;
  sortDirection: SortDirection;
  onSortChange: (field: SortField, direction: SortDirection) => void;
  allTags: string[];
  selectedTags: string[];
  onTagFilterChange: (tags: string[]) => void;
}

const SortControls: React.FC<SortControlsProps> = ({ 
  sortField, 
  sortDirection, 
  onSortChange,
  allTags,
  selectedTags,
  onTagFilterChange
}) => {
  const [showTagFilter, setShowTagFilter] = useState(false);

  const handleTagClick = (tag: string) => {
    if (selectedTags.includes(tag)) {
      onTagFilterChange(selectedTags.filter(t => t !== tag));
    } else {
      onTagFilterChange([...selectedTags, tag]);
    }
  };

  const handleClearFilters = () => {
    onTagFilterChange([]);
  };

  const handleSelectAllFilters = () => {
    onTagFilterChange([...allTags]);
  };

  return (
    <div className="sort-controls">
      <div className="sort-section">
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

      <div className="filter-section">
        <button 
          className={`filter-toggle ${showTagFilter ? 'active' : ''} ${selectedTags.length > 0 ? 'filtered' : ''}`}
          onClick={() => setShowTagFilter(!showTagFilter)}
          title="Filter by tags"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z" clipRule="evenodd" />
          </svg>
          {selectedTags.length > 0 && <span className="filter-count">{selectedTags.length}</span>}
        </button>

        {showTagFilter && (
          <div className="tag-filter-dropdown">
            <div className="tag-filter-header">
              <span>Filter by Tags</span>
              <div className="tag-filter-actions">
                <button className="tag-filter-action" onClick={handleSelectAllFilters}>All</button>
                <button className="tag-filter-action" onClick={handleClearFilters}>Clear</button>
              </div>
            </div>
            <div className="tag-filter-options">
              {allTags.length === 0 ? (
                <div className="no-tags-message">No tags available</div>
              ) : (
                allTags.map((tag) => (
                  <div 
                    key={tag} 
                    className={`tag-filter-option ${selectedTags.includes(tag) ? 'selected' : ''}`}
                    onClick={() => handleTagClick(tag)}
                  >
                    <span className="tag-filter-checkbox">
                      {selectedTags.includes(tag) && '✓'}
                    </span>
                    <span className="tag-filter-name">{tag}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SortControls;
