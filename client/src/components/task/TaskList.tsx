import React from 'react';
import Task from './Task';
import './TaskList.css';

interface MiniTasks {
  [key: string]: boolean;
}

interface TaskItem {
  id: number;
  title: string;
  description?: string;
  due_date: string;
  priority?: 'low' | 'medium' | 'high';
  mini_tasks?: MiniTasks;
  completed?: boolean;
  tags?: string[];
}

interface TaskListProps {
  tasks: TaskItem[];
  onTaskUpdate?: () => void; // Callback to refresh task list
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onTaskUpdate }) => {
  return (
    <div className="task-list">      {tasks.map((task, index) => (
        <Task
          key={task.id || index}
          id={task.id}
          title={task.title}
          description={task.description}
          due_date={task.due_date}
          priority={task.priority}
          mini_tasks={task.mini_tasks}
          completed={task.completed}
          tags={task.tags}
          onTaskUpdate={onTaskUpdate}
        />
      ))}
    </div>
  );
};

export default TaskList;
