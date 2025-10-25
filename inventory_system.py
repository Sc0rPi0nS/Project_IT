import pygame
import sys
import random
from item_class import Item, make_trial_item, item_pixel_size  # ✅ ดึงจาก item_class

pygame.init()

SCREEN = pygame.display.set_mode((920, 750))
SCREEN_WIDTH, SCREEN_HEIGHT = 920, 750
pygame.display.set_caption("Dual Inventory System (Aligned Layout)")

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


# ------------------ คลาสบล็อก (เชื่อมกับ item_class + แสดงภาพ + หมุนภาพ) ------------------
class Block:
    def __init__(self, x, y, w, h, color, item: Item = None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.dragging = False
        self.offset = (0, 0)
        self.spawn_point = (x, y)
        self.last_r_state = False
        self.item = item  # ✅ เก็บ item จริงจาก item_class

        # ✅ cache ภาพ (โหลดครั้งเดียว)
        self._base_image = None
        self._scaled_image = None
        self._rotation_quarters = 0  # นับจำนวนการหมุน 90°

    def _ensure_base_image(self):
        """โหลดรูปภาพจาก item_class (ครั้งเดียว)"""
        if not (self.item and self.item.definition.image_path):
            return
        if self._base_image is not None:
            return
        try:
            path = self.item.definition.image_path.replace("\\", "/")  # แก้ path บน Windows
            self._base_image = pygame.image.load(path).convert_alpha()
        except Exception as e:
            print("⚠️ โหลดรูปไม่สำเร็จ:", e)
            self._base_image = None

    def _update_scaled_image(self):
        """อัปเดตรูปหลังหมุนหรือขนาดเปลี่ยน"""
        if self._base_image is None:
            self._scaled_image = None
            return
        angle = -90 * (self._rotation_quarters % 4)
        rotated = pygame.transform.rotate(self._base_image, angle)
        self._scaled_image = pygame.transform.scale(rotated, (self.rect.width, self.rect.height))

    def draw(self):
        # ✅ แสดงภาพถ้ามี
        self._ensure_base_image()
        if self._base_image is not None:
            if (self._scaled_image is None or
                self._scaled_image.get_width() != self.rect.width or
                self._scaled_image.get_height() != self.rect.height):
                self._update_scaled_image()
            SCREEN.blit(self._scaled_image, self.rect)
            pygame.draw.rect(SCREEN, BLACK, self.rect, 2)
        else:
            pygame.draw.rect(SCREEN, self.color, self.rect)
            pygame.draw.rect(SCREEN, BLACK, self.rect, 2)

        # ชื่อ item
        if self.item:
            font = pygame.font.SysFont(None, 18)
            name_surface = font.render(self.item.definition.name, True, BLACK)
            SCREEN.blit(name_surface, (self.rect.x + 4, self.rect.y - 16))

        # จำนวน stack
        if self.item and getattr(self.item.definition, "stackable", False):
            font = pygame.font.SysFont(None, 18)
            qty = getattr(self.item, "quantity", 1)
            SCREEN.blit(font.render(f"x{qty}", True, BLACK),
                        (self.rect.right - 18, self.rect.bottom - 18))

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

        # หมุนตอนลาก
        if self.dragging:
            if keys[pygame.K_r] and not self.last_r_state:
                self.rotate()
                self.last_r_state = True
            elif not keys[pygame.K_r]:
                self.last_r_state = False
        return removed

    def rotate(self):
        """หมุน block + item_class และรูป"""
        if self.item and not self.item.can_rotate():
            return
        center = self.rect.center
        self.rect.width, self.rect.height = self.rect.height, self.rect.width
        self.rect.center = center
        if self.item:
            self.item.rotate()

        self._rotation_quarters = (self._rotation_quarters + 1) % 4
        if self._base_image is not None:
            self._update_scaled_image()

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

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # ✅ คลิกปุ่ม Search → สุ่ม Item จาก item_class.py
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if BOX_RECT.collidepoint(event.pos):
                if any(is_item_in_spawn_zone(b) for b in blocks):
                    print("⚠️ ต้องย้าย item ใน spawn zone ออกก่อน!")
                else:
                    new_item = make_trial_item()  # 🧩 ใช้ Item จริง
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
