import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, AlertCircle } from 'lucide-react';

const CompactDashboard = () => {
  const [resourceData, setResourceData] = useState([
    { time: '00:00', cpuUsage: 45, gpuUsage: 62, cpuMemory: 58, gpuMemory: 70 },
    { time: '00:05', cpuUsage: 52, gpuUsage: 58, cpuMemory: 62, gpuMemory: 72 },
    { time: '00:10', cpuUsage: 49, gpuUsage: 65, cpuMemory: 60, gpuMemory: 75 },
    { time: '00:15', cpuUsage: 47, gpuUsage: 71, cpuMemory: 63, gpuMemory: 78 },
    { time: '00:20', cpuUsage: 55, gpuUsage: 68, cpuMemory: 65, gpuMemory: 73 }
  ]);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-800 border border-gray-700 p-3 rounded-lg shadow-lg">
          <p className="text-gray-300 mb-1">{`Time: ${label}`}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {`${entry.name}: ${entry.value}%`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="p-4 bg-gray-900 min-h-screen">
      <div className="grid grid-cols-12 gap-4 h-screen max-h-[800px]">
        {/* Main Resource Monitor */}
        <div className="col-span-9">
          <Card className="h-full bg-gray-800 border-gray-700">
            <CardHeader className="pb-2 border-b border-gray-700">
              <CardTitle className="text-lg text-gray-100">System Resource Usage</CardTitle>
            </CardHeader>
            <CardContent className="pt-4">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart 
                  data={resourceData} 
                  margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
                >
                  <XAxis 
                    dataKey="time" 
                    stroke="#6b7280"
                    tick={{ fill: '#9ca3af' }}
                  />
                  <YAxis 
                    stroke="#6b7280"
                    tick={{ fill: '#9ca3af' }}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend 
                    wrapperStyle={{ color: '#e5e7eb' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="cpuUsage" 
                    stroke="#8b5cf6" 
                    name="CPU Usage %" 
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="gpuUsage" 
                    stroke="#10b981" 
                    name="GPU Usage %" 
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="cpuMemory" 
                    stroke="#f59e0b" 
                    name="CPU Memory %" 
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="gpuMemory" 
                    stroke="#3b82f6" 
                    name="GPU Memory %" 
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Right sidebar */}
        <div className="col-span-3 space-y-4">
          {/* System Status */}
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-4">
              <div className="flex items-center space-x-2">
                <Activity className="h-5 w-5 text-emerald-400" />
                <span className="font-medium text-gray-100">System Active</span>
              </div>
            </CardContent>
          </Card>

          {/* Critical Alerts */}
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-4">
              <div className="flex items-center space-x-2 mb-2">
                <AlertCircle className="h-5 w-5 text-amber-400" />
                <span className="font-medium text-gray-100">Alerts</span>
              </div>
              <div className="text-sm">
                <div className="text-gray-400">No critical alerts</div>
              </div>
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-4 space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-400">Active Processes</span>
                <span className="font-medium text-gray-100">12</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-400">Plugins (Active/Total)</span>
                <div className="flex items-center space-x-1">
                  <span className="font-medium text-emerald-400">3</span>
                  <span className="text-gray-400">/</span>
                  <span className="font-medium text-gray-100">5</span>
                </div>
              </div>
              <div className="text-xs text-gray-500">
                <div className="flex items-center justify-between">
                  <span>Active: Model Loader, CUDA Monitor, Logger</span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-400">Operations/s</span>
                <span className="font-medium text-gray-100">245</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
      {/* Bottom Tabs */}
      <div className="fixed bottom-0 left-0 right-0 bg-gray-800 border-t border-gray-700 p-2">
        <div className="flex justify-center space-x-4">
          <button className="px-4 py-2 text-gray-100 bg-gray-700 rounded-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500">
            Resources
          </button>
          <button className="px-4 py-2 text-gray-400 hover:text-gray-100 rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500">
            Plugins
          </button>
          <button className="px-4 py-2 text-gray-400 hover:text-gray-100 rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500">
            Operations
          </button>
          <button className="px-4 py-2 text-gray-400 hover:text-gray-100 rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500">
            Logs
          </button>
        </div>
      </div>
    </div>
  );
};

export default CompactDashboard;