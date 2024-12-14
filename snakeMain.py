import sys
from PyQt6.QtWidgets import QApplication
from snakeCntlr import SnakeGameController


def main() -> None:
    """
    Main function to initialize and run the Snake game application.

    This function creates a QApplication instance, initializes the game
    controller, and starts the event loop for the application.
    """
    app = QApplication(sys.argv)  # Create a Qt application
    game = SnakeGameController()  # Initialize the game controller
    game.show()  # Display the game window

    sys.exit(app.exec())  # Start the event loop and exit when done


if __name__ == "__main__":
    main()
