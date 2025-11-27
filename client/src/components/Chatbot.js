import React, { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

// Generate a unique session ID for this browser session
const generateSessionId = () => {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 15);
  return `session-${timestamp}-${random}`;
};

function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(() => {
    // Try to get existing session ID from localStorage
    const stored = localStorage.getItem('chatbot_session_id');
    if (stored) return stored;
    
    // Generate new session ID
    const newId = generateSessionId();
    localStorage.setItem('chatbot_session_id', newId);
    return newId;
  });
  const messagesEndRef = useRef(null);
  const chatbotApiUrl = 'http://localhost:5001';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message to chat
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${chatbotApiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: userMessage,
          session_id: sessionId
        }),
      });

      const data = await response.json();

      // Check if response contains an error
      if (data.error) {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: `I apologize, but I encountered an error: ${data.error}` 
        }]);
      } else if (data.response) {
        // Success - add assistant response
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: data.response 
        }]);
      } else {
        // Unexpected response format
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: 'I received an unexpected response. Please try again.' 
        }]);
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `I'm having trouble connecting to the chatbot service. Please make sure it's running on port 5001. Error: ${error.message}` 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const resetChat = () => {
    // Generate new session ID
    const newId = generateSessionId();
    setSessionId(newId);
    localStorage.setItem('chatbot_session_id', newId);
    
    // Clear messages
    setMessages([]);
  };

  return (
    <>
      {/* Chat Button */}
      <button 
        className="chat-button"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chat"
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <h3>🛒 Shopping Assistant</h3>
            <button onClick={resetChat} className="reset-button" title="Reset conversation">
              🔄
            </button>
          </div>

          <div className="chat-messages">
            {messages.length === 0 && (
              <div className="welcome-message">
                <p>👋 Hi! I'm your shopping assistant.</p>
                <p>I can help you:</p>
                <ul>
                  <li>Browse products</li>
                  <li>Get product details</li>
                  <li>Manage your cart</li>
                  <li>Find recommendations</li>
                </ul>
                <p>How can I help you today?</p>
              </div>
            )}
            
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                <div className="message-content">
                  {msg.content}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="message assistant">
                <div className="message-content typing">
                  <span></span><span></span><span></span>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-container">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything..."
              rows="2"
              disabled={isLoading}
            />
            <button 
              onClick={sendMessage} 
              disabled={isLoading || !input.trim()}
              className="send-button"
            >
              ➤
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default Chatbot;
