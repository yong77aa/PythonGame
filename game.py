import pygame # pygame ���̺귯���� import
import random
from time import sleep

WHITE = (255, 255, 255) # ����� ǥ���ϴ� ��
pad_width = 1024 # �������� ��
pad_height = 512 # �������� ����
background_width = 1024
aircraft_width = 90
aircraft_height = 55

enemy_width = 110
enemy_height = 80

fireball1_width = 140
fireball1_height = 60
fireball2_width = 86
fireball2_height = 60

def drawLife(count): # ���� ���
    global gamepad

    font = pygame.font.SysFont(None, 40)
    text = font.render('Life : ' + str(count), True, [255, 255, 255])
    gamepad.blit(text, (0,0))

def drawScore(count): # ������ �����ǿ� ��Ÿ��
    global gamepad

    font = pygame.font.SysFont(None, 40)
    text = font.render('Score : ' + str(count), True, [255, 255, 255])
    gamepad.blit(text, (150,0))

def gameOver(): # ������ ������ ���
    global gamepad
    pygame.mixer.music.pause()
    dispMessage('Game Over ! ')

def textObj(text, font): 
    textSurface = font.render(text, True, [255, 0, 0])
    return textSurface, textSurface.get_rect()

def dispMessage(text):
    global gamepad

    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((pad_width/2), (pad_height/2))
    gamepad.blit(TextSurf, TextRect)
    pygame.display.update()
    sleep(3)
    pygame.mixer.music.unpause()
    runGame()

def crash(): # ���� �ε��� ���
    global gamepad, explosion_sound
    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(explosion_sound)
    dispMessage('Game Over !')

def drawObject(obj, x, y): # �����ǿ� �׷����� ��ü 
    global gamepad
    gamepad.blit(obj, (x, y))

def back(background, x, y): # ��� �̹����� ������ ���� �׷��ִ� �Լ�
    global gamepad
    gamepad.blit(background, (x,y)) # x, y �� ���� ���� 0 �� �Ǿ�� �����ǿ� ��ƴ���� ä����


def airplane(x, y): # ������ ����⸦ ������ �� x, y ��ġ�� �׸�
    global gamepad, aircraft
    gamepad.blit(aircraft, (x,y))

def runGame(): # ���� ������ �����Ǵ� �Լ�
    global gamepad, aircraft ,clock, background1, background2 # �������� ����
    global enemy, fires, bullet, boom
    global shot_sound

    isShotEnemy = False # �Ѿ��� ���㸦 �����ߴ��� ���ߴ��� �Ǵ��ϱ� ���ؼ�
    boom_count = 0 # ���� �̹����� ȭ�鿡 ǥ�õǴ� �ð��� ���� ����

    enemy_passed = 3
    enemy_hit = 0

    bullet_xy = [] # ����Ʈ �ڷῡ ���� ��Ʈ�� Ű�� ���������� �Ѿ��� ��ǥ �߰�

    # ������ ����⸦ ������ �� �ش� ��ġ�� �׸�
    x = pad_width * 0.05
    y = pad_height * 0.8
    y_change = 0

    background1_x = 0 # ��� �̹����� �»�� �𼭸��� x ��ǥ, ���� ������ 0 ����
    background2_x = background_width # ��� �̹��� ���纻�� ��� �̹��� ���� �ٷ� ������ ��ġ��Ű���� ��ǥ ����

    # ���� ���ƿ� ��ġ ����, ���� x ��ǥ�� �������� �� ������ ��, y ��ǥ�� ������
    enemy_x = pad_width
    enemy_y = random.randrange(0, pad_height)

    # �ҵ��̰� ���ƿ� ��ġ ����
    fire_x = pad_width
    fire_y = random.randrange(0, pad_height)
    random.shuffle(fires) # fires �� �������� ���� �� ù��° ��Ҹ� ���� (�ҵ���, None �߿� ���õ�)
    fire = fires[0]
    
    crashed = False 
    while not crashed:
        for event in pygame.event.get():  # �����ǿ��� �߻��ϴ� �پ��� �̺�Ʈ ����
            if event.type == pygame.QUIT: # event Ÿ���� ���콺�� â�� �ݴ� ���̸� 
                crashed = True # crashed �� ���� True �� �����Ͽ� while �� ����

            # ���̸Ӱ� Ű������ �� ȭ��ǥ Ű�� �Ʒ� ȭ��ǥ Ű�� ������ ����Ⱑ �� �Ʒ��� 5 �ȼ��� �̵�
            # Ű�� ������ ��ȭ�� ����
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5

                # ���� ��Ʈ�� Ű�� ������ ���� ��ġ�� ����⿡�� �Ѿ��� �������� ��ǥ ����
                elif event.key == pygame.K_LCTRL:
                    pygame.mixer.Sound.play(shot_sound)
                    bullet_x = x + aircraft_width
                    bullet_y = y + aircraft_height/2
                    bullet_xy.append([bullet_x, bullet_y]) # bullet_xy ����Ʈ�� �߰�
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

      
        gamepad.fill(WHITE) # �׸����� ������� ä��

        # ��� �̹����� ��� �̹��� ���纻�� �������� 2�ȼ� ��ŭ �̵���Ŵ
        background1_x -= 2
        background2_x -= 2

        
        # ��� �̹����� �����ǿ��� ������ ������� �� ��ġ�� ��� �̹��� ���纻 ���������� ��ġ
        if background1_x == -background_width:
            background1_x = background_width
        # ��� �̹��� ���纻�� �����ǿ��� ������ ������� ��� �̹��� ���������� �ٽ� ��ġ
        if background2_x == -background_width:
            background2_x = background_width

        drawObject(background1, background1_x, 0)
        drawObject(background2, background2_x, 0)

        drawLife(enemy_passed)
        drawScore(enemy_hit)

        if enemy_passed == 0:
            gameOver()

        y += y_change # Ű���� �Է¿� ���� ������� y ��ǥ ����
        if y < 0:
            y = 0
        elif y > pad_height - aircraft_height: # ������� y ��ǥ�� ������ ���� ����
            y = pad_height - aircraft_height

        enemy_x -= 7  # ���� ����������� 7 �ȼ��� ���ƿ�����
        if enemy_x <= 0: # ���� ������ ���� ���ƿ� �� ��ġ �缳��
            enemy_passed -= 1
            enemy_x = pad_width
            enemy_y = random.randrange(0, pad_height)

        if fire == None: # fire �� none �� ��� 30 �ȼ��� �ٰ��� ( �ƹ��� ���ع��� ���� ��)
            fire_x -= 30 # �ð� ������ ����
        else:
            fire_x -= 15 # �Ѿ��� ������� ��� 15 �ȼ��� ���ƿ�

        if fire_x <= 0:
            fire_x = pad_width
            fire_y = random.randrange(0, pad_height)
            random.shuffle(fires)
            fire = fires[0]

        # ����Ʈ �ڷ� bullet_xy �� ��ǥ�� ��� ������ �ϳ��� ������ ��ǥ ����
        # �Ѿ��� �ӵ��� 15 �ȼ�
        # �Ѿ��� �������� �������� ����Ʈ���� �ش� ��ǥ ����
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[0] += 15
                bullet_xy[i][0] = bxy[0]
                if bxy[0] > enemy_x:
                    if bxy[1] > enemy_y and bxy[1] < enemy_y + enemy_height:
                        bullet_xy.remove(bxy)
                        isShotEnemy = True

                if bxy[0] >= pad_width:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass
        if x + aircraft_width > enemy_x:
            if (y > enemy_y and y < enemy_height) or \
               (y + aircraft_height > enemy_y and y + aircraft_height < enemy_y + enemy_height):
                crash()

        if fire[1] != None:
            if fire[0] == 0:
                fireball_width = fireball1_width
                fireball_height = fireball1_height
            elif fire[0] == 1:
                fireball_width = fireball2_width
                fireball_height = fireball2_height

            if x + aircraft_width > fire_x:
                if (y > fire_y and y < fire_y + fireball_height) or \
                   (y + aircraft_height > fire_y and y + aircraft_height < fire_y+fireball_height):
                    crash()

        drawObject(aircraft, x, y)
        drawObject(enemy, enemy_x, enemy_y)

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        if not isShotEnemy: # �Ѿ��� ���㿡 �������� �ʾҴٸ�
            drawObject(enemy, enemy_x, enemy_y) # ���㸦 ��� ȭ�鿡 �׸�
        else:
            drawObject(boom, enemy_x-35, enemy_y-20) # ���� ��ġ�� ���� �̹����� �׸�
            boom_count += 1 
            if boom_count > 10: # while ���� 10 �� ���������� ȭ�鿡 ǥ��
                boom_count = 0
                enemy_hit += 10
                enemy_x = pad_width
                enemy_y = random.randrange(0, pad_height-enemy_height) # ���ο� ���� ����
                isShotEnemy = False

        if fire[1] != None:
            drawObject(fire[1], fire_x, fire_y)

        pygame.display.update() # ������ ����
        clock.tick(100) # FPS ���� 60���� �����Ͽ� while �� �ݺ� 

    pygame.quit() # �ʱ�ȭ�� pygame ����
    quit()


def initGame():
    global gamepad, clock, aircraft, background1, background2
    global enemy, fires, bullet, boom
    global shot_sound, explosion_sound
    
    fires = [] # �Ѿ� 2���� None ��ü 5���� ���� ����Ʈ

    pygame.init() # pygame ���̺귯�� �ʱ�ȭ
    gamepad = pygame.display.set_mode((pad_width, pad_height)) # �������� ũ�⸦ ����
    pygame.display.set_caption('SHOOTING GAME') # ������ Ÿ��Ʋ

    # �̹��� ������ �о� ���������� �Ҵ�
    aircraft = pygame.image.load('images/airplane.png')

    background1 = pygame.image.load('images/background.png')
    background2 = background1.copy()

    enemy = pygame.image.load('images/enemy.png')

    fires.append((0, pygame.image.load('images/bullet1.png')))
    fires.append((1, pygame.image.load('images/bullet2.png')))
    
    boom = pygame.image.load('images/boom.gif').convert_alpha()

    for i in range(3):
        fires.append((i+2, None))

    bullet = pygame.image.load('images/bullet.png')

    shot_sound = pygame.mixer.Sound('images/shot.wav')
    explosion_sound = pygame.mixer.Sound('images/explosion.wav')

    pygame.mixer.music.load('images/mybgm.wav')
    pygame.mixer.music.play(-1)
    
    clock = pygame.time.Clock() # ������ �ʴ� ������ ���� (60) 
    runGame()

initGame() # ������ �ʱ�ȭ�ϰ� �����ϴ� �Լ�
    
