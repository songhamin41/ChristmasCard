const canvas = document.getElementById('snow');
const ctx = canvas.getContext('2d');

let particles = [];

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

function createParticle() {
    return {
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 4 + 1,
        speedY: Math.random() * 1 + 0.5,
    };
}

function updateParticles() {
    particles.forEach(p => {
        p.y += p.speedY;
        if (p.y > canvas.height) {
            p.y = 0;
            p.x = Math.random() * canvas.width;
        }
    });
}

function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'white';
    ctx.beginPath();
    particles.forEach(p => {
        ctx.moveTo(p.x, p.y);
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    });
    ctx.fill();
}

function animate() {
    updateParticles();
    drawParticles();
    requestAnimationFrame(animate);
}

function init() {
    resizeCanvas();
    particles = Array.from({ length: 200 }, createParticle);
    animate();
}

window.addEventListener('resize', resizeCanvas);
window.addEventListener('load', init);
