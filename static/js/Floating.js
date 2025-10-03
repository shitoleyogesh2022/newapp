const emojis = ["💖", "🌸", "💎", "🐢", "🌹", "❤️"];
const container = document.getElementById("floating-container");

function createEmoji() {
  const emoji = document.createElement("div");
  emoji.classList.add("emoji");
  emoji.innerText = emojis[Math.floor(Math.random() * emojis.length)];
  emoji.style.left = Math.random() * 100 + "vw";
  emoji.style.animationDuration = 3 + Math.random() * 5 + "s";
  container.appendChild(emoji);

  setTimeout(() => {
    emoji.remove();
  }, 8000);
}

setInterval(createEmoji, 800);