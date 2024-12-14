from enum import Enum
import random

class Direction(Enum):
    """
    Represents the possible directions the snake can move.
    """
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

# Define the offsets for each direction
direction_offsets = {
    Direction.UP: (0, -1),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0)
}

# Determine the opposite direction
opposite_directions = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT
}

def know_direction(og_x: int, og_y: int, move_x: int, move_y: int, current_dir: Direction) -> Direction:
    """
    Calculate the new direction to move from the original position to the new position.

    Args:
        og_x (int): Original x-coordinate.
        og_y (int): Original y-coordinate.
        move_x (int): New x-coordinate.
        move_y (int): New y-coordinate.
        current_dir (Direction): Current movement direction.

    Returns:
        Direction: The new direction to move.
    """
    new_x = move_x - og_x
    new_y = move_y - og_y

    if abs(new_x) > abs(new_y):
        if new_x > 0 and current_dir != Direction.LEFT:
            return Direction.RIGHT
        elif new_x < 0 and current_dir != Direction.RIGHT:
            return Direction.LEFT
    else:
        if new_y > 0 and current_dir != Direction.UP:
            return Direction.DOWN
        elif new_y < 0 and current_dir != Direction.DOWN:
            return Direction.UP

    return current_dir

class Snake:
    """
    Class representing the snake and its behavior.

    Attributes:
        food_position (tuple[int, int]): Current position of the food.
        body_position (list[tuple[int, int]]): Positions of the snake's body segments.
        ignore_body (bool): Whether to ignore collisions with the snake's own body.
        grid_size (int): Size of a single snake segment.
        scores (int): Player's score.
        frame_time (int): Time between game updates (snake speed).
        height (int): Arena height.
        width (int): Arena width.
        direction (Direction): Current movement direction of the snake.
    """

    def __init__(self) -> None:
        """
        Initialize the Snake instance with default attributes and starting positions.
        """
        self.food_position: tuple[int, int] | None = None
        self.body_position: list[tuple[int, int]] | None = None
        self.ignore_body: bool = True
        self.grid_size: int = 10
        self.scores: int = 0
        self.frame_time: int = 75
        self.height: int = 300
        self.width: int = 300
        self.start_body_position()
        self.direction: Direction = Direction.RIGHT
        self.spawn_food()

    def start_body_position(self) -> None:
        """
        Set the starting position of the snake in the middle of the arena.
        """
        mid_x = self.width // 2
        mid_y = self.height // 2
        self.body_position = [
            (mid_x, mid_y),
            (mid_x - self.grid_size, mid_y),
            (mid_x - 2 * self.grid_size, mid_y)
        ]

    def state_game(self) -> bool:
        """
        Check for game-over conditions such as collisions with walls or the snake's body.

        Returns:
            bool: True if the game is over, otherwise False.
        """
        head_x, head_y = self.body_position[0]

        if (head_x < 0 or
            head_x >= self.width or
            head_y < 0 or
            head_y >= self.height):
            return True

        if not self.ignore_body:
            body_only = self.body_position[1:]
            if (head_x, head_y) in body_only and (head_x, head_y) != self.food_position:
                return True

        return False

    def spawn_food(self) -> None:
        """
        Spawn food at a random position that is not occupied by the snake's body.
        """
        while True:
            food_x = random.randint(0, (self.width // self.grid_size) - 1) * self.grid_size
            food_y = random.randint(0, (self.height // self.grid_size) - 1) * self.grid_size
            if (food_x, food_y) not in self.body_position:
                self.food_position = (food_x, food_y)
                break

    def grow_snake(self, position: tuple[int, int]) -> None:
        """
        Grow the snake by adding a new segment at the specified position.

        Args:
            position (tuple[int, int]): Position to add the new segment.
        """
        self.body_position.insert(0, position)

    def move(self) -> None:
        """
        Move the snake in the current direction by updating its body positions.
        """
        new_head = self.get_position(self.body_position[0], self.direction)
        self.body_position.insert(0, new_head)
        self.body_position.pop()

    def get_position(self, position: tuple[int, int], direction: Direction) -> tuple[int, int]:
        """
        Calculate the next position of the snake's head based on the current direction.

        Args:
            position (tuple[int, int]): Current position.
            direction (Direction): Direction of movement.

        Returns:
            tuple[int, int]: New position of the snake's head.
        """
        x, y = position
        offset_x, offset_y = direction_offsets[direction]
        return x + offset_x * self.grid_size, y + offset_y * self.grid_size

    def eat(self) -> None:
        """
        Check if the snake's head is at the food position. If so, grow the snake, update the score, and spawn new food.
        """
        if self.is_food_eaten():
            self.grow_snake(self.body_position[0])
            self.update_score()
            self.spawn_food()

    def is_food_eaten(self) -> bool:
        """
        Check if the snake's head is at the food position.

        Returns:
            bool: True if food is eaten, otherwise False.
        """
        return self.food_position == self.body_position[0]

    def update_score(self) -> None:
        """
        Update the player's score based on the snake's length. Subtracts starting length of 3.
        """
        self.scores = len(self.body_position) - 3
