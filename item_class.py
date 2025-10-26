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
    image_path: Optional[str] = None  # path ของภาพ

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


# ====== ไอเทมตัวทดลอง 1: ขวดน้ำ ======
TRIAL_DEF = ItemDef(
    id="trial_water",
    name="Purified Water",
    size_w=1, size_h=2,
    rotatable=True,
    stackable=False,
    weight=1.0,
    value=120,
    image_path="item/น้ำสะอาด.png"
)

def make_trial_item(quantity: int = 1) -> Item:
    return Item(definition=TRIAL_DEF, quantity=quantity)


# ====== ไอเทมตัวทดลอง 2: แบตเตอรี่ ======
BATTERY_DEF = ItemDef(
    id="battery_aa",
    name="Battery",
    size_w=1, size_h=1,
    rotatable=True,
    stackable=True,
    max_stack=4,
    weight=0.3,
    value=80,
    image_path="item\เเบตเตอรี่.png"
)

def make_battery_item(quantity: int = 1) -> Item:
    return Item(definition=BATTERY_DEF, quantity=quantity)

# ====== ไอเทมตัวทดลอง 3: RTX GPU ======
RTX_DEF = ItemDef(
    id="gpu_rtx",
    name="RTX Graphics Card",
    size_w=3, size_h=2,
    rotatable=True,
    stackable=False,
    weight=2.5,
    value=5200,
    image_path="item\RTX พัง.png"
)

def make_rtx_item(quantity: int = 1) -> Item:
    return Item(definition=RTX_DEF, quantity=quantity)

# ====== ไอเทมตัวทดลอง 4: ยา (Medkit) ======
MEDKIT_DEF = ItemDef(
    id="medkit_basic",
    name="Medkit",
    size_w=1, size_h=1,
    rotatable=True,
    stackable=False,    # ไม่ stack กัน
    weight=0.5,
    value=250,
    image_path="item\ยา.png"   # ✅ path ไปยังรูปยา
)

def make_medkit_item(quantity: int = 1) -> Item:
    return Item(definition=MEDKIT_DEF, quantity=quantity)


# ====== Helper แปลงขนาดเป็นพิกเซล (ใช้กับ GRID_SIZE) ======
def item_pixel_size(item: Item, grid_size: int) -> Tuple[int, int]:
    return item.width_slots * grid_size, item.height_slots * grid_size
