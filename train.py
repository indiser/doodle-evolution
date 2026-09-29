import os
import pickle
import random
import pygame

import assets
from config import WIDTH, HEIGHT
from network import NeuralNetwork
from genetic import GeneticAlgorithm
from world import World

POPULATION_SIZE = 150
SAVE_DIR = "saves_doodle"
FAST_RENDER_EVERY = 30   # in turbo mode, draw once per N frames

pygame.init()
pygame.display.set_icon(assets.app_icon)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump - Neuroevolution (SPACE = turbo)")
clock = pygame.time.Clock()
font = pygame.font.Font(assets.get_path('Game_Assests/fonts/al-seana.ttf'), 20)

# 150 worlds would blow up your ears
assets.exploding_platform_sound.set_volume(0)

turbo = False


def load_latest():
    if not os.path.isdir(SAVE_DIR):
        return 1, None
    files = [f for f in os.listdir(SAVE_DIR)
             if f.startswith("doodle_gen_") and f.endswith(".pkl")]
    if not files:
        return 1, None
    latest = max(files, key=lambda f: int(f[len("doodle_gen_"):-len(".pkl")]))
    with open(os.path.join(SAVE_DIR, latest), "rb") as f:
        data = pickle.load(f)
    print(f"Loaded {latest}")
    return data["generation"], data["population_weights"]


def save(generation, weights_list, best_weights):
    os.makedirs(SAVE_DIR, exist_ok=True)
    name = f"doodle_gen_{generation}.pkl"
    with open(os.path.join(SAVE_DIR, name), "wb") as f:
        pickle.dump({"generation": generation, "population_weights": weights_list}, f)
    with open(os.path.join(SAVE_DIR, "doodle_best.pkl"), "wb") as f:
        pickle.dump(best_weights, f)
    for f in os.listdir(SAVE_DIR):
        if f.startswith("doodle_gen_") and f.endswith(".pkl") and f != name:
            os.remove(os.path.join(SAVE_DIR, f))


def make_brains(weights_list):
    brains = [NeuralNetwork() for _ in range(POPULATION_SIZE)]
    if weights_list is None:
        return brains
    try:
        for b, w in zip(brains, weights_list):
            b.set_weights(w)
    except ValueError as e:
        print(f"Save incompatible with network ({e}). Starting fresh.")
        return [NeuralNetwork() for _ in range(POPULATION_SIZE)]
    return brains


def run_generation(generation, brains):
    """Returns list of finished worlds, or None if window closed."""
    global turbo
    seed = random.randrange(2 ** 31)  # same level for everyone this gen
    worlds = [World(b, seed) for b in brains]
    frame = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                turbo = not turbo

        for w in worlds:
            if w.alive:
                w.step(w.brain.decide(w.get_state()))

        alive = [w for w in worlds if w.alive]
        if not alive:
            return worlds

        frame += 1
        if not turbo or frame % FAST_RENDER_EVERY == 0:
            best = max(alive, key=lambda w: w.fitness)
            best.draw(screen)
            hud = font.render(
                f"Gen {generation}  Alive {len(alive)}  Height {int(best.fitness)}",
                True, (0, 0, 0))
            screen.blit(hud, (8, 6))
            pygame.display.flip()

        if not turbo:
            clock.tick(60)


def main():
    generation, weights = load_latest()
    brains = make_brains(weights)
    ga = GeneticAlgorithm(population_size=POPULATION_SIZE, mutation_rate=0.15,
                          mutation_strength=0.5, elitism=10)

    while True:
        worlds = run_generation(generation, brains)
        if worlds is None:
            break

        ga.generation = generation - 1  # keep GA log in sync after resume
        new_weights = ga.next_generation(worlds)  # sorts worlds, best first
        best_weights = worlds[0].brain.get_weights().copy()

        generation += 1
        save(generation, new_weights, best_weights)
        brains = make_brains(new_weights)

    pygame.quit()


if __name__ == "__main__":
    main()