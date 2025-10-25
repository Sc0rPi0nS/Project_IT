# item_class.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple

# ====== โครงร่างชนิดไอเทม (นิยาม) ======
@dataclass(frozen=True)
class ItemDef:
    id: str
    name: str
    size_w: int           # ความกว้าง "จำนวนช่อง"
    size_h: int           # ความสูง "จำนวนช่อง"
    rotatable: bool = True
    stackable: bool = False
    max_stack: int = 1
    weight: float = 0.0
    value: int = 0
    image_path: Optional[str] = None  # ยังไม่ใช้รูป (ปล่อย None ไปก่อน)

# ====== อินสแตนซ์ไอเทมจริง ======
@dataclass
class Item:
    definition: ItemDef
    quantity: int = 1
    rotated: bool = False

    @property
    def width_slots(self) -> int:
        return self.definition.size_h if self.rotated else self.definition.size_w

    @property
    def height_slots(self) -> int:
        return self.definition.size_w if self.rotated else self.definition.size_h

    def can_rotate(self) -> bool:
        return self.definition.rotatable

    def rotate(self) -> bool:
        if not self.can_rotate():
            return False
        self.rotated = not self.rotated
        return True

    def can_stack_with(self, other: "Item") -> bool:
        return self.definition.stackable and self.definition.id == other.definition.id

    def add_to_stack(self, amount: int) -> int:
        if not self.definition.stackable or amount <= 0:
            return 0
        room = self.definition.max_stack - self.quantity
        take = max(0, min(amount, room))
        self.quantity += take
        return take

    @property
    def total_weight(self) -> float:
        return round(self.definition.weight * max(1, self.quantity), 3)

    @property
    def total_value(self) -> int:
        return self.definition.value * max(1, self.quantity)

# ====== ไอเทมตัวทดลอง 1 ชิ้น ======
# ตัวอย่าง: ขวดน้ำ 1x2 ช่อง หมุนได้ ไม่สแต็ก
TRIAL_DEF = ItemDef(
    id="trial_water",
    name="Purified Water (Trial)",
    size_w=1, size_h=2,
    rotatable=True,
    stackable=False,
    weight=1.0,
    value=120,
    image_path="Project_IT\item\น้ำสะอาด.png",
)

def make_trial_item(quantity: int = 1) -> Item:
    return Item(definition=TRIAL_DEF, quantity=quantity)

# helper แปลงขนาดเป็นพิกเซล (ใช้กับ GRID_SIZE)
def item_pixel_size(item: Item, grid_size: int) -> Tuple[int, int]:
    return item.width_slots * grid_size, item.height_slots * grid_size
