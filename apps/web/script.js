const apiBase = "http://localhost:8000/v1";

document.getElementById("submitBtn").addEventListener("click", async () => {
  const userId = document.getElementById("userId").value;
  const message = document.getElementById("message").value;
  const result = document.getElementById("result");

  result.textContent = "Running intake...";

  try {
    const res = await fetch(`${apiBase}/chat/intake`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, message }),
    });

    const data = await res.json();
    result.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    result.textContent = `Failed: ${error.message}`;
  }
});
