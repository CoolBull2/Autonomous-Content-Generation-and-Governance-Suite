import React, { useState } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { 
  HomeIcon,
  DocumentTextIcon,
  CogIcon,
  ChartBarIcon,
  SparklesIcon,
  Bars3Icon,
  XMarkIcon,
  BoltIcon,
  BeakerIcon,
  CpuChipIcon,
  RocketLaunchIcon
} from '@heroicons/react/24/outline';

const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navigation = [
    { 
      name: 'Content Generation', 
      href: '/generate', 
      icon: DocumentTextIcon,
      description: 'Create AI-powered content',
      color: 'from-indigo-500 to-purple-600'
    }
  ];

  return (
    <div className="h-screen flex overflow-hidden bg-gradient-to-br from-slate-50 via-gray-50 to-zinc-50">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-72 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        
        {/* Sidebar Background */}
        <div className="h-full flex flex-col overflow-y-auto border-r border-gray-200/50 bg-white/95 backdrop-blur-xl shadow-2xl">
          {/* Header */}
          <div className="relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600"></div>
            
            <div className="relative flex h-20 items-center justify-between px-6">
              <div className="flex items-center space-x-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/20 backdrop-blur-sm border border-white/30">
                  <SparklesIcon className="h-7 w-7 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-white">Content AI Suite</h1>
                  <p className="text-xs text-indigo-100 font-medium">Intelligent Content Platform</p>
                </div>
              </div>
              
              <button
                onClick={() => setSidebarOpen(false)}
                className="lg:hidden p-2 rounded-lg bg-white/20 text-white hover:bg-white/30"
              >
                <XMarkIcon className="h-5 w-5" />
              </button>
            </div>
          </div>
          
          {/* Navigation */}
          <nav className="flex-1 px-4 py-8 space-y-2">
            {navigation.map((item, index) => (
              <NavLink
                key={item.name}
                to={item.href}
                className={({ isActive }) =>
                  `group flex items-center px-4 py-4 text-sm font-semibold rounded-2xl transition-all duration-300 ${
                    isActive
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-xl'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <div className={`flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-xl transition-all duration-300 ${
                      isActive 
                        ? 'bg-white/20 backdrop-blur-sm' 
                        : 'bg-gray-100 group-hover:bg-indigo-100'
                    }`}>
                      <item.icon className={`h-5 w-5 ${isActive ? 'text-white' : 'text-gray-600'}`} />
                    </div>
                    
                    <div className="ml-4 flex-1">
                      <div className={`font-bold ${isActive ? 'text-white' : 'text-gray-900'}`}>
                        {item.name}
                      </div>
                      <div className={`text-xs mt-1 ${isActive ? 'text-indigo-100' : 'text-gray-500'}`}>
                        {item.description}
                      </div>
                    </div>
                  </>
                )}
              </NavLink>
            ))}
          </nav>

          {/* Bottom section */}
          <div className="p-4 border-t border-gray-200/50">
            <div className="rounded-2xl bg-gradient-to-br from-indigo-50 to-purple-50 p-4 border border-indigo-100">
              <div className="flex items-center space-x-3">
                <div className="h-10 w-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                  <span className="text-sm font-bold text-white">AI</span>
                </div>
                <div className="flex-1">
                  <div className="text-sm font-semibold text-gray-900">AI Assistant</div>
                  <div className="text-xs text-gray-600">Always here to help</div>
                </div>
                <BoltIcon className="h-5 w-5 text-indigo-500" />
              </div>
            </div>

            <div className="mt-4 px-2">
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>Version 2.1.0</span>
                <div className="flex items-center space-x-1">
                  <div className="h-2 w-2 rounded-full bg-emerald-400"></div>
                  <span>Online</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile menu button */}
      <button
        onClick={() => setSidebarOpen(true)}
        className="lg:hidden fixed top-4 left-4 z-40 flex h-12 w-12 items-center justify-center rounded-xl bg-white shadow-lg border text-gray-600"
      >
        <Bars3Icon className="h-6 w-6" />
      </button>

      {/* Main Content Area - Remove all padding and margins */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
