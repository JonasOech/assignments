import pygame
import sys
import math
import random
from .types import HashiwokakeroBoard
from typing import Callable




class HashiwokakeroGameEngine:
    board: HashiwokakeroBoard
    def __init__(self, solve: Callable[[HashiwokakeroBoard], bool], width=700, height=700):
        pygame.init()
        self.solve = solve
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Hashiwokakero (Bridges)")

        # Colors
        self.bg_color = (255, 248, 220)  # Not used with texture
        self.island_color = (100, 0, 0)  # Dark red islands
        self.grid_color = (139, 69, 19)  # Chocolate brown grid lines
        self.bridge_color = (30, 180, 150)  # Dark cyan bridges
        self.fraction_color = (0, 60, 0)  # Dark green fraction text

        self.cell_size = 50
        self.grid_size = 5
        self.margin = 50

        # Create paper texture
        self.bg_texture = self.create_paper_texture()

        # Load puzzle
        self.load_puzzle("puzzle1")

    def create_paper_texture(self):
        """Create a paper-like texture background"""
        texture = pygame.Surface((self.width, self.height))
        base_color = (253, 245, 230)  # Light cream color for paper
        texture.fill(base_color)

        # Add noise to create paper texture
        for y in range(0, self.height, 4):
            for x in range(0, self.width, 4):
                # Random slight color variation - keep within valid RGB range (0-255)
                noise = random.randint(-10, 10)
                r = max(0, min(255, base_color[0] + noise))
                g = max(0, min(255, base_color[1] + noise))
                b = max(0, min(255, base_color[2] + noise))

                # Draw a small dot
                pygame.draw.rect(texture, (r, g, b), (x, y, 2, 2))

        return texture

    def load_puzzle(self, puzzle_name="puzzle1", puzzle_data=None):
        """Load a predefined puzzle or from file"""

        # Set grid size based on puzzle
        if puzzle_name == "puzzle1":
            self.grid_size = 6
        elif puzzle_name == "puzzle2":
            self.grid_size = 10
        elif puzzle_name == "puzzle3":
            self.grid_size = 11
        else:
            self.grid_size = 6

        # Example puzzles of varying difficulty
        puzzles = {
            "puzzle1": [  # 6x6 puzzle
                (0, 0, 3), (0, 5, 4),
                (1, 1, 4), (1, 2, 4),
                (3, 2, 4), (3, 5, 4),
                (4, 1, 4), (4, 4, 4),
                (5, 0, 2), (5, 4, 3)
            ],
            "puzzle2": [  # 10x10 puzzle
                (0, 1, 1), (0, 2, 1), (0, 8, 1), (0, 9, 1),
                (1, 4, 2), (1, 5, 2),
                (2, 1, 2), (2, 2, 2), (2, 4, 4), (2, 5, 4),  (2, 8, 2), (2, 9, 2),
                (9, 1, 2), (9, 4, 4), (9, 5, 4), (9, 9, 2),
            ],
            "puzzle3": [  # 11x11 puzzle
                (0, 2, 1), (0, 4, 2), (0, 6, 2), (0, 8, 2), (0, 10, 1),
                (1, 0, 2), (1, 3, 4), (1, 5, 2), (1, 7, 1),
                (2, 4, 2), (2, 6, 4), (2, 8, 6), (2, 10, 3),
                (3, 1, 1), (3, 3, 3), (3, 5, 1),
                (4, 0, 2), (4, 4, 2), (4, 6, 4), (4, 8, 8), (4, 10, 5),
                (5, 2, 3), (5, 5, 4),
                (6, 0, 1), (6, 6, 3), (6, 8, 6), (6, 10, 4),
                (7, 3, 1), (7, 5, 4), (7, 7, 1),
                (8, 0, 2), (8, 2, 5), (8, 4, 1), (8, 6, 1), (8, 8, 2),
                (9, 3, 1), (9, 5, 3), (9, 7, 3), (9, 10, 2),
                (10, 0, 1), (10, 2, 3), (10, 4, 2), (10, 6, 2), (10, 9, 1),
            ],
        }

        island_data = puzzle_data if puzzle_data else puzzles.get(puzzle_name, puzzles["puzzle1"])
        self.board = HashiwokakeroBoard.from_tuple_definition(island_data, grid_size=self.grid_size)

    def set_board(self, board: HashiwokakeroBoard):
        """Set the game board to a specific HashiwokakeroBoard instance"""
        self.board = board
        self.grid_size = board.size

    def draw(self):
        self.screen.blit(self.bg_texture, (0, 0))
        self.draw_grid()
        self.draw_islands()
        self.draw_bridges()
        pygame.display.flip()

    def draw_grid(self):
        for i in range(self.grid_size + 1):
            # Horizontal lines
            pygame.draw.line(
                self.screen, self.grid_color,
                (self.margin, self.margin + i * self.cell_size),
                (self.margin + self.grid_size * self.cell_size, self.margin + i * self.cell_size)
            )
            # Vertical lines
            pygame.draw.line(
                self.screen, self.grid_color,
                (self.margin + i * self.cell_size, self.margin),
                (self.margin + i * self.cell_size, self.margin + self.grid_size * self.cell_size)
            )

    def draw_islands(self):
        for island in self.board.islands:
            x = self.margin + island.col * self.cell_size
            y = self.margin + island.row * self.cell_size

            # Draw island circle
            pygame.draw.circle(self.screen, self.island_color, (x, y), 15)

            # Draw island value
            font = pygame.font.SysFont('Arial', 18)
            text = font.render(str(island.value), True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)

            # Optional: Show current bridge count
            current = font.render(f"{self.board.island_bridge_count(island)}/{island.value}", True, self.fraction_color)
            current_rect = current.get_rect(center=(x, y + 25))
            self.screen.blit(current, current_rect)

    def draw_bridges(self):
        for bridge in self.board.bridges:
            x1 = self.margin + bridge.island1.col * self.cell_size
            y1 = self.margin + bridge.island1.row * self.cell_size
            x2 = self.margin + bridge.island2.col * self.cell_size
            y2 = self.margin + bridge.island2.row * self.cell_size

            # Draw horizontal bridge
            if bridge.island1.row == bridge.island2.row:
                if bridge.count == 1:
                    # Draw rope-like curve
                    self.draw_rope(x1, y1, x2, y2, horizontal=True)
                else:  # Double bridge
                    # Draw two parallel ropes
                    self.draw_rope(x1, y1 - 4, x2, y2 - 4, horizontal=True)
                    self.draw_rope(x1, y1 + 4, x2, y2 + 4, horizontal=True)

            # Draw vertical bridge
            else:
                if bridge.count == 1:
                    # Draw rope-like curve
                    self.draw_rope(x1, y1, x2, y2, horizontal=False)
                else:  # Double bridge
                    # Draw two parallel ropes
                    self.draw_rope(x1 - 4, y1, x2 - 4, y2, horizontal=False)
                    self.draw_rope(x1 + 4, y1, x2 + 4, y2, horizontal=False)

    def draw_rope(self, x1, y1, x2, y2, horizontal=True):
        """Draw a rope-like line between two points"""
        # Dark cyan rope color
        rope_color = (30, 180, 150)

        # Rest of the method stays the same
        amplitude = 3
        frequency = 15
        segments = max(int(abs(x2 - x1 if horizontal else y2 - y1) / 5), 2)

        points = []
        for i in range(segments + 1):
            t = i / segments
            if horizontal:
                x = x1 + (x2 - x1) * t
                y = y1 + amplitude * math.sin(t * frequency)
                points.append((int(x), int(y)))
            else:
                x = x1 + amplitude * math.sin(t * frequency)
                y = y1 + (y2 - y1) * t
                points.append((int(x), int(y)))

        for i in range(len(points) - 1):
            pygame.draw.line(self.screen, rope_color, points[i], points[i + 1], 2)

        for i in range(1, len(points) - 1, 2):
            if horizontal:
                pygame.draw.line(self.screen, rope_color,
                                 (points[i][0], points[i][1] - 1),
                                 (points[i][0], points[i][1] + 1), 1)
            else:
                pygame.draw.line(self.screen, rope_color,
                                 (points[i][0] - 1, points[i][1]),
                                 (points[i][0] + 1, points[i][1]), 1)



    def add_bridge(self, island1, island2, count=1):
        """Add a bridge between two islands"""
        self.board.add_bridge(island1, island2, count)

    def remove_bridge(self, bridge):
        """Remove a bridge and update island bridge counts"""
        self.board.bridges.remove(bridge)

    def run(self):
        """Main game loop"""
        running = True

        # Initialize solver

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:  # Press 'S' to solve
                        try:
                            if self.solve(self.board):
                                print("Puzzle solved!")
                            else:
                                print("No solution found.")
                        except Exception as e:
                            print(f"Error solving puzzle: {e}")
                    elif event.key == pygame.K_r:  # Press 'R' to reset
                        self.board.bridges = []
                    elif event.key == pygame.K_1:  # Load puzzle 1
                        self.load_puzzle("puzzle1")
                    elif event.key == pygame.K_2:  # Load puzzle 2
                        self.load_puzzle("puzzle2")
                    elif event.key == pygame.K_3:  # Load puzzle 2
                        self.load_puzzle("puzzle3")


            self.draw()
            pygame.time.delay(30)

        pygame.quit()

