import pgzrun
import random

WIDTH = 400
HEIGHT = 600

TITLE = "Space Commander"
FPS = 30

bg = Actor("space")
mode = "menu"
button_start = Actor("button_start", (200, 300))

player = Actor("player", (200, 550))
player.direction = "up"
count = 0

bullets = []

enemy_images = ["enemy_1", "enemy_2", "enemy_3", "enemy_4"]
enemies = []

obj_images = ["obj_1", "obj_2", "obj_3", "obj_4"]
objs = []

for i in range(2):
    x = random.randint(0, WIDTH)
    y = random.randint(-450, -50)
    image = random.choice(obj_images)
    obj = Actor(image, (x, y))
    obj.speed = random.randint(1, 3)
    objs.append(obj)

for i in range(3):
    x = random.randint(0, WIDTH)
    y = random.randint(-450, -50)
    image = random.choice(enemy_images)
    enemy = Actor(image, (x, y))
    enemy.speed = random.randint(2, 5)
    enemies.append(enemy)

def draw():
    global count

    if mode == "game":
        bg.draw()
        player.draw()

        for enemy in enemies:
            enemy.draw()

        for obj in objs:
            obj.draw()

        for bullet in bullets:
            bullet.draw()

        screen.draw.text(f"Score: {count}", (10, 10), color="blue", fontsize=30)

    if mode == "menu":
        bg.draw()
        button_start.draw()
        screen.draw.text("Press Enter", center=(200, 200), color="blue", fontsize=40)

    if mode == "end":
        bg.draw()
        screen.draw.text(f"Score: {count}", (160, 250), color="blue", fontsize=40)
        screen.draw.text("GAME OVER!", center=(200, 200), color="blue", fontsize=40)

def update():
    if mode == "game":
        enemy_ship()
        objects()
        collisions()

        for bullet in bullets:
            bullet.y += bullet.dy

def on_mouse_move(pos):
    global mode
    if mode == "game":
        player.pos = pos


def on_mouse_down(pos, button):
    global mode

    if button == mouse.LEFT:
        if button_start.collidepoint(pos):
            mode = 'game'

        if mode == "game":
            bullet = Actor("bullet")
            bullet.pos = player.pos
            bullet.dy = -10
            bullets.append(bullet)

def new_enemy():
    x = random.randint(0, WIDTH)
    y = -50
    image = random.choice(enemy_images)
    enemy = Actor(image, (x, y))
    enemy.speed = random.randint(2, 5)
    enemies.append(enemy)

def enemy_ship():
    for enemy in enemies[:]:
        enemy.y += enemy.speed
        if enemy.y > HEIGHT + 50:
            enemies.remove(enemy)
            new_enemy()

def new_obj():
    x = random.randint(0, WIDTH)
    y = -50
    image = random.choice(obj_images)
    obj = Actor(image, (x, y))
    obj.speed = random.randint(1, 3)
    objs.append(obj)   

def objects():
    for obj in objs[:]:
        obj.y += obj.speed
        if obj.y > HEIGHT + 50:
            objs.remove(obj)
            new_obj()

def collisions():
    global mode, count

    for enemy in enemies[:]:
        if player.colliderect(enemy):
            mode = 'end'

        for bullet in bullets[:]:
            if bullet.colliderect(enemy):
                count += 1
                enemies.remove(enemy)
                bullets.remove(bullet)
                new_enemy()
                break

    for obj in objs[:]:
        if player.colliderect(obj):
            mode = 'end'

        for bullet in bullets[:]:
            if bullet.colliderect(obj):
                count += 1
                objs.remove(obj)
                bullets.remove(bullet)
                new_obj()
                break
        
pgzrun.go()