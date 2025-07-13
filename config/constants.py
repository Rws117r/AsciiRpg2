"""
Configuration constants for the Dungeon Explorer game.
All colors, sizes, and game settings are defined here.
"""

# --- File Paths ---
JSON_FILE = 'dungeon.json'
FONT_FILE = 'DejaVuSansMono.ttf' # Make sure this path is correct

# --- Display Settings ---
BASE_FONT_SIZE = 16
BASE_CELL_SIZE = 24
INITIAL_VIEWPORT_WIDTH = 12
INITIAL_VIEWPORT_HEIGHT = 9
DEFAULT_ZOOM = 3.3
MIN_ZOOM = 0.5
MAX_ZOOM = 4.0
ZOOM_STEP = 0.1
HUD_HEIGHT = 120

# --- Colors ---
COLOR_BG = (183, 172, 160)
COLOR_VOID = (183, 172, 160)
COLOR_FLOOR = (240, 236, 224)
COLOR_FLOOR_GRID = (162, 160, 154)
COLOR_WALL = (0, 0, 0)
COLOR_WALL_SHADOW = (140, 134, 125)
COLOR_DOOR = (197, 185, 172)
COLOR_NOTE = (255, 255, 0)
COLOR_PLAYER = (255, 64, 64)
COLOR_MONSTER = (0, 150, 50)
COLOR_COLUMN = (100, 100, 100)
COLOR_WATER = (100, 150, 200)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_HP_BAR = (220, 20, 60)
COLOR_XP_BAR = (135, 206, 250)
COLOR_BAR_BG = (50, 50, 50)
COLOR_TORCH_ICON = (255, 165, 0)
COLOR_SPELL_CURSOR = (255, 0, 255)
COLOR_SPELL_MENU_BG = (10, 10, 40, 220)
COLOR_INPUT_BOX_ACTIVE = (200, 200, 255)
COLOR_INVENTORY_BG = (20, 20, 20)
COLOR_SELECTED_ITEM = (100, 150, 100)
COLOR_EQUIPPED_ITEM = (150, 100, 50)
COLOR_GREEN = (100, 255, 100)
COLOR_RED = (255, 100, 100)

# Character Creation Colors
COLOR_CREAM = (240, 236, 224)
COLOR_BUTTON_NORMAL = (140, 134, 125)
COLOR_BUTTON_HOVER = (162, 160, 154)
COLOR_BUTTON_ACTIVE = (100, 100, 100)
COLOR_TEXT_INPUT = (255, 255, 255)
COLOR_TEXT_INPUT_BORDER = (100, 100, 100)
COLOR_GOLD = (255, 215, 0)

# --- UI Icons ---
UI_ICONS = {
    "DAGGER": "\U0001F5E1",
    "SHIELD": "\U0001F6E1",
    "MONSTER": "\U0001F47D",
    "SPELL_CURSOR": "☄",
    "HEART": "♥",
    "SUN": "☼",
    "GOLD": "¤"
}

# --- Game Settings ---
TORCH_DURATION_SECONDS = 3600

# --- Starting Gold by Class ---
STARTING_GOLD = {
    "Fighter": 120,
    "Priest": 90,
    "Thief": 60,
    "Wizard": 40
}

# --- Class Restrictions ---
CLASS_WEAPON_RESTRICTIONS = {
    "Fighter": [],  # Can use all weapons
    "Priest": ["Club", "Crossbow", "Dagger", "Mace", "Longsword", "Staff", "Warhammer"],
    "Thief": ["Club", "Crossbow", "Dagger", "Shortbow", "Shortsword"],
    "Wizard": ["Dagger", "Staff"]
}

CLASS_ARMOR_RESTRICTIONS = {
    "Fighter": [],  # Can use all armor
    "Priest": [],   # Can use all armor
    "Thief": ["Leather armor", "Shield"],  # + Mithral chainmail
    "Wizard": ["Shield"]  # No armor except shields
}

# --- Character Data ---
RACES = ["Dwarf", "Elf", "Goblin", "Halfling", "Half-Orc", "Human"]
CLASSES = ["Fighter", "Priest", "Thief", "Wizard"]
ALIGNMENTS = ["Lawful", "Chaotic", "Neutral"]
STATS = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]


# ==================================================
# --- NEW: Modern UI Configuration ---
# ==================================================
MODERN_UI_ENABLED = True
USE_MODERN_CHARACTER_CREATION = True
USE_MODERN_INVENTORY = True
USE_MODERN_GEAR_SELECTION = True

# --- Optional: Modern UI Theme Overrides ---
# You can uncomment and change these to customize the look and feel
# MODERN_UI_ACCENT_COLOR = (255, 215, 0) # Gold
# MODERN_UI_SUCCESS_COLOR = (76, 175, 80) # Green
# MODERN_UI_ERROR_COLOR = (244, 67, 54) # Red
