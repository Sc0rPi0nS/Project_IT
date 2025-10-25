'''Menu Interface'''
import pygame
import subprocess
"from inventory_system import"
"from item_class import"
pygame.init()

# header
pygame.display.set_caption("Backpack")

# color
white = (255, 255, 255)
green = (0, 255, 0)

#music
pygame.mixer.music.load("sound/bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# resolution
screen = pygame.display.set_mode((920, 750))

# font
sys_font = pygame.font.SysFont("bytebounce", 100)

# background
bg_img = pygame.image.load("background/bg3.png").convert_alpha()
bg_img = pygame.transform.scale(bg_img, (920, 750))

# image

# สร้าง rect สำหรับปุ่ม
start_rect = pygame.Rect(0, 0, 300, 100)
start_rect.center = (460, 375)

setting_rect = pygame.Rect(0, 0, 400, 100)
setting_rect.center = (460, 500)

state = "menu"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and state == "menu":
            if start_rect.collidepoint(event.pos):
                subprocess.Popen(["python", "game.py"])
                running = False

    mouse_pos = pygame.mouse.get_pos()

    # แยกสีแต่ละปุ่ม
    start_color = green if start_rect.collidepoint(mouse_pos) else white
    setting_color = green if setting_rect.collidepoint(mouse_pos) else white

    # วาดพื้นหลัง + ปุ่ม
    screen.blit(bg_img, (0, 0))
    start_text = sys_font.render("START", True, start_color)
    setting_text = sys_font.render("SETTING", True, setting_color)
    screen.blit(start_text, start_text.get_rect(center=start_rect.center))
    screen.blit(setting_text, setting_text.get_rect(center=setting_rect.center))

    pygame.display.update()

pygame.quit()
