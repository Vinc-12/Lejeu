import pytest
import pygame

from le_jeu.dodge_the_roar import init_game, update_player_position, check_collision

@pytest.fixture
def game_init():
    """Fixture pour initialiser Pygame et charger les images."""
    pygame.init()
    return init_game()

def test_init_game(game_init):
    """Test pour vérifier l'initialisation des images."""
    screen, background, zebra_image, lion_image = game_init
    assert isinstance(screen, pygame.Surface)
    assert isinstance(background, pygame.Surface)
    assert isinstance(zebra_image, pygame.Surface)
    assert isinstance(lion_image, pygame.Surface)

@pytest.mark.parametrize("player_y, player_vel_y, is_jumping, expected_y, expected_vel_y, expected_jump", [
    (300, -10, True, 290, -9.15, True),
    (435, -10, True, 435, 0, False),  # Test pour revenir au sol
])
def test_update_player_position(player_y, player_vel_y, is_jumping, expected_y, expected_vel_y, expected_jump):
    """Test pour vérifier la mise à jour de la position du joueur."""
    new_y, new_vel_y, new_jump = update_player_position(player_y, player_vel_y, is_jumping, 500, 80)
    assert new_y == pytest.approx(expected_y, 0.1)
    assert new_vel_y == pytest.approx(expected_vel_y, 0.1)
    assert new_jump == expected_jump

@pytest.mark.parametrize("player_x, player_y, zebra_width, zebra_height, obstacle_x, lion_width, obstacle_y, expected", [
    (100, 300, 70, 80, 150, 60, 300, True),  # Test avec collision
    (100, 300, 70, 80, 200, 60, 300, False),  # Test sans collision
    (100, 300, 70, 80, 150, 60, 400, False),  # Test sans collision (différente hauteur)
])
def test_check_collision(player_x, player_y, zebra_width, zebra_height, obstacle_x, lion_width, obstacle_y, expected):
    """Test pour vérifier la détection des collisions."""
    assert check_collision(player_x, player_y, zebra_width, zebra_height, obstacle_x, lion_width, obstacle_y) == expected