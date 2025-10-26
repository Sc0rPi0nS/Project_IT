import pygame
import sys
import random
from item_class import Item, make_trial_item, item_pixel_size  # เชื่อมกับ item_class

pygame.init()

SCREEN = pygame.display.set_mode((920, 750))
SCREEN_WIDTH, SCREEN_HEIGHT = 920, 750
pygame.display.set_caption("Dual Inventory System (Contain + Auto-Trim)")

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

total_width = TOTAL_GRID_WIDTH + GAP_X + GRID_SIZE * 2
start_x = (SCREEN_WIDTH - total_width) // 2

GRID_ORIGIN = (start_x, MARGIN_TOP)

INVENTORY_RECT = pygame.Rect(
    GRID_ORIGIN[0],
    GRID_ORIGIN[1],
    TOTAL_GRID_WIDTH,
    TOTAL_GRID_HEIGHT
)


BOX_WIDTH, BOX_HEIGHT = GRID_SIZE * 2, GRID_SIZE
BOX_X = GRID_ORIGIN[0] + TOTAL_GRID_WIDTH + GAP_X
BOX_Y = MARGIN_TOP
BOX_RECT = pygame.Rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT)

SPAWN_ROWS, SPAWN_COLS = 3, 3
SPAWN_WIDTH = SPAWN_COLS * GRID_SIZE
SPAWN_HEIGHT = SPAWN_ROWS * GRID_SIZE
SPAWN_X = BOX_X + BOX_WIDTH // 2 - SPAWN_WIDTH // 2
SPAWN_Y = BOX_RECT.bottom + 20
SPAWN_ORIGIN = (SPAWN_X, SPAWN_Y)
SPAWN_RECT = pygame.Rect(SPAWN_X, SPAWN_Y, SPAWN_WIDTH, SPAWN_HEIGHT)

TRASH_WIDTH = GRID_SIZE * 2
TRASH_HEIGHT = GRID_SIZE
TRASH_X = SPAWN_RECT.centerx - TRASH_WIDTH // 2
TRASH_Y = SPAWN_RECT.bottom + 30
TRASH_RECT = pygame.Rect(TRASH_X, TRASH_Y, TRASH_WIDTH, TRASH_HEIGHT)


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


# ------------------ คลาส Block (เห็นรูปเต็ม: contain + auto-trim) ------------------
class Block:
    def __init__(self, x, y, w, h, color, item: Item = None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.dragging = False
        self.offset = (0, 0)
        self.spawn_point = (x, y)
        self.last_r_state = False
        self.item = item

        # รูปภาพ
        self._base_image = None
        self._rotation_quarters = 0  # หมุนทีละ 90°

    # โหลดภาพจาก item_class
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
            self._base_image = None

    def _make_scaled_surface(self, img, pad=2, trim_alpha=5):
        """
        ย่อ/ขยายภาพแบบ 'contain' (เห็นภาพเต็มเสมอ ไม่ครอป ไม่ยืด)
        + 'auto-trim' ขอบโปร่งใสออกก่อน เพื่อให้รูปใหญ่ที่สุดในกรอบ
        """
        # 1) หมุน
        angle = -90 * (self._rotation_quarters % 4)
        rotated = pygame.transform.rotate(img, angle)

        # 2) ตัดขอบโปร่งใส (แก้ปัญหาไฟล์มีพื้นที่ว่างรอบ ๆ)
        #    ปรับ trim_alpha สูงขึ้น (10-30) ถ้าขอบยังหนา
        try:
            trim_rect = rotated.get_bounding_rect(min_alpha=trim_alpha)
            trimmed = rotated.subsurface(trim_rect).copy()
        except Exception:
            trimmed = rotated

        # 3) พื้นที่ภายในของกรอบ (หัก padding)
        rw, rh = self.rect.width, self.rect.height
        inner_w = max(1, rw - pad * 2)
        inner_h = max(1, rh - pad * 2)

        # 4) contain = รักษาอัตราส่วนให้ “ด้านยาวสุด” แตะขอบ, มี letterbox ถ้าสัดส่วนไม่ตรง
        iw, ih = trimmed.get_size()
        img_ratio = iw / ih
        box_ratio = inner_w / inner_h

        if img_ratio > box_ratio:
            # ภาพกว้างกว่า → fit ตามความกว้าง
            new_w = inner_w
            new_h = max(1, int(inner_w / img_ratio))
        else:
            # ภาพสูงกว่า/เท่ากัน → fit ตามความสูง
            new_h = inner_h
            new_w = max(1, int(inner_h * img_ratio))

        scaled = pygame.transform.smoothscale(trimmed, (new_w, new_h))

        # 5) จัดกลางในกรอบ
        x = self.rect.x + pad + (inner_w - new_w) // 2
        y = self.rect.y + pad + (inner_h - new_h) // 2
        return scaled, (x, y)

    # วาดภาพ
    def draw(self):
        self._ensure_base_image()
        if self._base_image is not None:
            img, pos = self._make_scaled_surface(self._base_image, pad=2, trim_alpha=5)
            SCREEN.blit(img, pos)
            pygame.draw.rect(SCREEN, BLACK, self.rect, 2)
        else:
            pygame.draw.rect(SCREEN, self.color, self.rect)
            pygame.draw.rect(SCREEN, BLACK, self.rect, 2)

        # จำนวน stack
        if self.item and getattr(self.item.definition, "stackable", False):
            font = pygame.font.SysFont(None, 18)
            qty = getattr(self.item, "quantity", 1)
            SCREEN.blit(font.render(f"x{qty}", True, BLACK),
                        (self.rect.right - 18, self.rect.bottom - 18))

    # จัดการ event (ลาก/หมุน/ทิ้ง)
    def handle_event(self, event, all_blocks, keys):
        removed = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
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

        # หมุนตอนลาก (R)
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
        if self.item:
            self.item.rotate()
        self._rotation_quarters = (self._rotation_quarters + 1) % 4

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
        target_zone = "inventory" if dist_grid < dist_spawn else "spawn"

        col = int((self.rect.centerx - ox) // GRID_SIZE)
        row = int((self.rect.centery - oy) // GRID_SIZE)
        max_col = cols - (self.rect.width // GRID_SIZE)
        max_row = rows - (self.rect.height // GRID_SIZE)
        col = max(0, min(col, max_col))
        row = max(0, min(row, max_row))
        new_x = ox + col * GRID_SIZE
        new_y = oy + row * GRID_SIZE
        new_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)

        if target_zone == "inventory":
            for b in all_blocks:
                if b is not self and new_rect.colliderect(b.rect):
                    self.rect.x, self.rect.y = self.spawn_point
                    return
        self.rect.x, self.rect.y = new_x, new_y
        if target_zone == "spawn":
            self.spawn_point = (self.rect.x, self.rect.y)


# ------------------ ฟังก์ชันช่วย ------------------
def is_item_in_spawn_zone(block):
    return SPAWN_RECT.colliderect(block.rect)

def is_item_in_inventory_zone(block):
    # ถือว่าอยู่ใน inventory ถ้า block วางซ้อนทับกริดทางซ้าย
    return INVENTORY_RECT.colliderect(block.rect)

def calc_inventory_total_value(blocks):
    total = 0
    for b in blocks:
        if b.item and is_item_in_inventory_zone(b):
            total += b.item.total_value  # ใช้ total_value จาก item_class
    return total

def create_block_from_item(item: Item):
    """แปลง Item จริงจาก item_class เป็น Block ในเกม"""
    w, h = item_pixel_size(item, GRID_SIZE)
    sx = SPAWN_RECT.centerx - w // 2
    sy = SPAWN_RECT.centery - h // 2
    color = random.choice(ITEM_COLORS)
    return Block(sx, sy, w, h, color, item=item)


# ------------------ เริ่มต้น ------------------
blocks = []
clock = pygame.time.Clock()

# ------------------ Loop หลัก ------------------
while True:
    SCREEN.fill(WHITE)
    draw_grid(GRID_ORIGIN)
    draw_item_box()
    draw_spawn_zone()
    draw_trash()

    for b in blocks:
        b.draw()

    # === คำนวณราคาแล้วแสดงใต้ inventory zone ===
    inv_total_value = calc_inventory_total_value(blocks)
    draw_inventory_value(inv_total_value)

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # คลิกปุ่ม Search → สุ่ม Item จาก item_class.py
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if BOX_RECT.collidepoint(event.pos):
                if any(is_item_in_spawn_zone(b) for b in blocks):
                    print("⚠️ ต้องย้าย item ใน spawn zone ออกก่อน!")
                else:
                    new_item = make_trial_item()
                    new_block = create_block_from_item(new_item)
                    blocks.append(new_block)
                    print(f"เพิ่ม item จาก item_class: {new_item}")

        # ลาก / หมุน / ทิ้ง
        to_remove = []
        for b in blocks:
            if b.handle_event(event, blocks, keys):
                to_remove.append(b)
        for dead in to_remove:
            if dead in blocks:
                blocks.remove(dead)

    pygame.display.flip()
    clock.tick(60)
