# item_class.py
"""
Item classes for Dual Inventory System (pygame)
-----------------------------------------------
อิงจาก inventory_system.py
รองรับ:
 - การหมุน (R key)
 - การสแต็ก
 - น้ำหนัก/ราคา
 - โหลดภาพและสเกลอัตโนมัติ
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Tuple
import pygame


# =========================
#   Item Definitions
# =========================
@dataclass(frozen=True)
class ItemDef:
    id: str
    name: str
    size_w: int                 # ความกว้าง (จำนวนช่อง)
    size_h: int                 # ความสูง (จำนวนช่อง)
    rotatable: bool = True
    stackable: bool = False
    max_stack: int = 1
    weight: float = 0.0         # น้ำหนักต่อชิ้น
    value: int = 0              # มูลค่าต่อชิ้น
    image_path: Optional[str] = None  # พาธไฟล์รูปภาพ


# =========================
#   Item Instance
# =========================
@dataclass
class Item:
    definition: ItemDef
    quantity: int = 1
    rotated: bool = False

    # ---------- ขนาดของไอเทม (จำนวนช่อง) ----------
    @property
    def width_slots(self) -> int:
        return self.definition.size_h if self.rotated else self.definition.size_w

    @property
    def height_slots(self) -> int:
        return self.definition.size_w if self.rotated else self.definition.size_h

    # ---------- หมุน ----------
    def can_rotate(self) -> bool:
        return self.definition.rotatable

    def rotate(self) -> bool:
        if not self.can_rotate():
            return False
        self.rotated = not self.rotated
        return True

    # ---------- สแต็ก ----------
    def can_stack_with(self, other: "Item") -> bool:
        return (
            self.definition.stackable
            and self.definition.id == other.definition.id
        )

    def add_to_stack(self, amount: int) -> int:
        """เพิ่มจำนวนในสแต็ก คืนค่าจำนวนที่เพิ่มได้จริง"""
        if not self.definition.stackable or amount <= 0:
            return 0
        room = self.definition.max_stack - self.quantity
        take = max(0, min(amount, room))
        self.quantity += take
        return take

    # ---------- ค่ารวม ----------
    @property
    def total_weight(self) -> float:
        return round(self.definition.weight * max(1, self.quantity), 3)

    @property
    def total_value(self) -> int:
        return self.definition.value * max(1, self.quantity)

    def __repr__(self) -> str:
        r = "R" if self.rotated else ""
        q = f" x{self.quantity}" if self.definition.stackable else ""
        return f"<Item {self.definition.name}{r}{q}>"


# =========================
#   Pygame Utilities
# =========================
class ImageCache:
    """โหลดภาพและจำไว้เพื่อไม่ต้องโหลดซ้ำ"""
    def __init__(self):
        self._cache: Dict[Tuple[str, Tuple[int, int]], pygame.Surface] = {}

    def get(self, path: str, size_px: Tuple[int, int]) -> pygame.Surface:
        key = (path, size_px)
        surf = self._cache.get(key)
        if surf is None:
            img = pygame.image.load(path).convert_alpha()
            surf = pygame.transform.scale(img, size_px)
            self._cache[key] = surf
        return surf


def item_pixel_size(item: Item, grid_size: int) -> Tuple[int, int]:
    """แปลงขนาด (จำนวนช่อง) → พิกเซล"""
    return item.width_slots * grid_size, item.height_slots * grid_size


def build_block_payload(
    item: Item,
    grid_size: int,
    center_xy: Tuple[int, int],
    image_cache: Optional[ImageCache] = None
) -> Dict[str, object]:
    """
    สร้าง payload สำหรับผูกกับ Block ใน inventory_system
    return {
        "rect": pygame.Rect,
        "item": Item,
        "image": Optional[pygame.Surface]
    }
    """
    w, h = item_pixel_size(item, grid_size)
    rect = pygame.Rect(0, 0, w, h)
    rect.center = center_xy

    surf = None
    if item.definition.image_path:
        cache = image_cache or ImageCache()
        surf = cache.get(item.definition.image_path, (w, h))

    return {"rect": rect, "item": item, "image": surf}
