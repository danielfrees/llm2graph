import React, { useEffect, useRef } from 'react';

export function ChatComponent({ messages }) {
  const endOfMessagesRef = useRef(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]); // Dependency array includes messages, so this runs every time messages change

  return (
    <div className= {"max-h-[30vh] overflow-y-auto sm:max-h-[65vh]"} >
        {messages.map((message, index) => (
                <div key={index} className= {`flex items-center mb-2.5  ${index %2 === 1 ? 'justify-end': 'justify-start'}`}>
                  {index % 2 === 0 ? <img src="https://viso.ai/wp-content/uploads/2023/12/Llama-2-blog-image-1-1060x606.png" alt="Left" className="w-10 h-10 rounded-full mr-2" />:  <></>}                
                  <div key={index} className={index % 2 === 0 ? "bg-pink-200 p-4 rounded-lg" : "bg-pink-100 p-4 rounded-lg"}>
                    <p>{message}</p>
                  </div>
                  {index % 2 === 0 ? <></>:  <img src="https://t4.ftcdn.net/jpg/00/65/77/27/360_F_65772719_A1UV5kLi5nCEWI0BNLLiFaBPEkUbv5Fv.jpg" alt="Left" className="w-10 h-10 rounded-full ml-2" />}                

                  <div className = "m-5"></div>
                </div>
        ))}
      {/* Invisible element at the bottom of the container */}
      <div ref={endOfMessagesRef} />
    </div>
  );
}
