# Importamos las librerias necesarias
import pygame
import sys
import random

if __name__ == '__main__':
    # Inicializamos Pygame
    pygame.init()
    # Configuramos la ventana
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")
    # Configuramos los colores
    black = (0, 0, 0)
    green = (0, 255, 0)
    red = (255, 0, 0)
    # Configuramos el reloj de Pygame para controlar los FPS
    clock = pygame.time.Clock()
    fps = 15
    # Configuramos el tamaño de la serpiente
    snake_size = 10
    # Configuramos la posición inicial de la serpiente
    snake_pos = [[100, 50], [90, 50], [80, 50]]
    snake_direction = "RIGHT"
    change_to = snake_direction

    # Función para dibujar la serpiente
    def draw_snake(snake_pos):
        for pos in snake_pos:
            pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], snake_size, snake_size))

    # Función para detectar colisiones
    def collision_with_boundaries(snake_head):
        if snake_head[0][0] >= width or snake_head[0][0] < 0 or snake_head[0][1] >= height or snake_head[0][1] < 0:
            return True
        return False

    # Función para generar la posición de la comida de manera aleatoria
    def generate_food_position():
        return [random.randrange(1, (width//snake_size)) * snake_size, random.randrange(1, (height//snake_size)) * snake_size]

    # Función para dibujar la comida
    def draw_food(food_pos):
        pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size))

    # Función para detectar colisiones con la comida
    def collision_with_food(snake_head, food_pos):
        if snake_head[0] == food_pos[0] and snake_head[1] == food_pos[1]:
            return True
        return False

    # Función para mostrar la pantalla de inicio
    def show_start_screen():
        screen.fill(black)
        font = pygame.font.SysFont('Arial', 35)
        text = font.render('Press any key to start', True, (255, 255, 255))
        text_rect = text.get_rect(center=(width/2, height/2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    waiting = False

    # Función para mostrar la puntuación
    def show_score(score):
        font = pygame.font.SysFont('Arial', 30)
        text = font.render('Score: ' + str(score), True, (255, 255, 255))
        screen.blit(text, (5, 5))

    # Función para mostrar la pantalla de Game Over
    def show_game_over_screen(score):
        screen.fill(black)
        font = pygame.font.SysFont('Arial', 35)
        game_over_text = font.render('Game Over', True, red)
        score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(width / 2, height / 2 - 50))
        score_rect = score_text.get_rect(center=(width / 2, height / 2 + 10))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    waiting = False

    # Inicializamos la posición de la comida
    food_pos = generate_food_position()
    food_spawn = True
    # Mostramos la pantalla de inicio
    show_start_screen()
    # Inicializamos la puntuación
    score = 0

    # Bucle principal
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Captura de teclas para el movimiento
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                    change_to = 'RIGHT'
        # Actualización de la dirección de la serpiente
        if change_to == 'UP' and snake_direction != 'DOWN':
            snake_direction = 'UP'
        elif change_to == 'DOWN' and snake_direction != 'UP':
            snake_direction = 'DOWN'
        elif change_to == 'LEFT' and snake_direction != 'RIGHT':
            snake_direction = 'LEFT'
        elif change_to == 'RIGHT' and snake_direction != 'LEFT':
            snake_direction = 'RIGHT'
        # Movimiento de la serpiente
        if snake_direction == 'UP':
            snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] - snake_size])
        elif snake_direction == 'DOWN':
            snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] + snake_size])
        elif snake_direction == 'LEFT':
            snake_pos.insert(0, [snake_pos[0][0] - snake_size, snake_pos[0][1]])
        elif snake_direction == 'RIGHT':
            snake_pos.insert(0, [snake_pos[0][0] + snake_size, snake_pos[0][1]])
        # Comprobar si la serpiente ha chocado con los límites
        if collision_with_boundaries(snake_pos):
            show_game_over_screen(score)
        # Configuramos el fondo de la ventana
        screen.fill(black)
        show_score(score)
        # Dibujamos la serpiente
        draw_snake(snake_pos)
        # Dibujamos la comida
        if food_spawn:
            draw_food(food_pos)
        # Comprobar si la serpiente ha comido la comida
        if collision_with_food(snake_pos[0], food_pos):
            score += 1
            food_spawn = False
            # Generar nueva comida
            food_pos = generate_food_position()
            food_spawn = True
        else:
            # Eliminar el último segmento solo si no ha comido la comida
            snake_pos.pop()
        # Actualizamos la ventana
        pygame.display.flip()
        # Controlamos los FPS
        clock.tick(fps)