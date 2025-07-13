"""
Game state management and state-related enums.
"""

from enum import Enum

class GameState(Enum):
    """Main game states."""
    MAIN_MENU = 0
    CHAR_CREATION = 1
    PLAYING = 10
    SPELL_MENU = 11
    SPELL_TARGETING = 12
    INVENTORY = 13
    EQUIPMENT = 14
    CONTAINER_VIEW = 15
    ITEM_ACTION = 16

class CharCreationState(Enum):
    """Character creation substates."""
    NAME_INPUT = 0
    BIRTH_DETAILS = 1 # NEW state for birth date and age
    STAT_ROLLING = 2
    RACE_SELECTION = 3
    CLASS_SELECTION = 4
    ALIGNMENT_SELECTION = 5
    GOD_SELECTION = 6
    SPELL_SELECTION = 7
    GEAR_SELECTION = 8
    STATS_REVIEW = 9
    COMPLETE = 10

class GearSelectionState(Enum):
    """Gear selection substates."""
    CATEGORY_SELECTION = 0
    ITEM_SELECTION = 1
    QUANTITY_SELECTION = 2
    CONFIRM_PURCHASE = 3
    REVIEW_GEAR = 4
    COMPLETE = 5

class TileType(Enum):
    """Dungeon tile types."""
    VOID = 0
    FLOOR = 1
    DOOR_HORIZONTAL = 2
    DOOR_VERTICAL = 3
    DOOR_OPEN = 4
    NOTE = 5
    STAIRS_HORIZONTAL = 6
    STAIRS_VERTICAL = 7
