import React from 'react';

const TodoStats = ({ stats }) => {
  const completionRate = stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0;

  const statCards = [
    {
      title: 'Total Todos',
      value: stats.total,
      icon: '📝',
      color: 'bg-blue-50 text-blue-700 border-blue-200',
    },
    {
      title: 'Completed',
      value: stats.completed,
      icon: '✅',
      color: 'bg-green-50 text-green-700 border-green-200',
    },
    {
      title: 'Pending',
      value: stats.pending,
      icon: '⏳',
      color: 'bg-yellow-50 text-yellow-700 border-yellow-200',
    },
    {
      title: 'Completion Rate',
      value: `${completionRate}%`,
      icon: '📊',
      color: 'bg-purple-50 text-purple-700 border-purple-200',
    },
  ];

  return (
    <div className="mb-8">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Your Progress</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card, index) => (
          <div
            key={index}
            className={`bg-white border rounded-lg p-6 text-center ${card.color}`}
          >
            <div className="text-2xl mb-2">{card.icon}</div>
            <div className="text-2xl font-bold mb-1">{card.value}</div>
            <div className="text-sm font-medium">{card.title}</div>
          </div>
        ))}
      </div>
      
      {/* Progress Bar */}
      {stats.total > 0 && (
        <div className="mt-6 bg-white rounded-lg border p-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Overall Progress</span>
            <span className="text-sm text-gray-500">{completionRate}% Complete</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${completionRate}%` }}
            ></div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TodoStats;
