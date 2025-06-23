import './MainPage.css';
import React, { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/header/Header';
import TaskList from '../components/task/TaskList';
import AddTaskForm from '../components/forms/AddTaskForm';
import taskService, { Task as TaskType, CreateTaskRequest } from '../services/taskService';
import agentService, { AgentResponse } from '../services/agentService';
import AgentResponseBox from '../components/agent/AgentResponseBox';
import SortControls, { SortField, SortDirection } from '../components/task/SortControls';

interface LocalTask {
  title: string;
  description?: string;
  due_date: string;
  priority?: 'low' | 'medium' | 'high';
  mini_tasks: { [key: string]: boolean };
}

export default function MainPage() {
  const [tasks, setTasks] = useState<TaskType[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showSummary, setShowSummary] = useState(false);
  const [showRecommendations, setShowRecommendations] = useState(false);
  const [agentResponse, setAgentResponse] = useState<AgentResponse | null>(null);
  const [agentLoading, setAgentLoading] = useState(false);
  const [agentError, setAgentError] = useState<string | null>(null);
  const [sortField, setSortField] = useState<SortField>('due_date');
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/');
    }
  }, [navigate]);
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const fetchedTasks = await taskService.getTasks();
      setTasks(fetchedTasks);
      setError(null);
    } catch (err) {
      setError('Failed to fetch tasks. Please try again later.');
    }
  };

  const handleAddTask = async (taskData: CreateTaskRequest) => {
    try {
      await taskService.createTask(taskData);
      setShowAddForm(false);
      fetchTasks(); // Refresh the task list
    } catch (err) {
      setError('Failed to add task. Please try again.');
    }
  };

  const handleCancelAdd = () => {
    setShowAddForm(false);
  };

  const handleSummaryClick = async () => {
    setShowSummary(true);
    setShowRecommendations(false);
    setAgentLoading(true);
    setAgentError(null);
    
    try {
      const response = await agentService.getProjectSummary();
      setAgentResponse(response);
    } catch (err) {
      if (err instanceof Error) {
        setAgentError(err.message);
      } else {
        setAgentError('Failed to get project summary. Please try again.');
      }
    } finally {
      setAgentLoading(false);
    }
  };

  const handleRecommendationsClick = async () => {
    setShowSummary(false);
    setShowRecommendations(true);
    setAgentLoading(true);
    setAgentError(null);
    
    try {
      const response = await agentService.getTaskRecommendations();
      setAgentResponse(response);
    } catch (err) {
      if (err instanceof Error) {
        setAgentError(err.message);
      } else {
        setAgentError('Failed to get task recommendations. Please try again.');
      }
    } finally {
      setAgentLoading(false);
    }
  };
  const handleCloseAgentResponse = () => {
    setShowSummary(false);
    setShowRecommendations(false);
  };
  
  const handleSortChange = (field: SortField, direction: SortDirection) => {
    setSortField(field);
    setSortDirection(direction);
  };
  
  // Sort tasks based on current sort field and direction
  const sortedTasks = useMemo(() => {
    if (!tasks.length) return [];
    
    return [...tasks].sort((a, b) => {
      let comparison = 0;
      
      if (sortField === 'due_date') {
        const dateA = new Date(a.due_date).getTime();
        const dateB = new Date(b.due_date).getTime();
        comparison = dateA - dateB;
      } 
      else if (sortField === 'priority') {
        const priorityOrder = { high: 3, medium: 2, low: 1, undefined: 0 };
        const priorityA = priorityOrder[a.priority as keyof typeof priorityOrder] || 0;
        const priorityB = priorityOrder[b.priority as keyof typeof priorityOrder] || 0;
        comparison = priorityA - priorityB;
      } 
      else if (sortField === 'title') {
        comparison = a.title.localeCompare(b.title);
      }
      
      return sortDirection === 'asc' ? comparison : -comparison;
    });
  }, [tasks, sortField, sortDirection]);
    return (
    <div className="main-page">
      <Header />
      <div className="main-page-header">
        <div className="main-page-title-area">
          <h1 className="task-list-title">My Task List</h1>
          {tasks.length > 0 && (
            <SortControls 
              sortField={sortField} 
              sortDirection={sortDirection} 
              onSortChange={handleSortChange} 
            />
          )}
        </div>
        <div className="main-page-actions">
          <button className="agent-btn" onClick={handleSummaryClick}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
              <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
            </svg>
            Summarize
          </button>          <button className="agent-btn" onClick={handleRecommendationsClick}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
            Recommend
          </button><button className="add-task-btn" onClick={() => setShowAddForm(true)}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 3a1 1 0 00-1 1v5H4a1 1 0 100 2h5v5a1 1 0 102 0v-5h5a1 1 0 100-2h-5V4a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            Add Task
          </button>
        </div>      </div>      <main className="main-page-content">
        {error ? (
          <p className="error-message">{error}</p>
        ) : tasks.length === 0 ? (
          <p className="no-tasks-message">No tasks found. Click "Add Task" to get started!</p>
        ) : (
          <TaskList tasks={sortedTasks} onTaskUpdate={fetchTasks} />
        )}
      </main>
      
      {showAddForm && (
        <AddTaskForm onSubmit={handleAddTask} onCancel={handleCancelAdd} />
      )}
      
      {(showSummary || showRecommendations) && (
        <AgentResponseBox
          title={showSummary ? "Project Summary" : "Task Recommendations"}
          responseContent={showSummary ? agentResponse?.summary || null : agentResponse?.recommendations || null}
          metadata={agentResponse?.metadata}
          generatedAt={agentResponse?.generated_at}
          isLoading={agentLoading}
          error={agentError}
          onClose={handleCloseAgentResponse}
        />
      )}
    </div>
  );
}
