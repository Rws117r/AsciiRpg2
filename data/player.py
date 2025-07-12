"""
Player data structures and related functionality.
"""

from dataclasses import dataclass, field
from typing import List, Dict
import time

@dataclass
class Player:
    """Main player character data structure."""
    name: str
    title: str
    race: str
    alignment: str
    character_class: str
    level: int
    hp: int
    max_hp: int
    xp: int
    xp_to_next_level: int
    ac: int
    light_duration: float
    light_start_time: float
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    god: str = ""
    starting_spells: List[str] = field(default_factory=list)
    inventory: List = field(default_factory=list)
    equipment: Dict = field(default_factory=dict)  # equipped items
    gold: float = 0.0
    gear_slots_used: int = 0
    max_gear_slots: int = 10

def get_stat_modifier(stat_value: int) -> int:
    """Calculate ability modifier from stat value."""
    if stat_value <= 3:
        return -4
    elif stat_value <= 5:
        return -3
    elif stat_value <= 7:
        return -2
    elif stat_value <= 9:
        return -1
    elif stat_value <= 11:
        return 0
    elif stat_value <= 13:
        return +1
    elif stat_value <= 15:
        return +2
    elif stat_value <= 17:
        return +3
    else:
        return +4

def create_default_player() -> Player:
    """Create a player with default values for testing."""
    return Player(
        name="Test Character",
        title="Adventurer",
        race="Human",
        alignment="Neutral",
        character_class="Fighter",
        level=1,
        hp=10,
        max_hp=10,
        xp=0,
        xp_to_next_level=100,
        ac=11,
        light_duration=3600,
        light_start_time=time.time(),
        max_gear_slots=10
    )