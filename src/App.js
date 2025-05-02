import { useState } from 'react';
import './App.css';

function App() {
  const [llmInput, setLLMInput] = useState("")
  const [serverAnswer, setServerAnswer] = useState("")
  let buttonState = llmInput === '' ? true : false

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(`Your input is: ${llmInput}`)
    let postMessage = {
      text: llmInput
    }
    setLLMInput("")
    fetch("http://127.0.0.1:5000/response", {
      method: 'POST',
      body: JSON.stringify(postMessage),
    })
      .then(response => response.json())
      .then(data => {
        console.log(data); //Print the prediction. Debugging purposes only
        setServerAnswer(data.response)
      })
      .catch(error => {
        console.error('Error:', error);

      });
  }

  return (
    <>
      <h1>TELSIP LLM PLAYGROUND</h1>
      <article className="l-design-width">
        <div className="card">
          <h2>
            <svg className="icon" viewBox="0 0 20 20" aria-hidden="true">
              <path
                fill="currentColor"
                d="M15,17H14V9h3a3,3,0,0,1,3,3h0A5,5,0,0,1,15,17Zm1-6v3.83A3,3,0,0,0,18,12a1,1,0,0,0-1-1Z"
              />
              <rect
                fill="currentColor"
                x="1"
                y="7"
                width="15"
                height="12"
                rx="3"
                ry="3"
              />
              <path
                fill="var(--color-accent)"
                d="M7.07,5.42a5.45,5.45,0,0,1,0-4.85,1,1,0,0,1,1.79.89,3.44,3.44,0,0,0,0,3.06,1,1,0,0,1-1.79.89Z"
              />
              <path
                fill="var(--color-accent)"
                d="M3.07,5.42a5.45,5.45,0,0,1,0-4.85,1,1,0,0,1,1.79.89,3.44,3.44,0,0,0,0,3.06,1,1,0,1,1-1.79.89Z"
              />
              <path
                fill="var(--color-accent)"
                d="M11.07,5.42a5.45,5.45,0,0,1,0-4.85,1,1,0,0,1,1.79.89,3.44,3.44,0,0,0,0,3.06,1,1,0,1,1-1.79.89Z"
              />
            </svg>
            Currently Chatting with MistralAI
          </h2>

          <div className="request">
            <form onSubmit={handleSubmit}>
              <label className="input">
                <input
                  className="input__field"
                  type="text"
                  placeholder=" "
                  value={llmInput}
                  onChange={(e) => setLLMInput(e.target.value)}
                />
                <span className="input__label">Talk to the LLM</span>
              </label>
              <div className="button-group">
                <input
                  type="submit"
                  className="button"
                  disabled={buttonState}
                  value="Send"
                />
              </div>
            </form>
          </div>
        </div>
        {serverAnswer && (
          <div className="card card--inverted">
            <h2>
              <svg className="icon" viewBox="0 0 20 20" aria-hidden="true">
                <path
                  fill="#fab700"
                  d="M10 1a1 1 0 1 0-2 0v1.07A7 7 0 0 0 2 9v4a3 3 0 0 0 3 3v1a1 1 0 1 0 2 0v-1h6v1a1 1 0 1 0 2 0v-1a3 3 0 0 0 3-3V9a7 7 0 0 0-6-6.93V1a1 1 0 0 0-2 0v1zM4 9a6 6 0 0 1 12 0v4a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V9zm3 1a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm6 0a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"
                />
              </svg>
              LLM Answer
            </h2>
            <p>{serverAnswer}</p>
          </div>
        )}
      </article>

    </>
  )
}
export default App