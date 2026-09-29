# 🧬 Doodle Evolution

> *"What if Doodle Jump, but the doodler taught itself to play... and got annoyingly good at it?"*

A full Doodle Jump clone built in Pygame — complete with exploding platforms, bat monsters, and trampolines — plus a **neuroevolution AI** that trains a population of 150 doodlers using a genetic algorithm and a hand-rolled neural network. No PyTorch. No TensorFlow. Just NumPy, spite, and natural selection.

---

## 🎮 Play It Yourself

```bash
pip install -r requirements.txt
python main.py
```

Or watch the AI suffer through it:

```bash
python train.py
```

Press `SPACE` during training to toggle **turbo mode** (skips rendering most frames — the AI doesn't need to *see* to suffer faster).

---

## 🧠 How the AI Works

### The Brain — `network.py`

Each doodler has a tiny feedforward neural network as its brain:

```
8 inputs → 12 hidden (ReLU) → 3 outputs (left / stay / right)
```

**Inputs (all normalized to ~[-1, 1]):**

| # | Input | Why |
|---|-------|-----|
| 1 | Player X position | Where am I? |
| 2 | Y velocity | Am I going up or down? |
| 3-4 | dx, dy to nearest platform above | Where should I land? |
| 5-6 | dx, dy to 2nd nearest platform | Backup plan |
| 7-8 | dx, dy to nearest monster | Should I panic? |

The network outputs raw logits. `argmax` picks the action. No softmax needed — we're not training with gradients, we're doing **evolution**.

---

### The Evolution — `genetic.py`

Every generation, 150 doodlers are dropped into the **same procedurally generated level** (same RNG seed = fair competition). When they all die:

1. **Elitism** — Top 10 genomes survive unchanged. The best doodler's DNA is sacred.
2. **Tournament Selection** — Pick 10 random agents, keep the best. Repeat to find parents.
3. **Uniform Crossover** — Each weight gene is randomly inherited from parent 1 or parent 2.
4. **Mutation** — 15% of weights get nudged by Gaussian noise (`σ=0.5`), clipped to `[-5, 5]`.
5. **Random Immigrants** — ~10% of the new population is completely random. Keeps diversity alive.

```
Fitness = max height reached (in pixels scrolled)
```

Stagnation detection kills any doodler that hasn't made progress in 300 frames. No freeloaders.

---

### The World — `world.py`

Each of the 150 agents gets its own `World` instance — a fully self-contained simulation with its own platforms, monsters, feeders, and trampolines. They all run in the same Python loop, no threads needed.

The `get_state()` method handles **screen-wrap-aware distance calculation** so the brain doesn't get confused when a platform is on the other side of the screen edge.

---

## 🕹️ Game Features

### Platform Types

| Platform | Behavior |
|----------|----------|
| 🟩 Normal | Reliable. Boring. Essential. |
| 💥 Explosive | Turns red after ~1.3s, explodes at 2s. Lingers to taunt you. |
| 🔀 Horizontal | Slides wall-to-wall. Speed scales with score. |
| ↕️ Vertical | Bobs up and down. Also gets faster. |
| 🪨 Breakable | Crumbles on first touch. 4-frame death animation. |

### Entities

- **🦇 Bat Monster** — Hovers sinusoidally above its platform. Stomp it from above to bounce off. Touch it from the side and you're done.
- **🌀 Feeder** — 1.8× jump boost. Unlocks after score > 3000.
- **🤸 Trampoline** — 2.5× jump boost + a satisfying spin animation. Unlocks after score > 1000.

### Game States

```
MENU → PLAYING → PAUSED
                ↓
           DEATH_FALL  (camera keeps rising, world falls away dramatically)
                ↓
           GAME_OVER
```

The death fall is a cinematic touch — the world scrolls up as the doodler plummets, until every platform disappears off screen.

---

## 💾 Save System

Training progress is auto-saved after every generation:

```
saves_doodle/
├── doodle_gen_36.pkl   ← latest population weights
└── doodle_best.pkl     ← best individual ever seen
```

On restart, `train.py` automatically loads the latest checkpoint. The old generation file is deleted after saving the new one (no disk bloat).

The human game saves a high score to `highest_score.json`.

---

## 📁 Project Structure

```
Doodle-Evolution/
├── main.py          # Human-playable game loop
├── train.py         # Neuroevolution training loop
├── world.py         # Self-contained simulation (one per AI agent)
├── network.py       # Hand-rolled neural network (no ML frameworks)
├── genetic.py       # Genetic algorithm (selection, crossover, mutation)
├── Doodle.py        # Player class (movement, gravity, jump, spin)
├── Platform.py      # Normal, Exploding, and Moving platform classes
├── Monster.py       # Bat enemy with sinusoidal hover
├── Feeder.py        # Spring boost item
├── Trampoline.py    # Super-spring boost item
├── assets.py        # Asset loader
├── config.py        # All magic numbers in one place
└── Game_Assests/    # Sprites, sounds, fonts
```

---

## ⚙️ Config at a Glance — `config.py`

```python
WIDTH, HEIGHT       = 320, 600     # Classic Doodle Jump aspect ratio
GRAVITY             = 0.6
JUMP_STRENGTH       = -20
MOVE_SPEED          = 5
FEEDER_THRESHOLD    = 3000         # Score needed before feeders spawn
STAGNATION_LIMIT    = 300          # Frames of no progress before AI is killed
MAX_FRAMES          = 40000        # Hard cap per agent per generation
```

---

## 🔬 Technical Highlights

- **Zero ML framework dependency** — the neural network is pure NumPy matrix math
- **Genome = flat weight vector** — `get_weights()` / `set_weights()` serialize the entire network into a 1D array for clean GA operations
- **Seeded RNG per generation** — all 150 agents play the exact same level, making fitness comparison fair
- **Wrap-aware state inputs** — platform distances account for the screen wrapping at edges
- **Adaptive platform speed** — moving platforms get faster every 3000 points, so the AI can't just learn one speed

---

## 📦 Requirements

```
pygame
numpy
```

Python 3.8+ recommended.

---

## 🏷️ Suggested Repo Names

| Name | Vibe |
|------|------|
| `doodle-evolution` | Clean, descriptive, professional |
| `neuro-doodle` | Short, punchy |
| `doodle-jump-ai` | SEO-friendly, findable |
| `jumping-genes` | Clever, biology pun |
| `doodle-darwin` | Natural selection energy |
| `evolving-doodler` | Exactly what it says |


