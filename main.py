import os
import os
import sys
import cfg_1
import random
import pygame


def game_over(board, size):
    assert isinstance(size, int)
    number_of_cells = size * size
    for i in range(number_of_cells - 1):
        if board[i] != i:
            return False
    return True


def move_right(board, blank_cell_index, num_col):
    if blank_cell_index % num_col == 0:
        return blank_cell_index
    board[blank_cell_index - 1], board[blank_cell_index] = board[blank_cell_index], board[blank_cell_index - 1]
    return blank_cell_index - 1


def move_left(board, blank_cell_index, num_col):
    if (blank_cell_index + 1) % num_col == 0:
        return blank_cell_index
    board[blank_cell_index + 1], board[blank_cell_index] = board[blank_cell_index], board[blank_cell_index + 1]
    return blank_cell_index + 1


def move_down(board, blank_cell_index, num_col):
    if blank_cell_index < num_col:
        return blank_cell_index
    board[blank_cell_index - num_col], board[blank_cell_index] = board[blank_cell_index], board[blank_cell_index - num_col]
    return blank_cell_index - num_col


def move_up(board, blank_cell_index, num_col, num_rows):
    if blank_cell_index >= (num_rows - 1) * num_col:
        return blank_cell_index
    board[blank_cell_index + num_col], board[blank_cell_index] = board[blank_cell_index], board[blank_cell_index + num_col]
    return blank_cell_index + num_col


def create_board(num_rows, num_cells, num_col):
    board = []
    for i in range(num_cells):
        board.append(i)
    blank_cell_index = num_cells - 1
    board[blank_cell_index] = -1
    for i in range(cfg_1.randomNumber):
        direction = random.randint(0, 3)
        if direction == 0:
            blank_cell_index = move_left(board, blank_cell_index, num_col)
        elif direction == 1:
            blank_cell_index = move_right(board, blank_cell_index, num_col)
        elif direction == 2:
            blank_cell_index = move_up(board, blank_cell_index, num_col, num_rows)
        elif direction == 3:
            blank_cell_index = move_down(board, blank_cell_index, num_col)
    return board, blank_cell_index


def get_image(root_directory):
    image_name = os.listdir(root_directory)
    assert len(image_name) > 0
    return os.path.join(root_directory, random.choice(image_name))


def show_end_screen(screen, width, height):
    screen.fill(cfg_1.backgroundColor)
    font = pygame.font.Font(cfg_1.fontPath, width / 15)
    title = font.render('Congratulations you have won the game !', True, (233, 150, 122))
    rect = title.get_rect()
    rect.midtop = (width / 2, height / 2.5)
    screen.blit(title, rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.update()


def show_start_screen(screen, width, height):
    screen.fill(cfg_1.backgroundColor)
    tfont = pygame.font.Font(cfg_1.fontPath, width //15)
    cfont = pygame.font.Font(cfg_1.fontPath, width //20)
    title = tfont.render("Welcome to our puzzle game !", True, cfg_1.red)
    content1 = cfont.render("Press H, M or L to choose your difficulty ", True, cfg_1.blue)
    content2 = cfont.render("H- 5x5, M- 4x4, L- 3x3", True, cfg_1.blue)
    trect = title.get_rect()
    trect.midtop = (width/ 2, height/ 10)
    crect1 = content1.get_rect()
    crect1.midtop = (width / 2, height / 2.2)
    crect2 = content2.get_rect()
    crect2.midtop = (width / 2, height / 1.8)
    screen.blit(title, trect)
    screen.blit(content1, crect1)
    screen.blit(content2, crect2)
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('l') or event.key == ord('L'):
                    return 3
                elif event.key == ord('m') or event.key == ord('M'):
                    return 4
                elif event.key == ord('h') or event.key == ord('H'):
                    return 5
        pygame.display.update()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    game_images = pygame.image.load(get_image(cfg_1.picture_root_directory))
    game_images = pygame.transform.scale(game_images, cfg_1.screenSize)
    game_images_rect = game_images.get_rect()
    screen = pygame.display.set_mode(cfg_1.screenSize)
    pygame.display.set_caption("Puzzle")
    size = show_start_screen(screen,game_images_rect.width, game_images_rect.height)
    assert isinstance(size, int)
    num_rows, num_col = size, size
    num_cells = size * size
    cell_width = game_images_rect.width // num_col
    cell_height = game_images_rect.height // num_rows
    while True:
        game_board, blank_cell_index = create_board(num_rows, num_cells, num_col)
        if not game_over(game_board, size):
            break
    isrunning = True
    while isrunning:

        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    blank_cell_index = move_left(game_board, blank_cell_index, num_col)
                elif event.type == pygame.K_RIGHT or event.key == ord('d'):
                    blank_cell_index = move_right(game_board, blank_cell_index, num_col)
                elif event.type == pygame.K_RIGHT or event.key == ord('w'):
                    blank_cell_index = move_up(game_board, blank_cell_index,  num_col, num_rows)
                elif event.type == pygame.K_DOWN or event.key == ord('s'):
                    blank_cell_index == move_down(game_board, blank_cell_index, num_col)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                x_pos = x//cell_width
                y_pos = y//cell_height
                idx = x_pos + y_pos*num_col
                if idx == blank_cell_index-1:
                    blank_cell_index = move_right(game_board, blank_cell_index, num_col)
                elif idx == blank_cell_index+1:
                    blank_cell_index = move_left(game_board, blank_cell_index, num_col)
                elif idx == blank_cell_index+num_col:
                    blank_cell_index = move_up(game_board, blank_cell_index, num_rows, num_col)
                elif idx == blank_cell_index-num_col:
                    blank_cell_index = move_down(game_board, blank_cell_index, num_rows)
        if game_over(game_board, size):
            game_board[blank_cell_index] = num_cells - 1
            isrunning = False
        screen.fill(cfg_1.backgroundColor)
        for i in range(num_cells):
            if game_board[i] == -1:
                continue
            x_pos = i//num_col
            y_pos = i % num_col
            rect = pygame.Rect(y_pos*cell_width, x_pos*cell_height, cell_width, cell_height)
            img_area = pygame.Rect((game_board[i]%num_col)*cell_width, (game_board[i]//num_col)*cell_height, cell_width, cell_height)
            screen.blit(game_images, rect, img_area)
        for i in range(num_col+1):
            pygame.draw.line(screen, cfg_1.black, (i*cell_width, 0), (i*cell_width, game_images_rect.height))
        for i in range(num_rows+1):
            pygame.draw.line(screen, cfg_1.black, (0, i * cell_height), (game_images_rect.width, i * cell_height))
        pygame.display.update()
        clock.tick(cfg_1.FPS)
    show_end_screen(screen, game_images_rect.width, game_images_rect.height)






if __name__ == '__main__':
    main()
