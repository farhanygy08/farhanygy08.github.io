 DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Chatbot.AI - Your Sophisticated AI Chat Assistant</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

  :root {
    --color-bg: #1e1e2f;
    --color-primary: #7f5af0;
    --color-primary-hover: #6c48dc;
    --color-text: #e0e0ff;
    --color-text-secondary: #a0a0c0;
    --color-message-bg-user: #4f46e5;
    --color-message-bg-bot: #292942;
    --color-error: #ff6b6b;
  }

  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    font-family: 'Inter', sans-serif;
    background-color: var(--color-bg);
    color: var(--color-text);
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  header {
    background: var(--color-primary);
    padding: 1rem 1.5rem;
    font-weight: 600;
    font-size: 1.5rem;
    color: white;
    text-align: center;
    user-select: none;
  }

  main {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    padding: 1rem;
    overflow: hidden;
  }

  #chat-window {
    flex: 1 1 auto;
    overflow-y: auto;
    padding-right: 0.5rem;
    margin-bottom: 1rem;
  }

  .message {
    max-width: 75%;
    padding: 0.75rem 1rem;
    margin-bottom: 0.8rem;
    border-radius: 12px;
    line-height: 1.4;
    white-space: pre-wrap;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    font-size: 1rem;
  }

  .message.user {
    background-color: var(--color-message-bg-user);
    color: white;
    margin-left: auto;
    border-bottom-right-radius: 0;
  }
  .message.bot {
    background-color: var(--color-message-bg-bot);
    color: var(--color-text);
    margin-right: auto;
    border-bottom-left-radius: 0;
  }

  #input-container {
    display: flex;
    gap: 0.75rem;
  }

  #prompt-input {
    flex: 1 1 auto;
    padding: 0.75rem 1rem;
    border-radius: 9999px;
    border: none;
    font-size: 1rem;
    outline-offset: 2px;
    outline-color: var(--color-primary);
    background-color: #2a2a4a;
    color: var(--color-text);
    transition: background-color 0.2s ease;
  }
  #prompt-input:focus {
    background-color: #3b3b6f;
  }

  button#send-btn {
    background-color: var(--color-primary);
    border: none;
    border-radius: 9999px;
    padding: 0 1.25rem;
    font-weight: 600;
    color: white;
    cursor: pointer;
    transition: background-color 0.2s ease;
    user-select: none;
  }
  button#send-btn:hover:not(:disabled) {
    background-color: var(--color-primary-hover);
  }
  button#send-btn:disabled {
    background-color: #5d4efc88;
    cursor: not-allowed;
  }

  #api-key-container {
    background-color: #2a2a4a;
    padding: 0.75rem 1rem;
    border-radius: 9999px;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    max-width: 480px;
    margin-left: auto;
    margin-right: auto;
  }
  #api-key-input {
    flex: 1 1 auto;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 9999px;
    font-size: 0.9rem;
    background-color: #1f1f3a;
    color: var(--color-text);
    outline-offset: 2px;
    outline-color: var(--color-primary);
  }
  #api-key-input:focus {
    background-color: #353566;
  }
  #save-api-btn {
    background-color: var(--color-primary);
    border: none;
    border-radius: 9999px;
    padding: 0.4rem 1rem;
    font-weight: 600;
    color: white;
    cursor: pointer;
    user-select: none;
    transition: background-color 0.2s ease;
  }
  #save-api-btn:hover {
    background-color: var(--color-primary-hover);
  }

  #status-bar {
    text-align: center;
    margin-bottom: 1rem;
    height: 1.25rem;
    color: var(--color-error);
    font-weight: 600;
    font-size: 0.9rem;
  }

  footer {
    font-size: 0.8rem;
    text-align: center;
    padding: 0.5rem 1rem;
    color: var(--color-text-secondary);
    user-select: none;
  }

  /* Scrollbar styling */
  #chat-window::-webkit-scrollbar {
    width: 8px;
  }
  #chat-window::-webkit-scrollbar-thumb {
    background-color: #5c5c95;
    border-radius: 4px;
  }
</style>
</head>
<body>
<header>Chatbot.AI - Ask Me Anything</header>
<main>
  <div id="api-key-container" title="Enter your OpenAI API key for free usage">
    <input id="api-key-input" type="password" placeholder="Enter your OpenAI API key" aria-label="OpenAI API key"/>
    <button id="save-api-btn" aria-label="Save API key">Save Key</button>
  </div>
  <div id="status-bar" role="alert" aria-live="assertive"></div>
  <div id="chat-window" role="log" aria-live="polite" aria-relevant="additions"></div>
  <form id="input-container" aria-label="Send message to chatbot">
    <input id="prompt-input" type="text" autocomplete="off" placeholder="Type your message here..." aria-label="Chat message input" required />
    <button type="submit" id="send-btn" disabled>Send</button>
  </form>
</main>
<footer>Powered by OpenAI API | Your API key is never sent anywhere else | Chatbot.AI &copy; 2024</footer>

<script>
  const chatWindow = document.getElementById('chat-window');
  const inputForm = document.getElementById('input-container');
  const promptInput = document.getElementById('prompt-input');
  const sendBtn = document.getElementById('send-btn');
  const apiKeyInput = document.getElementById('api-key-input');
  const saveApiBtn = document.getElementById('save-api-btn');
  const statusBar = document.getElementById('status-bar');

  let apiKey = sessionStorage.getItem('openai_api_key') || '';
  apiKeyInput.value = apiKey;
  updateSendButton();

  saveApiBtn.addEventListener('click', () => {
    const key = apiKeyInput.value.trim();
    if (key.length === 0) {
      statusBar.textContent = 'API key cannot be empty.';
      return;
    }
    sessionStorage.setItem('openai_api_key', key);
    apiKey = key;
    statusBar.textContent = 'API key saved successfully.';
    updateSendButton();
  });

  function updateSendButton() {
    sendBtn.disabled = !apiKey || !promptInput.value.trim();
  }

  promptInput.addEventListener('input', () => {
    updateSendButton();
  });

  function appendMessage(text, sender = 'bot') {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message');
    msgDiv.classList.add(sender);
    msgDiv.textContent = text;
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  async function callOpenAI(messages) {
    const url = 'https://api.openai.com/v1/chat/completions';
    const body = {
      model: 'gpt-4',
      messages: messages,
      temperature: 0.8,
      max_tokens: 1000,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0
    };
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apiKey
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error.message || 'OpenAI API error');
    }
    const data = await response.json();
    return data.choices[0].message.content.trim();
  }

  inputForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userInput = promptInput.value.trim();
    if (!userInput) return;

    appendMessage(userInput, 'user');
    promptInput.value = '';
    updateSendButton();
    statusBar.textContent = 'Thinking...';

    try {
      // For full chat context, keep all previous messages
      // Here we simulate a session by only sending the last user message and one system prompt for sophisticaton.

      const systemPrompt = {
        role: 'system',
        content: "You are Chatbot.AI, a super sophisticated, helpful AI assistant that answers all questions clearly and kindly."
      };

      // Collect chat history for the session (optional: limit to last few messages)
      // Extract previous messages from chat log
      let messages = [systemPrompt];
      const chatMessages = chatWindow.querySelectorAll('.message');
      // We want to recreate the conversation in the form OpenAI API expects
      // Alternate user and bot messages
      let userTurn = true;
      for (let i = 0; i < chatMessages.length; i++) {
        const msg = chatMessages[i].textContent;
        if (userTurn) {
          messages.push({role: 'user', content: msg});
        } else {
          messages.push({role: 'assistant', content: msg});
        }
        userTurn = !userTurn;
      }
      // But last user message is included above also, so append current message only once
      // So remove last duplicate - but for simplicity let's just include all history except the very last user message
      // Then add last user message now
      // But implemented above includes all history including the current. It might be fine.

      // To avoid duplication, we'd ideally store messages in an array variable and push on each message
      // For this demo, just send last two messages to conserve tokens
      messages = [systemPrompt,
        {role: 'user', content: userInput}
      ];

      const botResponse = await callOpenAI(messages);
      appendMessage(botResponse, 'bot');
      statusBar.textContent = '';
    } catch (err) {
      statusBar.textContent = 'Error: ' + err.message;
      appendMessage('Sorry, there was an error: ' + err.message, 'bot');
    }
  });
</script>

</body>
</html>

