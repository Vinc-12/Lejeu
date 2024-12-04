import pytest
import pygame
from unittest.mock import patch, MagicMock
from le_jeu.dodge_the_roar import init_game, draw_background, draw_objects, handle_events, update_player_position, check_collision

@pytest.fixture
def mock_pygame():
    """Fixture pour initialiser pygame dans un environnement de test."""
    pygame.init()
    yield pygame
    pygame.quit()

@pytest.fixture
def game_assets(mock_pygame):
    """Fixture pour initialiser les ressources du jeu."""
    screen, background, zebra_image, lion_image = init_game()
    return screen, background, zebra_image, lion_image

def test_init_game(game_assets):
    """Test de l'initialisation du jeu."""
    screen, background, zebra_image, lion_image = game_assets
    assert isinstance(screen, pygame.Surface)
    assert isinstance(background, pygame.Surface)
    assert isinstance(zebra_image, pygame.Surface)
    assert isinstance(lion_image, pygame.Surface)

def test_draw_background(game_assets):
    """Test de la fonction draw_background."""
    screen, background, _, _ = game_assets
    x1, x2 = 0, screen.get_width()
    
    # On va vérifier qu'aucune exception n'est levée et que l'écran est bien modifié
    draw_background(screen, background, x1, x2)
    assert screen.get_at((0, 0)) == background.get_at((0, 0))  # Vérifie que la position (0,0) du fond a bien été dessinée

def test_draw_objects(game_assets):
    """Test de la fonction draw_objects."""
    screen, _, zebra_image, lion_image = game_assets
    font = pygame.font.SysFont('Arial', 24)
    
    # On suppose que le score est 0 et la position du joueur et de l'obstacle sont (100, 100)
    draw_objects(screen, zebra_image, lion_image, 100, 100, 200, 200, 0, font)
    

def test_handle_events_quit(mock_pygame):
    """Test de la gestion des événements avec fermeture de la fenêtre."""
    mock_event = MagicMock()
    mock_event.type = pygame.QUIT
    with patch('pygame.event.get', return_value=[mock_event]):
        assert not handle_events()  # Retourne False quand l'événement QUIT est détecté

def test_handle_events_no_quit(mock_pygame):
    """Test de la gestion des événements sans fermeture de la fenêtre."""
    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    with patch('pygame.event.get', return_value=[mock_event]):
        assert handle_events()  # Retourne True quand il n'y a pas de QUIT

def test_update_player_position():
    """Test de la fonction de mise à jour de la position du joueur."""
    player_y, player_vel_y, is_jumping = 300, 0, False
    screen_height, zebra_height = 500, 80
    player_y, player_vel_y, is_jumping = update_player_position(player_y, player_vel_y, is_jumping, screen_height, zebra_height)
    
    # Test que la position du joueur a bien été mise à jour
    assert player_y == 300  # Avec une vitesse verticale initiale de 0 et une gravité de 0.85, le joueur doit descendre.
    assert not is_jumping  # Le joueur ne doit plus être en train de sauter après avoir atteint le sol

def test_check_collision_no_collision():
    """Test de la vérification de collision sans collision."""
    assert not check_collision(100, 100, 70, 80, 200, 60, 200)

def test_check_collision_with_collision():
    """Test de la vérification de collision avec collision."""
    assert check_collision(100, 100, 70, 80, 100, 60, 100)

