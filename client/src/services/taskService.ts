import api from '../api';

export interface Task {
  id: number;
  title: string;
  description?: string;
  due_date: string;
  priority?: 'low' | 'medium' | 'high';
  tags?: string[];
  mini_tasks: { [key: string]: boolean };
  completed?: boolean;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  due_date: string;
  priority?: 'low' | 'medium' | 'high';
  tags?: string[];
}

class TaskService {  async getTasks(): Promise<Task[]> {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    console.log('Token found:', token ? 'Yes' : 'No');
    console.log('Making request to:', '/tasks');

    try {
      const response = await api.get('/tasks', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      return response.data;
    } catch (error: any) {
      console.error('API Error:', error.response?.status, error.response?.data);
      if (error.response?.status === 401) {
        // Token is invalid or expired, clear it and redirect to login
        localStorage.removeItem('access_token');
        window.location.href = '/';
        throw new Error('Your session has expired. Please log in again.');
      }
      throw error;
    }
  }

  async createTask(taskData: CreateTaskRequest): Promise<Task> {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    try {
      const response = await api.post('/tasks', taskData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      return response.data;
    } catch (error: any) {
      if (error.response?.status === 401) {
        localStorage.removeItem('access_token');
        window.location.href = '/';
        throw new Error('Your session has expired. Please log in again.');
      }
      throw error;
    }
  }

  async updateTask(taskId: number, taskData: Partial<Task>): Promise<Task> {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    try {      
      const response = await api.put(`/tasks/${taskId}`, taskData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      return response.data;
    } catch (error: any) {
      if (error.response?.status === 401) {
        localStorage.removeItem('access_token');
        window.location.href = '/';
        throw new Error('Your session has expired. Please log in again.');
      }
      throw error;
    }
  }

  async deleteTask(taskId: number): Promise<void> {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    try {
      await api.delete(`/tasks/${taskId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
    } catch (error: any) {
      if (error.response?.status === 401) {
        localStorage.removeItem('access_token');
        window.location.href = '/';
        throw new Error('Your session has expired. Please log in again.');
      }
      throw error;
    }
  }
}

export default new TaskService();
