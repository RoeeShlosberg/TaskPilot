import React, { useState, useEffect, useRef } from 'react';
import taskService from '../../services/taskService';
import './Task.css';

interface MiniTasks {
  [key: string]: boolean;
}

interface TaskProps {
  title: string;
  description?: string;
  due_date: string;
  priority?: 'low' | 'medium' | 'high';
  mini_tasks?: MiniTasks;
  completed?: boolean;
  tags?: string[];
  id?: number;
  onTaskUpdate?: () => void; // Callback to refresh task list
}

const Task: React.FC<TaskProps> = ({ title, description, due_date, priority, mini_tasks = {}, completed = false, tags = [], id, onTaskUpdate }) => {  const [isExpanded, setIsExpanded] = useState(false);
  const [newMiniTask, setNewMiniTask] = useState('');
  const [newTag, setNewTag] = useState('');
  const [showPriorityPicker, setShowPriorityPicker] = useState(false);
  const [isEditingDescription, setIsEditingDescription] = useState(false);
  const [isEditingDueDate, setIsEditingDueDate] = useState(false);
  const [showDeleteConfirmation, setShowDeleteConfirmation] = useState(false);
  const [dueDateValue, setDueDateValue] = useState(due_date);
  const [descriptionValue, setDescriptionValue] = useState(
    // If description is a single space or undefined, set to empty string
    description === ' ' || description === undefined ? '' : description
  );
  const priorityPickerRef = useRef<HTMLDivElement>(null);
  const descriptionInputRef = useRef<HTMLInputElement>(null);
  const dueDateRef = useRef<HTMLDivElement>(null);useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (priorityPickerRef.current && !priorityPickerRef.current.contains(event.target as Node)) {
        setShowPriorityPicker(false);
      }
      
      if (dueDateRef.current && !dueDateRef.current.contains(event.target as Node) && isEditingDueDate) {
        // Cancel due date editing when clicking outside
        setIsEditingDueDate(false);
        // Reset to original value
        setDueDateValue(due_date);
      }
    };

    if (showPriorityPicker || isEditingDueDate) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showPriorityPicker, isEditingDueDate, due_date]);

  // Focus the description input when editing mode is enabled
  useEffect(() => {
    if (isEditingDescription && descriptionInputRef.current) {
      descriptionInputRef.current.focus();
    }
  }, [isEditingDescription]);
  
  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const handleToggleTaskCompletion = async () => {
    if (!id) {
      console.log('No task ID available');
      return;
    }

    try {
      // Toggle the completed status
      const newCompletedStatus = !completed;

      // Use taskService to update the task
      await taskService.updateTask(id, {
        "completed": newCompletedStatus
      });
      
      // Call the callback to refresh the task list
      if (onTaskUpdate) {
        onTaskUpdate();
      }
    } catch (error: any) {
      console.error('Failed to toggle task completion:', error);
      alert(`Error: ${error?.message || error}`);
    }
  };  const handleAddMiniTask = async () => {
    if (!newMiniTask.trim() || !id) {
      console.log('Missing data:', { newMiniTask: newMiniTask.trim(), id });
      return;
    }

    try {
      const updatedMiniTasks = {
        ...mini_tasks,
        [newMiniTask.trim()]: false
      };

      // Use taskService to update the task
      await taskService.updateTask(id, {
        mini_tasks: updatedMiniTasks
      });

      // Clear the input
      setNewMiniTask('');
            
      // Call the callback to refresh the task list
      if (onTaskUpdate) {
        onTaskUpdate();
      }
    } catch (error: any) {
      console.error('Failed to add mini-task:', error);
      alert(`Error: ${error?.message || error}`);
    }
  };
  const handleToggleMiniTask = async (miniTaskName: string, currentStatus: boolean) => {
    if (!id) {
      console.log('No task ID available');
      return;
    }

    try {
      // Toggle the mini-task status
      const updatedMiniTasks = {
        ...mini_tasks,
        [miniTaskName]: !currentStatus
      };

      // Use taskService to update the task
      await taskService.updateTask(id, {
        mini_tasks: updatedMiniTasks
      });
      
      // Call the callback to refresh the task list
      if (onTaskUpdate) {
        onTaskUpdate();
      }
    } catch (error: any) {
      console.error('Failed to toggle mini-task completion:', error);
      alert(`Error: ${error?.message || error}`);
    }
  };
  const handlePriorityClick = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent event bubbling
    setShowPriorityPicker(!showPriorityPicker);
  };
  
  const handleDueDateClick = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent event bubbling
    setIsEditingDueDate(true);
  };
  
  const handleDueDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDueDateValue(e.target.value);
  };
  
  const handleDueDateSave = async () => {
    if (!id) {
      console.log('No task ID available');
      return;
    }
    
    try {
      // Validate that the date is not empty and is a valid date
      if (!dueDateValue || new Date(dueDateValue).toString() === 'Invalid Date') {
        alert('Please enter a valid date');
        return;
      }
      
      // Use taskService to update the task due date
      await taskService.updateTask(id, {
        due_date: dueDateValue
      });
      
      // Exit editing mode
      setIsEditingDueDate(false);
      
      // Call the callback to refresh the task list
      if (onTaskUpdate) {
        onTaskUpdate();
      }
    } catch (error: any) {
      console.error('Failed to update due date:', error);
      alert(`Error: ${error?.message || error}`);
    }
  };
  
  const handleDueDateCancel = () => {
    // Reset to original value and exit editing mode
    setDueDateValue(due_date);
    setIsEditingDueDate(false);
  };
  
  const handleDueDateKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleDueDateSave();
    } else if (e.key === 'Escape') {
      handleDueDateCancel();
    }
  };const handlePriorityChange = async (newPriority: 'low' | 'medium' | 'high') => {
    if (!id) {
      console.log('No task ID available');
      return;
    }

    try {
      // Use taskService to update the task priority
      await taskService.updateTask(id, {
        priority: newPriority
      });
      
      // Hide the priority picker
      setShowPriorityPicker(false);
      
      // Call the callback to refresh the task list
      if (onTaskUpdate) {
        onTaskUpdate();
      }
    } catch (error: any) {
      console.error('Failed to update task priority:', error);
      alert(`Error: ${error?.message || error}`);
    }
  };
  
  const handleDescriptionClick = () => {
    setIsEditingDescription(true);
  };
  
  const handleDescriptionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDescriptionValue(e.target.value);
  };
    const handleDescriptionSave = async () => {
    if (!id) {
      console.log('No task ID available');
      return;
    }
    
    try {
      // Check if description is empty or only whitespace
      const trimmedDescription = descriptionValue.trim();
      
      // Use taskService to update the task description
      // If the description is empty, send a single space to indicate "no description"
      await taskService.updateTask(id, {
        description: trimmedDescription === '' ? ' ' : descriptionValue
      });
      
      // If description was empty, set the local state to empty string for display purposes
      if (trimmedDescription === '') {
        setDescriptionValue('');
      }
      
      // Exit editing mode
      setIsEditingDescription(false);
      
      // Call the callback to refresh the task list
      if (onTaskUpdate) {
        onTaskUpdate();
      }
    } catch (error: any) {
      console.error('Failed to update task description:', error);
      alert(`Error: ${error?.message || error}`);
    }
  };
    const handleDescriptionKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleDescriptionSave();
    } else if (e.key === 'Escape') {
      // Cancel editing and revert to original value
      setDescriptionValue(description || '');
      setIsEditingDescription(false);
    }
  };
  
  const handleDeleteTask = async () => {
    if (!id) {
      console.log('No task ID available');
      return;
    }
    
    try {
      // Use taskService to delete the task
      await taskService.deleteTask(id);
      
      // Call the callback to refresh the task list
      if (onTaskUpdate) {
        onTaskUpdate();
      }
      
      // Hide the confirmation dialog
      setShowDeleteConfirmation(false);
    } catch (error: any) {
      console.error('Failed to delete task:', error);
      alert(`Error: ${error?.message || error}`);
    }
  };
  
  const handleDeleteMiniTask = async (miniTaskName: string) => {
    if (!id) {
      console.log('No task ID available');
      return;
    }
    
    try {
      // Create a new mini_tasks object without the specified task
      const updatedMiniTasks = { ...mini_tasks };
      delete updatedMiniTasks[miniTaskName];
      
      // Use taskService to update the task
      await taskService.updateTask(id, {
        mini_tasks: updatedMiniTasks
      });
      
      // Call the callback to refresh the task list
      if (onTaskUpdate) {
        onTaskUpdate();
      }
    } catch (error: any) {
      console.error('Failed to delete mini-task:', error);
      alert(`Error: ${error?.message || error}`);
    }
  };

  const handleDeleteTag = async (tagToDelete: string) => {
    if (!id) {
      console.log('No task ID available');
      return;
    }

    try {
      // Filter out the tag to delete
      const updatedTags = tags.filter(tag => tag !== tagToDelete);
      
      // Use taskService to update the task
      await taskService.updateTask(id, {
        tags: updatedTags
      });
      
      // Call the callback to refresh the task list
      if (onTaskUpdate) {
        onTaskUpdate();
      }
    } catch (error: any) {
      console.error('Failed to delete tag:', error);
      alert(`Error: ${error?.message || error}`);
    }
  };
  const handleAddTag = async () => {
    if (!newTag.trim() || !id) {
      return;
    }

    try {
      // Initialize tags as an empty array if it's null or undefined
      const currentTags = Array.isArray(tags) ? tags : [];
      
      // Check if tag already exists
      if (currentTags.includes(newTag.trim())) {
        alert('This tag already exists!');
        return;
      }

      // Create a new tags array with the new tag
      const updatedTags = [...currentTags, newTag.trim()];
      
      // Use taskService to update the task
      await taskService.updateTask(id, {
        tags: updatedTags
      });
      
      // Clear the input
      setNewTag('');
      
      // Call the callback to refresh the task list
      if (onTaskUpdate) {
        onTaskUpdate();
      }
    } catch (error: any) {
      console.error('Failed to add tag:', error);
      alert(`Error: ${error?.message || error}`);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleAddMiniTask();
    }
  };

  const getPriorityColor = () => {
    switch (priority) {
      case 'low':
        return 'green';
      case 'medium':
        return 'yellow';
      case 'high':
        return 'red';
      default:
        return 'white';
    }
  };

  return (
    <div className="task">      <div className="task-header">
        <div 
          className={`task-checkbox ${completed ? 'completed' : ''}`}
          onClick={handleToggleTaskCompletion}
        ></div>
        <span 
          className={`task-title ${completed ? 'completed' : ''}`}
          onClick={toggleExpand}        >
          {title}
        </span>        <div 
          className="task-due-date-container"
          ref={dueDateRef}
        >
          {isEditingDueDate ? (
            <div className="due-date-edit">
              <input
                type="date"
                className="due-date-input"
                value={dueDateValue}
                onChange={handleDueDateChange}
                onKeyDown={handleDueDateKeyPress}
              />
              <div className="due-date-buttons">
                <button className="save-due-date-btn" onClick={handleDueDateSave}>
                  Save
                </button>
                <button className="cancel-due-date-btn" onClick={handleDueDateCancel}>
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <span 
              className="task-due-date"
              onClick={handleDueDateClick}
            >
              {new Date(due_date).toLocaleDateString()}
            </span>
          )}
        </div>        {/* Tags display - show only 1 tag in closed view */}
        {tags && Array.isArray(tags) && tags.length > 0 && (
          <div className="task-tags-container">
            <span className="task-tag">
              {tags[0]}
              {isExpanded && (
                <span 
                  className="tag-delete" 
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteTag(tags[0]);
                  }}
                  title="Remove tag"
                >
                  ×
                </span>
              )}
            </span>
            {tags.length > 1 && (
              <span className="task-tag-count">+{tags.length - 1}</span>
            )}
          </div>
        )}
        
        <div className="task-priority-container" ref={priorityPickerRef}>
          <div 
            className={`task-priority ${priority || 'none'}`}
            onClick={handlePriorityClick}
          ></div>
          {showPriorityPicker && (
            <div className="priority-picker">
              <div 
                className="priority-option low"
                onClick={() => handlePriorityChange('low')}
                title="Low Priority"
              ></div>
              <div 
                className="priority-option medium"
                onClick={() => handlePriorityChange('medium')}
                title="Medium Priority"
              ></div>
              <div 
                className="priority-option high"
                onClick={() => handlePriorityChange('high')}
                title="High Priority"
              ></div>
            </div>
          )}
        </div>
        <button className="task-toggle" onClick={toggleExpand}>
          {isExpanded ? '▼' : '▶'}
        </button>
      </div>      {isExpanded && (        <div className="task-details">
          {isEditingDescription ? (
            <div className="task-description-edit">
              <input
                ref={descriptionInputRef}
                type="text"
                className="description-input"
                value={descriptionValue}
                onChange={handleDescriptionChange}
                onKeyDown={handleDescriptionKeyPress}
                onBlur={handleDescriptionSave}
                placeholder="Add description..."
              />
              <button className="save-description-btn" onClick={handleDescriptionSave}>
                Save
              </button>
            </div>
          ) : (            <p 
              className="task-description" 
              onClick={handleDescriptionClick}
            >
              {description && description !== ' ' ? 
                description : 
                <span className="no-description">Add description...</span>
              }
            </p>
          )}          <div className="mini-tasks">{mini_tasks && Object.entries(mini_tasks).map(([key, value]) => (
              <div key={key} className="mini-task">
                <div 
                  className={`mini-task-checkbox ${value ? 'completed' : ''}`}
                  onClick={() => handleToggleMiniTask(key, value)}
                ></div>
                <span className={`mini-task-text ${value ? 'completed' : ''}`}>
                  {key}
                </span>                <div 
                  className="mini-task-delete"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteMiniTask(key);
                  }}
                  title="Delete mini-task"
                >
                  🗑️
                </div>
              </div>
            ))}
            <div className="mini-task mini-task-add">
              <div className="mini-task-add-button" onClick={handleAddMiniTask}>+</div>
              <input
                type="text"
                className="mini-task-input"
                value={newMiniTask}
                onChange={(e) => setNewMiniTask(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Add new mini-task..."
              />
            </div>
          </div>          <div className="task-actions-row">          {/* All tags in expanded view */}
            <div className="task-expanded-tags">
              {tags && Array.isArray(tags) && tags.length > 0 ? (
                <>                  {tags.map((tag, index) => (
                    <span key={index} className="task-expanded-tag">
                      {tag}
                      <span 
                        className="tag-delete" 
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteTag(tag);
                        }}
                        title="Remove tag"
                      >
                        ×
                      </span>
                    </span>
                  ))}
                  <input
                    type="text"
                    className="add-tag-input"
                    value={newTag}
                    onChange={(e) => setNewTag(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault();
                        handleAddTag();
                      }
                    }}
                    placeholder="Add tag..."
                  />
                </>
              ) : (
                <>
                  <span className="no-tags">No tags</span>
                  <input
                    type="text"
                    className="add-tag-input"
                    value={newTag}
                    onChange={(e) => setNewTag(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault();
                        handleAddTag();
                      }
                    }}
                    placeholder="Add tag..."
                  />
                </>
              )}
            </div>
            
            <button 
              className="delete-task-btn"
              onClick={() => setShowDeleteConfirmation(true)}
            >
              Delete Task
            </button>
          </div>
            {showDeleteConfirmation && (
            <div className="delete-confirmation">
              <p>Are you sure you want to delete this task?</p>
              <div className="delete-confirmation-buttons">
                <button 
                  className="confirm-delete-btn"
                  onClick={handleDeleteTask}
                >
                  Yes, Delete
                </button>
                <button 
                  className="cancel-delete-btn"
                  onClick={() => setShowDeleteConfirmation(false)}
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Task;
