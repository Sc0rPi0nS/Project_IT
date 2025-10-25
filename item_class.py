"""Item in game the scavenger"""
# item.py
from dataclasses import dataclass

@dataclass
class ItemDef:
    id: str
    name: str
    size_w: int  # หน่วย "ช่อง"
    size_h: int
    rotatable: bool = True
    stackable: bool = False
    max_stack: int = 1
    weight: float = 0.0
    value: int = 0

class Item:
    """ตัวอย่างอินสแตนซ์ของไอเท็ม 1 ชิ้นในเกม (ยังไม่ผูกกับ grid)"""
    def __init__(self, definition: ItemDef, quantity: int = 1):
        self.defn = definition
        self.qty = quantity
        self.rotated = False  # True = หมุน 90°

    @property
    def width_slots(self):
        return self.defn.size_h if self.rotated else self.defn.size_w

    @property
    def height_slots(self):
        return self.defn.size_w if self.rotated else self.defn.size_h

    def can_rotate(self) -> bool:
        return self.defn.rotatable

    def rotate(self) -> bool:
        if not self.can_rotate():
            return False
        self.rotated = not self.rotated
        return True

    def __repr__(self):
        r = "R" if self.rotated else ""
        return f"<Item {self.defn.name}{r} x{self.qty}>"
