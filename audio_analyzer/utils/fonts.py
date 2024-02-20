from dataclasses import dataclass
from typing import Optional, Tuple
from tkinter.font import Font

def extend(font, family=None, size=None, weight=None, slant=None):
    return Font(
        family = font['family'] or family,
        size = font['size'] or size,
        weight = font['weight'] or weight,
        slant = font['slant'] or slant,
    )

@dataclass
class Fonts():
    default: Optional[Font] = None
    bold: Optional[Font] = None
    italic: Optional[Font] = None
    title: Optional[Font] = None
