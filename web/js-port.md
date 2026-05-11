# JavaScript Port Plan

Purpose
- Port the core Pygame simulations in this repo to a browser-based JavaScript implementation using HTML5 Canvas.

Scope
- Primary sources: `main.py` (Moving Squares) and `boids_exam.py` (Boids).
- Target output: runnable, bundler-free ES6 JavaScript files under `web/` with a simple `index.html` to load them.

Target environment
- Browser (desktop), modern browsers (Chrome/Firefox/Edge). Use ES6 modules where helpful but keep files runnable without a bundler.

High-level mapping (Python -> JavaScript)
- `pygame.Surface` & drawing -> `canvas` 2D context (`CanvasRenderingContext2D`).
- `clock.tick(fps)` -> `requestAnimationFrame` loop with manual dt calculation or `setInterval` fallback.
- Event loop (`pygame.event`) -> DOM `keydown` / `keyup` and `beforeunload` for quitting.
- `pygame.Rect` collision -> manual AABB math or helper functions.
- Per-frame `dt` (seconds) retained for physics; multiply velocities by `dt`.

Planned output files (examples)
- `web/index.html` — loader and canvas element
- `web/styles.css` — minimal styles
- `web/moving-squares.js` — port of `main.py` behavior
- `web/boids.js` — port of `boids_exam.py` behavior
- `web/js-port.md` — this plan
- `web/js-port-validation.md` — validation checklist and smoke tests

Run instructions (development)
- Serve the `web/` folder and open `index.html` in a browser. Example quick server:

```bash
python -m http.server 8000
# then open http://localhost:8000/web/index.html
```

Next steps
1. Scaffold `index.html`, `styles.css`, and initial `moving-squares.js` (canvas, main loop, dt).
2. Port `Square` class and draw/update logic, then iterate behavior features (flee, chasing, eat, trails).
3. Port `Boid` class from `boids_exam.py` into `boids.js` (optional parallel port).
4. Validate with the checklist in `web/js-port-validation.md` and iterate.
