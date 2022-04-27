import random

import pygame
import os
from characters import common
##########################################################
# 초기화 (반드시 필요)
pygame.init()

# 화면 크기 설정
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption('sparta fighter')

# FPS
clock = pygame.time.Clock()

##########################################################

# 1. 사용자 게임 초기화 (배경화면, 게임이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)    # 현재 파일 위치 반환
images_path = os.path.join(current_path, 'images')

# 배경
background = pygame.image.load(os.path.join(images_path, 'background.png'))

# 스테이지
stage = pygame.image.load(os.path.join(images_path, 'stage.png'))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# 체력바
hp_bar = pygame.image.load(os.path.join(images_path, 'hp_bar.png'))
hp_point = pygame.image.load(os.path.join(images_path, 'hp_point.png'))
hp_point_red = pygame.image.load(os.path.join(images_path, 'hp_point_red.png'))

# 궁극기 게이지
energy_bar = pygame.image.load(os.path.join(images_path, 'energy_bar.png'))
energy_point = pygame.image.load(os.path.join(images_path, 'energy_point.png'))
energy_point_red = pygame.image.load(os.path.join(images_path, 'energy_point_red.png'))

# 폰트
game_font = pygame.font.Font(None, 100)
total_time = 60
start_ticks = pygame.time.get_ticks()

# 사용자 캐릭터
a = common.Fighter(images_path, 'character.png')
a.name = '1p'
a.x_pos = screen_width / 3 - a.width / 2            # 현재 x좌표
a.y_pos = screen_height - a.height - stage_height   # 현재 y좌표

# 적 캐릭터
b = common.Fighter(images_path, 'character.png')
b.name = '2p'
b.x_pos = screen_width * 2 / 3 - b.width / 2        # 현재 x좌표
b.y_pos = screen_height - b.height - stage_height   # 현재 y좌표
b.position = 1
b.vector = -100

# 적 캐릭터의 랜덤 행동 부분
rnd_ticks = 0
rnd_delay = 3
rnd_bool = True

game_result = 'Quit'

# 현재 눌린 키
key_down_font = pygame.font.Font(None, 50)
current_key_down = ''

# 이벤트 루프
running = True   # 게임 진행 변수
while running:
    dt = clock.tick(120) # 초당 프레임수

    # 2. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 종료 이벤트
            running = False
        if event.type == pygame.KEYDOWN:        # 버튼이 눌렸을 때
            if not a.hit_bool:
                if event.key == pygame.K_LEFT:      # <- 방향키일 때
                    a.to_x -= a.x_speed * dt
                    a.vector = -100
                    current_key_down = 'LEFT'
                elif event.key == pygame.K_RIGHT:   # -> 방향키일 때
                    a.to_x += a.x_speed * dt
                    a.vector = 100
                    current_key_down = 'RIGHT'
                elif event.key == pygame.K_UP:  # up 방향키일 때
                    if a.y_pos == screen_height - stage_height - a.height:
                        a.to_y += a.y_speed * dt
                        a.jump_bool = True
                    current_key_down = 'UP'
                elif event.key == pygame.K_z:   # z 키가 눌리면 상단 공격
                    a.attack_temp = 1
                    current_key_down = 'Z'
                elif event.key == pygame.K_x:   # x 키가 눌리면 중단 공격
                    a.attack_temp = 2
                    current_key_down = 'X'
                elif event.key == pygame.K_c:   # c 키가 눌리면 하단 공격
                    a.attack_temp = 3
                    current_key_down = 'C'
                elif event.key == pygame.K_v:  # c 키가 눌리면 하단 수비
                    if a.energy == 100:
                        a.attack_temp = 4
                    current_key_down = 'V'
                elif event.key == pygame.K_a:  # a 키가 눌리면 상단 수비
                    a.defend_mode = 1
                    current_key_down = 'A'
                elif event.key == pygame.K_s:  # b 키가 눌리면 중단 수비
                    a.defend_mode = 2
                    current_key_down = 'S'
                elif event.key == pygame.K_d:  # c 키가 눌리면 하단 수비
                    a.defend_mode = 3
                    current_key_down = 'D'

    if event.type == pygame.KEYUP:          # 버튼을 뗐을 때
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                a.to_x = 0
            elif event.key == pygame.K_z or event.key == pygame.K_x \
                    or event.key == pygame.K_c or event.key == pygame.K_v:
                a.attack_temp = 0
            elif event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                a.defend_mode = 0
            current_key_down = ''

# 3. 게임 캐릭터 위치 정의
    a.move_char(screen_height, screen_width, stage_height, dt)
    b.move_char(screen_height, screen_width, stage_height, dt)

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(stage, (0, screen_height - stage_height))

    # 랜덤 행동
    rnd1 = random.randint(1, 1)
    rnd2 = random.randint(1, 3)
    if rnd_bool and not b.hit_bool:    # 공격 / 수비가 가능하면
        rnd_ticks = pygame.time.get_ticks()
        rnd_bool = False
        if rnd1 == 1:      # rnd1, rnd2에 따라 공격 또는 수비
            b.attack_temp = rnd2
        else:
            b.defend_mode = rnd2
    elif (pygame.time.get_ticks() - rnd_ticks) / 1000 > rnd_delay:
        print(a.energy, b.energy)
        b.defend_mode = 0
        rnd_bool = True
    else:
        b.attack_temp = 0

    b.draw_char(screen, a)
    a.draw_char(screen, b)

    # 체력바 그리기
    screen.blit(hp_bar, (50, 50))
    screen.blit(hp_bar, (550, 50))
    if a.hp > 0:
        a_hp_width = a.hp / 100 * 400
        a_hp_x_pos = 450 - a_hp_width
        while a_hp_width > 0:
            a_hp_width -= 20
            if a.hp > 30:
                screen.blit(hp_point, (a_hp_x_pos, 50))
            else:
                screen.blit(hp_point_red, (a_hp_x_pos, 50))
            a_hp_x_pos += 20
    if b.hp > 0:
        b_hp_width = b.hp / 100 * 400
        b_hp_x_pos = 550
        while b_hp_width > 0:
            b_hp_width -= 20
            if b.hp > 30:
                screen.blit(hp_point, (b_hp_x_pos, 50))
            else:
                screen.blit(hp_point_red, (b_hp_x_pos, 50))
            b_hp_x_pos += 20

    # 궁극기 게이지 그리기
    screen.blit(energy_bar, (50, 125))
    screen.blit(energy_bar, (850, 125))

    a_energy_width = a.energy
    a_energy_x_pos = 50 + a_hp_width
    while a_energy_width > 0:
        a_energy_width -= 5
        if a.energy != 100:
            screen.blit(energy_point, (a_energy_x_pos, 125))
        else:
            screen.blit(energy_point_red, (a_energy_x_pos, 125))
        a_energy_x_pos += 5
    b_energy_width = b.energy
    b_energy_x_pos = 850 + 100 - b_energy_width
    while b_energy_width > 0:
        b_energy_width -= 5
        if b.energy != 100:
            screen.blit(energy_point, (b_energy_x_pos, 125))
        else:
            screen.blit(energy_point_red, (b_energy_x_pos, 125))
        b_energy_x_pos += 5

    # 눌린 키 출력
    msg = key_down_font.render(current_key_down, True, (0, 0, 0))
    msg_rect = msg.get_rect(center=(50, int(screen_height - 20)))
    screen.blit(msg, msg_rect)


    # 생사여부 판단 후 게임 종료
    if not a.status_check() or not b.status_check():
        if a.status_check():
            winner = a.name
            loser = b.name
        else:
            winner = b.name
            loser = a.name
        game_result = f'Winner : {winner}'
        running = False

    # 타이머
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    current_time = int(total_time - elapsed_time)
    if current_time < 10:
        time_text = '0' + str(current_time)
        timer = game_font.render(time_text, True, (255, 0, 0))
    else:
        time_text = str(current_time)
        timer = game_font.render(time_text, True, (0, 0, 0))
    screen.blit(timer, (460, 45))

    # 타임 아웃 시 체력이 더 많은 캐릭터가 승리, 체력이 같으면 무승부
    if total_time - elapsed_time <= 0:
        if a.hp > b.hp:
            winner = a.name
        elif b.hp > a.hp:
            winner = b.name
        else:
            winner = 0

        if winner == 0:
            game_result = f'Time out - Draw'
        else:
            game_result = f'Time out - Winner {winner}'

        running = False

    pygame.display.update() # 게임 화면 업데이트

# 게임 결과 출력
msg = game_font.render(game_result, True, (255, 255, 255))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 종료시 2초 대기후 종료
pygame.time.delay(2000)

# pygame 종료
pygame.quit()
