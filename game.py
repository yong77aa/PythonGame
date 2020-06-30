import pygame # pygame 라이브러리를 import
import random
from time import sleep

WHITE = (255, 255, 255) # 흰색을 표현하는 값
pad_width = 1024 # 게임판의 폭
pad_height = 512 # 게임판의 높이
background_width = 1024
aircraft_width = 90
aircraft_height = 55

enemy_width = 110
enemy_height = 80

fireball1_width = 140
fireball1_height = 60
fireball2_width = 86
fireball2_height = 60

def drawLife(count): # 남은 목숨
    global gamepad

    font = pygame.font.SysFont(None, 40)
    text = font.render('Life : ' + str(count), True, [255, 255, 255])
    gamepad.blit(text, (0,0))

def drawScore(count): # 점수를 게임판에 나타냄
    global gamepad

    font = pygame.font.SysFont(None, 40)
    text = font.render('Score : ' + str(count), True, [255, 255, 255])
    gamepad.blit(text, (150,0))

def gameOver(): # 게임이 오버된 경우
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

def crash(): # 적과 부딪힌 경우
    global gamepad, explosion_sound
    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(explosion_sound)
    dispMessage('Game Over !')

def drawObject(obj, x, y): # 게임판에 그려지는 객체 
    global gamepad
    gamepad.blit(obj, (x, y))

def back(background, x, y): # 배경 이미지를 게임판 위에 그려주는 함수
    global gamepad
    gamepad.blit(background, (x,y)) # x, y 의 값이 각각 0 이 되어야 게임판에 빈틈없이 채워짐


def airplane(x, y): # 조정할 비행기를 게임판 위 x, y 위치에 그림
    global gamepad, aircraft
    gamepad.blit(aircraft, (x,y))

def runGame(): # 실제 게임이 구동되는 함수
    global gamepad, aircraft ,clock, background1, background2 # 전역변수 선언
    global enemy, fires, bullet, boom
    global shot_sound

    isShotEnemy = False # 총알이 박쥐를 명중했는지 안했는지 판단하기 위해서
    boom_count = 0 # 폭발 이미지가 화면에 표시되는 시간을 위한 변수

    enemy_passed = 3
    enemy_hit = 0

    bullet_xy = [] # 리스트 자료에 왼쪽 컨트롤 키를 누를때마다 총알의 좌표 추가

    # 조정할 비행기를 게임판 위 해당 위치에 그림
    x = pad_width * 0.05
    y = pad_height * 0.8
    y_change = 0

    background1_x = 0 # 배경 이미지의 좌상단 모서리의 x 좌표, 최초 값으로 0 지정
    background2_x = background_width # 배경 이미지 복사본을 배경 이미지 원본 바로 다음에 위치시키도록 좌표 지정

    # 적이 날아올 위치 설정, 적의 x 좌표는 게임판의 맨 오른쪽 끝, y 좌표는 무작위
    enemy_x = pad_width
    enemy_y = random.randrange(0, pad_height)

    # 불덩이가 날아올 위치 설정
    fire_x = pad_width
    fire_y = random.randrange(0, pad_height)
    random.shuffle(fires) # fires 를 무작위로 섞은 후 첫번째 요소를 선택 (불덩이, None 중에 선택됨)
    fire = fires[0]
    
    crashed = False 
    while not crashed:
        for event in pygame.event.get():  # 게임판에서 발생하는 다양한 이벤트 리턴
            if event.type == pygame.QUIT: # event 타입이 마우스로 창을 닫는 것이면 
                crashed = True # crashed 의 값을 True 로 설정하여 while 문 종료

            # 게이머가 키보드의 위 화살표 키와 아래 화살표 키를 누르면 비행기가 위 아래로 5 픽셀씩 이동
            # 키를 놓으면 변화가 없음
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5

                # 왼쪽 컨트롤 키를 누르면 현재 위치의 비행기에서 총알이 나가도록 좌표 설정
                elif event.key == pygame.K_LCTRL:
                    pygame.mixer.Sound.play(shot_sound)
                    bullet_x = x + aircraft_width
                    bullet_y = y + aircraft_height/2
                    bullet_xy.append([bullet_x, bullet_y]) # bullet_xy 리스트에 추가
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

      
        gamepad.fill(WHITE) # 그림판을 흰색으로 채움

        # 배경 이미지와 배경 이미지 복사본을 왼쪽으로 2픽셀 만큼 이동시킴
        background1_x -= 2
        background2_x -= 2

        
        # 배경 이미지가 게임판에서 완전히 사라지면 그 위치를 배경 이미지 복사본 오른쪽으로 위치
        if background1_x == -background_width:
            background1_x = background_width
        # 배경 이미지 복사본이 게임판에서 완전히 사라지면 배경 이미지 오른쪽으로 다시 위치
        if background2_x == -background_width:
            background2_x = background_width

        drawObject(background1, background1_x, 0)
        drawObject(background2, background2_x, 0)

        drawLife(enemy_passed)
        drawScore(enemy_hit)

        if enemy_passed == 0:
            gameOver()

        y += y_change # 키보드 입력에 따라 비행기의 y 좌표 변경
        if y < 0:
            y = 0
        elif y > pad_height - aircraft_height: # 비행기의 y 좌표르 게임판 내로 제한
            y = pad_height - aircraft_height

        enemy_x -= 7  # 적이 비행기쪽으로 7 픽셀씩 날아오게함
        if enemy_x <= 0: # 왼쪽 끝까지 가면 날아올 적 위치 재설정
            enemy_passed -= 1
            enemy_x = pad_width
            enemy_y = random.randrange(0, pad_height)

        if fire == None: # fire 이 none 인 경우 30 픽셀씩 다가옴 ( 아무런 방해물이 없는 것)
            fire_x -= 30 # 시간 지연을 위해
        else:
            fire_x -= 15 # 총알이 날라오는 경우 15 픽셀씩 날아옴

        if fire_x <= 0:
            fire_x = pad_width
            fire_y = random.randrange(0, pad_height)
            random.shuffle(fires)
            fire = fires[0]

        # 리스트 자료 bullet_xy 에 좌표가 들어 있으면 하나씩 추출해 좌표 갱신
        # 총알의 속도는 15 픽셀
        # 총알이 게임판을 지나가면 리스트에서 해당 좌표 삭제
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

        if not isShotEnemy: # 총알이 박쥐에 명중하지 않았다면
            drawObject(enemy, enemy_x, enemy_y) # 박쥐를 계속 화면에 그림
        else:
            drawObject(boom, enemy_x-35, enemy_y-20) # 박쥐 위치에 폭발 이미지를 그림
            boom_count += 1 
            if boom_count > 10: # while 문을 10 번 돌릴때까지 화면에 표시
                boom_count = 0
                enemy_hit += 10
                enemy_x = pad_width
                enemy_y = random.randrange(0, pad_height-enemy_height) # 새로운 박쥐 등장
                isShotEnemy = False

        if fire[1] != None:
            drawObject(fire[1], fire_x, fire_y)

        pygame.display.update() # 게임판 생성
        clock.tick(100) # FPS 값을 60으로 설정하여 while 문 반복 

    pygame.quit() # 초기화한 pygame 종료
    quit()


def initGame():
    global gamepad, clock, aircraft, background1, background2
    global enemy, fires, bullet, boom
    global shot_sound, explosion_sound
    
    fires = [] # 총알 2개와 None 객체 5개를 담을 리스트

    pygame.init() # pygame 라이브러리 초기화
    gamepad = pygame.display.set_mode((pad_width, pad_height)) # 게임판의 크기를 설정
    pygame.display.set_caption('SHOOTING GAME') # 게임판 타이틀

    # 이미지 파일을 읽어 전역변수에 할당
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
    
    clock = pygame.time.Clock() # 게임의 초당 프레임 설정 (60) 
    runGame()

initGame() # 게임을 초기화하고 시작하는 함수
    
