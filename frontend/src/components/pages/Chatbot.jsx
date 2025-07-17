import React, { useState } from "react";
import axios from "axios";

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    const handleSendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { sender: "user", text: input };
        setMessages((prev) => [...prev, userMessage]);

        try {
            const response = await axios.post("http://127.0.0.1:8000/api/chatbot/", {
                message: input,
            });

            console.log("Bot Response:", response.data.reply); // Log response

            const botMessage = { sender: "bot", text: response.data.reply };
            setMessages((prev) => [...prev, botMessage]);
        } catch (error) {
            console.error("Error sending message:", error);
        }

        setInput("");
    };

    return (
        <div className="chat-container">
            <div className="chat-box">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
            </div>

            <div className="input-box">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type a message..."
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
};

export default Chatbot;
