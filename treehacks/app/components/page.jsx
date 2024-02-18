"use client"
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { useEffect, useState } from "react"
import { ChatComponent } from "./ui/chatcontainer"

export function HomePage() {

  const [messages, setMessages] = useState(() => {
    if (typeof window !== 'undefined') {
      const savedmessages = localStorage.getItem('messages');
      return savedmessages ? JSON.parse(savedmessages) : ["Hi there, what can I help you with today"];
      }
  });
  const [input, setInput] = useState("");
  const [isEnlarged, setIsEnlarged] = useState(false);

  const getMessages = async () => {
    var response = { "role": "assistant", "content": "I am a bot"}
    try {
      response = await fetch("http://localhost:5328/", {
        method: "POST",
        // mode: "no-cors",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 'role': "user", 'content': input }),
      });
      response = await response.json();
    } catch (error) {
      console.error("Error:", error);
    }

    return response["content"];
  };

  const [loading, setLoading] = useState(false);

  const toggleEnlarged = () => {
    setIsEnlarged(!isEnlarged);
  };

  const clearMessages = () => {
    setMessages(["Hi there, what can I help you with today"]);
  };

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };
  const onSubmitInput = async () => {
    if (input.trim() === "") return;
    setLoading(true);
    const aimessage = await getMessages();
    setMessages([...messages, input, aimessage]);
    setLoading(false);
    setInput("");
    console.log(messages);
  }
  const handleKeyDown = (event) => {
    // Check if the key pressed is the Enter key
    if (event.key === 'Enter') {
      onSubmitInput();
    }
  };
  
  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('messages', JSON.stringify(messages));
    }
  }, [messages]);

  return (
    (<div className="bg-[#ffccd5] min-h-screen">
      <nav className="bg-white py-4">
        <div className="container mx-auto flex justify-between items-center px-4">
          <h1 className="text-2xl font-bold">Insightful.ai</h1>
          <div className="flex space-x-4">
            <Button className="px-4 py-2">Home</Button>
            <Button className="px-4 py-2" variant="outline">
              Sign In
            </Button>
            <Button className="px-4 py-2">Sign Up</Button>
          </div>
        </div>
      </nav>
      <div className="container mx-auto px-4">
        <div className="flex flex-col sm:flex-row justify-between items-center mt-8">
          <div className="flex flex-col items-center space-y-6">
            <img className ={`cursor-pointer justify-center rounded-lg ${isEnlarged ? 'w-[50vw] max-w-none h-auto' : 'w-auto h-auto'}`} src = "https://i.stack.imgur.com/ZfipQ.png" onDoubleClick={toggleEnlarged}/>
          </div>
          <div className = "m-2.5"></div>
          <div className={`bg-white rounded-lg shadow-lg p-6 ${isEnlarged ? 'w-auto' : 'sm:w-[50vw]'} `}>
              <div className="flex flex-col space-y-6">

              <div className="flex justify-end">
                <Button className="bg-red-500 w-2 h-7 text-white" variant="secondary" onClick={clearMessages}>
                  <div className="flex items-center space-x-2">
                    <span>x</span>
                  </div>
                </Button>
              </div>
              <div class="w-full h-1 bg-black"></div>

              <ChatComponent messages = {messages} />
              <div className="flex items-center">
                <Input className="flex-1" placeholder="Type something" value = {input} onChange = {handleInputChange} onKeyDown = {handleKeyDown}/>
                <Button className="ml-2 bg-black text-white" variant="secondary" onClick = {onSubmitInput}>
                  {`>`}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>)
  );
}

