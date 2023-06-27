import pygame
from GUI import *

pygame.init()
pygame.display.set_caption('TetriX')


def main_game():
    t = TetriX_GUI()

    while t.game_running and not t.game_over:
        action = None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            action = DOWN_KEY

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t.game_running = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    t.game_running = False
                    pygame.display.quit()
                    quit()
                elif event.key == pygame.K_p:
                    game_paused = True
                    while game_paused:
                        for sub_event in pygame.event.get():
                            if sub_event.type == pygame.KEYDOWN and sub_event.key == pygame.K_p:
                                game_paused = False
                elif event.key == pygame.K_SPACE:
                    action = DROP_KEY
                elif event.key == pygame.K_UP:
                    action = ROTATE_KEY
                elif event.key == pygame.K_RIGHT:
                    action = RIGHT_KEY
                elif event.key == pygame.K_LEFT:
                    action = LEFT_KEY

        t.play_game(action)

        if t.check_game_over():
            t.game_running = False
            t.game_over = True

    while t.game_over:
        t.window.fill(color=BACKGROUND_COLOR)
        font = pygame.font.SysFont(FONT, FONT_SIZE*2)
        game_over_text = font.render("GAME OVER", True, FONT_COLOR)
        game_over_len, game_over_height = game_over_text.get_rect().size
        t.window.blit(game_over_text, (SCREEN_WIDTH / 2 -
                      game_over_len / 2, SCREEN_HEIGHT / 3 + game_over_height / 2))

        final_score_text = font.render(
            "Final Score: " + str(t.score), True, FONT_COLOR)
        final_score_len, final_score_height = final_score_text.get_rect().size
        t.window.blit(final_score_text, (SCREEN_WIDTH / 2 - final_score_len /
                      2, 2 * SCREEN_HEIGHT / 3 + final_score_height / 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                t.game_over = False

    pygame.quit()


if __name__ == '__main__':
    main_game()
