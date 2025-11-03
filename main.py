'''Menu Interface'''
import pygame
import subprocess
"from inventory_system import"
"from item_class import"
pygame.init()

#state
state = "menu"
volume = 1
player_name = ""
input_active = False

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

#font
sys_font = pygame.font.SysFont("bytebounce", 100)
small_font = pygame.font.SysFont("bytebounce", 50)

# background
bg_img = pygame.image.load("background/bg2.png").convert_alpha()
bg_img = pygame.transform.scale(bg_img, (920,750))
tutorial_img = pygame.image.load("background/tutorial.png").convert_alpha()
tutorial_img = pygame.transform.scale(tutorial_img, (500,600))

#rect

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

#game run
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == "menu":
                if start_rect.collidepoint(event.pos):
                    click_sound.play()
                    state = "input_name"
                    input_active = True
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
        #input
        elif event.type == pygame.KEYDOWN and state == "input_name" and input_active:
            if event.key == pygame.K_RETURN:
                if player_name.strip() != "":
                    subprocess.Popen(["python", "inventory_system.py", str(volume), player_name])
                    running = False
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                if len(player_name) < 9:
                    player_name += event.unicode

    SCREEN.blit(bg_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    
    #menu
    if state == "menu":
            # ---------- Title game----------
            title_font = pygame.font.SysFont("bytebounce", 120)
            title_text = title_font.render("THE SCAVANGER", True, brown)
            title_rect = title_text.get_rect(center=(SCREEN.get_width() // 2, 100))

            #outline
            outline_color = frame
            outline_thickness = 3
            for dx in [-outline_thickness, 0, outline_thickness]:
                for dy in [-outline_thickness, 0, outline_thickness]:
                    if dx != 0 or dy != 0:
                        outline_text = title_font.render("THE SCAVANGER", True, outline_color)
                        SCREEN.blit(outline_text, title_rect.move(dx, dy))

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

    #input
    elif state == "input_name":
        #frame
        pygame.draw.rect(SCREEN, brown, input_frame, border_radius=20)
        pygame.draw.rect(SCREEN, frame, input_frame, 5, border_radius=20)

        #text
        prompt_font = pygame.font.SysFont("bytebounce", 55)
        prompt_text = prompt_font.render("Enter Your Name:", True, white)
        SCREEN.blit(prompt_text, prompt_text.get_rect(center=(input_frame.centerx, input_frame.top + 80)))

        #input frame
        input_box = pygame.Rect(input_frame.left + 50, input_frame.top + 120, input_frame.width - 100, 60)
        pygame.draw.rect(SCREEN, white, input_box, border_radius=10)        # Background ของ input
        pygame.draw.rect(SCREEN, frame, input_box, 3, border_radius=10)     # ขอบ

        #name
        name_font = pygame.font.SysFont("bytebounce", 50)
        name_text = name_font.render(player_name, True, black)
        SCREEN.blit(name_text, (input_box.x + 10, input_box.y + 10))

        #cursor
        if input_active:
            cursor_time = pygame.time.get_ticks() // 500 % 2  # กระพริบทุก 0.5 วินาที
            if cursor_time == 0:
                cursor_x = input_box.x + 10 + name_text.get_width() + 2
                cursor_y = input_box.y + 10
                cursor_height = name_text.get_height()
                pygame.draw.line(SCREEN, black, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 3)
        
        #enter
        enter_rect = pygame.Rect(0, 0, 200, 60)
        enter_rect.center = (input_frame.centerx, input_box.bottom + 60)
        enter_color = green if enter_rect.collidepoint(mouse_pos) else white
        enter_text = sys_font.render("ENTER", True, enter_color)
        SCREEN.blit(enter_text, enter_text.get_rect(center=enter_rect.center))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if enter_rect.collidepoint(event.pos) and player_name.strip() != "":
                click_sound.play()
                subprocess.Popen(["python", "inventory_system.py", str(volume), player_name])
                running = False

        #back
        back_color = text_press if back_rect.collidepoint(mouse_pos) else white
        back_text = sys_font.render("BACK", True, back_color)
        SCREEN.blit(back_text, back_text.get_rect(center=back_rect.center))
    
    #tutorial
    elif state == "tutorial":
        #imaga tutorial
        img_rect = tutorial_img.get_rect(center=tutorial_frame.center)
        
        rounded_surface = pygame.Surface(tutorial_img.get_size(), pygame.SRCALPHA)
        
        radius = 30
        mask = pygame.Surface(tutorial_img.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255), mask.get_rect(), border_radius=radius)
        
        rounded_surface.blit(tutorial_img, (0, 0))
        rounded_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        shadow = pygame.Surface((img_rect.width + 10, img_rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 120), shadow.get_rect(), border_radius=radius + 5)
        SCREEN.blit(shadow, img_rect.move(5, 5))

        SCREEN.blit(rounded_surface, img_rect)
        pygame.draw.rect(SCREEN, frame, img_rect, 8, border_radius=radius)

        #back
        back_color = text_press if back_rect.collidepoint(mouse_pos) else white
        back_text = sys_font.render("BACK", True, back_color)
        SCREEN.blit(back_text, back_text.get_rect(center=back_rect.center))

        # ---------- หน้า setting ----------
    elif state == "setting":
        #setting frame
        pygame.draw.rect(SCREEN, brown, setting_frame, border_radius=20)
        pygame.draw.rect(SCREEN, frame, setting_frame, 5, border_radius=20)

        #volume
        setting_font = sys_font.render("SETTING", True, text_press)
        vol_text = small_font.render(f"Volume: {int(round(volume*100))}%", True, text_press)
        SCREEN.blit(vol_text,(350,390))

        #plus-minus
        plus_color = white if vol_plus_rect.collidepoint(mouse_pos) else text_press
        minus_color = white if vol_minus_rect.collidepoint(mouse_pos) else text_press

        plus_text = small_font.render("+", True, plus_color)
        minus_text = small_font.render("-", True, minus_color)
        SCREEN.blit(setting_font, (330,300))
        SCREEN.blit(plus_text, plus_text.get_rect(center=vol_plus_rect.center))
        SCREEN.blit(minus_text, minus_text.get_rect(center=vol_minus_rect.center))


        #back
        back_color = text_press if back_rect.collidepoint(mouse_pos) else white
        back_text = sys_font.render("BACK", True, back_color)
        SCREEN.blit(back_text, back_text.get_rect(center=back_rect.center))

    elif state == "credits":
        pygame.draw.rect(SCREEN, brown, credits_frame, border_radius=20)
        pygame.draw.rect(SCREEN, frame, credits_frame, 5, border_radius=20)
        
        #credit frame
        clip_surf = SCREEN.subsurface(credits_frame)

        credits_lines = [
            "CREDITS",
            "",
            "Game Director : Chanawat",
            "Game Designer : Inthuch, Chanawat",
            "Programming : Thanawit, Bunyapul",
            "UI/UX Designer",
            "Bunyapul, Thanawit, Inthuch",
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
            credits_y = credits_frame.height

        for i, text in enumerate(credits_lines):
            surf = credit_font.render(text, True, text_press)
            rect = surf.get_rect(center=(credits_frame.width // 2, credits_y + i * line_height))
            clip_surf.blit(surf, rect)

        credits_y -= 0.1
        if credits_y + total_height < 0:
            credits_y = credits_frame.height

        #back
        back_color = text_press if back_rect.collidepoint(mouse_pos) else white
        back_text = sys_font.render("BACK", True, back_color)
        SCREEN.blit(back_text, back_text.get_rect(center=back_rect.center))

    pygame.display.flip()

pygame.quit()
