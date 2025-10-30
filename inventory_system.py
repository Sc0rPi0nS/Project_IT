import pygame
import sys
import random
# เชื่อมกับ item_class
from item_class import Item, make_trial_item, item_pixel_size\
    , make_medkit_item, make_battery_item, make_rtx_item, make_canfood_item,make_dirwater_item,make_cucumber_item\
    , make_Flashlight_item, make_Bandage_item, make_DirtMeat_item, make_Antivirus_item, make_Baseball_item, make_Binocular_item\
    , make_Bread_item, make_Compass_item, make_EnergyBar_item, make_Glasses_item, make_Keyboard_item, make_Lighter_item\
    , make_Mouse_item, make_Converse_item, make_Jordan_item, make_Mac_item, make_Mask_item, make_Msi_item, make_Opthus_item\
    , make_Panda_item, make_Puma_item, make_Radio_item, make_Vans_item, make_IT_item

pygame.init()

SCREEN = pygame.display.set_mode((920, 750))
pygame.display.set_caption("Dual Inventory System (No Stack Overlay)")

GRID_SIZE = 60
ROWS, COLS = 5, 5
MARGIN_TOP = 140

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
ITEM_COLORS = [(255, 80, 80), (80, 200, 120), (80, 120, 255), (255, 220, 100)]

# ---------- Layout ----------
TOTAL_GRID_WIDTH = COLS * GRID_SIZE
TOTAL_GRID_HEIGHT = ROWS * GRID_SIZE
GAP_X = 100
start_x = (920 - (TOTAL_GRID_WIDTH + GAP_X + GRID_SIZE * 2)) // 2
GRID_ORIGIN = (start_x, MARGIN_TOP)
INVENTORY_RECT = pygame.Rect(GRID_ORIGIN[0], GRID_ORIGIN[1], TOTAL_GRID_WIDTH, TOTAL_GRID_HEIGHT)

BOX_WIDTH, BOX_HEIGHT = GRID_SIZE * 2, GRID_SIZE
BOX_X = GRID_ORIGIN[0] + TOTAL_GRID_WIDTH + GAP_X
BOX_Y = MARGIN_TOP
BOX_RECT = pygame.Rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT)

SPAWN_ROWS, SPAWN_COLS = 3, 3
SPAWN_WIDTH, SPAWN_HEIGHT = SPAWN_COLS * GRID_SIZE, SPAWN_ROWS * GRID_SIZE
SPAWN_X = BOX_X + BOX_WIDTH // 2 - SPAWN_WIDTH // 2
SPAWN_Y = BOX_RECT.bottom + 20
SPAWN_ORIGIN = (SPAWN_X, SPAWN_Y)
SPAWN_RECT = pygame.Rect(SPAWN_X, SPAWN_Y, SPAWN_WIDTH, SPAWN_HEIGHT)

TRASH_RECT = pygame.Rect(SPAWN_RECT.centerx - GRID_SIZE, SPAWN_RECT.bottom + 30, GRID_SIZE * 2, GRID_SIZE)

# ------------------ ฟังก์ชันวาด ------------------
def draw_grid(origin):
    ox, oy = origin
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(SCREEN, GRAY, (ox + c * GRID_SIZE, oy + r * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def draw_inventory_value(total_value):
    font = pygame.font.SysFont(None, 28)
    text_surface = font.render(f"Value : {total_value}", True, BLACK)
    text_x = INVENTORY_RECT.centerx - text_surface.get_width() // 2
    text_y = INVENTORY_RECT.bottom + 10
    SCREEN.blit(text_surface, (text_x, text_y))

def draw_spawn_zone():
    ox, oy = SPAWN_ORIGIN
    for r in range(SPAWN_ROWS):
        for c in range(SPAWN_COLS):
            pygame.draw.rect(SCREEN, (220, 240, 255),
                             (ox + c * GRID_SIZE, oy + r * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
    pygame.draw.rect(SCREEN, BLACK, SPAWN_RECT, 3)

def draw_trash():
    pygame.draw.rect(SCREEN, (240, 240, 240), TRASH_RECT)
    pygame.draw.rect(SCREEN, BLACK, TRASH_RECT, 3)
    font = pygame.font.SysFont(None, 28)
    text_surface = font.render("TRASH", True, BLACK)
    SCREEN.blit(text_surface, text_surface.get_rect(center=TRASH_RECT.center))

def draw_item_box():
    pygame.draw.rect(SCREEN, (230, 230, 230), BOX_RECT)
    pygame.draw.rect(SCREEN, BLACK, BOX_RECT, 3)
    font = pygame.font.SysFont(None, 32)
    SCREEN.blit(font.render("Search", True, BLACK),
                font.render("Search", True, BLACK).get_rect(center=BOX_RECT.center))


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
        # ❌ ไม่มีเลขคูณ x1/xN อีกต่อไป

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
        spawn_center = (ox2 + SPAWN_COLS * GRID_SIZE / 2, oy2 + SPAWN_ROWS * GRID_SIZE / 2)
        dist_grid = abs(cx - grid_center[0]) + abs(cy - grid_center[1])
        dist_spawn = abs(cx - spawn_center[0]) + abs(cy - spawn_center[1])
        ox, oy = (ox1, oy1) if dist_grid < dist_spawn else (ox2, oy2)
        cols = COLS if dist_grid < dist_spawn else SPAWN_COLS
        rows = ROWS if dist_grid < dist_spawn else SPAWN_ROWS
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

# ------------------DROP TABLE------------------
# ปรับเรทแค่ตรงนี้พอ! (ไม่ต้องรวมเป็น 100 ก็ได้)
DROP_WEIGHTS = {
    "Purified Water": 10,
    "Battery":        15,
    "RTX GPU":        1,
    "Medkit":         10,
    "Canned Food":    10,
    "Dirty water":    20,
    "Cucamber":      25,
    "Flashlight":     15,
    "Bandage":        10,
    "Dirt Meat": 20,
    "Antivirus": 10,
    "Baseball Bat": 15,
    "Binoculars": 20,
    "Bread": 25,
    "Compass": 10,
    "Energy Bar": 10,
    "Glasses": 15,
    "Keyboard": 10,
    "Lighter": 15,
    "Mouse": 15,
    "Converse": 5,
    "Jordan": 3,
    "Mac": 3,
    "Mask": 10,
    "MSI": 3,
    "Opthus": 3,
    "Panda": 3,
    "Puma" : 3,
    "Radio": 15,
    "Vans" : 3,
    "IT" : 0.1
}

# map ชื่อ -> factory (เฉพาะตัวที่มีอยู่จริง)
FACTORIES = {
    "Purified Water": lambda: make_trial_item(1),
    "Battery":        (lambda: make_battery_item(1)) if callable(make_battery_item) else None,
    "RTX GPU":        (lambda: make_rtx_item(1))     if callable(make_rtx_item) else None,
    "Medkit":         (lambda: make_medkit_item(1))  if callable(make_medkit_item) else None,
    "Canned Food":    (lambda: make_canfood_item(1)) if callable(make_canfood_item) else None,
    "Dirty water":    (lambda: make_dirwater_item(1)) if callable(make_dirwater_item) else None,
    "Cucamber":      (lambda: make_cucumber_item(1)) if callable(make_cucumber_item) else None,
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
    "IT":           (lambda: make_IT_item(1)) if callable(make_IT_item) else None
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
        # กันพังถ้าเผลอลบหมด
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
    SCREEN.fill(WHITE)
    draw_grid(GRID_ORIGIN)
    draw_item_box()
    draw_spawn_zone()
    draw_trash()
    for b in blocks:
        b.draw()
    draw_inventory_value(calc_inventory_total_value(blocks))

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit(); sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and BOX_RECT.collidepoint(event.pos):
            if any(is_item_in_spawn_zone(b) for b in blocks):
                print("⚠️ ต้องย้าย item ใน spawn zone ออกก่อน!")
            else:
                new_item = roll_item_from_drop_table()
                new_block = create_block_from_item(new_item)
                blocks.append(new_block)
        for b in list(blocks):
            if b.handle_event(event, blocks, keys):
                blocks.remove(b)

    pygame.display.flip()
    clock.tick(60)
