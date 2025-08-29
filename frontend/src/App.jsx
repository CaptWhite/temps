import { useState, useEffect } from "react";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("/api/hello")
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <div className="w-full h-full flex justify-center items-center">
      <h1 className="text-3xl font-bold">{message}</h1>
    </div>
  );
}

export default App;
