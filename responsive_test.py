import pygame
import sys
import random
import subprocess
import json
import os

from item_class import Item, make_trial_item, item_pixel_size, \
    make_medkit_item, make_battery_item, make_rtx_item, make_canfood_item
# responsive added and close bottom added
pygame.init()

# ---------- Responsive Screen ----------
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Dual Inventory System (Responsive)")

#json
LEADERBOARD_FILE = "leaderboard.json"
# ---------- โหลด leaderboard ----------
if os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "r") as f:
        try:
            leaderboard = json.load(f)
        except json.JSONDecodeError:
            leaderboard = []
else:
    leaderboard = []

#playername 
if len(sys.argv) > 1: 
    player_name = sys.argv[1] 
else: 
    player_name = "Guest"

# ---------- Base Colors ----------
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
DARK_RED = (150, 0, 0)
green = (0, 255, 0)
frame = (96, 62, 62)
brown = (218, 169, 107)
text_press = (145, 92, 67)
ITEM_COLORS = [(255, 80, 80), (80, 200, 120), (80, 120, 255), (255, 220, 100)]

# ---------- Font ----------
timer_font = pygame.font.SysFont("bytebounce", 120)  # 60 px
time_up = False
score_added = False
small_font = pygame.font.SysFont("bytebounce", 60)

#image
bgimg = pygame.image.load("background/Inventory backg1.png").convert_alpha()
bgimg = pygame.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
happy_img = pygame.image.load("background/Victory.png").convert_alpha()
happy_img = pygame.transform.scale(happy_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# ---------- Timer ----------
countdown_time = 30  # วินาที (2 นาที)
start_ticks = pygame.time.get_ticks()


# ---------- Grid & Layout (responsive ratios) ----------
def calc_layout():
    global GRID_SIZE, ROWS, COLS, MARGIN_TOP, GAP_X
    global TOTAL_GRID_WIDTH, TOTAL_GRID_HEIGHT
    global GRID_ORIGIN, INVENTORY_RECT, BOX_RECT, SPAWN_RECT, TRASH_RECT
    global SPAWN_ORIGIN, BOX_X, BOX_Y

    ROWS, COLS = 5, 5
    GRID_SIZE = int(SCREEN_HEIGHT * 0.09)
    MARGIN_TOP = int(SCREEN_HEIGHT * 0.18)
    GAP_X = int(SCREEN_WIDTH * 0.08)

    TOTAL_GRID_WIDTH = COLS * GRID_SIZE
    TOTAL_GRID_HEIGHT = ROWS * GRID_SIZE
    start_x = (SCREEN_WIDTH - (TOTAL_GRID_WIDTH + GAP_X + GRID_SIZE * 2)) // 2
    GRID_ORIGIN = (start_x, MARGIN_TOP)
    INVENTORY_RECT = pygame.Rect(GRID_ORIGIN[0], GRID_ORIGIN[1], TOTAL_GRID_WIDTH, TOTAL_GRID_HEIGHT)

    BOX_WIDTH, BOX_HEIGHT = GRID_SIZE * 2, GRID_SIZE
    BOX_X = GRID_ORIGIN[0] + TOTAL_GRID_WIDTH + GAP_X
    BOX_Y = MARGIN_TOP
    BOX_RECT = pygame.Rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT)

    SPAWN_ROWS, SPAWN_COLS = 3, 3
    SPAWN_WIDTH, SPAWN_HEIGHT = SPAWN_COLS * GRID_SIZE, SPAWN_ROWS * GRID_SIZE
    SPAWN_X = BOX_X + BOX_WIDTH // 2 - SPAWN_WIDTH // 2
    SPAWN_Y = BOX_RECT.bottom + int(SCREEN_HEIGHT * 0.03)
    SPAWN_ORIGIN = (SPAWN_X, SPAWN_Y)
    SPAWN_RECT = pygame.Rect(SPAWN_X, SPAWN_Y, SPAWN_WIDTH, SPAWN_HEIGHT)

    TRASH_RECT = pygame.Rect(
        SPAWN_RECT.centerx - GRID_SIZE,
        SPAWN_RECT.bottom + int(SCREEN_HEIGHT * 0.04),
        GRID_SIZE * 2,
        GRID_SIZE
    )

    # ปุ่มปิดเกม (Responsive)
    menu_radius = int(min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.035 * 1.4)
    menu_x = SCREEN_WIDTH - menu_radius - 20
    menu_y = menu_radius + 20
    global MENU_BTN_CENTER, MENU_BTN_RADIUS
    MENU_BTN_CENTER = (menu_x, menu_y)
    MENU_BTN_RADIUS = menu_radius

calc_layout()
# ---------- ฟังก์ชันเพิ่มคะแนน ----------
def add_score(player_name,score):
    global leaderboard
    leaderboard.append({"name": player_name,"score": score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)  # เรียงจากสูงไปต่ำ
    # เก็บแค่ 10 อันดับล่าสุด
    if len(leaderboard) > 10:
        leaderboard = leaderboard[:10]
    # บันทึกลงไฟล์
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=4)

# ---------- ฟังก์ชันแสดง leaderboard ----------
def show_leaderboard(surface, font, start_x, start_y):
    y = start_y
    for idx, entry in enumerate(leaderboard):
        text = font.render(f"{idx+1}. {entry['score']}", True, (0,0,0))
        surface.blit(text, (start_x, y))
        y += text.get_height() + 5

# ---------- Drawing ----------
play_again_rect = pygame.Rect(0, 0, 250, 70)
play_again_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 150)  # วางใต้ข้อความ Time's Up

def draw_play_again_button(surface):
    pygame.draw.rect(surface, (100, 200, 255), play_again_rect, border_radius=15)
    pygame.draw.rect(surface, BLACK, play_again_rect, 3, border_radius=15)
    font = pygame.font.SysFont("bytebounce", 40)
    text_surface = font.render("Play Again", True, BLACK)
    surface.blit(text_surface, text_surface.get_rect(center=play_again_rect.center))
def draw_menu_button(surface, center, radius):
    mouse_pos = pygame.mouse.get_pos()
    cx, cy = center
    dx = mouse_pos[0] - cx
    dy = mouse_pos[1] - cy
    hovering = dx*dx + dy*dy <= radius*radius
    # เปลี่ยนสีถ้า hover
    fill_color = WHITE if hovering else brown
    # วงกลมหลัก
    pygame.draw.circle(surface, fill_color, center, radius)
    # ขอบวงกลม
    pygame.draw.circle(surface, frame, center, radius, 4)

    # วาดขีดสามขีด
    cx, cy = center
    for i in range(-1, 2):  # -1, 0, 1
        y = cy + i * 15
        rect = pygame.Rect(0, 0, 45, 5)
        rect.center = (cx, y)
        pygame.draw.rect(surface, frame, rect, border_radius=4)

def draw_grid(origin):
    ox, oy = origin
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(SCREEN, GRAY, (ox + c * GRID_SIZE, oy + r * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def draw_inventory_value(total_value):
    font = pygame.font.SysFont("bytebounce", int(GRID_SIZE * 0.6))
    text_surface = font.render(f"VALUE : {total_value}", True, BLACK)
    text_x = INVENTORY_RECT.centerx - text_surface.get_width() // 2
    text_y = INVENTORY_RECT.bottom + int(GRID_SIZE * 0.3)
    SCREEN.blit(text_surface, (text_x, text_y))

def draw_spawn_zone():
    ox, oy = SPAWN_ORIGIN
    SPAWN_ROWS, SPAWN_COLS = 3, 3
    for r in range(SPAWN_ROWS):
        for c in range(SPAWN_COLS):
            pygame.draw.rect(SCREEN, (220, 240, 255),
                             (ox + c * GRID_SIZE, oy + r * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
    pygame.draw.rect(SCREEN, BLACK, SPAWN_RECT, 3)

def draw_trash():
    pygame.draw.rect(SCREEN, (240, 240, 240), TRASH_RECT)
    pygame.draw.rect(SCREEN, BLACK, TRASH_RECT, 3)
    font = pygame.font.SysFont("bytebounce", int(GRID_SIZE * 0.6))
    text_surface = font.render("TRASH", True, BLACK)
    SCREEN.blit(text_surface, text_surface.get_rect(center=TRASH_RECT.center))

def draw_item_box():
    pygame.draw.rect(SCREEN, (230, 230, 230), BOX_RECT)
    pygame.draw.rect(SCREEN, BLACK, BOX_RECT, 3)
    font = pygame.font.SysFont("bytebounce", int(GRID_SIZE * 0.6))
    text_surface = font.render("SEARCH", True, BLACK)
    SCREEN.blit(text_surface, text_surface.get_rect(center=BOX_RECT.center))

# ---------- Class ----------
class Block:
    def __init__(self, x, y, w, h, color, item: Item = None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.item = item
        self.dragging = False
        self.offset = (0, 0)
        self.spawn_point = (x, y)
        self.last_r_state = False
        self._base_image = None
        self._rotation_quarters = 0

    def _ensure_base_image(self):
        if not (self.item and getattr(self.item.definition, "image_path", None)):
            return
        if self._base_image is not None:
            return
        try:
            path = self.item.definition.image_path.replace("\\", "/")
            self._base_image = pygame.image.load(path).convert_alpha()
        except Exception as e:
            print("⚠️ โหลดรูปไม่สำเร็จ:", e)

    def _make_scaled_surface(self, img, pad=2, trim_alpha=5):
        angle = -90 * (self._rotation_quarters % 4)
        rotated = pygame.transform.rotate(img, angle)
        try:
            trim_rect = rotated.get_bounding_rect(min_alpha=trim_alpha)
            trimmed = rotated.subsurface(trim_rect).copy()
        except Exception:
            trimmed = rotated
        rw, rh = self.rect.width, self.rect.height
        inner_w, inner_h = rw - pad * 2, rh - pad * 2
        iw, ih = trimmed.get_size()
        ratio = iw / ih
        box_ratio = inner_w / inner_h
        if ratio > box_ratio:
            new_w, new_h = inner_w, int(inner_w / ratio)
        else:
            new_h, new_w = inner_h, int(inner_h * ratio)
        scaled = pygame.transform.smoothscale(trimmed, (new_w, new_h))
        x = self.rect.x + pad + (inner_w - new_w) // 2
        y = self.rect.y + pad + (inner_h - new_h) // 2
        return scaled, (x, y)

    def draw(self):
        self._ensure_base_image()
        if self._base_image is not None:
            img, pos = self._make_scaled_surface(self._base_image)
            SCREEN.blit(img, pos)
        else:
            pygame.draw.rect(SCREEN, self.color, self.rect)
        pygame.draw.rect(SCREEN, BLACK, self.rect, 2)

    def handle_event(self, event, all_blocks, keys):
        removed = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.dragging = True
            mx, my = event.pos
            self.offset = (self.rect.x - mx, self.rect.y - my)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                if TRASH_RECT.colliderect(self.rect):
                    removed = True
                else:
                    self.snap_to_nearest(all_blocks)
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            self.rect.x = mx + self.offset[0]
            self.rect.y = my + self.offset[1]
        if self.dragging:
            if keys[pygame.K_r] and not self.last_r_state:
                self.rotate()
                self.last_r_state = True
            elif not keys[pygame.K_r]:
                self.last_r_state = False
        return removed

    def rotate(self):
        if self.item and not self.item.can_rotate():
            return
        center = self.rect.center
        self.rect.width, self.rect.height = self.rect.height, self.rect.width
        self.rect.center = center
        self._rotation_quarters = (self._rotation_quarters + 1) % 4
        if self.item:
            self.item.rotate()

    def snap_to_nearest(self, all_blocks):
        ox1, oy1 = GRID_ORIGIN
        ox2, oy2 = SPAWN_ORIGIN
        cx, cy = self.rect.center
        grid_center = (ox1 + COLS * GRID_SIZE / 2, oy1 + ROWS * GRID_SIZE / 2)
        spawn_center = (ox2 + 3 * GRID_SIZE / 2, oy2 + 3 * GRID_SIZE / 2)
        dist_grid = abs(cx - grid_center[0]) + abs(cy - grid_center[1])
        dist_spawn = abs(cx - spawn_center[0]) + abs(cy - spawn_center[1])
        ox, oy = (ox1, oy1) if dist_grid < dist_spawn else (ox2, oy2)
        cols = COLS if dist_grid < dist_spawn else 3
        rows = ROWS if dist_grid < dist_spawn else 3
        col = int((self.rect.centerx - ox) // GRID_SIZE)
        row = int((self.rect.centery - oy) // GRID_SIZE)
        col = max(0, min(col, cols - (self.rect.width // GRID_SIZE)))
        row = max(0, min(row, rows - (self.rect.height // GRID_SIZE)))
        new_x, new_y = ox + col * GRID_SIZE, oy + row * GRID_SIZE
        new_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)
        if any(b is not self and new_rect.colliderect(b.rect) for b in all_blocks):
            self.rect.x, self.rect.y = self.spawn_point
        else:
            self.rect.x, self.rect.y = new_x, new_y
            self.spawn_point = (self.rect.x, self.rect.y)

# ---------- Helper ----------
def is_item_in_spawn_zone(block): return SPAWN_RECT.colliderect(block.rect)
def is_item_in_inventory_zone(block): return INVENTORY_RECT.colliderect(block.rect)
def calc_inventory_total_value(blocks): return sum(b.item.total_value for b in blocks if b.item and is_item_in_inventory_zone(b))
def create_block_from_item(item: Item):
    w, h = item_pixel_size(item, GRID_SIZE)
    sx, sy = SPAWN_RECT.centerx - w // 2, SPAWN_RECT.centery - h // 2
    return Block(sx, sy, w, h, random.choice(ITEM_COLORS), item=item)

# ---------- Drop Table ----------
DROP_WEIGHTS = {
    "Purified Water": 20,
    "Battery":        20,
    "RTX GPU":        20,
    "Medkit":         20,
    "Canned Food":    80,
}

FACTORIES = {
    "Purified Water": lambda: make_trial_item(1),
    "Battery":        (lambda: make_battery_item(1)) if callable(make_battery_item) else None,
    "RTX GPU":        (lambda: make_rtx_item(1))     if callable(make_rtx_item) else None,
    "Medkit":         (lambda: make_medkit_item(1))  if callable(make_medkit_item) else None,
    "Canned Food":    (lambda: make_canfood_item(1)) if callable(make_canfood_item) else None,
}

def build_drop_table():
    table = []
    for name, weight in DROP_WEIGHTS.items():
        fac = FACTORIES.get(name)
        if fac is None or weight <= 0:
            continue
        table.append({"name": name, "factory": fac, "weight": weight})
    return table

DROP_TABLE = build_drop_table()

def roll_item_from_drop_table():
    entries = [e for e in DROP_TABLE if e.get("weight", 0) > 0]
    total = sum(e["weight"] for e in entries)
    r = random.uniform(0, total)
    acc = 0.0
    for e in entries:
        acc += e["weight"]
        if r <= acc:
            return e["factory"]()
    return entries[-1]["factory"]()

# ---------- Main ----------
blocks, clock = [], pygame.time.Clock()

while True:
    # ---------- Timer Update ----------
    elapsed_ms = pygame.time.get_ticks() - start_ticks
    elapsed_sec = elapsed_ms // 1000
    remaining = max(0, countdown_time - elapsed_sec)
    if remaining == 0:
        time_up = True
    if not time_up:
        SCREEN.blit(bgimg,(0,0))
        draw_grid(GRID_ORIGIN)
        draw_item_box()
        draw_spawn_zone()
        draw_trash()
        draw_menu_button(SCREEN, MENU_BTN_CENTER, MENU_BTN_RADIUS)
        for b in blocks:
            b.draw()
        draw_inventory_value(calc_inventory_total_value(blocks))

        #time text
        minutes = remaining // 60
        seconds = remaining % 60
        timer_color = RED if remaining <= 10 else BLACK  # แดงเมื่อเหลือ 10 วินาที
        timer_text = timer_font.render(f"{minutes:02d}:{seconds:02d}", True, timer_color)
        timer_x = SCREEN_WIDTH // 2 - timer_text.get_width() // 2
        timer_y = 20  # 20px จากขอบบน
            # วาดกรอบสี่เหลี่ยมล้อมรอบ
        padding = 10
        timer_rect = pygame.Rect(
            timer_x - padding,
            timer_y - padding,
            timer_text.get_width() + padding*2,
            timer_text.get_height() + padding*2
        )
        pygame.draw.rect(SCREEN, WHITE, timer_rect,border_radius=15)       # กรอบพื้นหลังสีขาว
        pygame.draw.rect(SCREEN, BLACK, timer_rect, 3,border_radius=15)    # ขอบสีดำหนา 3
        SCREEN.blit(timer_text, (timer_x, timer_y))
         # --- หน้าจอ Time's Up --- 
    else:
        SCREEN.blit(happy_img, (0,0)) 
        text_surface = timer_font.render("Time's Up!", True, RED) 
        rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6)) 
        pygame.draw.rect(SCREEN, WHITE, rect.inflate(40, 20), border_radius=15) 
        pygame.draw.rect(SCREEN, BLACK, rect.inflate(40, 20), 4, border_radius=15) 
        SCREEN.blit(text_surface, rect) 
        if not score_added: 
            score = calc_inventory_total_value(blocks) 
            add_score(player_name,score) 
            score_added = True 
            # แสดง leaderboard 
        leaderboard_width = 700 
        leaderboard_height = 500 
        leaderboard_x = SCREEN_WIDTH//2 - leaderboard_width//2 
        leaderboard_y = SCREEN_HEIGHT//2 - leaderboard_height//2 
        leaderboard_rect = pygame.Rect(leaderboard_x, leaderboard_y, leaderboard_width, leaderboard_height) 
        pygame.draw.rect(SCREEN, WHITE, leaderboard_rect, border_radius=10) 
        pygame.draw.rect(SCREEN, BLACK, leaderboard_rect, 3, border_radius=10) 
        show_leaderboard(SCREEN, small_font, leaderboard_x+20, leaderboard_y+20)

        #Play again
        play_again_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT*5//6)  # อยู่ล่างสุด
        draw_play_again_button(SCREEN)
    # ---------- Event Handling ----------
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            calc_layout()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos
                dx = mx - MENU_BTN_CENTER[0]
                dy = my - MENU_BTN_CENTER[1]
                if dx*dx + dy*dy <= MENU_BTN_RADIUS*MENU_BTN_RADIUS:
                    subprocess.Popen(["python", "main.py"])
                    pygame.quit(); sys.exit()
                elif BOX_RECT.collidepoint(event.pos):
                    if any(is_item_in_spawn_zone(b) for b in blocks):
                        print("⚠️ ต้องย้าย item ใน spawn zone ออกก่อน!")
                    else:
                        new_item = roll_item_from_drop_table()
                        new_block = create_block_from_item(new_item)
                        blocks.append(new_block)
                elif time_up and play_again_rect.collidepoint(event.pos):
                    # รีเซ็ตเกม
                    blocks.clear()
                    start_ticks = pygame.time.get_ticks()
                    time_up = False
                    score_added = False

        for b in list(blocks):
            if b.handle_event(event, blocks, keys):
                blocks.remove(b)

    pygame.display.flip()
    clock.tick(60)
