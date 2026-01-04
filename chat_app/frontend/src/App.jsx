import { useEffect, useState } from "react";

const ws = new WebSocket("ws://localhost:8000/ws"); // WebSocket connection

function App() {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState([]);

  // Receive messages from WebSocket
  useEffect(() => {
    ws.onmessage = (event) => {
      setMessages((prev) => [...prev, JSON.parse(event.data)]);
    };
  }, []);

  // Send message via WebSocket
  const sendMessage = () => {
    if (!text) return;
    ws.send(JSON.stringify({ user: "User", text }));
    setText("");
  };

  // Fetch all messages from backend GET /messages
  const getMessages = async () => {
    try {
      const response = await fetch("http://localhost:8000/messages");
      const data = await response.json();
      setMessages(data); // update messages state with all data from Mongo
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Chat App</h2>

      {/* Button to fetch messages */}
      <button onClick={getMessages}>Get Messages</button>

      <div style={{ marginTop: 20 }}>
        {messages.map((m, i) => (
          <p key={i}>
            <b>{m.user}:</b> {m.text}
          </p>
        ))}
      </div>

      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your message"
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;
