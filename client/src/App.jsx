import React, { useState } from 'react';
import axios from 'axios';
import { Shield, Brain, Lock, Unlock, Zap, Copy, Terminal } from 'lucide-react';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [mode, setMode] = useState('encrypt'); // 'encrypt' or 'decrypt'
  const [input, setInput] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');
  const [payload, setPayload] = useState('');

  const handleProcess = async () => {
    if (!input || !password) return;
    setLoading(true);
    setResult('');
    
    try {
      if (mode === 'encrypt') {
        const response = await axios.post(`${API_URL}/encrypt`, {
          message: input,
          password: password
        });
        setResult(response.data.camouflage_text);
        setPayload(response.data.raw_payload);
      } else {
        const response = await axios.post(`${API_URL}/decrypt`, {
          camouflage_text: input,
          password: password
        });
        setResult(response.data.message);
      }
    } catch (error) {
      setResult(`ERROR: ${error.response?.data?.detail || 'Process failed'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <div className="logo">VACHANA-CRYPT</div>
        <div className="badge">Sarvam-30B Powered</div>
      </header>

      <main className="grid-layout">
        {/* Left Side: Input Vault */}
        <section className="glass-card">
          <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
            <button 
              className={`primary-btn ${mode !== 'encrypt' && 'secondary'}`}
              onClick={() => { setMode('encrypt'); setInput(''); setResult(''); }}
              style={{ background: mode === 'encrypt' ? '' : 'rgba(255,255,255,0.05)', color: mode === 'encrypt' ? '' : '#fff' }}
            >
              <Lock size={18} /> Encrypt
            </button>
            <button 
              className={`primary-btn ${mode !== 'decrypt' && 'secondary'}`}
              onClick={() => { setMode('decrypt'); setInput(''); setResult(''); }}
              style={{ background: mode === 'decrypt' ? '' : 'rgba(255,255,255,0.05)', color: mode === 'decrypt' ? '' : '#fff' }}
            >
              <Unlock size={18} /> Decrypt
            </button>
          </div>

          <h2>
            {mode === 'encrypt' ? <Shield size={20} /> : <Terminal size={20} />}
            {mode === 'encrypt' ? 'Secure Vault' : 'Extraction Terminal'}
          </h2>

          <div className="input-group">
            <label>{mode === 'encrypt' ? 'Secret Message' : 'Camouflage Text'}</label>
            <textarea 
              rows="6" 
              placeholder={mode === 'encrypt' ? 'Enter sensitive information...' : 'Paste the AI-generated text...'}
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Master Key (AES-256)</label>
            <input 
              type="password" 
              placeholder="Enter cryptographic password..."
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button 
            className="primary-btn" 
            onClick={handleProcess}
            disabled={loading}
          >
            {loading ? (
              <div className="neural-pulse"></div>
            ) : (
              <>{mode === 'encrypt' ? <Zap size={18} /> : <Unlock size={18} />} {mode === 'encrypt' ? 'Generate Camouflage' : 'Decrypt Secret'}</>
            )}
          </button>
        </section>

        {/* Right Side: Neural Output */}
        <section className="glass-card">
          <h2>
            <Brain size={20} /> 
            {mode === 'encrypt' ? 'Sarvam-30B Neural Output' : 'Decrypted Truth'}
          </h2>
          
          <div className="output-area">
            {result ? (
              <div className={mode === 'encrypt' ? 'hinglish-text' : ''}>
                {result}
              </div>
            ) : (
              <div style={{ color: 'rgba(255,255,255,0.2)', textAlign: 'center', marginTop: '4rem' }}>
                <Brain size={48} style={{ marginBottom: '1rem', opacity: 0.2 }} />
                <p>Waiting for process initiation...</p>
              </div>
            )}
          </div>

          {mode === 'encrypt' && result && (
            <div style={{ marginTop: '1.5rem' }}>
              <label style={{ fontSize: '0.7rem', color: 'var(--accent-emerald)' }}>CRYPTO-PAYLOAD DETECTED</label>
              <div style={{ 
                fontSize: '0.7rem', 
                background: 'rgba(0,0,0,0.5)', 
                padding: '0.5rem', 
                borderRadius: '8px',
                wordBreak: 'break-all',
                color: 'var(--text-secondary)'
              }}>
                {payload}
              </div>
            </div>
          )}
        </section>
      </main>

      <footer style={{ marginTop: '4rem', textAlign: 'center', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
        <p>© 2026 Vachana-Crypt • Sovereignty through Intelligence • Local Systems Only</p>
      </footer>
    </div>
  );
}

export default App;
