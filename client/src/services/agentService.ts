import api from '../api';

export interface AgentResponse {
  summary?: string;
  recommendations?: string;
  metadata: {
    total_tasks?: number;
    completed_tasks?: number;
    pending_tasks: number;
    completion_rate?: number;
    high_priority_tasks?: number;
    overdue_tasks?: number;
  };
  generated_at: string;
  prompt_type: string;
}

class AgentService {  async getProjectSummary(): Promise<AgentResponse> {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    try {
      const response = await api.get('/agent/summary', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error: any) {
      console.error('Error fetching project summary:', error);
      if (error.response?.status === 401) {
        // Token is invalid or expired, clear it and redirect to login
        localStorage.removeItem('access_token');
        window.location.href = '/';
        throw new Error('Your session has expired. Please log in again.');
      }
      throw error;
    }
  }
  async getTaskRecommendations(): Promise<AgentResponse> {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    try {
      const response = await api.get('/agent/recommendations', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error: any) {
      console.error('Error fetching task recommendations:', error);
      if (error.response?.status === 401) {
        // Token is invalid or expired, clear it and redirect to login
        localStorage.removeItem('access_token');
        window.location.href = '/';
        throw new Error('Your session has expired. Please log in again.');
      }
      throw error;
    }
  }
}

export default new AgentService();
