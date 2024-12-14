# snake_controller.py
from PyQt6.QtCore import Qt
from snakeVw import SnakeGameWindow
from snakeMdl import Direction

class SnakeGameController(SnakeGameWindow):
    """
    Controller that manages game events based on user input.
    """
    def __init__(self):
        """
        Initialize SnakeGameController
        """
        super().__init__()

    def keyPressEvent(self, event):
        """
        Handle key presses.

        Args:
            event (Qt.KeyEvent): key press event.
        """
        if event.key() == Qt.Key.Key_Up:
            self.snake.direction = Direction.UP
        elif event.key() == Qt.Key.Key_Down:
            self.snake.direction = Direction.DOWN
        elif event.key() == Qt.Key.Key_Left:
            self.snake.direction = Direction.LEFT
        elif event.key() == Qt.Key.Key_Right:
            self.snake.direction = Direction.RIGHT

    def timerEvent(self, event):
        """
        Handle timer events, such as moving the snake or updating the game.

        Args:
            event (Qt.TimerEvent): timer event
        """
        if self.snake.state_game():
            self.game_over()
            return

        self.snake.move()
        self.snake.eat()
        self.update()
