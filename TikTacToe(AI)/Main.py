import pygame as p
import sys
import time
import subprocess

p.init()

class Square(p.sprite.Sprite):
    def __init__(self, x_id, y_id, number):
        super().__init__()
        self.width = 120
        self.height = 120
        self.x = x_id * self.width
        self.y = y_id * self.height
        self.content = ''
        self.number = number
        self.image = blank_image
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = (self.x, self.y)

    def clicked(self, x_val, y_val):
        global turn, won

        if self.content == '':
            if self.rect.collidepoint(x_val, y_val):
                self.content = turn
                board[self.number] = turn

                if turn == 'x':
                    self.image = x_image
                    self.image = p.transform.scale(self.image, (self.width, self.height))
                    turn = 'o'
                    checkWinner('x')

                    if not won:
                        CompMove()

                else:
                    self.image = o_image
                    self.image = p.transform.scale(self.image, (self.width, self.height))
                    turn = 'x'
                    checkWinner('o')

class Button(p.sprite.Sprite):
    def __init__(self, text, x, y, width, height, action, font, font_size, color, hover_color):
        super().__init__()
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.font = p.font.SysFont(font, font_size)
        self.color = color
        self.hover_color = hover_color
        self.image = p.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.draw_button()

    def draw_button(self):
        self.image.fill(self.color)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(text_surface, text_rect)

    def update(self):
        if self.rect.collidepoint(p.mouse.get_pos()):
            self.image.fill(self.hover_color)
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2))
            self.image.blit(text_surface, text_rect)
        else:
            self.image.fill(self.color)
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2))
            self.image.blit(text_surface, text_rect)

    def clicked(self):
        if self.rect.collidepoint(p.mouse.get_pos()):
            if self.action == 'rematch':
                p.quit()
                subprocess.run(["python", "tak.py"])
            elif self.action == 'exit':
                p.quit()
                sys.exit()

def checkWinner(player):
    global background, won, startX, startY, endX, endY

    for i in range(8):
        if board[winners[i][0]] == player and board[winners[i][1]] == player and board[winners[i][2]] == player:
            won = True
            getPos(winners[i][0], winners[i][2])
            break

    if won:
        Update()
        drawLine(startX, startY, endX, endY)

        square_group.empty()
        background = p.image.load(player.upper() + ' Wins.png')
        background = p.transform.scale(background, (WIDTH, HEIGHT))
        rematch_button = Button("Rematch", WIDTH // 2 - 75, HEIGHT - 150, 150, 50, 'rematch', 'Arial Bold', 38, (0, 100, 200), (0, 150, 255))
        exit_button = Button("Exit", WIDTH // 2 - 75, HEIGHT - 90, 150, 50, 'exit', 'Arial Bold', 38, (200, 50, 50), (255, 100, 100))
        button_group.add(rematch_button, exit_button)

def Winner(player):
    global compMove, move

    for i in range(8):
        if board[winners[i][0]] == player and board[winners[i][1]] == player and board[winners[i][2]] == '':
            compMove = winners[i][2]
            move = False

        elif board[winners[i][0]] == player and board[winners[i][1]] == '' and board[winners[i][2]] == player:
            compMove = winners[i][1]
            move = False

        elif board[winners[i][0]] == '' and board[winners[i][1]] == player and board[winners[i][2]] == player:
            compMove = winners[i][0]
            move = False

def CompMove():
    global move, background

    move = True

    if move:
        Winner('o')

    if move:
        Winner('x')

    if move:
        checkDangerPos()

    if move:
        checkCentre()

    if move:
        checkCorner()

    if move:
        checkEdge()

    if not move:
        for square in squares:
            if square.number == compMove:
                square.clicked(square.x, square.y)

    else:
        Update()
        time.sleep(1)
        square_group.empty()
        background = p.image.load('Tie Game.png')
        background = p.transform.scale(background, (WIDTH, HEIGHT))
        rematch_button = Button("Rematch", WIDTH // 2 - 75, HEIGHT - 150, 150, 50, 'Rematch', 'Arial Bold', 38, (0, 100, 200), (0, 150, 255))
        exit_button = Button("Exit", WIDTH // 2 - 75, HEIGHT - 90, 150, 50, 'exit', 'Arial Bold', 38, (200, 50, 50), (255, 100, 100))

        button_group.add(rematch_button, exit_button)

def checkDangerPos():
    global move, compMove

    if board == dangerPos1:
        compMove = 2
        move = False

    elif board == dangerPos2:
        compMove = 4
        move = False

    elif board == dangerPos3:
        compMove = 1
        move = False

    elif board == dangerPos4:
        compMove = 4
        move = False

    elif board == dangerPos5:
        compMove = 7
        move = False

    elif board == dangerPos6:
        compMove = 9
        move = False

    elif board == dangerPos7:
        compMove = 9
        move = False

    elif board == dangerPos8:
        compMove = 7
        move = False

    elif board == dangerPos9:
        compMove = 9
        move = False

def checkCentre():
    global compMove, move

    if board[5] == '':
        compMove = 5
        move = False

def checkCorner():
    global compMove, move

    for i in range(1, 11, 2):
        if i != 5:
            if board[i] == '':
                compMove = i
                move = False
                break

def checkEdge():
    global compMove, move

    for i in range(2, 10, 2):
        if board[i] == '':
            compMove = i
            move = False
            break

def getPos(n1, n2):
    global startX, startY, endX, endY

    for sqs in squares:
        if sqs.number == n1:
            startX = sqs.x
            startY = sqs.y

        elif sqs.number == n2:
            endX = sqs.x
            endY = sqs.y

def drawLine(x1, y1, x2, y2):
    p.draw.line(win, (0, 0, 0), (x1, y1), (x2, y2), 15)
    p.display.update()
    time.sleep(2)

def Update():
    win.blit(background, (0, 0))
    square_group.draw(win)
    square_group.update()
    button_group.draw(win)
    button_group.update()
    p.display.update()

def run_game():
    global run, move, won, turn
    move = True
    won = False
    turn = 'x'
    while run:
        clock.tick(60)
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False

            if event.type == p.MOUSEBUTTONDOWN and turn == 'x':
                mx, my = p.mouse.get_pos()
                for s in squares:
                    s.clicked(mx, my)

            if event.type == p.MOUSEBUTTONDOWN and (won or move):
                for button in button_group:
                    button.clicked()

        if move and not won:
            CompMove()

        Update()

def main():
    global WIDTH, HEIGHT, win, blank_image, x_image, o_image, background, move, won, compMove, square_group, button_group, squares, winners, board, dangerPos1, dangerPos2, dangerPos3, dangerPos4, dangerPos5, dangerPos6, dangerPos7, dangerPos8, dangerPos9, startX, startY, endX, endY, turn, run, clock
    WIDTH = 500
    HEIGHT = 500

    win = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Tic Tac Toe')
    clock = p.time.Clock()

    blank_image = p.image.load('Blank.png')
    x_image = p.image.load('x.png')
    o_image = p.image.load('o.png')
    background = p.image.load('Background.png')

    background = p.transform.scale(background, (WIDTH, HEIGHT))

    move = True
    won = False
    compMove = 5

    square_group = p.sprite.Group()
    button_group = p.sprite.Group()
    squares = []

    winners = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    board = ['' for i in range(10)]

    dangerPos1 = ['', 'x', '', '', '', 'o', '', '', '', 'x']
    dangerPos2 = ['', '', '', 'x', '', 'o', '', 'x', '', '']
    dangerPos3 = ['', '', '', 'x', 'x', 'o', '', '', '', '']
    dangerPos4 = ['', 'x', '', '', '', 'o', 'x', '', '', '']
    dangerPos5 = ['', '', '', '', 'x', 'o', '', '', '', 'x']
    dangerPos6 = ['', '', '', '', '', 'o', 'x', 'x', '', '']
    dangerPos7 = ['', '', '', '', '', 'o', 'x', '', 'x', '']
    dangerPos8 = ['', 'x', '', '', '', 'o', '', '', 'x', '']
    dangerPos9 = ['', '', '', 'x', '', 'o', '', '', 'x', '']

    startX = 0
    startY = 0
    endX = 0
    endY = 0

    num = 1
    for y in range(1, 4):
        for x in range(1, 4):
            sq = Square(x, y, num)
            square_group.add(sq)
            squares.append(sq)

            num += 1

    turn = 'x'
    run = True
    start_button = Button("Start", WIDTH // 2 - 75, HEIGHT // 2 - 50, 150, 50, 'start', 'Arial Bold', 38, (0, 100, 200), (0, 150, 255))
    lets_play_text_line1 = p.font.SysFont('Comic Sans MS', 30).render("Come on let's play ", True, (23, 63, 63))
    lets_play_rect_line1 = lets_play_text_line1.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    lets_play_text_line2 = p.font.SysFont('Comic Sans MS', 20).render("I choose O you take X", True, (23, 63, 63))
    lets_play_rect_line2 = lets_play_text_line2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))

    button_group.add(start_button)

    while run:
        clock.tick(60)
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False

            if event.type == p.MOUSEBUTTONDOWN and turn == 'x':
                mx, my = p.mouse.get_pos()
                for s in squares:
                    s.clicked(mx, my)

            if event.type == p.MOUSEBUTTONDOWN and won:
                for button in button_group:
                    button.clicked()

            if event.type == p.MOUSEBUTTONDOWN and not won and start_button.rect.collidepoint(p.mouse.get_pos()):
                button_group.empty()
                run_game()

        win.blit(background, (0, 0))
        win.blit(lets_play_text_line1, lets_play_rect_line1)
        win.blit(lets_play_text_line2, lets_play_rect_line2)
        button_group.draw(win)
        button_group.update()
        p.display.update()

    p.quit()
    sys.exit()

if __name__ == "__main__":
    main()
