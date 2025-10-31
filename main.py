'''Menu Interface'''
import pygame
import subprocess
"from inventory_system import"
"from item_class import"
pygame.init()

#state
state = "menu"
volume = 1
player_name = ""  # ชื่อผู้เล่นเริ่มต้นว่าง
input_active = False  # ตรวจสอบว่ากำลังพิมพ์อยู่หรือไม่

# header
pygame.display.set_caption("The Scavanger")

# color
white = (255, 255, 255)
black = (0,0,0)
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
start_rect.center = (470, 250)

tuto_rect = pygame.Rect(0, 0, 350, 100)
tuto_rect.center = (470, 370)

setting_rect = pygame.Rect(0, 0, 400, 100)
setting_rect.center = (470, 490)

credits_rect = pygame.Rect(0, 0, 500, 100)
credits_rect.center = (470, 610)

input_frame = pygame.Rect(0, 0, 400, 200)
input_frame.center = (470, 300)

tutorial_frame = pygame.Rect(0, 0, 800, 550)
tutorial_frame.center = (470, 300)

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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == "menu":
                if start_rect.collidepoint(event.pos):
                    click_sound.play()
                    state = "input_name"
                    input_active = True  # เริ่มรับ input
                elif tuto_rect.collidepoint(event.pos):
                    click_sound.play()
                    state = "tutorial"
                elif setting_rect.collidepoint(event.pos):
                    click_sound.play()
                    state = "setting"
                elif credits_rect.collidepoint(event.pos):
                    click_sound.play()
                    state = "credits"
            elif state in ["input_name","tutorial", "setting", "credits"]:
                if back_rect.collidepoint(event.pos):
                    click_sound.play()
                    state = "menu"

        elif event.type == pygame.KEYDOWN and state == "input_name" and input_active:
            if event.key == pygame.K_RETURN:  # กด Enter เริ่มเกม
                if player_name.strip() != "":
                    subprocess.Popen(["python", "inventory_system.py", str(volume), player_name])
                    running = False
            elif event.key == pygame.K_BACKSPACE:  # ลบตัวอักษร
                player_name = player_name[:-1]
            else:
                if len(player_name) < 9:  # จำกัดความยาวชื่อ
                    player_name += event.unicode

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
            tuto_color = white if tuto_rect.collidepoint(mouse_pos) else text_press
            setting_color = white if setting_rect.collidepoint(mouse_pos) else text_press
            credits_color = white if credits_rect.collidepoint(mouse_pos) else text_press

            start_text = sys_font.render("START", True, start_color)
            tuto_text = sys_font.render("TUTORIAL", True, tuto_color)
            setting_text = sys_font.render("SETTING", True, setting_color)
            credits_text = sys_font.render("CREDITS", True, credits_color)

            start_box = start_text.get_rect(center=start_rect.center)
            tuto_box = tuto_text.get_rect(center=tuto_rect.center)
            setting_box = setting_text.get_rect(center=setting_rect.center)
            credits_box = credits_text.get_rect(center=credits_rect.center)
            padding = 30
            start_box.inflate_ip(padding, padding)
            tuto_box.inflate_ip(padding, padding)
            setting_box.inflate_ip(padding, padding)
            credits_box.inflate_ip(padding, padding)

            pygame.draw.rect(SCREEN, brown, start_box, border_radius=20)
            pygame.draw.rect(SCREEN, frame, start_box, 5, border_radius=20)
            pygame.draw.rect(SCREEN, brown, tuto_box, border_radius=20)
            pygame.draw.rect(SCREEN, frame, tuto_box, 5, border_radius=20)
            pygame.draw.rect(SCREEN, brown, setting_box, border_radius=20)
            pygame.draw.rect(SCREEN, frame, setting_box, 5, border_radius=20)
            pygame.draw.rect(SCREEN, brown, credits_box, border_radius=20)
            pygame.draw.rect(SCREEN, frame, credits_box, 5, border_radius=20)
            SCREEN.blit(start_text, start_text.get_rect(center=start_rect.center))
            SCREEN.blit(tuto_text, tuto_text.get_rect(center=tuto_rect.center))
            SCREEN.blit(setting_text, setting_text.get_rect(center=setting_rect.center))
            SCREEN.blit(credits_text, credits_text.get_rect(center=credits_rect.center))

    elif state == "input_name":
        # วาดกรอบใหญ่
        pygame.draw.rect(SCREEN, brown, input_frame, border_radius=20)
        pygame.draw.rect(SCREEN, frame, input_frame, 5, border_radius=20)

        # ข้อความชี้แนะ
        prompt_font = pygame.font.SysFont("bytebounce", 55)
        prompt_text = prompt_font.render("Enter Your Name:", True, white)
        SCREEN.blit(prompt_text, prompt_text.get_rect(center=(input_frame.centerx, input_frame.top + 80)))

        # กรอบกล่องใส่ชื่อ
        input_box = pygame.Rect(input_frame.left + 50, input_frame.top + 120, input_frame.width - 100, 60)
        pygame.draw.rect(SCREEN, white, input_box, border_radius=10)        # Background ของ input
        pygame.draw.rect(SCREEN, frame, input_box, 3, border_radius=10)     # ขอบ

        # แสดงชื่อที่พิมพ์
        name_font = pygame.font.SysFont("bytebounce", 50)
        name_text = name_font.render(player_name, True, black)
        SCREEN.blit(name_text, (input_box.x + 10, input_box.y + 10))

        # เคอร์เซอร์กระพริบ
        if input_active:
            cursor_time = pygame.time.get_ticks() // 500 % 2  # กระพริบทุก 0.5 วินาที
            if cursor_time == 0:
                cursor_x = input_box.x + 10 + name_text.get_width() + 2
                cursor_y = input_box.y + 10
                cursor_height = name_text.get_height()
                pygame.draw.line(SCREEN, black, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 3)
        # ปุ่ม Enter
        enter_rect = pygame.Rect(0, 0, 200, 60)
        enter_rect.center = (input_frame.centerx, input_box.bottom + 60)
        enter_color = green if enter_rect.collidepoint(mouse_pos) else white
        enter_text = sys_font.render("ENTER", True, enter_color)
        SCREEN.blit(enter_text, enter_text.get_rect(center=enter_rect.center))

        # ตรวจสอบปุ่ม Enter
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if enter_rect.collidepoint(event.pos) and player_name.strip() != "":
                click_sound.play()
                subprocess.Popen(["python", "inventory_system.py", str(volume), player_name])
                running = False

        # ปุ่ม Back
        back_color = text_press if back_rect.collidepoint(mouse_pos) else white
        back_text = sys_font.render("BACK", True, back_color)
        SCREEN.blit(back_text, back_text.get_rect(center=back_rect.center))
    
    elif state == "tutorial": 
            pygame.draw.rect(SCREEN, brown, tutorial_frame, border_radius=20)
            pygame.draw.rect(SCREEN, frame, tutorial_frame, 5, border_radius=20)
            # แปะ tutorial text
            tutorial_lines = [
                "Goal: Collect as many valuable items as you can before the timer runs out!",
                "Your total item value = your final score.",
                "                                                How to Play                                ",
                "Search for items: Click the Search box (blue area on the right) to spawn random items.",
                "Each item has a different value rare ones score big!",
                "Move items: Click + drag an item to move it.",
                "Drop items into the 5x5 inventory grid (left side) to store them.",
                "Rotate items: While dragging, press R to rotate.",
                "Rotate strategically to make everything fit!",
                "Trash unwanted items:",
                "Drag any item into the trash zone (bottom-right) to delete it. 🗑️",
                "🧨 Timer",
                "You’ve got 30 seconds to collect and organize items.",
                "When time’s up → your score is calculated automatically.",
                "🏆 Leaderboard",
                "After time’s up, your score gets saved.",
                "Only the Top 10 players make it to the board.",
                "Can you beat your own high score? 😏",
                "💡 Tips",
                "Bigger items don’t always mean better value — check the total 'Value' bar.",
                "You can press H to show grid hitboxes for better placement.",
                "Don’t waste time! Each second counts. 🕐",
            ]
            tutorial_font = pygame.font.SysFont("bytebounce", 20)
            line_height = 35

            # ปุ่ม Back
            back_color = text_press if back_rect.collidepoint(mouse_pos) else white
            back_text = sys_font.render("BACK", True, back_color)
            SCREEN.blit(back_text, back_text.get_rect(center=back_rect.center))
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
            "Game Director : Chanawat",
            "Game Designer : Inthuch, Chanawat",
            "Programming : Thanawit, Bunyapul",
            "UI/UX Designer : Bunyapul, Thanawit, Inthuch",
            "Artist : Phacharaphol, Thanawit",
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
