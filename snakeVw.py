from PyQt6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QLabel, QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QBasicTimer, QTimer, Qt
import time
from snakeMdl import Snake, Direction

class SnakeGameWindow(QMainWindow):
    """
    Main game window for the Snake game.
    Handles rendering, user input, and updates.
    """

    def __init__(self):
        """
        Initialize the Snake game window.
        """
        super().__init__()

        self.snake = Snake()
        self.init_ui()
        self.timer = QBasicTimer()
        self.timer.start(self.snake.frame_time, self)

        self.start_time = time.time()
        self.fps_timer = QTimer()

        self.setWindowTitle('Snake Game')
        self.show()

    def init_ui(self) -> None:
        """
        Set up the user interface elements for the game.
        """
        self.setMinimumSize(self.snake.width, self.snake.height)
        self.setStatusTip('Use arrow keys to control the snake.')

    def update_status_bar(self) -> None:
        """
        Update the status bar with the current score and elapsed time.
        """
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        elapsed_seconds = int(elapsed_time)
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        total_time = f"Time: {minutes:02}:{seconds:02}"

        status = f"Score: {self.snake.scores} | {total_time}"
        self.statusBar().showMessage(status)

    def paintEvent(self, e) -> None:
        """
        Handle the paint event to draw game elements.
        """
        painter = QPainter(self)
        try:
            self.draw_snake(painter)
            self.draw_food(painter)
        finally:
            self.update_status_bar()

    def draw_snake(self, painter: QPainter) -> None:
        """
        Draw the snake on the game board.
        """
        body_position = self.snake.body_position
        block_size = self.snake.grid_size

        painter.setPen(Qt.PenStyle.NoPen)
        for index, (x, y) in enumerate(body_position):
            if index == 0:  # Snake head
                painter.setBrush(QColor(255, 0, 0))  # Red head
                painter.drawRect(x, y, block_size, block_size)
            else:
                painter.setBrush(QColor(0, 255, 0))
                painter.drawRect(x, y, block_size, block_size)

    def draw_food(self, painter: QPainter) -> None:
        """
        Draw the food item on the game board.
        """
        food_position = self.snake.food_position
        block_size = self.snake.grid_size
        if food_position:
            painter.setBrush(QColor(0, 0, 255))  # Food is blue
            painter.drawEllipse(food_position[0], food_position[1], block_size, block_size)

    def timerEvent(self, event) -> None:
        """
        Handle timer events for updating the game state.
        """
        if self.snake.state_game():
            self.game_over()
        else:
            self.snake.move()
            self.update()

    def keyPressEvent(self, event) -> None:
        """
        Handle key presses for controlling the snake's direction.
        """
        if event.key() == Qt.Key.Key_Up:
            self.snake.direction = Direction.UP
        elif event.key() == Qt.Key.Key_Down:
            self.snake.direction = Direction.DOWN
        elif event.key() == Qt.Key.Key_Left:
            self.snake.direction = Direction.LEFT
        elif event.key() == Qt.Key.Key_Right:
            self.snake.direction = Direction.RIGHT

    def game_over(self) -> None:
        """
        Handle the game over scenario by displaying a message box.
        """
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        elapsed_seconds = int(elapsed_time)
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        elapsed_time_str = f"{minutes:02}:{seconds:02}"

        msg_widget = QWidget()
        layout = QVBoxLayout()
        score_label = QLabel(f"Game Over! Score: {self.snake.scores}")
        time_label = QLabel(f"{elapsed_time_str}")

        layout.addWidget(score_label)
        layout.addWidget(time_label)
        msg_widget.setLayout(layout)

        msg = QMessageBox(self)
        msg.setWindowTitle("Game Over")
        msg.setInformativeText(f"Game Over!\nScore: {self.snake.scores}\nElapsed Time: {elapsed_time_str}")
        msg.setStyleSheet("QLabel{font-size: 12pt; font-family: 'Comic Sans MS';}")
        msg.setMinimumWidth(200)
        msg.setMinimumHeight(180)
        msg.exec()

        self.snake.start_body_position()  # Reset the game
        self.snake.scores = 0
        self.start_time = time.time()
        self.update()
