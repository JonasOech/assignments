from dataclasses import dataclass
from typing import Optional, List
@dataclass(frozen=True)
class Island:
    row: int
    col: int
    value: int 
    """Required number of bridges"""


@dataclass(frozen=True)
class Bridge:
    island1: Island
    island2: Island
    count: int  
    """1 or 2 bridges"""



class HashiwokakeroBoard:
    size: int
    islands: List[Island]
    bridges: List[Bridge]
    __island_map: dict[tuple[int, int], Island]
    
    def __init__(self, islands: List[Island], bridges: Optional[List[Bridge]] = None, size: int = 6):
        self.size = size
        self.islands = islands
        self.bridges = bridges if bridges is not None else []
        self.__island_map = {(island.row, island.col):island for island in islands}
    
    @staticmethod
    def from_tuple_definition(island_data: List[tuple[int,int,int]], grid_size: int = 6):
        islands = [Island(*values) for values in island_data]
        return HashiwokakeroBoard(size=grid_size, islands=islands, bridges=[])

    def get_island(self, row: int, col: int):
        return self.__island_map.get((row, col), None)

    def island_bridge_count(self, island: Island):
        """Returns the number of bridges connected to the island."""
        return sum(bridge.count for bridge in self.bridges if island in (bridge.island1, bridge.island2))

    def add_bridge(self, island1: Island, island2: Island, count:int):
        
        if count not in (1, 2):
            raise ValueError("Bridge count must be either 1 or 2.")
        if island1 == island2:
            raise ValueError("Cannot connect an island to itself.")
        
        # Check if the islands are already connected by a bridge
        existing_bridge = next((b for b in self.bridges if (b.island1 == island1 and b.island2 == island2) or (b.island1 == island2 and b.island2 == island1)), None)
        if existing_bridge:
            raise ValueError(f"Bridge between {island1} and {island2} already exists.")
        
        bridge = Bridge(island1, island2, count)
        self.bridges.append(bridge)


    def find_potential_connections(self):
        """Find all potential connections between islands"""
        connections = []

        # For each island, find valid connections in four directions
        for island in self.islands:
            # Look in all 4 directions (up, right, down, left)
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                # Find the next island (if any) in this direction
                next_island = self.find_next_island(island, dx, dy)
                if next_island:
                    # Make sure we don't add the same connection twice
                    if (island, next_island) not in connections and (next_island, island) not in connections:
                        connections.append((island, next_island))

        return connections

    def find_next_island(self, start_island: Island, dx: int, dy: int):
        """Find the next island (if any) in the specified direction"""
        row, col = start_island.row, start_island.col

        # Move one step in the direction
        row += dy
        col += dx

        # Continue until out of bounds
        while 0 <= row < self.size and 0 <= col < self.size:
            # Check if there's an island at this position
            island = self.get_island(row, col)
            if island:
                return island

            # Continue in same direction
            row += dy
            col += dx

        return None
