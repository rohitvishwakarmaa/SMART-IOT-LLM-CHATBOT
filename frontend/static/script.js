async function sendMessage() {
  const input = document.getElementById("userInput");
  const messages = document.getElementById("messages");
  const message = input.value.trim();
  if (!message) return; // ignore empty

  // Append user's message
  messages.innerHTML += `<p class="user-message"><b>You:</b> ${escapeHtml(message)}</p>`;

  // Scroll down to latest message
  messages.scrollTop = messages.scrollHeight;

  // Send to backend
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();

    let replyText;

    if (typeof data.reply === "object") {
      // If reply is an object, pretty-print it
      replyText = JSON.stringify(data.reply, null, 2);
    } else {
      // If reply is a string, try to parse as JSON first
      try {
        const parsed = JSON.parse(data.reply);
        replyText = JSON.stringify(parsed, null, 2);
      } catch {
        // If parsing fails, use as-is
        replyText = data.reply;
      }
    }

    // Display bot reply inside <pre> to preserve formatting
    messages.innerHTML += `<pre class="bot-message"><b>Bot:</b>\n${escapeHtml(replyText)}</pre>`;
    messages.scrollTop = messages.scrollHeight;
  } catch (error) {
    messages.innerHTML += `<p class="bot-message error"><b>Bot:</b> Error connecting to server.</p>`;
    messages.scrollTop = messages.scrollHeight;
  }

  input.value = "";
  input.focus();
}

// Simple HTML escape function to prevent injection
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Allow sending message on Enter key press
document.getElementById("userInput").addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});
