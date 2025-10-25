import pygame
import sys
import random

pygame.init()

# ------------------ ตั้งค่า ------------------
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()
pygame.display.set_caption("Inventory System (Free Rotate While Dragging)")

GRID_SIZE = 80
ROWS, COLS = 6, 6
MARGIN_TOP = 300

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
ITEM_COLORS = [(255, 80, 80), (80, 200, 120), (80, 120, 255), (255, 220, 100)]

GRID_ORIGIN = (400, MARGIN_TOP)
BOX_WIDTH, BOX_HEIGHT = GRID_SIZE * 2, GRID_SIZE
BOX_X = SCREEN_WIDTH - BOX_WIDTH - 400
BOX_Y = SCREEN_HEIGHT // 2 - BOX_HEIGHT // 2
BOX_RECT = pygame.Rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT)

SPAWN_ROWS, SPAWN_COLS = 3, 3
SPAWN_ORIGIN = (BOX_X - GRID_SIZE // 2, BOX_RECT.bottom + 40)
SPAWN_RECT = pygame.Rect(
    SPAWN_ORIGIN[0], SPAWN_ORIGIN[1],
    SPAWN_COLS * GRID_SIZE, SPAWN_ROWS * GRID_SIZE
)


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
            pygame.draw.rect(SCREEN, (220, 240, 255), (ox + c * GRID_SIZE, oy + r * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
    pygame.draw.rect(SCREEN, BLACK, SPAWN_RECT, 3)


def draw_item_box():
    pygame.draw.rect(SCREEN, (230, 230, 230), BOX_RECT)
    pygame.draw.rect(SCREEN, BLACK, BOX_RECT, 3)
    font = pygame.font.SysFont(None, 32)
    SCREEN.blit(font.render("Random Item", True, BLACK),
                font.render("Random Item", True, BLACK).get_rect(center=BOX_RECT.center))


# ------------------ คลาสบล็อก ------------------
class Block:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.dragging = False
        self.offset = (0, 0)
        self.spawn_point = (x, y)
        self.last_r_state = False  # ป้องกันหมุนรัว

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)
        pygame.draw.rect(SCREEN, BLACK, self.rect, 2)

    def handle_event(self, event, all_blocks, keys):
        # เริ่มลาก
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mx, my = event.pos
                self.offset = (self.rect.x - mx, self.rect.y - my)

        # ปล่อยเมาส์
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                self.snap_to_nearest(all_blocks)

        # ระหว่างลาก
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            self.rect.x = mx + self.offset[0]
            self.rect.y = my + self.offset[1]

        # ✅ หมุนได้ทันทีระหว่างลาก (ไม่ตรวจชน)
        if self.dragging:
            if keys[pygame.K_r] and not self.last_r_state:
                self.rotate()  # หมุนได้อิสระ
                self.last_r_state = True
            elif not keys[pygame.K_r]:
                self.last_r_state = False

    def rotate(self):
        """หมุน 90° โดยไม่ตรวจชน"""
        # เก็บ center เดิมไว้เพื่อหมุนรอบกลาง
        center = self.rect.center
        self.rect.width, self.rect.height = self.rect.height, self.rect.width
        self.rect.center = center  # คงจุดหมุนกลางเดิม

    def snap_to_nearest(self, all_blocks):
        """snap เข้ากับ grid ฝั่งซ้าย หรือ spawn zone"""
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

        # ถ้าอยู่ใน inventory แล้วชน → กลับ spawn zone
        if target_zone == "inventory":
            for b in all_blocks:
                if b is not self and new_rect.colliderect(b.rect):
                    self.rect.x, self.rect.y = self.spawn_point
                    return

        # snap ปกติ
        self.rect.x, self.rect.y = new_x, new_y
        if target_zone == "spawn":
            self.spawn_point = (self.rect.x, self.rect.y)


# ------------------ ฟังก์ชันช่วย ------------------
def is_item_in_spawn_zone(block):
    return SPAWN_RECT.colliderect(block.rect)


def random_item():
    size = random.choice([(GRID_SIZE, GRID_SIZE), (GRID_SIZE * 2, GRID_SIZE)])
    color = random.choice(ITEM_COLORS)
    sx = SPAWN_RECT.centerx - size[0] // 2
    sy = SPAWN_RECT.centery - size[1] // 2
    return Block(sx, sy, size[0], size[1], color)


# ------------------ เริ่มต้น ------------------
blocks = []
clock = pygame.time.Clock()

# ------------------ Loop หลัก ------------------
while True:
    SCREEN.fill(WHITE)
    draw_grid(GRID_ORIGIN)
    draw_item_box()
    draw_spawn_zone()
    for b in blocks:
        b.draw()

    keys = pygame.key.get_pressed()  # ตรวจปุ่ม R ทุกเฟรม

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # คลิกปุ่มสุ่ม
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if BOX_RECT.collidepoint(event.pos):
                if any(is_item_in_spawn_zone(b) for b in blocks):
                    print("⚠️ ต้องย้าย item ใน spawn zone ออกก่อน!")
                else:
                    blocks.append(random_item())

        # ส่ง event ให้ทุก block
        for b in blocks:
            b.handle_event(event, blocks, keys)

    pygame.display.flip()
    clock.tick(60)
