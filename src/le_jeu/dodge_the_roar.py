import pygame
import random
from pathlib import Path
from typing import Tuple

def init_game() -> Tuple[pygame.Surface, pygame.Surface, pygame.Surface, pygame.Surface]:
    """
    Initialise Pygame, la fenêtre de jeu, et charge les images nécessaires.
    
    Returns:
        Tuple[pygame.Surface, pygame.Surface, pygame.Surface, pygame.Surface]: 
        La fenêtre de jeu, l'image d'arrière-plan, l'image du zèbre et l'image du lion.
    """
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Aide Zébra à survivre aux méchants lions !")
    
    image_folder = Path(__file__).parents[2].joinpath('data')
    background = pygame.image.load(image_folder.joinpath('paysage.png'))
    background = pygame.transform.scale(background, (800, 500))
    
    zebra_image = pygame.image.load(image_folder.joinpath('zebre.png'))
    zebra_image = pygame.transform.scale(zebra_image, (70, 80))
    
    lion_image = pygame.image.load(image_folder.joinpath('lion.png'))
    lion_image = pygame.transform.scale(lion_image, (60, 70))
    
    return screen, background, zebra_image, lion_image

def draw_background(screen: pygame.Surface, background: pygame.Surface, x1: int, x2: int) -> None:
    """
    Dessine l'arrière-plan et le fait défiler.
    
    Args:
        screen (pygame.Surface): La fenêtre de jeu.
        background (pygame.Surface): L'image d'arrière-plan.
        x1 (int): Position x du premier segment de l'arrière-plan.
        x2 (int): Position x du second segment de l'arrière-plan.
    """
    screen.blit(background, (x1, 0))
    screen.blit(background, (x2, 0))

def draw_objects(screen: pygame.Surface, zebra_image: pygame.Surface, lion_image: pygame.Surface,
                 player_x: int, player_y: int, obstacle_x: int, obstacle_y: int, score: int, font: pygame.font.Font) -> None:
    """
    Dessine le personnage, l'obstacle et affiche le score.
    
    Args:
        screen (pygame.Surface): La fenêtre de jeu.
        zebra_image (pygame.Surface): Image du zèbre.
        lion_image (pygame.Surface): Image du lion.
        player_x (int): Position x du personnage.
        player_y (int): Position y du personnage.
        obstacle_x (int): Position x de l'obstacle.
        obstacle_y (int): Position y de l'obstacle.
        score (int): Score actuel.
        font (pygame.font.Font): Police pour l'affichage du score.
    """
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(zebra_image, (player_x, player_y))
    screen.blit(lion_image, (obstacle_x, obstacle_y))

def handle_events() -> bool:
    """
    Gère les événements Pygame et vérifie si l'utilisateur ferme la fenêtre.
    
    Returns:
        bool: True si la fenêtre doit rester ouverte, False sinon.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def update_player_position(player_y: int, player_vel_y: int, is_jumping: bool, screen_height: int, zebra_height: int) -> Tuple[int, int, bool]:
    """
    Met à jour la position verticale du joueur et gère l'état de saut.
    
    Args:
        player_y (int): Position y actuelle du joueur.
        player_vel_y (int): Vitesse verticale du joueur.
        is_jumping (bool): Indique si le joueur est en train de sauter.
        screen_height (int): Hauteur de la fenêtre de jeu.
        zebra_height (int): Hauteur de l'image du personnage.
    
    Returns:
        Tuple[int, int, bool]: Nouvelle position y, nouvelle vitesse y et état de saut.
    """
    if is_jumping:
        player_y += player_vel_y
        player_vel_y += 0.85  # Gravité
        
        if player_y >= screen_height - zebra_height - 100:
            player_y = screen_height - zebra_height - 100
            is_jumping = False
    return player_y, player_vel_y, is_jumping

def check_collision(player_x: int, player_y: int, zebra_width: int, zebra_height: int,
                    obstacle_x: int, lion_width: int, obstacle_y: int) -> bool:
    """
    Vérifie la collision entre le personnage et l'obstacle.
    
    Args:
        player_x (int): Position x du joueur.
        player_y (int): Position y du joueur.
        zebra_width (int): Largeur du joueur.
        zebra_height (int): Hauteur du joueur.
        obstacle_x (int): Position x de l'obstacle.
        lion_width (int): Largeur de l'obstacle.
        obstacle_y (int): Position y de l'obstacle.
    
    Returns:
        bool: True s'il y a collision, sinon False.
    """
    return (player_x + zebra_width > obstacle_x and player_x < obstacle_x + lion_width and
            player_y + zebra_height > obstacle_y)

def main() -> None:
    """
    Fonction principale qui exécute le jeu.
    """
    screen, background, zebra_image, lion_image = init_game()
    clock = pygame.time.Clock()
    
    player_x = 100
    player_y = screen.get_height() - 80 - 100
    player_vel_y = 0
    is_jumping = False
    
    background_x1 = 0
    background_x2 = screen.get_width()
    background_speed = 2
    
    obstacle_x = screen.get_width()
    obstacle_y = screen.get_height() - 70 - 100
    obstacle_speed = 5
    
    score = 0
    font = pygame.font.SysFont('Arial', 24)
    running = True
    
    while running:
        clock.tick(30)
        background_x1 -= background_speed
        background_x2 -= background_speed
        
        if background_x1 <= -screen.get_width():
            background_x1 = screen.get_width()
        if background_x2 <= -screen.get_width():
            background_x2 = screen.get_width()
        
        running = handle_events()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not is_jumping:
            is_jumping = True
            player_vel_y = -16
        
        player_y, player_vel_y, is_jumping = update_player_position(player_y, player_vel_y, is_jumping, screen.get_height(), 80)
        
        draw_background(screen, background, background_x1, background_x2)
        draw_objects(screen, zebra_image, lion_image, player_x, player_y, obstacle_x, obstacle_y, score, font)
        
        obstacle_x -= obstacle_speed
        if obstacle_x < -60:
            obstacle_x = screen.get_width()
            score += 1
            obstacle_speed += 1
        
        if check_collision(player_x, player_y, 70, 80, obstacle_x, 60, obstacle_y):
            running = False
        
        pygame.display.flip()
    
    # Affichage du message de fin de jeu
    screen.fill((255, 255, 255))
    game_over_text = font.render('Game Over! Appuyez sur une touche pour quitter.', True, (0, 0, 0))
    screen.blit(game_over_text, (screen.get_width() // 2 - 270, screen.get_height() // 2 - 20))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
    
    pygame.quit()

if __name__ == "__main__":
    main()