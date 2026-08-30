import { useEffect, useState } from "react"

function App() {
  const [message, setMessage] = useState("Загрузка...")

  useEffect(() => {
    fetch("http://127.0.0.1:8000/about")
      .then(response => response.json())
      .then(data => {
        setMessage(data.message)
      })
  }, [])

  return (
    <>
      <h1>React</h1>
      <p>{message}</p>
    </>
  )
}

export default App