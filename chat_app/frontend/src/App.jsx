
import { useEffect, useState } from "react";

const ws = new WebSocket("ws://localhost:8000/ws");

function App() {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");

  useEffect(() => {
    ws.onmessage = (event) => {
      setMessages((prev) => [...prev, JSON.parse(event.data)]);
    };
  }, []);

  const sendMessage = () => {
    if (!text) return;
    ws.send(JSON.stringify({ user: "User", text }));
    setText("");
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Chat App</h2>
      {messages.map((m, i) => (
        <p key={i}><b>{m.user}:</b> {m.text}</p>
      ))}
      <input value={text} onChange={e => setText(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;
