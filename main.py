'''Menu Interface'''
import pygame
import subprocess
"from inventory_system import"
"from item_class import"
pygame.init()

#state
state = "menu"
volume = 1

# header
pygame.display.set_caption("Backpack")

# color
white = (255, 255, 255)
green = (0, 255, 0)
brown = (139, 69, 19)

#music
pygame.mixer.music.load("sound/bg_music.mp3")
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

# resolution
screen = pygame.display.set_mode((920, 750))

# font
sys_font = pygame.font.SysFont("bytebounce", 100)
small_font = pygame.font.SysFont("bytebounce", 50)

# background
bg_img = pygame.image.load("background/bg3.png").convert_alpha()
bg_img = pygame.transform.scale(bg_img, (920, 750))

# image


# สร้าง rect สำหรับปุ่ม

start_rect = pygame.Rect(0, 0, 300, 100)
start_rect.center = (470, 375)

setting_rect = pygame.Rect(0, 0, 400, 100)
setting_rect.center = (470, 500)

credits_rect = pygame.Rect(0, 0, 500, 100)
credits_rect.center = (470, 625)

setting_frame = pygame.Rect(0, 0, 400, 200)
setting_frame.center = (470, 375)

credits_frame = pygame.Rect(0, 0, 400, 600)
credits_frame.center = (470, 375)

setting_title = pygame.Rect(0, 0, 400, 100)
setting_title.center = (470, 500)

back_rect = pygame.Rect(0, 0, 200, 60)
back_rect.center = (470, 600)

vol_plus_rect = pygame.Rect(0, 0, 50, 50)
vol_plus_rect.center = (620, 409)

vol_minus_rect = pygame.Rect(0, 0, 50, 50)
vol_minus_rect.center = (320, 410)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and state == "menu":
            if start_rect.collidepoint(event.pos):
                subprocess.Popen(["python", "inventory_system.py"])
                running = False

            elif setting_rect.collidepoint(event.pos):
                state = "setting"

            elif credits_rect.collidepoint(event.pos):
                state = "credits"

        elif event.type == pygame.MOUSEBUTTONDOWN and state == "setting":
            if back_rect.collidepoint(event.pos):
                state = "menu"
            elif vol_plus_rect.collidepoint(event.pos):
                volume = min(1.0, volume + 0.1)
                pygame.mixer.music.set_volume(volume)
            elif vol_minus_rect.collidepoint(event.pos):
                volume = max(0.0, volume - 0.1)
                pygame.mixer.music.set_volume(volume)

        elif event.type == pygame.MOUSEBUTTONDOWN and state == "credits":
            if back_rect.collidepoint(event.pos):
                state = "menu"

    screen.blit(bg_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    if state == "menu":
            start_color = green if start_rect.collidepoint(mouse_pos) else white
            setting_color = green if setting_rect.collidepoint(mouse_pos) else white
            credits_color = green if credits_rect.collidepoint(mouse_pos) else white

            start_text = sys_font.render("START", True, start_color)
            setting_text = sys_font.render("SETTING", True, setting_color)
            credits_text = sys_font.render("CREDITS", True, credits_color)

            start_box = start_text.get_rect(center=start_rect.center)
            setting_box = setting_text.get_rect(center=setting_rect.center)
            credits_box = credits_text.get_rect(center=credits_rect.center)
            padding = 30
            start_box.inflate_ip(padding, padding)
            setting_box.inflate_ip(padding, padding)
            credits_box.inflate_ip(padding, padding)

            pygame.draw.rect(screen, brown, start_box, border_radius=20)
            pygame.draw.rect(screen, brown, setting_box, border_radius=20)
            pygame.draw.rect(screen, brown, credits_box, border_radius=20)
            screen.blit(start_text, start_text.get_rect(center=start_rect.center))
            screen.blit(setting_text, setting_text.get_rect(center=setting_rect.center))
            screen.blit(credits_text, credits_text.get_rect(center=credits_rect.center))

        # ---------- หน้า setting ----------
    elif state == "setting":
        # วาดกรอบสี่เหลี่ยม
        pygame.draw.rect(screen, brown, setting_frame, border_radius=20)
        pygame.draw.rect(screen, green, setting_frame, 5, border_radius=20)

        # แสดง Volume ตรงกลาง
        setting_font = sys_font.render("SETTING", True, white)
        vol_text = small_font.render(f"Volume: {int(volume*100)}%", True, white)
        screen.blit(vol_text,(350,390))

                # ปุ่ม + / -
        plus_color = green if vol_plus_rect.collidepoint(mouse_pos) else white
        minus_color = green if vol_minus_rect.collidepoint(mouse_pos) else white

        # ตัวอักษร + / - บนปุ่ม (ไม่มี background)
        plus_text = small_font.render("+", True, plus_color)# สีตัวอักษร
        minus_text = small_font.render("-", True, minus_color)
        screen.blit(setting_font, (330,300))
        screen.blit(plus_text, plus_text.get_rect(center=vol_plus_rect.center))
        screen.blit(minus_text, minus_text.get_rect(center=vol_minus_rect.center))


        # ปุ่ม Back
        back_color = green if back_rect.collidepoint(mouse_pos) else white
        back_text = sys_font.render("BACK", True, back_color)
        screen.blit(back_text, back_text.get_rect(center=back_rect.center))

    elif state == "credits":
        pygame.draw.rect(screen, brown, credits_frame, border_radius=20)
        pygame.draw.rect(screen, green, credits_frame, 5, border_radius=20)

        back_color = green if back_rect.collidepoint(mouse_pos) else white
        back_text = sys_font.render("BACK", True, back_color)
        screen.blit(back_text, back_text.get_rect(center=back_rect.center))

    pygame.display.flip()

pygame.quit()
