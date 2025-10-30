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
    value=200,
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
    value=60,
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
    value=2400,
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
    value=120,
    image_path="item\ยา.png"   # ✅ path ไปยังรูปยา
)

def make_medkit_item(quantity: int = 1) -> Item:
    return Item(definition=MEDKIT_DEF, quantity=quantity)

# ====== ไอเทมตัวทดลอง 4: can food ======
CANFOOD_DEF = ItemDef(
    id="can_food",
    name="Canned Food",
    size_w=1,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=250,
    image_path="item/can food.png"
)

def make_canfood_item(quantity: int = 1) -> Item:
    return Item(definition=CANFOOD_DEF, quantity=quantity)

DIRWATER_DEF = ItemDef(
    id="dirty water",
    name="Dirty Water",
    size_w=1,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=100,
    image_path="item\น้ำเน่า.png"
)

def make_dirwater_item(quantity: int = 1) -> Item:
    return Item(definition=DIRWATER_DEF, quantity=quantity)

CUCUMBER_DEF = ItemDef(
    id="cucumber",
    name="Cucumber",
    size_w=1,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=200,
    image_path="item\เเตงกวาเดอง.png"
)

def make_cucumber_item(quantity: int = 1) -> Item:
    return Item(definition=CUCUMBER_DEF, quantity=quantity)

FLASHLIGT_DEF = ItemDef(
    id="Flashlight",
    name="Flashlight",
    size_w=1,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=280,
    image_path="item\ไฟฉาย.png"
)

def make_Flashlight_item(quantity: int = 1) -> Item:
    return Item(definition=FLASHLIGT_DEF, quantity=quantity)

BANDAGE_DEF = ItemDef(
    id="Bandage",
    name="Bandage",
    size_w=1,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=100,
    image_path="item\ผ้าพันเเผล.png"
)

def make_Bandage_item(quantity: int = 1) -> Item:
    return Item(definition=BANDAGE_DEF, quantity=quantity)

DIRTMEAT_DEF = ItemDef(
    id="DirtMeat",
    name="Dirt Meat",
    size_w=1,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=80,
    image_path="item\เนื้อเน่า.png"
)

def make_DirtMeat_item(quantity: int = 1) -> Item:
    return Item(definition=DIRTMEAT_DEF, quantity=quantity)

ANTIVIRUS_DEF = ItemDef(
    id="Antivirus",
    name="Antivirus",
    size_w=1,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=160,
    image_path="itemlot2\Antivirus.png"
)

def make_Antivirus_item(quantity: int = 1) -> Item:
    return Item(definition=ANTIVIRUS_DEF, quantity=quantity)

BASEBALL_DEF = ItemDef(
    id="Baseball",
    name="Baseball",
    size_w=3,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=420,
    image_path="itemlot2\Baseball.png"
)

def make_Baseball_item(quantity: int = 1) -> Item:
    return Item(definition=BASEBALL_DEF, quantity=quantity)

BINOCULAR_DEF = ItemDef(
    id="BINOCULAR",
    name="BINOCULAR",
    size_w=2,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=180,
    image_path="itemlot2\Binoculars.png"
)

def make_Binocular_item(quantity: int = 1) -> Item:
    return Item(definition=BINOCULAR_DEF, quantity=quantity)

BREAD_DEF = ItemDef(
    id="Bread",
    name="Bread",
    size_w=1,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=60,
    image_path="itemlot2\Bread.png"
)

def make_Bread_item(quantity: int = 1) -> Item:
    return Item(definition=BREAD_DEF, quantity=quantity)

COMPASS_DEF = ItemDef(
    id="Compass",
    name="Compass",
    size_w=1,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=260,
    image_path="itemlot2\compass.png"
)

def make_Compass_item(quantity: int = 1) -> Item:
    return Item(definition=COMPASS_DEF, quantity=quantity)

ENERGYBAR_DEF = ItemDef(
    id="EnergyBar",
    name="EnergyBar",
    size_w=1,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=120,
    image_path="itemlot2\energy_bar.png"
)

def make_EnergyBar_item(quantity: int = 1) -> Item:
    return Item(definition=ENERGYBAR_DEF, quantity=quantity)

GLASSES_DEF = ItemDef(
    id="Glass",
    name="Glass",
    size_w=2,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=100,
    image_path="itemlot2\glass.png"
)

def make_Glasses_item(quantity: int = 1) -> Item:
    return Item(definition=GLASSES_DEF, quantity=quantity)

KEYBOARD_DEF = ItemDef(
    id="Keyboard",
    name="Keyboard",
    size_w=3,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=840,
    image_path="itemlot2\keyboard.png"
)

def make_Keyboard_item(quantity: int = 1) -> Item:
    return Item(definition=KEYBOARD_DEF, quantity=quantity)

LIGHTER_DEF = ItemDef(
    id="Lighter",
    name="Lighter",
    size_w=1,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=120,
    image_path="itemlot2\lighter.png"
)

def make_Lighter_item(quantity: int = 1) -> Item:
    return Item(definition=LIGHTER_DEF, quantity=quantity)

MOUSE_DEF = ItemDef(
    id="Mouse",
    name="Mouse",
    size_w=1,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=130,
    image_path="itemlot2\mouse.png"
)

def make_Mouse_item(quantity: int = 1) -> Item:
    return Item(definition=MOUSE_DEF, quantity=quantity)

CONVERSE_DEF = ItemDef(
    id="Converse",
    name="Converse",
    size_w=2,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=800,
    image_path="itemlot3\Converse.png"
)

def make_Converse_item(quantity: int = 1) -> Item:
    return Item(definition=CONVERSE_DEF, quantity=quantity)

JORDAN_DEF = ItemDef(
    id="Jordan",
    name="Jordan",
    size_w=2,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=1200,
    image_path="itemlot3\Jordan.png"
)

def make_Jordan_item(quantity: int = 1) -> Item:
    return Item(definition=JORDAN_DEF, quantity=quantity)

MAC_DEF = ItemDef(
    id="Mac",
    name="Mac",
    size_w=3,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=1440,
    image_path="itemlot3\Mac.png"
)

def make_Mac_item(quantity: int = 1) -> Item:
    return Item(definition=MAC_DEF, quantity=quantity)

MASK_DEF = ItemDef(
    id="Mask",
    name="Mask",
    size_w=2,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=320,
    image_path="itemlot3\Mask.png"
)

def make_Mask_item(quantity: int = 1) -> Item:
    return Item(definition=MASK_DEF, quantity=quantity)

MSI_DEF = ItemDef(
    id="MSI",
    name="MSI",
    size_w=3,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=1200,
    image_path="itemlot3\Msi.png"
)

def make_Msi_item(quantity: int = 1) -> Item:
    return Item(definition=MSI_DEF, quantity=quantity)

OPTHUS_DEF = ItemDef(
    id="Opthus",
    name="Opthus",
    size_w=2,
    size_h=1,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=320,
    image_path="itemlot3\opthus.png"
)

def make_Opthus_item(quantity: int = 1) -> Item:
    return Item(definition=OPTHUS_DEF, quantity=quantity)

PANDA_DEF = ItemDef(
    id="Panda",
    name="Panda",
    size_w=2,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=560,
    image_path="itemlot3\panda.png"
)

def make_Panda_item(quantity: int = 1) -> Item:
    return Item(definition=PANDA_DEF, quantity=quantity)

PUMA_DEF = ItemDef(
    id="Puma",
    name="Puma",
    size_w=2,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=560,
    image_path="itemlot3\puma.png"
)

def make_Puma_item(quantity: int = 1) -> Item:
    return Item(definition=PUMA_DEF, quantity=quantity)

RADIO_DEF = ItemDef(
    id="Raio",
    name="Radio",
    size_w=2,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=280,
    image_path="itemlot3\Radio.png"
)

def make_Radio_item(quantity: int = 1) -> Item:
    return Item(definition=RADIO_DEF, quantity=quantity)

VANS_DEF = ItemDef(
    id="Vans",
    name="Vans",
    size_w=2,
    size_h=2,
    rotatable=True,
    stackable=False,
    max_stack=1,
    weight=0.5,
    value=560,
    image_path="itemlot3\Vans.png"
)

def make_Vans_item(quantity: int = 1) -> Item:
    return Item(definition=VANS_DEF, quantity=quantity)

IT_DEF = ItemDef(
    id="it",
    name="it",
    size_w=2, size_h=2,
    rotatable=True,
    stackable=False,
    weight=1.0,
    value=5000,
    image_path="itemlot3\IT_shirt.png"
)

def make_IT_item(quantity: int = 1) -> Item:
    return Item(definition=IT_DEF, quantity=quantity)

# ====== Helper แปลงขนาดเป็นพิกเซล (ใช้กับ GRID_SIZE) ======
def item_pixel_size(item: Item, grid_size: int) -> Tuple[int, int]:
    return item.width_slots * grid_size, item.height_slots * grid_size