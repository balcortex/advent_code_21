from typing import List
import numpy as np

RAW = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


class Board:
    def __init__(self, board: np.ndarray) -> None:
        self.board = board
        self.remaining = np.copy(board)
        self.count = np.zeros_like(self.board)
        self.last = -1

        self.nr, self.nc = self.board.shape

    def mark(self, number: int) -> None:
        self.last = number
        if number in self.board:
            i, j = np.where(self.board == number)
            self.remaining[i, j] = 0
            self.count[i, j] = 1

    @property
    def score(self) -> int:
        return np.sum(self.remaining) * self.last

    @property
    def is_winner(self) -> bool:
        for r in self.count:
            if all(r):
                return True

        for c in self.count.T:
            if all(c):
                return True

        return False

    @classmethod
    def parse(cls, text: str) -> "Board":
        arr = [list(map(int, line.split())) for line in text.split("\n")]
        return cls(np.array(arr))


class BingoGame:
    def __init__(self, numbers: np.array, boards: List[Board]) -> None:
        self.numbers = numbers
        self.boards = boards

    def play(self) -> int:
        for number in self.numbers:
            for board in self.boards:
                board.mark(number)

                if board.is_winner:
                    return board.score

        return -1

    @classmethod
    def parse(cls, text: str) -> "BingoGame":
        lines = text.split("\n\n")
        numbers = np.array(list(map(int, lines[0].split(","))))
        boards = [Board.parse(l) for l in lines[1:]]

        return cls(numbers, boards)


BGAME = BingoGame.parse(RAW)
assert BGAME.play() == 4512

with open("inputs/day_04.txt", encoding="UTF-8") as f:
    bgame = BingoGame.parse(f.read())
    print(bgame.play())


class BingoGame2:
    def __init__(self, numbers: np.array, boards: List[Board]) -> None:
        self.numbers = numbers
        self.boards = boards
        self.winner_scores = []

    def play(self) -> int:
        for number in self.numbers:
            for board in self.boards:
                if board.is_winner:
                    continue

                board.mark(number)

                if board.is_winner:
                    self.winner_scores.append(board.score)
                    continue

            if len(self.winner_scores) == len(self.boards):
                return self.winner_scores[-1]

        return -1

    @classmethod
    def parse(cls, text: str) -> "BingoGame":
        lines = text.split("\n\n")
        numbers = np.array(list(map(int, lines[0].split(","))))
        boards = [Board.parse(l) for l in lines[1:]]

        return cls(numbers, boards)


BGAME2 = BingoGame2.parse(RAW)
assert BGAME2.play() == 1924

with open("inputs/day_04.txt", encoding="UTF-8") as f:
    bgame2 = BingoGame2.parse(f.read())
    print(bgame2.play())
