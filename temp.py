from random import randint

class Fighter():
    hp = 100
    alive = True

    def damage(self, attack):
        self.hp = self.hp - attack
        if self.hp <= 0:
            self.alive = False

    def attack(self, attack_type, enemy):
        if attack_type:
            enemy.damage(10)
        else:
            enemy.damage(15)

a = Fighter()
b = Fighter()

while a.alive and b.alive:
    x = randint(1, 2)
    y = randint(1, 2)

    if x == 1:
        a.attack(y, b)
    else:
        b.attack(y, a)

    print(x, y, f'a hp : {a.hp}, b hp : {b.hp}')
