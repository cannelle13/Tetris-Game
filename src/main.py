import pygame
import sys
from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetris Game")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 400)

down_key_pressed = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_SPACE:
                game.paused = not game.paused
                game.pause()
            if event.key == pygame.K_LEFT and not game.game_over:
                game.move_left()
            if event.key == pygame.K_RIGHT and not game.game_over:
                game.move_right()
            if event.key == pygame.K_DOWN and not game.game_over:
                game.move_down()
                game.update_score(0, 1)
                down_key_pressed = True
            if event.key == pygame.K_UP and not game.game_over:
                game.rotate()

        if event.type == GAME_UPDATE and not game.game_over:
            game.move_down()
            if game.score >= game.current_level * 1000:
                game.current_level += 1
                if game.current_level <= len(game.levels):
                    pygame.time.set_timer(GAME_UPDATE, game.levels[game.current_level])
                print(f"Level increased to {game.current_level}")
            if not game.game_over:
                if down_key_pressed and pygame.key.get_pressed()[pygame.K_DOWN]:
                    game.move_down()
                    game.update_score(0, 1)
                else:
                    down_key_pressed = False

    # Drawing
    score_value_surface = title_font.render(str(game.score), True, Colors.white)

    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))

    if game.game_over:
        screen.blit(game_over_surface, (320, 450, 50, 50))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(
        score_value_surface,
        score_value_surface.get_rect(
            centerx=score_rect.centerx, centery=score_rect.centery
        ),
    )
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)
