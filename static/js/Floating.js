function createFloatingHearts() {
    const container = document.getElementById('floating-container');
    const symbols = ['❤️', '💕', '💝', '🌸', '✨'];
    
    function createHeart() {
        const heart = document.createElement('div');
        const symbol = symbols[Math.floor(Math.random() * symbols.length)];
        const startPosition = Math.random() * 100;
        
        heart.innerHTML = symbol;
        heart.style.cssText = `
            position: fixed;
            left: ${startPosition}vw;
            top: -50px;
            font-size: ${Math.random() * 10 + 15}px;
            animation: float ${Math.random() * 5 + 10}s linear;
            opacity: 0.7;
            z-index: 1000;
            pointer-events: none;
        `;
        
        container.appendChild(heart);
        
        // Remove heart after animation
        setTimeout(() => {
            heart.remove();
        }, 15000);
    }

    // Create new heart every 2 seconds
    setInterval(createHeart, 2000);
    
    // Create initial batch of hearts
    for(let i = 0; i < 5; i++) {
        setTimeout(createHeart, i * 500);
    }
}

// Add floating animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0.7;
        }
        100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Start animation when page loads
document.addEventListener('DOMContentLoaded', createFloatingHearts);
