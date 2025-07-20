import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import ContentGeneration from './components/ContentGeneration';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route path="generate" element={<ContentGeneration />} />
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
