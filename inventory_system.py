import pygame
import sys

pygame.init()

# ------------------ ตั้งค่า ------------------
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()
pygame.display.set_caption("Dual Inventory System (2x1 block)")

GRID_SIZE = 80
ROWS, COLS = 6, 6
GAP = 100  # ช่องว่างระหว่าง 2 ตาราง
MARGIN_TOP = 300

# สี
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 80, 80)
BLACK = (0, 0, 0)

# ตำแหน่งเริ่มของสองตาราง
LEFT_GRID_ORIGIN = (400, MARGIN_TOP)
RIGHT_GRID_ORIGIN = (500 + COLS * GRID_SIZE + GAP, MARGIN_TOP)


# ------------------ ฟังก์ชันวาด ------------------
def draw_grid(origin):
    ox, oy = origin
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(ox + c * GRID_SIZE, oy + r * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(SCREEN, GRAY, rect, 1)


# ------------------ คลาสบล็อค ------------------
class Block:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.dragging = False
        self.offset = (0, 0)

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)
        pygame.draw.rect(SCREEN, BLACK, self.rect, 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset = (self.rect.x - mouse_x, self.rect.y - mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                self.snap_to_grid()

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset[0]
                self.rect.y = mouse_y + self.offset[1]

    def snap_to_grid(self):
        # หาตารางที่ใกล้สุด (ซ้ายหรือขวา)
        cx = self.rect.centerx
        cy = self.rect.centery
        left_cx = LEFT_GRID_ORIGIN[0] + COLS * GRID_SIZE / 2
        right_cx = RIGHT_GRID_ORIGIN[0] + COLS * GRID_SIZE / 2
        grid_origin = LEFT_GRID_ORIGIN if abs(cx - left_cx) < abs(cx - right_cx) else RIGHT_GRID_ORIGIN

        # คำนวณตำแหน่ง row/col
        ox, oy = grid_origin
        col = int((self.rect.centerx - ox) // GRID_SIZE)
        row = int((self.rect.centery - oy) // GRID_SIZE)

        # จำกัดขอบไม่ให้เกิน
        max_col = COLS - (self.rect.width // GRID_SIZE)
        max_row = ROWS - (self.rect.height // GRID_SIZE)
        col = max(0, min(col, max_col))
        row = max(0, min(row, max_row))

        # snap ให้ตรงช่อง
        self.rect.x = ox + col * GRID_SIZE
        self.rect.y = oy + row * GRID_SIZE


# ------------------ เริ่มต้น ------------------
block = Block(
    LEFT_GRID_ORIGIN[0] + 10,
    LEFT_GRID_ORIGIN[1] + 10,
    2 * GRID_SIZE,
    GRID_SIZE,
    RED
)

clock = pygame.time.Clock()

# ------------------ Loop หลัก ------------------
while True:
    SCREEN.fill(WHITE)

    # วาดตาราง
    draw_grid(LEFT_GRID_ORIGIN)
    draw_grid(RIGHT_GRID_ORIGIN)

    # วาดบล็อค
    block.draw()

    # ตรวจจับ event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        block.handle_event(event)

    pygame.display.flip()
    clock.tick(60)
