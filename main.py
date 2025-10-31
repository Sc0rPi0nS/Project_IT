'''Menu Interface'''
import pygame
import subprocess
"from inventory_system import"
"from item_class import"
pygame.init()

#state
state = "menu"
volume = 1
player_name = "Chotipat"

# header
pygame.display.set_caption("The Scavanger")

# color
white = (255, 255, 255)
green = (0, 255, 0)
frame = (96, 62, 62)
brown = (218, 169, 107)
text_press = (145, 92, 67)

#music
pygame.mixer.music.load("sound/bg_music.mp3")
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)
click_sound = pygame.mixer.Sound("sound/click-sound.mp3")
click_sound.set_volume(1)

# resolution
SCREEN = pygame.display.set_mode((920,750), pygame.RESIZABLE)

# font
sys_font = pygame.font.SysFont("bytebounce", 100)
small_font = pygame.font.SysFont("bytebounce", 50)

# background
bg_img = pygame.image.load("background/bg2.png").convert_alpha()
bg_img = pygame.transform.scale(bg_img, (920,750))

# สร้าง rect สำหรับปุ่ม

start_rect = pygame.Rect(0, 0, 300, 100)
start_rect.center = (470, 320)

setting_rect = pygame.Rect(0, 0, 400, 100)
setting_rect.center = (470, 450)

credits_rect = pygame.Rect(0, 0, 500, 100)
credits_rect.center = (470, 580)

setting_frame = pygame.Rect(0, 0, 400, 200)
setting_frame.center = (470, 375)

credits_frame = pygame.Rect(0, 0, 600, 560)
credits_frame.center = (470, 320)

setting_title = pygame.Rect(0, 0, 400, 100)
setting_title.center = (470, 500)

back_rect = pygame.Rect(0, 0, 200, 60)
back_rect.center = (470, 630)

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
                click_sound.play()
                subprocess.Popen(["python", "inventory_system.py", str(volume),player_name])
                running = False

            elif setting_rect.collidepoint(event.pos):
                click_sound.play()
                state = "setting"

            elif credits_rect.collidepoint(event.pos):
                click_sound.play()
                state = "credits"

        elif event.type == pygame.MOUSEBUTTONDOWN and state == "setting":
            click_sound.play()
            if back_rect.collidepoint(event.pos):
                state = "menu"
            elif vol_plus_rect.collidepoint(event.pos):
                click_sound.play()
                volume = min(1.0, volume + 0.1)
                pygame.mixer.music.set_volume(volume)
            elif vol_minus_rect.collidepoint(event.pos):
                click_sound.play()
                volume = max(0.0, volume - 0.1)
                pygame.mixer.music.set_volume(volume)

        elif event.type == pygame.MOUSEBUTTONDOWN and state == "credits":
            click_sound.play()
            if back_rect.collidepoint(event.pos):
                state = "menu"

    SCREEN.blit(bg_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    if state == "menu":
            # ---------- Title game----------
            title_font = pygame.font.SysFont("bytebounce", 120)
            title_text = title_font.render("THE SCAVANGER", True, brown)
            title_rect = title_text.get_rect(center=(SCREEN.get_width() // 2, 100))  # ตรงกลางบน

            #outline
            outline_color = frame
            outline_thickness = 3
            for dx in [-outline_thickness, 0, outline_thickness]:
                for dy in [-outline_thickness, 0, outline_thickness]:
                    if dx != 0 or dy != 0:  # ข้ามตำแหน่งตรงกลาง
                        outline_text = title_font.render("THE SCAVANGER", True, outline_color)
                        SCREEN.blit(outline_text, title_rect.move(dx, dy))

            # วาดข้อความ
            SCREEN.blit(title_text, title_rect)

            start_color = white if start_rect.collidepoint(mouse_pos) else text_press
            setting_color = white if setting_rect.collidepoint(mouse_pos) else text_press
            credits_color = white if credits_rect.collidepoint(mouse_pos) else text_press

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

            pygame.draw.rect(SCREEN, brown, start_box, border_radius=20)
            pygame.draw.rect(SCREEN, frame, start_box, 5, border_radius=20)
            pygame.draw.rect(SCREEN, brown, setting_box, border_radius=20)
            pygame.draw.rect(SCREEN, frame, setting_box, 5, border_radius=20)
            pygame.draw.rect(SCREEN, brown, credits_box, border_radius=20)
            pygame.draw.rect(SCREEN, frame, credits_box, 5, border_radius=20)
            SCREEN.blit(start_text, start_text.get_rect(center=start_rect.center))
            SCREEN.blit(setting_text, setting_text.get_rect(center=setting_rect.center))
            SCREEN.blit(credits_text, credits_text.get_rect(center=credits_rect.center))

        # ---------- หน้า setting ----------
    elif state == "setting":
        # วาดกรอบสี่เหลี่ยม
        pygame.draw.rect(SCREEN, brown, setting_frame, border_radius=20)
        pygame.draw.rect(SCREEN, frame, setting_frame, 5, border_radius=20)

        # แสดง Volume ตรงกลาง
        setting_font = sys_font.render("SETTING", True, text_press)
        vol_text = small_font.render(f"Volume: {int(round(volume*100))}%", True, text_press)
        SCREEN.blit(vol_text,(350,390))

                # ปุ่ม + / -
        plus_color = white if vol_plus_rect.collidepoint(mouse_pos) else text_press
        minus_color = white if vol_minus_rect.collidepoint(mouse_pos) else text_press

        # ตัวอักษร + / - บนปุ่ม (ไม่มี background)
        plus_text = small_font.render("+", True, plus_color)# สีตัวอักษร
        minus_text = small_font.render("-", True, minus_color)
        SCREEN.blit(setting_font, (330,300))
        SCREEN.blit(plus_text, plus_text.get_rect(center=vol_plus_rect.center))
        SCREEN.blit(minus_text, minus_text.get_rect(center=vol_minus_rect.center))


        # ปุ่ม Back
        back_color = text_press if back_rect.collidepoint(mouse_pos) else white
        back_text = sys_font.render("BACK", True, back_color)
        SCREEN.blit(back_text, back_text.get_rect(center=back_rect.center))

    elif state == "credits":
        pygame.draw.rect(SCREEN, brown, credits_frame, border_radius=20)
        pygame.draw.rect(SCREEN, frame, credits_frame, 5, border_radius=20)
        
            # ---------- สร้าง Surface สำหรับ clipping ----------
        clip_surf = SCREEN.subsurface(credits_frame)  # วาดเฉพาะในกรอบ

        credits_lines = [
            "CREDITS",
            "",
            "Game Design : Thanawit Wanthong",
            "Programming : Thanawit Wanthong",
            "Art & UI : Thanawit Wanthong",
            "Music : Free Background Theme",
            "",
            "Special Thanks",
            "You, for playing this game!",
            "",
            "Thank you for playing!",
        ]

        credit_font = pygame.font.SysFont("bytebounce", 40)
        line_height = 50
        total_height = len(credits_lines) * line_height

        if "credits_y" not in locals():
            credits_y = credits_frame.height  # เริ่มจากด้านล่างกรอบ

        # วาดแต่ละบรรทัดภายใน clip_surf
        for i, text in enumerate(credits_lines):
            surf = credit_font.render(text, True, text_press)
            rect = surf.get_rect(center=(credits_frame.width // 2, credits_y + i * line_height))
            clip_surf.blit(surf, rect)

        # เลื่อนขึ้น
        credits_y -= 0.1  # ความเร็วปรับได้
        if credits_y + total_height < 0:  # ถ้าเลื่อนหมด
            credits_y = credits_frame.height  # เริ่มใหม่ หรือกลับเมนู


        back_color = text_press if back_rect.collidepoint(mouse_pos) else white
        back_text = sys_font.render("BACK", True, back_color)
        SCREEN.blit(back_text, back_text.get_rect(center=back_rect.center))

    pygame.display.flip()

pygame.quit()
