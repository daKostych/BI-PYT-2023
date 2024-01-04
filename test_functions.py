import os
import pytest
from unittest.mock import MagicMock, patch
from pylint.lint import Run
from pylint.reporters import CollectingReporter
from wall import Wall
from paddle import Paddle
from ball import Ball
from game import Game
from network import Network
from game_variables import *


@pytest.mark.parametrize("file_path", ["server.py", "client.py", "network.py", "game.py", "wall.py", "paddle.py",
                                       "ball.py", "game_variables"])
def test_codestyle_score(file_path):
    """ Test codestyle score for each file. """
    file_path = os.path.abspath(file_path)
    rep = CollectingReporter()
    r = Run(['--disable=C0301,C0103', '-sn', file_path], reporter=rep, exit=False)
    score = r.linter.stats.global_note
    print(f'pylint score = {score} for file {file_path}')
    assert score == 10


def test_wall_init():
    # Arrange
    wall = Wall()

    # Assert
    assert wall.width > 0
    assert wall.height > 0
    assert isinstance(wall.blocks, list)


def test_create_wall():
    # Arrange
    wall = Wall()

    # Act
    wall.create_wall()

    # Assert
    assert len(wall.blocks) == rows * cols


def test_paddle_initialization():
    paddle = Paddle()
    assert paddle.width == 124
    assert paddle.height == 15
    assert paddle.x == int((screen_width / 2) - paddle.width // 2)
    assert paddle.y == screen_height - paddle.height - 8
    assert paddle.rect == pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)


def test_paddle_movement_within_screen():
    paddle = Paddle()
    initial_x = paddle.x
    mouse_x = initial_x + 20  # move the mouse to the right
    paddle.move(mouse_x)
    assert paddle.x == mouse_x - paddle.width // 2
    assert paddle.rect == pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)


def test_paddle_movement_restriction():
    paddle = Paddle()
    initial_x = paddle.x
    mouse_x = screen_width + 20  # move the mouse outside the screen to the right
    paddle.move(mouse_x)
    assert paddle.x == initial_x  # should not move beyond the screen width
    assert paddle.rect == pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)


def test_paddle_draw():
    paddle = Paddle()
    mock_screen = MagicMock(spec=pygame.surface.Surface)
    with patch('pygame.draw.rect') as mock_draw_rect:
        paddle.draw(mock_screen)
    mock_draw_rect.assert_called_once_with(mock_screen, paddle_col, paddle.rect)


def test_ball_initialization():
    ball = Ball(100, 200)
    assert ball.ball_rad == 10
    assert ball.x == 90  # (100 - 10)
    assert ball.y == 200
    assert ball.rect == pygame.Rect(90, 200, 20, 20)
    assert ball.speed_x == 4
    assert ball.speed_y == -4
    assert ball.game_over == 0


def test_ball_move_collision_with_paddle():
    ball = Ball(100, 200)
    paddle = Paddle()
    turn = [0]
    threshold = 8
    ball.paddle_collision = MagicMock()
    ball.move(paddle, Wall(), turn)
    assert ball.paddle_collision.called_once_with(paddle, turn, threshold)


def test_ball_move_collision_with_wall():
    ball = Ball(100, 200)
    wall = Wall()
    threshold = 8
    ball.blocks_collision = MagicMock()
    ball.move(Paddle(), wall, [0])
    assert ball.blocks_collision.called_once_with(wall, threshold)


def test_ball_move_collision_with_screen_boundaries():
    ball = Ball(100, 200)
    ball.screen_collision = MagicMock()
    ball.move(Paddle(), Wall(), [0])
    assert ball.screen_collision.called_once()


def test_paddle_collision_no_collision():
    ball = Ball(100, 200)
    paddle = Paddle()
    turn = [0]
    threshold = 8
    ball.rect = pygame.Rect(0, 0, 20, 20)  # Ball at the top-left corner
    paddle.rect = pygame.Rect(50, 50, 100, 15)  # Paddle with center at (100, 57.5)

    ball.paddle_collision(paddle, turn, threshold)

    assert turn[0] == 0  # Turn should not be incremented
    assert ball.speed_x == 4  # Speed should not be modified
    assert ball.speed_y == -4


def test_paddle_collision_top_collision():
    ball = Ball(100, 200)
    paddle = Paddle()
    turn = [0]
    threshold = 8
    ball.rect = pygame.Rect(100, 57.5, 20, 20)  # Ball at the center of the paddle
    paddle.rect = pygame.Rect(50, 50, 100, 15)  # Paddle with center at (100, 57.5)

    ball.paddle_collision(paddle, turn, threshold)

    assert turn[0] == 1  # Turn should be incremented
    assert ball.speed_x == -4  # Speed should be reversed on the X-axis
    assert ball.speed_y == -4  # Speed should be reversed on the Y-axis


def test_paddle_collision_side_collision():
    ball = Ball(100, 200)
    paddle = Paddle()
    turn = [0]
    threshold = 8
    ball.rect = pygame.Rect(120, 57.5, 20, 20)  # Ball at the right side of the paddle
    paddle.rect = pygame.Rect(50, 50, 100, 15)  # Paddle with center at (100, 57.5)

    ball.paddle_collision(paddle, turn, threshold)

    assert turn[0] == 1  # Turn should be incremented
    assert ball.speed_x == -4  # Speed should be reversed on the X-axis
    assert ball.speed_y == -4  # Speed should not be modified


def test_ball_blocks_collision():
    ball = Ball(10, 10)
    wall = Wall()
    wall.blocks = [[pygame.Rect(0, 0, 20, 20), 2]]  # Mocked wall with one block
    ball.blocks_collision(wall, 8)
    assert wall.blocks[0][1] == 1  # Block strength should be reduced


def test_ball_screen_collision():
    ball = Ball(100, 0)  # Ball at the top
    ball.speed_x = 4
    ball.speed_y = -4
    ball.screen_collision()
    assert ball.speed_x == 4  # Speed should be reversed on the X-axis
    assert ball.speed_y == 4   # Speed should be reversed on the Y-axis
    assert ball.game_over == 0  # Game should not be over

    ball.rect = pygame.Rect(0, screen_height - 20, 20, 20)  # Ball at the left-bottom corner
    ball.screen_collision()
    assert ball.game_over == -1  # Game should be over (loss)


def test_init_game():
    # Arrange
    game = Game()

    # Assert
    assert isinstance(game.wall, Wall)
    assert isinstance(game.paddle, Paddle)
    assert isinstance(game.ball, Ball)
    assert game.turn == [0]
    assert game.ready == [False, False]
    assert game.game_over == 0


def test_update_game():
    # Arrange
    game = Game()
    mouse_pos = (100, 200)
    game.paddle.move = MagicMock()
    game.ball.move = MagicMock()

    # Act
    game.update_game(mouse_pos)

    # Assert
    game.paddle.move.assert_called_once_with(mouse_pos[0])
    game.ball.move.assert_called_once_with(game.paddle, game.wall, game.turn)


def test_reset_game():
    # Arrange
    game = Game()

    # Act
    game.reset()

    # Assert
    assert isinstance(game.wall, Wall)
    assert isinstance(game.paddle, Paddle)
    assert isinstance(game.ball, Ball)
    assert game.turn == [0]
    assert game.ready == [False, False]
    assert game.game_over == 0


@pytest.fixture
def mock_socket():
    with patch('socket.socket') as mock_socket:
        yield mock_socket


def test_network_init(mock_socket):
    # Arrange
    ip = '127.0.0.1'
    port = 5555

    # Act
    network = Network(ip, port)

    # Assert
    assert network.host == ip
    assert network.port == port
