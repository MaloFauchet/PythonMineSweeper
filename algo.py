from random import randint


class Algo:
    def __init__(self, size=(10, 10), mine_number=2):
        self.grid = [[0 for _ in range(size[0])] for _ in range(size[1])]
        self.size = size
        self.mine_position = []
        self.mine_number = mine_number
        self.plant_mine()
        self.get_mine_around()
    
    def add_one_to_case_around(self, i, j):
        # Check up
        if i > 0 and self.grid[i-1][j] != -1:
            self.grid[i-1][j] += 1
        # Check down
        if i < self.size[1]-1 and self.grid[i+1][j] != -1:
            self.grid[i+1][j] += 1
        # Check left
        if j > 0 and self.grid[i][j-1] != -1:
            self.grid[i][j-1] += 1
        # Check right
        if j < self.size[0]-1 and self.grid[i][j+1] != -1:
            self.grid[i][j+1] += 1
        # Check top-left
        if i > 0 and j > 0 and self.grid[i-1][j-1] != -1:
            self.grid[i-1][j-1] += 1
        # Check top-right
        if i > 0 and j < self.size[0]-1 and self.grid[i-1][j+1] != -1:
            self.grid[i-1][j+1] += 1
        # Check below-left
        if i < self.size[1]-1 and j > 0 and self.grid[i+1][j-1] != -1:
            self.grid[i+1][j-1] += 1
        # Check below-right
        if i < self.size[1]-1 and j < self.size[0]-1 and self.grid[i+1][j+1] != -1:
            self.grid[i+1][j+1] += 1

    def get_mine_around(self):
        for mine in self.mine_position:
            self.add_one_to_case_around(mine[0], mine[1])

    def plant_mine(self):
        mine_planted: int = 0
        len_i = len(self.grid) - 1
        len_j = len(self.grid[0]) - 1

        while mine_planted < self.mine_number:
            x, y = randint(0, len_i), randint(0, len_j)
            if (x, y) not in self.mine_position:
                self.mine_position.append((x, y))
                self.grid[x][y] = -1
                mine_planted += 1

    def print(self):
        for liste in self.grid:
            for num in liste:
                print(f"{num:>4}", end='')
            print()
