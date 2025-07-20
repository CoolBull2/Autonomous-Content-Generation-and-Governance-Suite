import React, { useState } from 'react';
import { 
  PlusIcon,
  ArrowPathIcon,
  DocumentTextIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  SparklesIcon,
  UserGroupIcon,
  AdjustmentsHorizontalIcon,
  ClipboardDocumentListIcon,
  ArrowDownTrayIcon,
  EyeIcon,
  StarIcon,
  TagIcon,
  ClockIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';
import axios from 'axios';

const ContentGeneration = () => {
  const [formData, setFormData] = useState({
    topic: '',
    target_audience: 'general',
    style_guide: {
      tone: 'professional',
      length: 'medium'
    }
  });

  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedContent, setGeneratedContent] = useState(null);
  const [error, setError] = useState(null);
  const [exportLoading, setExportLoading] = useState({
    pdf: false,
    word: false,
    json: false
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name.includes('.')) {
      const [parent, child] = name.split('.');
      setFormData(prev => ({
        ...prev,
        [parent]: {
          ...prev[parent],
          [child]: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsGenerating(true);
    setError(null);
    setGeneratedContent(null);

    try {
      const requestData = {
        type: 'text',
        topic: formData.topic,
        target_audience: formData.target_audience,
        style_guide: formData.style_guide
      };

      const response = await axios.post('http://localhost:8000/generate-and-govern', requestData);
      setGeneratedContent(response.data.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while generating content');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExportPDF = async () => {
    if (!generatedContent) return;
    
    setExportLoading(prev => ({ ...prev, pdf: true }));
    try {
      const response = await axios.post('http://localhost:8000/export/pdf', generatedContent, {
        responseType: 'blob'
      });
      
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `content_report_${Date.now()}.pdf`;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('PDF export failed:', error);
      alert('Failed to export PDF. Please try again.');
    } finally {
      setExportLoading(prev => ({ ...prev, pdf: false }));
    }
  };

  const handleExportWord = async () => {
    if (!generatedContent) return;
    
    setExportLoading(prev => ({ ...prev, word: true }));
    try {
      const response = await axios.post('http://localhost:8000/export/word', generatedContent, {
        responseType: 'blob'
      });
      
      const blob = new Blob([response.data], { 
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
      });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `content_report_${Date.now()}.docx`;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Word export failed:', error);
      alert('Failed to export Word document. Please try again.');
    } finally {
      setExportLoading(prev => ({ ...prev, word: false }));
    }
  };

  const handleExportJSON = async () => {
    if (!generatedContent) return;
    
    setExportLoading(prev => ({ ...prev, json: true }));
    try {
      const jsonData = JSON.stringify(generatedContent, null, 2);
      const blob = new Blob([jsonData], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `content_analysis_${Date.now()}.json`;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('JSON export failed:', error);
      alert('Failed to export JSON. Please try again.');
    } finally {
      setExportLoading(prev => ({ ...prev, json: false }));
    }
  };

  const getDecisionColor = (decision) => {
    switch (decision) {
      case 'Approved':
        return 'text-emerald-700 bg-emerald-100 border-emerald-200';
      case 'Needs Revision':
        return 'text-amber-700 bg-amber-100 border-amber-200';
      case 'Rejected':
        return 'text-rose-700 bg-rose-100 border-rose-200';
      default:
        return 'text-slate-700 bg-slate-100 border-slate-200';
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-emerald-600 bg-emerald-50';
    if (score >= 60) return 'text-amber-600 bg-amber-50';
    return 'text-rose-600 bg-rose-50';
  };

  return (
    <div className="h-full bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <div className="h-full flex flex-col">
        {/* Header Section - Reduced height */}
        <div className="flex-shrink-0 p-6 pb-4">
          <div className="relative overflow-hidden rounded-2xl">
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-600 to-purple-600 transform -skew-y-1"></div>
            <div className="relative bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-4 sm:space-y-0">
                <div className="flex items-center space-x-4">
                  <div className="flex-shrink-0 w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                    <SparklesIcon className="w-7 h-7 text-white" />
                  </div>
                  <div>
                    <h1 className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                      Content Generation Studio
                    </h1>
                    <p className="text-gray-600 mt-1 font-medium">Create intelligent, governed content with AI</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3 px-4 py-2 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-full border border-indigo-200">
                  <DocumentTextIcon className="w-5 h-5 text-indigo-600" />
                  <span className="text-sm font-semibold text-indigo-700">AI Text Generator</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Area - Make it scrollable */}
        <div className="flex-1 overflow-y-auto px-6 pb-6">
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 h-full">
            {/* Generation Form */}
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden flex flex-col">
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 px-6 py-4 flex-shrink-0">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                    <PlusIcon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h2 className="text-lg font-bold text-white">Create New Content</h2>
                    <p className="text-indigo-100 text-sm">Configure your content parameters</p>
                  </div>
                </div>
              </div>
              
              <div className="flex-1 overflow-y-auto">
                <form onSubmit={handleSubmit} className="p-6 space-y-6">
                  {/* Topic Input */}
                  <div className="space-y-2">
                    <label className="flex items-center space-x-2 text-sm font-semibold text-gray-800 mb-3">
                      <ClipboardDocumentListIcon className="w-5 h-5 text-indigo-600" />
                      <span>Content Topic</span>
                    </label>
                    <div className="relative">
                      <input
                        type="text"
                        name="topic"
                        value={formData.topic}
                        onChange={handleInputChange}
                        placeholder="What would you like to write about today?"
                        className="w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-indigo-500 focus:ring-4 focus:ring-indigo-50 transition-all duration-300 text-gray-800 placeholder-gray-500 bg-gradient-to-r from-gray-50 to-white"
                        required
                      />
                      <div className="absolute inset-y-0 right-0 flex items-center pr-4">
                        <TagIcon className="w-5 h-5 text-gray-400" />
                      </div>
                    </div>
                  </div>

                  {/* Target Audience */}
                  <div className="space-y-2">
                    <label className="flex items-center space-x-2 text-sm font-semibold text-gray-800 mb-3">
                      <UserGroupIcon className="w-5 h-5 text-indigo-600" />
                      <span>Target Audience</span>
                    </label>
                    <div className="relative">
                      <select
                        name="target_audience"
                        value={formData.target_audience}
                        onChange={handleInputChange}
                        className="w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-indigo-500 focus:ring-4 focus:ring-indigo-50 transition-all duration-300 text-gray-800 bg-gradient-to-r from-gray-50 to-white appearance-none"
                      >
                        <option value="general">🌍 General Audience</option>
                        <option value="tech_professionals">💻 Tech Professionals</option>
                        <option value="business_leaders">👔 Business Leaders</option>
                        <option value="healthcare_professionals">🏥 Healthcare Professionals</option>
                        <option value="students">🎓 Students</option>
                        <option value="marketers">📊 Marketing Professionals</option>
                      </select>
                      <div className="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
                        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                        </svg>
                      </div>
                    </div>
                  </div>

                  {/* Style Guide Settings */}
                  <div className="space-y-4">
                    <div className="flex items-center space-x-2 mb-4">
                      <AdjustmentsHorizontalIcon className="w-5 h-5 text-indigo-600" />
                      <span className="text-sm font-semibold text-gray-800">Style Configuration</span>
                    </div>
                    
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <label className="block text-sm font-medium text-gray-700">Tone & Voice</label>
                        <div className="relative">
                          <select
                            name="style_guide.tone"
                            value={formData.style_guide.tone}
                            onChange={handleInputChange}
                            className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-50 transition-all duration-300 text-gray-800 bg-white appearance-none"
                          >
                            <option value="professional">🎯 Professional</option>
                            <option value="casual">😊 Casual</option>
                            <option value="friendly">🤝 Friendly</option>
                            <option value="authoritative">👑 Authoritative</option>
                            <option value="creative">🎨 Creative</option>
                            <option value="conversational">💬 Conversational</option>
                          </select>
                          <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                            <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                            </svg>
                          </div>
                        </div>
                      </div>

                      <div className="space-y-2">
                        <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
                          <ClockIcon className="w-4 h-4" />
                          <span>Content Length</span>
                        </label>
                        <div className="relative">
                          <select
                            name="style_guide.length"
                            value={formData.style_guide.length}
                            onChange={handleInputChange}
                            className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-50 transition-all duration-300 text-gray-800 bg-white appearance-none"
                          >
                            <option value="short">⚡ Short (~200 words)</option>
                            <option value="medium">📄 Medium (200-500 words)</option>
                            <option value="long">📚 Long (500+ words)</option>
                          </select>
                          <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                            <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                            </svg>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={isGenerating}
                    className={`w-full py-4 px-6 rounded-xl font-bold text-white transition-all duration-300 shadow-lg ${
                      isGenerating 
                        ? 'bg-gradient-to-r from-gray-400 to-gray-500 cursor-not-allowed' 
                        : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700'
                    }`}
                  >
                    <div className="flex items-center justify-center space-x-3">
                      {isGenerating ? (
                        <>
                          <ArrowPathIcon className="w-6 h-6 animate-spin" />
                          <span>Generating Content...</span>
                        </>
                      ) : (
                        <>
                          <SparklesIcon className="w-6 h-6" />
                          <span>Generate AI Content</span>
                        </>
                      )}
                    </div>
                  </button>

                  {isGenerating && (
                    <div className="text-center space-y-2">
                      <div className="flex justify-center space-x-1">
                        <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      </div>
                      <p className="text-sm text-gray-600 font-medium">AI is crafting your content...</p>
                    </div>
                  )}
                </form>

                {error && (
                  <div className="mx-6 mb-6 p-4 bg-gradient-to-r from-red-50 to-rose-50 border-2 border-red-200 rounded-xl">
                    <div className="flex items-start space-x-3">
                      <ExclamationCircleIcon className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
                      <div>
                        <h4 className="font-semibold text-red-800 mb-1">Generation Failed</h4>
                        <p className="text-red-700 text-sm">{error}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Results Panel */}
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden flex flex-col">
              <div className="bg-gradient-to-r from-emerald-500 to-teal-600 px-6 py-4 flex-shrink-0">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                    <EyeIcon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h2 className="text-lg font-bold text-white">Generated Content</h2>
                    <p className="text-emerald-100 text-sm">Review and export your content</p>
                  </div>
                </div>
              </div>
              
              <div className="flex-1 overflow-y-auto p-6">
                {!generatedContent && !isGenerating && (
                  <div className="h-full flex items-center justify-center">
                    <div className="text-center space-y-4">
                      <div className="w-24 h-24 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto">
                        <DocumentTextIcon className="w-12 h-12 text-gray-400" />
                      </div>
                      <div className="space-y-2">
                        <h3 className="text-lg font-semibold text-gray-700">Ready to Generate</h3>
                        <p className="text-gray-500">Your AI-generated content will appear here</p>
                        <p className="text-sm text-gray-400">Fill out the form and click generate to get started</p>
                      </div>
                    </div>
                  </div>
                )}

                {isGenerating && (
                  <div className="h-full flex items-center justify-center">
                    <div className="text-center space-y-6">
                      <div className="relative w-24 h-24 mx-auto">
                        <div className="absolute inset-0 rounded-full border-4 border-indigo-100"></div>
                        <div className="absolute inset-0 rounded-full border-4 border-indigo-500 border-t-transparent animate-spin"></div>
                        <ArrowPathIcon className="w-8 h-8 text-indigo-500 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
                      </div>
                      <div className="space-y-2">
                        <h3 className="text-lg font-semibold text-gray-700">AI Working...</h3>
                        <p className="text-gray-600">Generating and reviewing your content</p>
                      </div>
                    </div>
                  </div>
                )}

                {generatedContent && (
                  <div className="space-y-8">
                    {/* Final Decision */}
                    {generatedContent.final_decision && (
                      <div className="relative overflow-hidden">
                        <div className="absolute inset-0 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl"></div>
                        <div className={`relative p-6 rounded-xl border-2 ${getDecisionColor(generatedContent.final_decision.final_decision)}`}>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              {generatedContent.final_decision.final_decision === 'Approved' ? (
                                <div className="w-10 h-10 bg-emerald-500 rounded-full flex items-center justify-center">
                                  <CheckCircleIcon className="w-6 h-6 text-white" />
                                </div>
                              ) : (
                                <div className="w-10 h-10 bg-amber-500 rounded-full flex items-center justify-center">
                                  <ExclamationCircleIcon className="w-6 h-6 text-white" />
                                </div>
                              )}
                              <div>
                                <span className="font-bold text-gray-800">Content Review Status</span>
                                <p className="text-sm text-gray-600 mt-1">AI governance assessment complete</p>
                              </div>
                            </div>
                            <span className={`px-4 py-2 rounded-full text-sm font-bold border-2 ${getDecisionColor(generatedContent.final_decision.final_decision)}`}>
                              {generatedContent.final_decision.final_decision}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Generated Text Content */}
                    {(generatedContent.content || generatedContent.text_content) && (
                      <div className="space-y-4">
                        <div className="flex items-center space-x-2">
                          <DocumentTextIcon className="w-5 h-5 text-indigo-600" />
                          <h3 className="font-bold text-gray-900">Generated Content</h3>
                        </div>
                        <div className="relative">
                          <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 rounded-xl"></div>
                          <div className="relative p-6 border-2 border-indigo-100 rounded-xl bg-white/80 backdrop-blur-sm">
                            <div className="prose prose-sm sm:prose-base max-w-none">
                              <p className="text-gray-800 leading-relaxed whitespace-pre-wrap font-medium">
                                {generatedContent.content || generatedContent.text_content}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Review Summary */}
                    {generatedContent.final_decision?.summary && (
                      <div className="space-y-4">
                        <div className="flex items-center space-x-2">
                          <ChartBarIcon className="w-5 h-5 text-indigo-600" />
                          <h3 className="font-bold text-gray-900">Review Analysis</h3>
                        </div>
                        <div className="bg-gradient-to-r from-gray-50 to-slate-50 p-6 rounded-xl border border-gray-200">
                          <div className="space-y-3">
                            {generatedContent.final_decision.summary.map((point, index) => (
                              <div key={index} className="flex items-start space-x-3 group">
                                <div className="w-6 h-6 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 group-hover:scale-110 transition-transform duration-200">
                                  <span className="text-white text-xs font-bold">{index + 1}</span>
                                </div>
                                <p className="text-gray-700 font-medium leading-relaxed">{point}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Quality Score */}
                    {generatedContent.final_decision?.final_score && (
                      <div className="space-y-4">
                        <div className="flex items-center space-x-2">
                          <StarIcon className="w-5 h-5 text-indigo-600" />
                          <h3 className="font-bold text-gray-900">Quality Assessment</h3>
                        </div>
                        <div className={`p-6 rounded-xl border-2 ${getScoreColor(generatedContent.final_decision.final_score * 100)}`}>
                          <div className="flex items-center justify-between">
                            <div>
                              <span className="font-semibold text-gray-800">Overall Quality Score</span>
                              <p className="text-sm text-gray-600 mt-1">Based on AI governance criteria</p>
                            </div>
                            <div className="text-right">
                              <div className="text-3xl font-bold text-gray-800">
                                {(generatedContent.final_decision.final_score * 100).toFixed(1)}%
                              </div>
                              <div className="flex items-center justify-end space-x-1 mt-1">
                                {[...Array(5)].map((_, i) => (
                                  <StarIcon 
                                    key={i} 
                                    className={`w-4 h-4 ${
                                      i < Math.floor((generatedContent.final_decision.final_score * 5)) 
                                        ? 'text-yellow-400 fill-current' 
                                        : 'text-gray-300'
                                    }`} 
                                  />
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Export Options */}
                    <div className="space-y-6 pt-6 border-t border-gray-200">
                      <div className="flex items-center space-x-2">
                        <ArrowDownTrayIcon className="w-5 h-5 text-indigo-600" />
                        <h3 className="font-bold text-gray-900">Export Options</h3>
                      </div>
                      
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        {generatedContent.final_decision && (
                          <>
                            <button 
                              onClick={handleExportPDF} 
                              disabled={exportLoading.pdf}
                              className={`group relative overflow-hidden p-4 rounded-xl border-2 transition-all duration-300 ${
                                exportLoading.pdf 
                                  ? 'bg-gray-100 border-gray-200 cursor-not-allowed' 
                                  : 'bg-gradient-to-br from-red-50 to-pink-50 border-red-200 hover:border-red-300 hover:shadow-lg hover:-translate-y-1'
                              }`}
                            >
                              <div className="flex flex-col items-center space-y-3">
                                {exportLoading.pdf ? (
                                  <ArrowPathIcon className="w-8 h-8 text-gray-400 animate-spin" />
                                ) : (
                                  <div className="w-12 h-12 bg-gradient-to-br from-red-500 to-pink-600 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                                    <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                                      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                                    </svg>
                                  </div>
                                )}
                                <div className="text-center">
                                  <div className="font-bold text-gray-800">
                                    {exportLoading.pdf ? 'Exporting...' : 'Export PDF'}
                                  </div>
                                  <div className="text-xs text-gray-600 mt-1">Professional report</div>
                                </div>
                              </div>
                            </button>
                            
                            <button 
                              onClick={handleExportWord} 
                              disabled={exportLoading.word}
                              className={`group relative overflow-hidden p-4 rounded-xl border-2 transition-all duration-300 ${
                                exportLoading.word 
                                  ? 'bg-gray-100 border-gray-200 cursor-not-allowed' 
                                  : 'bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200 hover:border-blue-300 hover:shadow-lg hover:-translate-y-1'
                              }`}
                            >
                              <div className="flex flex-col items-center space-y-3">
                                {exportLoading.word ? (
                                  <ArrowPathIcon className="w-8 h-8 text-gray-400 animate-spin" />
                                ) : (
                                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                                    <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                                      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                                    </svg>
                                  </div>
                                )}
                                <div className="text-center">
                                  <div className="font-bold text-gray-800">
                                    {exportLoading.word ? 'Exporting...' : 'Export Word'}
                                  </div>
                                  <div className="text-xs text-gray-600 mt-1">Editable document</div>
                                </div>
                              </div>
                            </button>
                          </>
                        )}
                        
                        <button 
                          onClick={handleExportJSON} 
                          disabled={exportLoading.json}
                          className={`group relative overflow-hidden p-4 rounded-xl border-2 transition-all duration-300 ${
                            exportLoading.json 
                              ? 'bg-gray-100 border-gray-200 cursor-not-allowed' 
                              : 'bg-gradient-to-br from-green-50 to-emerald-50 border-green-200 hover:border-green-300 hover:shadow-lg hover:-translate-y-1'
                          }`}
                        >
                          <div className="flex flex-col items-center space-y-3">
                            {exportLoading.json ? (
                              <ArrowPathIcon className="w-8 h-8 text-gray-400 animate-spin" />
                            ) : (
                              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                                <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                                  <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                                </svg>
                              </div>
                            )}
                            <div className="text-center">
                              <div className="font-bold text-gray-800">
                                {exportLoading.json ? 'Exporting...' : 'Export JSON'}
                              </div>
                              <div className="text-xs text-gray-600 mt-1">Raw data format</div>
                            </div>
                          </div>
                        </button>
                      </div>
                      
                      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-4 rounded-xl border border-indigo-200">
                        <div className="flex items-start space-x-3">
                          <svg className="w-5 h-5 text-indigo-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                          </svg>
                          <div>
                            <p className="text-sm font-semibold text-indigo-800 mb-1">Export Information</p>
                            <p className="text-xs text-indigo-700">
                              Choose your preferred format to save and share your AI-generated content analysis. 
                              All exports include governance review data and quality metrics.
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContentGeneration;
