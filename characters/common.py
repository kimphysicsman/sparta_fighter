import random

import pygame
import os


# 파이터 캐릭터 클래스
class Fighter:
    name = 'empty'
    hp = 100  # 캐릭터 체력
    alive = True  # 살아있는지 여부
    to_x = 0  # x방향 백터
    to_y = 0  # y방향 벡터
    x_speed = 0.4  # x방향 스피드
    y_speed = 0.7  # y방향 스피드
    x_pos = 0  # 캐릭터 x 좌표
    y_pos = 0  # 캐릭터 y 좌표
    vector = 100  # 캐릭터가 바라보는 방향 - -100:왼쪽, 100:오른쪽
    defend_mode = 0  # 수비모드 - 0:수비안함, 1:상단수비, 2:중단수비, 3:하단수비
    attack_mode = 0  # 공격모드 - 0:공격안함, 1:상단공격, 2:중단공격, 3:하단공격
    high_rage = 60  # 상단 범위
    middle_rage = 120  # 중단 범위
    low_rage = 90  # 하단 범위
    damages = [0, 15, 5, 10]  # 0, 상단, 중단, 하단 공격 데미지
    critical_p = 4  # 크리티컬 확률 = 1/critical_p
    critical_d = 2  # 크리티컬 데미지 (2배)

    # 공격 모션
    attack_delay = 0.5  # 모션 시간
    attack_ticks = 0  # 공격 성공한 시간
    attack_temp = 0  # 공격의 종류를 담는 변수
    ready_delay = 0.7  # 공격 전 준비동작 시간

    # 피격 모션
    hit_delay = 0.7  # 피격 당하는 시간
    hit_ticks = 0  # 피격 당한 시간
    hit_type = 0  # 피격 종류 - 0:피격아님, 1:상단피격, 2:중단피격, 3:하단피격
    critical_hit = False  # 크리티컬 피격 여부 - True:크리티컬발생, False:크리티컬발생안함
    effect_delay = 0.5  # 공격 / 수비 이펙트 지속 시간
    effect_bool = False  # 수비 이펙트 여부 - True:이펙트나오는중, False:이펙트안나오는중
    effect_ticks = 0  # 수비 이펙트 시작 시간

    attack_bool = False  # 공격 중 인지 여부 - True:공격중, False:공격중아님
    ready_bool = False  # 공격 전 준비동작 중인지 여부 - True:공격준비중, False:준비중아님
    jump_bool = False  # 점프 중인지 판단하는 변수 - True:점프중, False:점프중아님
    hit_bool = False  # 피격 상태 여부 - True:피격중, False:피격중아님

    position = -1   # 캐릭터의 적과의 상대적 위치 - -1:왼쪽, 1:오른쪽

    # statuses = ('none', 'ready', 'attack', 'hit', 'jump')

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
        self.attack_high_ready = pygame.image.load(os.path.join(images_path, 'attack_high_ready.png'))
        self.attack_middle_ready = pygame.image.load(os.path.join(images_path, 'attack_middle_ready.png'))
        self.attack_low_ready = pygame.image.load(os.path.join(images_path, 'attack_low_ready.png'))
        self.attack_effect = pygame.image.load(os.path.join(images_path, 'attack_effect.png'))
        self.font = pygame.font.Font(None, 30)  # 효과 폰트
        self.defend_effect = self.font.render('defend!!', True, (0, 0, 0))  # 수비 성공시 이펙트 메시지
        self.critical_effect = self.font.render('critical!!', True, (0, 0, 0))  # 크리티컬시 이펙트 메시지
        self.size = self.char.get_rect().size  # 캐릭터 사이즈
        self.width = self.size[0]  # 캐릭터 너비
        self.height = self.size[1]  # 캐릭터 높이

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
            critical = False  # 크리티컬 발생 유무
            p = random.randint(1, self.critical_p)
            if p == 1:
                critical = True
            if critical:
                damage = self.critical_d * self.damages[attack_type]
            else:
                damage = self.damages[attack_type]

            enemy.get_hit(attack_type, critical, damage)

    # 공격 성공 여부 체크
    # attack_type : 공격 종류 - 1:상단, 2:중단, 3:하단
    # enemy : 적의 캐릭터
    def attack_check(self, attack_type, enemy):
        if attack_type != 0:
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
                        enemy.effect_bool = True
                        enemy.effect_ticks = pygame.time.get_ticks()
                        return False
                    return True
            else:
                return False
        else:
            return False

    # 피격 판정
    # hit_type : 받은 공격의 종류 - 1:상단, 2:중단, 3:하단
    def get_hit(self, hit_type, critical, damage):
        if not self.hit_bool:
            self.damage(damage)
            self.hit_ticks = pygame.time.get_ticks()
            self.hit_bool = True
            self.hit_type = hit_type
            self.attack_bool = False
            self.attack_mode = 0
            self.ready_bool = 0
            self.jump_bool = 0
            self.critical_hit = critical

    # 캐릭터 그리기
    # screen        : 화면
    # enemy         : 적의 캐릭터
    # attack_bool   : 공격 모션 중인지 여부
    # attack_delay  : 공격 모션 시간
    # attack_ticks  : 공격 성공한 시간
    # attack_temp   : 공격의 종류를 담는 변수
    def draw_char(self, screen, enemy):
        if self.hit_bool:
            # 피격 상태이면 다른 행동 못함
            screen.blit(self.hit_img, (self.x_pos, self.y_pos))
            hit_time = (pygame.time.get_ticks() - self.hit_ticks) / 1000
            if hit_time < self.effect_delay:
                if self.hit_type == 1:
                    screen.blit(self.attack_effect, (self.x_pos + 50 * -1 * self.position, self.y_pos - 50))
                    if self.critical_hit:
                        screen.blit(self.critical_effect, (self.x_pos + 50 * -1 * self.position, self.y_pos - 50))
                elif self.hit_type == 2:
                    screen.blit(self.attack_effect,
                                (self.x_pos + 50 * -1 * self.position, self.y_pos - 50 + self.high_rage))
                    if self.critical_hit:
                        screen.blit(self.critical_effect,
                                    (self.x_pos + 50 * -1 * self.position, self.y_pos - 50 + self.high_rage))
                elif self.hit_type == 3:
                    screen.blit(self.attack_effect, (
                    self.x_pos + 50 * -1 * self.position, self.y_pos - 50 + self.high_rage + self.middle_rage))
                    if self.critical_hit:
                        screen.blit(self.critical_effect, (
                        self.x_pos + 50 * -1 * self.position, self.y_pos - 50 + self.high_rage + self.middle_rage))
            if hit_time > self.hit_delay:
                self.hit_bool = False
                self.hit_ticks = 0
                self.critical_hit = False
        else:
            screen.blit(self.char, (self.x_pos, self.y_pos))

            # 공격 그리기
            # 수비 중이 아닐 때만 가능
            if self.defend_mode == 0:
                # 공격 준비 중인지 확인
                if self.ready_bool:
                    # 공격 후 흐른 시간
                    ready_time = (pygame.time.get_ticks() - self.attack_ticks) / 1000
                    if ready_time > self.ready_delay:
                        self.ready_bool = False
                        self.attack_bool = True
                    else:
                        if self.attack_mode == 1:
                            screen.blit(self.attack_high_ready, (self.x_pos, self.y_pos))
                        elif self.attack_mode == 2:
                            screen.blit(self.attack_middle_ready, (self.x_pos, self.y_pos + self.high_rage))
                        elif self.attack_mode == 3:
                            screen.blit(self.attack_low_ready,
                                        (self.x_pos, self.y_pos + self.high_rage + self.middle_rage))

                # 공격 모션 중인지 확인
                if self.attack_bool:
                    attack_time = (pygame.time.get_ticks() - self.attack_ticks) / 1000 - self.ready_delay
                    if attack_time > self.attack_delay:
                        self.attack_mode = 0
                        self.attack_bool = False
                    else:
                        self.attack(self.attack_mode, enemy)
                        if self.attack_mode == 1:
                            screen.blit(self.attack_high_img, (self.x_pos + self.vector, self.y_pos))
                        elif self.attack_mode == 2:
                            screen.blit(self.attack_middle_img, (self.x_pos + self.vector, self.y_pos + self.high_rage))
                        elif self.attack_mode == 3:
                            screen.blit(self.attack_low_img,
                                        (self.x_pos + self.vector, self.y_pos + self.high_rage + self.middle_rage))

                # 공겨 준비 중 아니고
                # 공격 모션 중 아니면 공격 가능
                if not self.ready_bool and not self.attack_bool:
                    # 최초 공격 버튼 눌렀을 때
                    if self.attack_temp != 0:
                        self.attack_ticks = pygame.time.get_ticks()
                        self.attack_mode = self.attack_temp
                        self.ready_bool = True

            # 수비 그리기
            # 공격 중이 아닐 때, 점프 중이 아닐 때만 가능
            elif self.attack_mode == 0 and self.defend_mode != 0:
                if self.defend_mode == 1:
                    screen.blit(self.defend_high_img, (self.x_pos, self.y_pos))
                elif self.defend_mode == 2:
                    screen.blit(self.defend_middle_img, (self.x_pos, self.y_pos + self.high_rage))
                elif self.defend_mode == 3:
                    screen.blit(self.defend_low_img, (self.x_pos, self.y_pos + self.high_rage + self.middle_rage))

                if self.effect_bool:
                    defend_time = (pygame.time.get_ticks() - self.effect_ticks) / 1000
                    if defend_time < self.effect_delay:
                        if self.defend_mode == 1:
                            screen.blit(self.defend_effect, (self.x_pos + 50 * -1 * self.position, self.y_pos - 20))
                        elif self.defend_mode == 2:
                            screen.blit(self.defend_effect,
                                        (self.x_pos + 50 * -1 * self.position, self.y_pos + self.high_rage + 20))
                        elif self.defend_mode == 3:
                            screen.blit(self.defend_effect,
                                        (self.x_pos + 50 * -1 * self.position,
                                         self.y_pos + self.high_rage + self.middle_rage - 10))

                    else:
                        self.effect_bool = False
                        self.effect_ticks = 0

    # 캐릭터 이동
    # screen_height : 화면 높이
    # screen_width : 화면 너비
    # stage_height : 스테이지 높이
    # dt : 이동 프레임 수
    def move_char(self, screen_height, screen_width, stage_height, dt):
        # 수비 중이 아닐 때만 이동 가능
        if self.jump_bool and self.defend_mode == 0 and not self.hit_bool:
            self.to_y = -12
            self.jump_bool = False
        elif self.y_pos < screen_height - stage_height - self.height:
            self.to_y += 0.02 * dt
        else:
            self.y_pos = screen_height - stage_height - self.height
            self.to_y = 0
        self.y_pos += self.to_y

        if self.defend_mode == 0 and not self.hit_bool:
            self.x_pos += self.to_x

        if self.hit_bool:
            self.x_pos += self.position / 15 * dt

        if self.x_pos < 0:  # 벽에 막힐 경우
            self.x_pos = 0
        elif self.x_pos > screen_width - self.width:
            self.x_pos = screen_width - self.width
