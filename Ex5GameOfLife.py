# package exercises
#  * Program for Conway's game of life.
#  * See https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
#  *
#  * This is a graphical program using pygame to draw on the screen.
#  * There's a bit of "drawing" code to make this happen (far below).
#  * You don't need to implement (or understand) any of it.
#  * NOTE: To run tests must uncomment in init() method, see comment
#  *
#  * Use functional decomposition!
#  *
#  * See:
#  * - UseEnum
#  * - PygameSample (don't need to understand, just if you're curious)
from enum import Enum
from typing import List
import pygame


# Main program
def game_of_life():
    pygame.init()
    world = World()
    GameOfLifeView(world)
    world.run()


class Cell(Enum):
    DEAD = 0
    ALIVE = 1


class World:

    all_cells: List[List[Cell]] = []
    observers = []

    def __init__(self):
        # test()        # <--------------- Uncomment to test!
        n_locations = 10000
        distribution = 0.8   # % of locations holding a Cell
        self.create_world(n_locations, distribution)
        self.clock = pygame.time.Clock()
        self.cells = []

    def create_world(self, n_locations, distribution):
        import random
        import math
        # TODO Create and populate world

        self.cell_quantity(distribution, n_locations)

        random.shuffle(self.cells)
        self.cell_matrix(n_locations)

    def cell_matrix(self, n_locations):
        import math
        self.all_cells = [self.cells[x:x + int(math.sqrt(n_locations))] for x in range(0, len(self.cells), int(math.sqrt(n_locations)))]

    def cell_quantity(self, distribution, n_locations):
        live_cell_quantity = int(n_locations * distribution)
        dead_cell_quantity = int(n_locations - live_cell_quantity)
        self.cells = [Cell.ALIVE] * live_cell_quantity + [Cell.DEAD] * dead_cell_quantity

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.notify()

    def update(self):
        # TODO Update (logically) the world
        for i in range(len(self.all_cells)):
            for j in range(len(self.all_cells)):
                cell_neighbours = self.cell_neighbours(i, j)
                live_cell_neighbours = cell_neighbours.count(Cell.ALIVE)
                if self.all_cells[i][j] == Cell.ALIVE and live_cell_neighbours == 2 or live_cell_neighbours == 3:
                    pass
                elif self.all_cells[i][j] == Cell.ALIVE and live_cell_neighbours < 2 or live_cell_neighbours > 3:
                    self.all_cells[i][j] = Cell.DEAD

                elif self.all_cells[i][j] == Cell.DEAD and live_cell_neighbours == 3:
                    self.all_cells[i][j] = Cell.ALIVE

        pass
        self.notify_observers()  # Tell the view to render

    def cell_neighbours(self, i, j):
        temp_neighbour = []
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if self.is_valid_location(len(self.all_cells), x, y) and (x != i and y != j):
                    temp_neighbour.append(self.all_cells[x][y])

        return temp_neighbour

    @staticmethod
    def is_valid_location(size: int, row: int, col: int):
        if 0 <= row < size and 0 <= col < size:
            return True
        else:
            return False

    def run(self):
        # Variable to keep the main loop running
        running = True
        # Main loop
        while running:
            self.update()
            # Ensure program maintains a rate of 2 frames per second
            self.clock.tick(4)
            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == pygame.QUIT:
                    running = False


# -------- Write methods below this --------------


# ---------- Testing -----------------
# Here you run your tests i.e. call your logic methods
# to see that they really work
def test():
    # Hard coded test world
    test_world: List[List[Cell]] = [
        [Cell.ALIVE, Cell.ALIVE, Cell.DEAD],
        [Cell.ALIVE, Cell.DEAD, Cell.DEAD],
        [Cell.DEAD, Cell.DEAD, Cell.ALIVE]]

    size = len(test_world)
    # TODO tests!


# -------- Below is Pygame View stuff, nothing to do --------------
class GameOfLifeView:

    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 400

    def __init__(self, world_ref: World):
        self.the_world = world_ref
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.the_world.add_observer(self)

    def notify(self):
        self.render()

    def render(self):
        self.screen.fill((255, 255, 255))
        size = len(self.the_world.all_cells)
        for row in range(size):
            for col in range(size):
                x = 3 * col + 50
                y = 3 * row + 50
                self.render_cell(x, y, self.the_world.all_cells[row][col])

        pygame.display.flip()

    def render_cell(self, x, y, cell: Cell):
        if cell == Cell.ALIVE:
            color = (255, 0, 0)
        else:
            color = (255, 255, 255)
        surf = pygame.Surface((3, 3))
        surf.fill(color)
        self.screen.blit(surf, (x, y))


if __name__ == "__main__":
    game_of_life()
