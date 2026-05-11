# JavaScript Port Validation Checklist

Purpose
- A compact checklist and smoke-test plan to validate the browser port after initial implementation.

Smoke tests
- [ ] The page loads without console errors and displays a canvas element.
- [ ] Canvas dimensions match the expected `WIDTH` × `HEIGHT` values from the source.
- [ ] Entities (squares / boids) appear and move visually.
- [ ] Keyboard controls map correctly (ESC/Q to quit or stop simulation; S/A/C/W toggles mapped where applicable).
- [ ] No uncaught exceptions in the console during animation.

Behavioral checks
- [ ] `dt` scaling reproduces approximate speeds across machines (objects travel similar distances per real second).
- [ ] Wrapping vs bouncing walls behave as in Python version.
- [ ] Flee, chasing, and eating behaviors operate without major visible glitches.
- [ ] Trails render and age out over time for `Moving Squares`.

Performance & compatibility
- [ ] Stable ~60 FPS on a development machine for small test counts (adjust entity counts for larger tests).
- [ ] Test in Chrome and Firefox; verify rendering and input work similarly.

Validation steps
1. Serve the `web/` directory with `python -m http.server 8000` and open `http://localhost:8000/web/index.html`.
2. Observe console for errors; fix JS runtime issues first.
3. Toggle behavior flags and verify on-screen feedback.
4. If differences appear, check dt calculations, unit conversions, and random seed differences.

Known differences to watch for
- Floating point timing differences and `requestAnimationFrame` vs fixed-step loops can change movement slightly.
- Pygame-specific drawing details (antialiasing, line thickness) may render differently in canvas.
