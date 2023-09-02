from random import randint


class Algo:
    def __init__(self, size=(10, 10), mine_number=2):
        self.grid = [[0 for _ in range(size[0])] for _ in range(size[1])]
        self.size = size
        self.mine_position = []
        self.mine_number = mine_number
        self.plant_mine()
        self.get_mine_around()

    def get_mine_around(self):
        len_i = self.size[1] - 1
        len_j = self.size[0] - 1
        for i in range(len_i+1):
            for j in range(len_j+1):
                # Skip, if it contains a mine
                if self.grid[i][j] == -1:
                    continue

                # Check up
                if i > 0 and self.grid[i - 1][j] == -1:
                    self.grid[i][j] = self.grid[i][j] + 1
                # Check down
                if i < len_i and self.grid[i + 1][j] == -1:
                    self.grid[i][j] = self.grid[i][j] + 1
                # Check left
                if j > 0 and self.grid[i][j - 1] == -1:
                    self.grid[i][j] = self.grid[i][j] + 1
                # Check right
                if j < len_i and self.grid[i][j + 1] == -1:
                    self.grid[i][j] = self.grid[i][j] + 1
                # Check top-left
                if i > 0 and j > 0 and self.grid[i - 1][j - 1] == -1:
                    self.grid[i][j] = self.grid[i][j] + 1
                # Check top-right
                if i > 0 and j < len_i and self.grid[i - 1][j + 1] == -1:
                    self.grid[i][j] = self.grid[i][j] + 1
                # Check below-left
                if i < len_i and j > 0 and self.grid[i + 1][j - 1] == -1:
                    self.grid[i][j] = self.grid[i][j] + 1
                # Check below-right
                if i < len_i and j < len_i and self.grid[i + 1][j + 1] == -1:
                    self.grid[i][j] = self.grid[i][j] + 1

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
