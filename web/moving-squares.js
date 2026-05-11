// moving-squares.js — ES6 port of main.py (Moving Squares)

const MIN_SIZE = 10;
const MAX_SIZE = 50;
const MAX_SPEED = 1; // base used in size->speed calc in original

const WIDTH = 1080;
const HEIGHT = 920;
const TRAILS_LENGTH = 30;

const canvas = document.getElementById('canvas');
canvas.width = WIDTH;
canvas.height = HEIGHT;
const ctx = canvas.getContext('2d');

class Square {
  constructor() {
    this.trail = [];
    this.reset();
  }

  move(dt) {
    if (Math.random() < 0.02) {
      const angle = (Math.random() * 0.4) - 0.2;
      const cosA = Math.cos(angle);
      const sinA = Math.sin(angle);
      const newDx = this.dx * cosA - this.dy * sinA;
      const newDy = this.dx * sinA + this.dy * cosA;
      this.dx = newDx;
      this.dy = newDy;
    }

    const speed = Math.hypot(this.dx, this.dy);
    if (speed > 0) {
      const factor = Math.min(this.maxSpeed, speed) / speed;
      this.dx *= factor;
      this.dy *= factor;
    }

    this.x += this.dx * dt;
    this.y += this.dy * dt;

    // wrap horizontally
    if (this.x < 0) this.x = WIDTH;
    else if (this.x > WIDTH) this.x = 0;

    // wrap vertically
    if (this.y < 0) this.y = HEIGHT;
    else if (this.y > HEIGHT) this.y = 0;

    this.trail.push([this.x + this.size / 2, this.y + this.size / 2]);
    if (this.trail.length > TRAILS_LENGTH) this.trail.shift();
  }

  checkCollision(other) {
    return !(this.x + this.size < other.x ||
             this.x > other.x + other.size ||
             this.y + this.size < other.y ||
             this.y > other.y + other.size);
  }

  eat(allSquares) {
    for (const other of allSquares) {
      if (other === this) continue;
      if (this.size > other.size && this.checkCollision(other)) {
        this.size += other.size * 0.3;
        this.size = Math.min(this.size, MAX_SIZE);
        other.reset();
      }
    }
  }

  flee(allSquares, dt) {
    for (const other of allSquares) {
      if (other === this) continue;
      if (other.size > this.size) {
        let dx = (this.x + this.size / 2) - (other.x + other.size / 2);
        let dy = (this.y + this.size / 2) - (other.y + other.size / 2);
        const dist = Math.hypot(dx, dy);
        if (dist > 0 && dist < 200) {
          dx /= dist;
          dy /= dist;
          const strength = (200 - dist) / 200;
          this.dx += dx * 500 * strength * dt;
          this.dy += dy * 500 * strength * dt;
        }
      }
    }
  }

  chasing(allSquares, dt) {
    let closest = null;
    let closestDist = Infinity;
    for (const other of allSquares) {
      if (other === this || other.size >= this.size) continue;
      const dx = (other.x + other.size / 2) - (this.x + this.size / 2);
      const dy = (other.y + other.size / 2) - (this.y + this.size / 2);
      const dist = Math.hypot(dx, dy);
      if (dist < closestDist) {
        closestDist = dist;
        closest = [dx, dy, dist];
      }
    }
    if (closest && closestDist > 0 && closestDist < 200) {
      let [dx, dy, dist] = closest;
      dx /= dist;
      dy /= dist;
      const strength = (200 - dist) / 200;
      this.dx += dx * 600 * strength * dt;
      this.dy += dy * 600 * strength * dt;
    }
  }

  updateLife(dt) {
    this.life -= dt;
    if (this.life <= 0) this.reset();
  }

  reset() {
    if (typeof this.size === 'undefined') this.size = Math.floor(Math.random() * (MAX_SIZE - MIN_SIZE + 1)) + MIN_SIZE;
    const speedFact = (MAX_SIZE - this.size) / (MAX_SIZE - MIN_SIZE + 1);
    this.maxSpeed = Math.max(100.0, MAX_SPEED * speedFact);
    this.x = Math.random() * (WIDTH - this.size);
    this.y = Math.random() * (HEIGHT - this.size);
    this.dx = (Math.random() < 0.5 ? -1 : 1) * (Math.random() * (this.maxSpeed - 50) + 50);
    this.dy = (Math.random() < 0.5 ? -1 : 1) * (Math.random() * (this.maxSpeed - 50) + 50);
    this.color = [
      Math.floor(Math.random() * 206) + 50,
      Math.floor(Math.random() * 206) + 50,
      Math.floor(Math.random() * 206) + 50,
    ];
    this.life = Math.random() * 10 + 10;
    this.trail = [];
  }

  draw(ctx) {
    ctx.fillStyle = `rgb(${this.color[0]}, ${this.color[1]}, ${this.color[2]})`;
    ctx.fillRect(this.x, this.y, this.size, this.size);

    if (this.trail.length > 1) {
      ctx.beginPath();
      for (let i = 1; i < this.trail.length; i++) {
        const [x1, y1] = this.trail[i - 1];
        const [x2, y2] = this.trail[i];
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
      }
      ctx.strokeStyle = `rgba(${this.color[0]}, ${this.color[1]}, ${this.color[2]}, 0.9)`;
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  }
}

// Create squares
const squares = [];
for (let i = 0; i < 5; i++) {
  const s = new Square();
  s.size = 25;
  squares.push(s);
}
for (let i = 0; i < 10; i++) {
  const s = new Square();
  s.size = 10;
  squares.push(s);
}
for (let i = 0; i < 30; i++) {
  const s = new Square();
  s.size = 4;
  squares.push(s);
}

let running = true;
let lastTime = performance.now();

function loop(now) {
  const dt = (now - lastTime) / 1000.0;
  lastTime = now;

  ctx.fillStyle = 'rgb(30,30,30)';
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  // behaviors
  for (const sq of squares) {
    sq.flee(squares, dt);
    sq.eat(squares);
  }
  for (const sq of squares) {
    sq.chasing(squares, dt);
  }

  for (const sq of squares) {
    sq.move(dt);
    sq.updateLife(dt);
  }

  for (const sq of squares) {
    sq.draw(ctx);
  }

  if (running) requestAnimationFrame(loop);
}

requestAnimationFrame(loop);

window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') running = false;
});
