import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { todoAPI } from '../services/api';
import TodoForm from '../components/TodoForm';
import TodoList from '../components/TodoList';
import TodoStats from '../components/TodoStats';

const DashboardPage = () => {
  const { user } = useAuth();
  const [todos, setTodos] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    status: 'all', // all, completed, pending
    priority: 'all', // all, low, medium, high
  });

  // Fetch todos
  const fetchTodos = useCallback(async () => {
    try {
      setLoading(true);
      const params = {};
      if (filters.status !== 'all') {
        params.completed = filters.status === 'completed';
      }
      if (filters.priority !== 'all') {
        params.priority = filters.priority;
      }
      
      const response = await todoAPI.getTodos(params);
      setTodos(response.data.todos);
    } catch (err) {
      setError('Failed to fetch todos');
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  // Fetch stats
  const fetchStats = async () => {
    try {
      const response = await todoAPI.getStats();
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  useEffect(() => {
    fetchTodos();
    fetchStats();
  }, [fetchTodos]);

  // Handle todo creation
  const handleTodoCreate = async (todoData) => {
    try {
      const response = await todoAPI.createTodo(todoData);
      setTodos(prev => [response.data.todo, ...prev]);
      fetchStats(); // Refresh stats
      return { success: true };
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Failed to create todo';
      return { success: false, error: errorMessage };
    }
  };

  // Handle todo update
  const handleTodoUpdate = async (id, updateData) => {
    try {
      const response = await todoAPI.updateTodo(id, updateData);
      setTodos(prev => prev.map(todo => 
        todo.id === id ? response.data.todo : todo
      ));
      fetchStats(); // Refresh stats
      return { success: true };
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Failed to update todo';
      return { success: false, error: errorMessage };
    }
  };

  // Handle todo deletion
  const handleTodoDelete = async (id) => {
    try {
      await todoAPI.deleteTodo(id);
      setTodos(prev => prev.filter(todo => todo.id !== id));
      fetchStats(); // Refresh stats
      return { success: true };
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Failed to delete todo';
      return { success: false, error: errorMessage };
    }
  };

  // Handle filter changes
  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value,
    }));
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome back, {user?.first_name}!
        </h1>
        <p className="text-gray-600">
          Manage your tasks and stay organized
        </p>
      </div>

      {/* Stats Section */}
      {stats && <TodoStats stats={stats} />}

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Todo Form */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Add New Todo</h2>
            <TodoForm onSubmit={handleTodoCreate} />
          </div>
        </div>

        {/* Todo List */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                <h2 className="text-xl font-semibold mb-4 sm:mb-0">Your Todos</h2>
                
                {/* Filters */}
                <div className="flex space-x-4">
                  <select
                    value={filters.status}
                    onChange={(e) => handleFilterChange('status', e.target.value)}
                    className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="all">All Status</option>
                    <option value="pending">Pending</option>
                    <option value="completed">Completed</option>
                  </select>
                  
                  <select
                    value={filters.priority}
                    onChange={(e) => handleFilterChange('priority', e.target.value)}
                    className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="all">All Priority</option>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>
            </div>
            
            <div className="p-6">
              {error && (
                <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                  {error}
                </div>
              )}
              
              <TodoList
                todos={todos}
                loading={loading}
                onUpdate={handleTodoUpdate}
                onDelete={handleTodoDelete}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
