import pygame
import os

# 파이터 캐릭터 클래스
class Fighter:
    name = 'empty'
    hp = 100             # 캐릭터 체력
    alive = True         # 살아있는지 여부
    to_x = 0             # x방향 백터
    to_y = 0             # y방향 벡터
    x_speed = 0.4        # x방향 스피드
    y_speed = 0.7        # y방향 스피드
    x_pos = 0            # 캐릭터 x 좌표
    y_pos = 0            # 캐릭터 y 좌표
    vector = 100         # 캐릭터가 바라보는 방향 - -100:왼쪽, 100:오른쪽
    defend_mode = 0      # 수비모드 - 0:수비안함, 1:상단수비, 2:중단수비, 3:하단수비
    attack_mode = 0      # 공격모드 - 0:공격안함, 1:상단공격, 2:중단공격, 3:하단공격
    hit_mode = False     # 피격상태 - False:피격중아님, True: 피격중임
    high_rage = 60       # 상단 범위
    middle_rage = 120    # 중단 범위
    low_rage = 90        # 하단 범위

    jump_bool = False    # 점프 중인지 판단하는 변수

    # 공격시 다음 공격까지 쿨타임
    attack_bool = False  # 쿨타임 중인지 여부
    attack_delay = 1     # 쿨타임 시간
    attack_ticks = 0     # 공격 성공한 시간
    attack_temp = 0      # 공격의 종류를 담는 변수

    # 피격 쿨타임
    hit_delay = 0.5      # 쿨타임 시간
    hit_ticks = 0        # 피격당한 시간


    # pygame 캐릭터 생성
    # images_path : 캐릭터 이지미 경로 / image : 이미지 명
    def __init__(self, images_path, image):
        self.char = pygame.image.load(os.path.join(images_path, image))
        self.hit_img = pygame.image.load(os.path.join(images_path, 'character_hit.png'))
        self.attack_high_img = pygame.image.load(os.path.join(images_path, 'attack_high.png'))
        self.attack_middle_img = pygame.image.load(os.path.join(images_path, 'attack_middle.png'))
        self.attack_low_img = pygame.image.load(os.path.join(images_path, 'attack_low.png'))
        self.defend_high_img = pygame.image.load(os.path.join(images_path, 'defend_high.png'))
        self.defend_middle_img = pygame.image.load(os.path.join(images_path, 'defend_middle.png'))
        self.defend_low_img = pygame.image.load(os.path.join(images_path, 'defend_low.png'))
        self.size = self.char.get_rect().size   # 캐릭터 사이즈
        self.width = self.size[0]               # 캐릭터 너비
        self.height = self.size[1]              # 캐릭터 높이

    # 피격 시 받는 데미지
    # attack : 받는 데미지
    def damage(self, attack):
        self.hp = self.hp - attack
        if self.hp <= 0:
            self.alive = False

    # 살았는지 죽었는지 상태 확인
    def status_check(self):
        if self.alive:
            return True
        else:
            return False

    # 상단/중단/하단 공격
    # attack_type : 공격 종류 - 1:상단, 2:중단, 3:하단
    # enemy : 적의 캐릭터
    def attack(self, attack_type, enemy):
        if self.attack_check(attack_type, enemy):
            if attack_type == 1:
                enemy.get_hit(1)
                print(f'상단 공격 성공! {self.name} hp : {self.hp} / {enemy.name} hp : {enemy.hp}')
            elif attack_type == 2:
                enemy.get_hit(2)
                print(f'중단 공격 성공! {self.name} hp : {self.hp} / {enemy.name} hp : {enemy.hp}')
            else:
                enemy.get_hit(3)
                print(f'하단 공격 성공! {self.name} hp : {self.hp} / {enemy.name} hp : {enemy.hp}')

    # 공격 성공 여부 체크
    # attack_type : 공격 종류 - 1:상단, 2:중단, 3:하단
    # enemy : 적의 캐릭터
    def attack_check(self, attack_type, enemy):
        # 1. 공격 종류에 따른 rect를 만들어서
        if attack_type == 1:
            rect = self.attack_high_img.get_rect()
            rect.left = self.x_pos + self.vector
            rect.top = self.y_pos
        elif attack_type == 2:
            rect = self.attack_middle_img.get_rect()
            rect.left = self.x_pos + self.vector
            rect.top = self.y_pos + self.high_rage
        elif attack_type == 3:
            rect = self.attack_low_img.get_rect()
            rect.left = self.x_pos + self.vector
            rect.top = self.y_pos + self.high_rage + self.middle_rage

        # 2. 적 rect와
        enemy_rect = enemy.char.get_rect()
        enemy_rect.left = enemy.x_pos
        enemy_rect.top = enemy.y_pos

        # 3. 서로 충돌하는지 확인
        if rect.colliderect(enemy_rect):
            if enemy.defend_mode == 0:
                return True
            # 4. 적이 수비 중이 었다면
            else:
                if enemy.defend_mode == 1:
                    defend_y_0 = enemy.y_pos
                    defend_y_1 = enemy.y_pos + enemy.high_rage
                elif enemy.defend_mode == 2:
                    defend_y_0 = enemy.y_pos + enemy.high_rage
                    defend_y_1 = enemy.y_pos + enemy.high_rage + enemy.middle_rage
                elif enemy.defend_mode == 3:
                    defend_y_0 = enemy.y_pos + enemy.high_rage + enemy.middle_rage
                    defend_y_1 = enemy.y_pos + enemy.high_rage + enemy.middle_rage + enemy.low_rage


                # 5. 수비 성공 여부 체크
                if rect.top >= defend_y_0 and rect.top + rect.height <= defend_y_1:
                    print('수비 성공')
                    return False
            return True

    # 피격 판정
    # hit_type : 받은 공격의 종류 - 1:상단, 2:중단, 3:하단
    def get_hit(self, hit_type):
        if hit_type == 1:
            self.damage(15)
        elif hit_type == 2:
            self.damage(5)
        else:
            self.damage(10)
        self.hit_ticks = pygame.time.get_ticks()
        self.hit_mode = True


    # 캐릭터 그리기
    # screen        : 화면
    # enemy         : 적의 캐릭터
    # attack_bool   : 쿨타임 중인지 여부
    # attack_delay  : 쿨타임 시간
    # attack_ticks  : 공격 성공한 시간
    # attack_temp   : 공격의 종류를 담는 변수
    def draw_char(self, screen, enemy):
        if self.hit_mode:
            # 피격 상태이면 다른 행동 못함
            screen.blit(self.hit_img, (self.x_pos, self.y_pos))
            hit_time = (pygame.time.get_ticks() - self.hit_ticks) / 1000
            if hit_time > self.hit_delay:
                self.hit_mode = False
                self.hit_ticks = 0
        else:
            screen.blit(self.char, (self.x_pos, self.y_pos))

            # 공격 그리기
            # 수비 중이 아닐 때만 가능
            #             # 현재 시간 - 공격 성공한 시간 > 쿨타임 시간 : 공격 다시 가능
            if self.defend_mode == 0:
                cool_time = (pygame.time.get_ticks() - self.attack_ticks) / 1000
                if cool_time > self.attack_delay:
                    self.attack_bool = False
                    self.attack_mode = 0
                else:
                    if self.attack_mode == 1:
                        screen.blit(self.attack_high_img, (self.x_pos + self.vector, self.y_pos))
                    elif self.attack_mode == 2:
                        screen.blit(self.attack_middle_img, (self.x_pos + self.vector, self.y_pos + self.high_rage))
                    elif self.attack_mode == 3:
                        screen.blit(self.attack_low_img, (self.x_pos + self.vector, self.y_pos + self.high_rage + self.middle_rage))
    
                if not self.attack_bool:
                    if self.attack_temp == 1:
                        screen.blit(self.attack_high_img, (self.x_pos + self.vector, self.y_pos))
                        self.attack(self.attack_temp, enemy)
                        self.attack_bool = True
                        self.attack_ticks = pygame.time.get_ticks()
                        self.attack_mode = 1
                    elif self.attack_temp == 2:
                        screen.blit(self.attack_middle_img, (self.x_pos + self.vector, self.y_pos + self.high_rage))
                        self.attack(self.attack_temp, enemy)
                        self.attack_bool = True
                        self.attack_ticks = pygame.time.get_ticks()
                        self.attack_mode = 2
                    elif self.attack_temp == 3:
                        screen.blit(self.attack_low_img, (self.x_pos + self.vector, self.y_pos + self.high_rage + self.middle_rage))
                        self.attack(self.attack_temp, enemy)
                        self.attack_bool = True
                        self.attack_ticks = pygame.time.get_ticks()
                        self.attack_mode = 3
    
            # 수비 그리기
            # 공격 중이 아닐 때, 점프 중이 아닐 때만 가능
            if self.attack_mode == 0:
                if self.defend_mode == 1:
                    screen.blit(self.defend_high_img, (self.x_pos, self.y_pos))
                elif self.defend_mode == 2:
                    screen.blit(self.defend_middle_img, (self.x_pos, self.y_pos + self.high_rage))
                elif self.defend_mode == 3:
                    screen.blit(self.defend_low_img, (self.x_pos, self.y_pos + self.high_rage + self.middle_rage))

    # 캐릭터 이동
    # screen_height : 화면 높이
    # screen_width : 화면 너비
    # stage_height : 스테이지 높이
    # dt : 이동 프레임 수
    def move_char(self, screen_height, screen_width, stage_height, dt):
        # 수비 중이 아닐 때만 이동 가능
        if self.jump_bool and self.defend_mode == 0:
            self.to_y = -12
            self.jump_bool = False
        elif self.y_pos < screen_height - stage_height - self.height:
            self.to_y += 0.02 * dt
        else:
            self.y_pos = screen_height - stage_height - self.height
            self.to_y = 0
        self.y_pos += self.to_y

        if self.defend_mode == 0:
            self.x_pos += self.to_x
            if self.x_pos < 0:  # 벽에 막힐 경우
                self.x_pos = 0
            elif self.x_pos > screen_width - self.width:
                self.x_pos = screen_width - self.width
