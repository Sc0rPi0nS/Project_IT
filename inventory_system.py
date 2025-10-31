import pygame
import sys
import random
import os
import json
import subprocess
# ---------- item_class ----------
from item_class import Item, make_trial_item, item_pixel_size\
    , make_medkit_item, make_battery_item, make_rtx_item, make_canfood_item, make_dirwater_item, make_cucumber_item\
    , make_Flashlight_item, make_Bandage_item, make_DirtMeat_item, make_Antivirus_item, make_Baseball_item, make_Binocular_item\
    , make_Bread_item, make_Compass_item, make_EnergyBar_item, make_Glasses_item, make_Keyboard_item, make_Lighter_item\
    , make_Mouse_item, make_Converse_item, make_Jordan_item, make_Mac_item, make_Mask_item, make_Msi_item, make_Opthus_item\
    , make_Panda_item, make_Puma_item, make_Radio_item, make_Vans_item, make_IT_item

pygame.init()

SCREEN = pygame.display.set_mode((920, 750))
pygame.display.set_caption("Dual Inventory System (No Stack Overlay)")

##json
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

volume = float(sys.argv[1]) if len(sys.argv) > 2 else 1
player_name = sys.argv[2] if len(sys.argv) > 1 else "Guest"
pygame.mixer.music.load("sound/bg_music.mp3")
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

## ---------- Timer ----------
countdown_time = 30 # (1 นาที)
start_ticks = pygame.time.get_ticks()

# ---------------- BACKGROUND ----------------
bgimg = pygame.image.load("background/Inventory backg.png").convert_alpha()
bgimg = pygame.transform.scale(bgimg, (920, 750))
happy_img = pygame.image.load("background/Victory.png").convert_alpha()
happy_img = pygame.transform.scale(happy_img, (920, 750))
## ---------- Font ----------
score_font = pygame.font.SysFont("bytebounce", 25)
timer_font = pygame.font.SysFont("bytebounce", 120)  # 60 px
time_up = False
score_added = False
small_font = pygame.font.SysFont("bytebounce", 60)

# ---------- Grid / Layout (calibrated) ----------
GRID_SIZE = 65
ROWS, COLS = 5, 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
DARK_RED = (150, 0, 0)
green = (0, 255, 0)
frame = (96, 62, 62)
brown = (218, 169, 107)
text_press = (145, 92, 67)
ITEM_COLORS = [(255, 80, 80), (80, 200, 120), (80, 120, 255), (255, 220, 100)]

TOTAL_GRID_WIDTH  = COLS * GRID_SIZE
TOTAL_GRID_HEIGHT = ROWS * GRID_SIZE

# กริดใหญ่ซ้าย (Inventory 5x5)
GRID_ORIGIN = (153, 286)
INVENTORY_RECT = pygame.Rect(GRID_ORIGIN[0], GRID_ORIGIN[1], TOTAL_GRID_WIDTH, TOTAL_GRID_HEIGHT)

# ปุ่ม Search (2x1 ช่อง)
BOX_WIDTH, BOX_HEIGHT = GRID_SIZE * 2, GRID_SIZE
BOX_RECT = pygame.Rect(579, 287, BOX_WIDTH, BOX_HEIGHT)

# กริด Spawn 3x3 (กระจกขวา)
SPAWN_ROWS, SPAWN_COLS = 3, 3
SPAWN_ORIGIN = (547, 373)
SPAWN_RECT = pygame.Rect(SPAWN_ORIGIN[0], SPAWN_ORIGIN[1], SPAWN_COLS * GRID_SIZE, SPAWN_ROWS * GRID_SIZE)

# ปุ่ม/พื้นที่ TRASH
TRASH_RECT = pygame.Rect(578, 597, GRID_SIZE * 2, GRID_SIZE)

# ปุ่มปิดเกม (Responsive)
menu_radius = int(min(920, 750) * 0.035 * 1.4)
menu_x = 920 - menu_radius - 20
menu_y = menu_radius + 20
global MENU_BTN_CENTER, MENU_BTN_RADIUS
MENU_BTN_CENTER = (menu_x, menu_y)
MENU_BTN_RADIUS = menu_radius

# ------------------ ฟังก์ชันวาด ------------------
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
    # เพิ่มหัวข้อ "Top 10"
    header_font = pygame.font.SysFont("bytebounce", 35)
    header_text = header_font.render("Top 10", True, BLACK)
    surface.blit(header_text, (start_x+45, y))
    y += header_text.get_height() + 10  # เว้นระยะก่อนอันดับ 1
    for idx, entry in enumerate(leaderboard):
        text = score_font.render(f"{idx+1}. {entry['name']} - {entry['score']}", True, BLACK)
        surface.blit(text, (start_x, y))
        y += text.get_height() + 5

# ---------- Drawing ----------
play_again_rect = pygame.Rect(0, 0, 250, 70)
play_again_rect.center = (920//2, 750//2 + 150)  # วางใต้ข้อความ Time's Up

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

# ---------- ควบคุมการแสดงปุ่ม ----------
SHOW_BUTTONS = False          # False = ไม่วาดปุ่ม (ล่องหน แต่ยังคลิกได้)
SHOW_HITBOX_WHEN_HOLD = True  # กดค้าง H เพื่อโชว์กรอบ hitbox ชั่วคราว

# ---------- ค่าความโปร่งใสของกริด ----------
GRID_LINE_ALPHA = 110          # ยิ่งต่ำยิ่งโปร่ง (แนะนำ 80–140)
GRID_BORDER_ALPHA = 170
GRID_LINE_COLOR   = (255, 255, 255, GRID_LINE_ALPHA)   # เส้นขาวโปร่งใส
GRID_BORDER_COLOR = (0, 0, 0, GRID_BORDER_ALPHA)       # กรอบดำโปร่งใส

# ---------- ควบคุมการแสดงปุ่ม ----------
SHOW_BUTTONS = False          # False = ไม่วาดปุ่ม (ล่องหน แต่ยังคลิกได้)
SHOW_HITBOX_WHEN_HOLD = True  # กดค้าง H เพื่อโชว์กรอบ hitbox ชั่วคราว

# ---------- ค่าความโปร่งใสของกริด ----------
GRID_LINE_ALPHA = 110          # ยิ่งต่ำยิ่งโปร่ง (แนะนำ 80–140)
GRID_BORDER_ALPHA = 170
GRID_LINE_COLOR   = (255, 255, 255, GRID_LINE_ALPHA)   # เส้นขาวโปร่งใส
GRID_BORDER_COLOR = (0, 0, 0, GRID_BORDER_ALPHA)       # กรอบดำโปร่งใส

# ------------------ ฟังก์ชันวาด ------------------
def draw_grid_alpha(origin, rows, cols, cell_size, line_color, border_color, border_w=2):
    """วาดกริดโปร่งใสลงบน Surface แบบ SRCALPHA แล้ว blit ทับพื้นหลัง"""
    w, h = cols * cell_size, rows * cell_size
    surf = pygame.Surface((w, h), pygame.SRCALPHA)

    # เส้นแนวตั้ง
    for c in range(cols + 1):
        x = c * cell_size
        pygame.draw.line(surf, line_color, (x, 0), (x, h), 1)

    # เส้นแนวนอน
    for r in range(rows + 1):
        y = r * cell_size
        pygame.draw.line(surf, line_color, (0, y), (w, y), 1)

    # เส้นกรอบรอบนอก
    pygame.draw.rect(surf, border_color, (0, 0, w, h), border_w)

    SCREEN.blit(surf, origin)

def draw_inventory_grid():
    draw_grid_alpha(GRID_ORIGIN, ROWS, COLS, GRID_SIZE, GRID_LINE_COLOR, GRID_BORDER_COLOR, border_w=2)

def draw_spawn_grid():
    draw_grid_alpha(SPAWN_ORIGIN, SPAWN_ROWS, SPAWN_COLS, GRID_SIZE, GRID_LINE_COLOR, GRID_BORDER_COLOR, border_w=3)

def draw_inventory_value(total_value):
    font = pygame.font.SysFont(None, 28)
    text_surface = font.render(f"Value : {total_value}", True, BLACK)
    text_x = INVENTORY_RECT.centerx - text_surface.get_width() // 2
    text_y = INVENTORY_RECT.bottom + 10
    SCREEN.blit(text_surface, (text_x, text_y))

def draw_trash():
# ล่องหนโดยไม่วาดปุ่ม แต่ยังใช้ TRASH_RECT ตรวจชนได้
    # ล่องหนโดยไม่วาดปุ่ม แต่ยังใช้ TRASH_RECT ตรวจชนได้
    if SHOW_BUTTONS:
        pygame.draw.rect(SCREEN, (240, 240, 240), TRASH_RECT)
        pygame.draw.rect(SCREEN, BLACK, TRASH_RECT, 3)
        font = pygame.font.SysFont(None, 28)
        text_surface = font.render("TRASH", True, BLACK)
        SCREEN.blit(text_surface, text_surface.get_rect(center=TRASH_RECT.center))
    elif SHOW_HITBOX_WHEN_HOLD and pygame.key.get_pressed()[pygame.K_h]:
        # โชว์กรอบเมื่อกดค้าง H (debug)
        debug = pygame.Surface(TRASH_RECT.size, pygame.SRCALPHA)
        debug.fill((255, 0, 0, 60))
        SCREEN.blit(debug, TRASH_RECT.topleft)
        pygame.draw.rect(SCREEN, (255, 0, 0), TRASH_RECT, 2)

def draw_item_box():
# ล่องหนโดยไม่วาดปุ่ม แต่ยังใช้ BOX_RECT ตรวจคลิกได้
    # ล่องหนโดยไม่วาดปุ่ม แต่ยังใช้ BOX_RECT ตรวจคลิกได้
    if SHOW_BUTTONS:
        pygame.draw.rect(SCREEN, (230, 230, 230), BOX_RECT)
        pygame.draw.rect(SCREEN, BLACK, BOX_RECT, 3)
        font = pygame.font.SysFont(None, 32)
        label = font.render("Search", True, BLACK)
        SCREEN.blit(label, label.get_rect(center=BOX_RECT.center))
    elif SHOW_HITBOX_WHEN_HOLD and pygame.key.get_pressed()[pygame.K_h]:
        # โชว์กรอบเมื่อกดค้าง H (debug)
        debug = pygame.Surface(BOX_RECT.size, pygame.SRCALPHA)
        debug.fill((0, 128, 255, 60))
        SCREEN.blit(debug, BOX_RECT.topleft)
        pygame.draw.rect(SCREEN, (0, 128, 255), BOX_RECT, 2)

# ------------------ คลาส Block ------------------
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
        grid_center  = (ox1 + COLS * GRID_SIZE / 2,  oy1 + ROWS * GRID_SIZE / 2)
        spawn_center = (ox2 + 3    * GRID_SIZE / 2,  oy2 + 3    * GRID_SIZE / 2)
        dist_grid  = abs(cx - grid_center[0])  + abs(cy - grid_center[1])
        dist_spawn = abs(cx - spawn_center[0]) + abs(cy - spawn_center[1])

        if dist_grid < dist_spawn:
            ox, oy, cols, rows = ox1, oy1, COLS, ROWS
        else:
            ox, oy, cols, rows = ox2, oy2, 3, 3

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
            if dist_grid >= dist_spawn:
                self.spawn_point = (self.rect.x, self.rect.y)

# ------------------ Helper ------------------
def is_item_in_spawn_zone(block): return SPAWN_RECT.colliderect(block.rect)
def is_item_in_inventory_zone(block): return INVENTORY_RECT.colliderect(block.rect)
def calc_inventory_total_value(blocks): return sum(b.item.total_value for b in blocks if b.item and is_item_in_inventory_zone(b))
def create_block_from_item(item: Item):
    w, h = item_pixel_size(item, GRID_SIZE)
    sx, sy = SPAWN_RECT.centerx - w // 2, SPAWN_RECT.centery - h // 2
    return Block(sx, sy, w, h, random.choice(ITEM_COLORS), item=item)

# ------------------ DROP TABLE ------------------
DROP_WEIGHTS = {
    "Purified Water": 10, "Battery": 15, "RTX GPU": 1, "Medkit": 10, "Canned Food": 10,
    "Dirty water": 20, "Cucamber": 25, "Flashlight": 15, "Bandage": 10, "Dirt Meat": 20,
    "Antivirus": 10, "Baseball Bat": 15, "Binoculars": 20, "Bread": 25, "Compass": 10,
    "Energy Bar": 10, "Glasses": 15, "Keyboard": 10, "Lighter": 15, "Mouse": 15,
    "Converse": 5, "Jordan": 3, "Mac": 3, "Mask": 10, "MSI": 3, "Opthus": 3,
    "Panda": 3, "Puma": 3, "Radio": 15, "Vans": 3, "IT": 1
}

FACTORIES = {
    "Purified Water": lambda: make_trial_item(1),
    "Battery":        (lambda: make_battery_item(1)) if callable(make_battery_item) else None,
    "RTX GPU":        (lambda: make_rtx_item(1))     if callable(make_rtx_item) else None,
    "Medkit":         (lambda: make_medkit_item(1))  if callable(make_medkit_item) else None,
    "Canned Food":    (lambda: make_canfood_item(1)) if callable(make_canfood_item) else None,
    "Dirty water":    (lambda: make_dirwater_item(1)) if callable(make_dirwater_item) else None,
    "Cucamber":       (lambda: make_cucumber_item(1)) if callable(make_cucumber_item) else None,
    "Flashlight":     (lambda: make_Flashlight_item(1)) if callable(make_Flashlight_item) else None,
    "Bandage":        (lambda: make_Bandage_item(1)) if callable(make_Bandage_item) else None,
    "Dirt Meat":      (lambda: make_DirtMeat_item(1)) if callable(make_DirtMeat_item) else None,
    "Antivirus":      (lambda: make_Antivirus_item(1)) if callable(make_Antivirus_item) else None,
    "Baseball Bat":   (lambda: make_Baseball_item(1)) if callable(make_Baseball_item) else None,
    "Binoculars":     (lambda: make_Binocular_item(1)) if callable(make_Binocular_item) else None,
    "Bread":          (lambda: make_Bread_item(1)) if callable(make_Bread_item) else None,
    "Compass":        (lambda: make_Compass_item(1)) if callable(make_Compass_item) else None,
    "Energy Bar":     (lambda: make_EnergyBar_item(1)) if callable(make_EnergyBar_item) else None,
    "Glasses":        (lambda: make_Glasses_item(1)) if callable(make_Glasses_item) else None,
    "Keyboard":       (lambda: make_Keyboard_item(1)) if callable(make_Keyboard_item) else None,
    "Lighter":        (lambda: make_Lighter_item(1)) if callable(make_Lighter_item) else None,
    "Mouse":          (lambda: make_Mouse_item(1)) if callable(make_Mouse_item) else None,
    "Converse":       (lambda: make_Converse_item(1)) if callable(make_Converse_item) else None,
    "Jordan":         (lambda: make_Jordan_item(1)) if callable(make_Jordan_item) else None,
    "Mac":            (lambda: make_Mac_item(1)) if callable(make_Mac_item) else None,
    "Mask":           (lambda: make_Mask_item(1)) if callable(make_Mask_item) else None,
    "MSI":            (lambda: make_Msi_item(1)) if callable(make_Msi_item) else None,
    "Opthus":         (lambda: make_Opthus_item(1)) if callable(make_Opthus_item) else None,
    "Panda":          (lambda: make_Panda_item(1)) if callable(make_Panda_item) else None,
    "Puma":           (lambda: make_Puma_item(1)) if callable(make_Puma_item) else None,
    "Radio":          (lambda: make_Radio_item(1)) if callable(make_Radio_item) else None,
    "Vans":           (lambda: make_Vans_item(1)) if callable(make_Vans_item) else None,
    "IT":             (lambda: make_IT_item(1)) if callable(make_IT_item) else None
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

def show_drop_rates():
    total = sum(d["weight"] for d in DROP_TABLE)
    print("\n🎯 Current Drop Rates:")
    if total <= 0 or not DROP_TABLE:
        print(" (empty)")
    else:
        for d in DROP_TABLE:
            pct = (d["weight"] / total * 100)
            print(f" - {d['name']:<15}: {pct:>5.1f}%")
    print("──────────────────────────────")

def roll_item_from_drop_table():
    entries = [e for e in DROP_TABLE if e.get("weight", 0) > 0]
    if not entries:
        return make_trial_item(1)
    total = sum(e["weight"] for e in entries)
    r = random.uniform(0, total)
    acc = 0.0
    for e in entries:
        acc += e["weight"]
        if r <= acc:
            return e["factory"]()
    return entries[-1]["factory"]()

# ------------------ Main ------------------
blocks, clock = [], pygame.time.Clock()
show_drop_rates()

while True:
# ---------- Timer Update ----------
    elapsed_ms = pygame.time.get_ticks() - start_ticks
    elapsed_sec = elapsed_ms // 1000
    remaining = max(0, countdown_time - elapsed_sec)
    if remaining == 0:
        time_up = True
    if not time_up:
        SCREEN.blit(bgimg,(0,0))
        # วาดกริดแบบโปร่งใส
        draw_spawn_grid()
        draw_item_box()
        draw_trash()
        draw_inventory_grid()
        draw_menu_button(SCREEN, MENU_BTN_CENTER, MENU_BTN_RADIUS)
        for b in blocks:
            b.draw()
        draw_inventory_value(calc_inventory_total_value(blocks))

        #time text
        minutes = remaining // 60
        seconds = remaining % 60
        timer_color = RED if remaining <= 10 else BLACK  # แดงเมื่อเหลือ 10 วินาที
        timer_text = timer_font.render(f"{minutes:02d}:{seconds:02d}", True, timer_color)
        timer_x = 920 // 2 - timer_text.get_width() // 2
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
    else:
        # --- หน้าจอ Time's Up --- 
        SCREEN.blit(happy_img, (0,0)) 
        if not score_added: 
            score = calc_inventory_total_value(blocks) 
            add_score(player_name,score) 
            score_added = True 
        name_font = pygame.font.SysFont("bytebounce", 60)
        # --- ฟังก์ชันวาดข้อความพร้อม outline ---
        def draw_text_with_outline(text, font, text_color, outline_color, pos, outline_thickness=3):
            base_surface = font.render(text, True, text_color)
            for dx in [-outline_thickness, 0, outline_thickness]:
                for dy in [-outline_thickness, 0, outline_thickness]:
                    if dx != 0 or dy != 0:
                        outline_surface = font.render(text, True, outline_color)
                        SCREEN.blit(outline_surface, (pos[0] + dx, pos[1] + dy))
            SCREEN.blit(base_surface, pos)

        # --- Player name ---
        name_text = f"Player: {player_name}"
        name_surface = name_font.render(name_text, True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(920//2, 300))
        draw_text_with_outline(name_text, name_font, BLACK, WHITE, name_rect.topleft)

        # --- Score ---
        score_text = f"Score: {score}"
        score_surface = name_font.render(score_text, True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(920//2, name_rect.bottom + 40))
        draw_text_with_outline(score_text, name_font, BLACK, WHITE, score_rect.topleft)

        # แสดง leaderboard 
        leaderboard_width = int(920 * 0.25) 
        leaderboard_height = int(750 * 0.4) 
        leaderboard_x = 920 - leaderboard_width - 50 
        leaderboard_y = 750*0.35 
        leaderboard_rect = pygame.Rect(leaderboard_x, leaderboard_y, leaderboard_width, leaderboard_height) 

        pygame.draw.rect(SCREEN, brown, leaderboard_rect, border_radius=10) 
        pygame.draw.rect(SCREEN, frame, leaderboard_rect, 3, border_radius=10)
        # หัวข้อ Leaderboard ด้านบนกรอบ
        title_font = pygame.font.SysFont("bytebounce", 40)
        title_surface = title_font.render("Leaderboard", True, BLACK)
        
        # จัดตำแหน่งให้อยู่เหนือกรอบนิดหน่อย (กลางแนวนอน)
        title_x = leaderboard_rect.centerx - title_surface.get_width() // 2
        title_y = leaderboard_rect.top - title_surface.get_height() - 10  # 10px เหนือกรอบ
        title_rect = title_surface.get_rect(topleft=(title_x, title_y))
        #outline
        outline_color = frame
        outline_thickness = 3
        for dx in [-outline_thickness, 0, outline_thickness]:
            for dy in [-outline_thickness, 0, outline_thickness]:
                if dx != 0 or dy != 0:  # ข้ามตำแหน่งตรงกลาง
                    outline_text = title_font.render("Leaderboard", True, WHITE)
                    SCREEN.blit(outline_text, title_rect.move(dx, dy))

        SCREEN.blit(title_surface, (title_x, title_y))
        show_leaderboard(SCREEN, small_font, leaderboard_x+20, leaderboard_y+20)

        #Play again
        play_again_rect.center = (920//2, 750*5//6)  # อยู่ล่างสุด
        draw_play_again_button(SCREEN)


    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit(); sys.exit()
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
        for b in blocks[:]:
            if b.handle_event(event, blocks, keys):
                blocks.remove(b)

    pygame.display.flip()
    clock.tick(60)
