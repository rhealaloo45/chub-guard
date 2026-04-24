import React from 'react';
import OpenAI from 'openai';

function App() {
  const handleClick = async () => {
    // This uses a deprecated pattern
    const result = await ChatCompletion.create({
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: "Hello" }]
    });
    console.log(result);
  };

  return <button onClick={handleClick}>Ask AI</button>;
}

export default App;
