"""
Item data structures and definitions.
All gear, weapons, armor, and item-related functionality.
"""

from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class GearItem:
    """Base class for all gear items."""
    name: str
    cost_gp: int = 0
    cost_sp: int = 0
    cost_cp: int = 0
    gear_slots: int = 1
    quantity_per_slot: int = 1
    description: str = ""
    category: str = "General"
    properties: List[str] = field(default_factory=list)

@dataclass
class Weapon(GearItem):
    """Weapon item with combat properties."""
    weapon_type: str = "M"  # M=Melee, R=Ranged, M/R=Both
    range_type: str = "C"   # C=Close, N=Near, F=Far
    damage: str = "1d4"
    weapon_properties: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.category = "Weapon"

@dataclass
class Armor(GearItem):
    """Armor item with protection properties."""
    ac_bonus: str = "11"
    armor_properties: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.category = "Armor"

@dataclass
class Kit(GearItem):
    """Kit containing multiple items."""
    contents: List[Tuple[str, int]] = field(default_factory=list)  # (item_name, quantity)
    
    def __post_init__(self):
        self.category = "Kit"

@dataclass
class InventoryItem:
    """Represents an item in a player's inventory."""
    item: GearItem
    quantity: int = 1

# --- Item Definitions ---

GENERAL_GEAR = {
    "Arrows (20)": GearItem("Arrows (20)", cost_gp=1, quantity_per_slot=20, 
                           description="Ammunition for shortbows or longbows"),
    "Backpack": GearItem("Backpack", cost_gp=2, gear_slots=0, 
                        description="Holds all the gear you can carry. Don't lose it. First one is free to carry"),
    "Caltrops": GearItem("Caltrops", cost_sp=5, 
                        description="Tiny iron spikes. Creatures stepping on them take 1 damage and move at half speed for 10 rounds"),
    "Crossbow bolts (20)": GearItem("Crossbow bolts (20)", cost_gp=1, quantity_per_slot=20,
                                   description="Ammunition for crossbows"),
    "Crowbar": GearItem("Crowbar", cost_sp=5, 
                       description="Grants advantage on checks to pry open stuck objects"),
    "Flask or bottle": GearItem("Flask or bottle", cost_sp=3,
                               description="Glass containers that hold one draught of liquid"),
    "Flint and steel": GearItem("Flint and steel", cost_sp=5,
                               description="A small fire starter. Routine attempts to light a fire always succeed"),
    "Gem": GearItem("Gem", cost_gp=10, quantity_per_slot=10,
                   description="Gems come in numerous varieties and are very valuable"),
    "Grappling hook": GearItem("Grappling hook", cost_gp=1,
                              description="A rope anchor with three curved tines"),
    "Iron spikes (10)": GearItem("Iron spikes (10)", cost_gp=1, quantity_per_slot=10,
                                description="Strong spikes with holes for threading rope. Can be hammered in with weapons"),
    "Lantern": GearItem("Lantern", cost_gp=5,
                       description="Casts light up to double near distance. Requires oil. Has a shutter to hide light"),
    "Mirror": GearItem("Mirror", cost_gp=10,
                      description="A small, polished mirror"),
    "Oil flask": GearItem("Oil flask", cost_sp=5,
                         description="Fuels a lantern for one hour. Covers close area and burns for 4 rounds, dealing 1d4 damage each round"),
    "Pole": GearItem("Pole", cost_sp=5,
                    description="Wooden, 10' long"),
    "Rations (3)": GearItem("Rations (3)", cost_sp=5, quantity_per_slot=3,
                           description="Three days of food and water supply for one person"),
    "Rope, 60'": GearItem("Rope, 60'", cost_gp=1,
                         description="Hemp rope, 60 feet long"),
    "Torch": GearItem("Torch", cost_sp=5,
                     description="Sheds light to near distance. Burns for one hour of real time"),
    "Coin": GearItem("Coin", cost_gp=0, quantity_per_slot=100, gear_slots=0,
                    description="Currency. First 100 coins are free to carry")
}
WEAPONS = {
    "Bastard sword": Weapon("Bastard sword", cost_gp=10, gear_slots=2, weapon_type="M", 
                           range_type="C", damage="1d8/1d10", weapon_properties=["V"]),
    "Club": Weapon("Club", cost_cp=5, weapon_type="M", range_type="C", damage="1d4"),
    "Crossbow": Weapon("Crossbow", cost_gp=8, weapon_type="R", range_type="F", 
                      damage="1d6", weapon_properties=["2H", "L"]),
    "Dagger": Weapon("Dagger", cost_gp=1, weapon_type="M/R", range_type="C/N", 
                    damage="1d4", weapon_properties=["F", "Th"]),
    "Greataxe": Weapon("Greataxe", cost_gp=10, gear_slots=2, weapon_type="M", 
                      range_type="C", damage="1d8/1d10", weapon_properties=["V"]),
    "Greatsword": Weapon("Greatsword", cost_gp=12, gear_slots=2, weapon_type="M", 
                        range_type="C", damage="1d12", weapon_properties=["2H"]),
    "Javelin": Weapon("Javelin", cost_sp=5, weapon_type="M/R", range_type="C/F", 
                     damage="1d4", weapon_properties=["Th"]),
    "Longbow": Weapon("Longbow", cost_gp=8, weapon_type="R", range_type="F", 
                     damage="1d8", weapon_properties=["2H"]),
    "Longsword": Weapon("Longsword", cost_gp=9, weapon_type="M", range_type="C", damage="1d8"),
    "Mace": Weapon("Mace", cost_gp=5, weapon_type="M", range_type="C", damage="1d6"),
    "Shortbow": Weapon("Shortbow", cost_gp=6, weapon_type="R", range_type="F", 
                      damage="1d4", weapon_properties=["2H"]),
    "Shortsword": Weapon("Shortsword", cost_gp=7, weapon_type="M", range_type="C", damage="1d6"),
    "Spear": Weapon("Spear", cost_sp=5, weapon_type="M/R", range_type="C/N", 
                   damage="1d6", weapon_properties=["Th"]),
    "Staff": Weapon("Staff", cost_sp=5, weapon_type="M", range_type="C", 
                   damage="1d4", weapon_properties=["2H"]),
    "Warhammer": Weapon("Warhammer", cost_gp=10, weapon_type="M", range_type="C", 
                       damage="1d10", weapon_properties=["2H"])
}

ARMOR = {
    "Leather armor": Armor("Leather armor", cost_gp=10, ac_bonus="11 + DEX mod"),
    "Chainmail": Armor("Chainmail", cost_gp=60, gear_slots=2, ac_bonus="13 + DEX mod", 
                      armor_properties=["Disadv on stealth, swim"]),
    "Plate mail": Armor("Plate mail", cost_gp=130, gear_slots=3, ac_bonus="15", 
                       armor_properties=["No swim, disadv stealth"]),
    "Shield": Armor("Shield", cost_gp=10, ac_bonus="+2", 
                   armor_properties=["Occupies one hand"]),
    "Mithral": Armor("Mithral upgrade", cost_gp=0, gear_slots=-1,
                    description="Upgrade for metal armor. x4 cost, -1 gear slot, no penalty stealth/swim")
}

KITS = {
    "Crawling Kit": Kit("Crawling Kit", cost_gp=7, gear_slots=7,
                       description="Essential dungeon exploration gear",
                       contents=[
                           ("Backpack", 1), ("Flint and steel", 1), ("Torch", 2),
                           ("Rations (3)", 1), ("Iron spikes (10)", 1),
                           ("Grappling hook", 1), ("Rope, 60'", 1)
                       ])
}

# --- Item Utility Functions ---

def get_all_items():
    """Get dictionary of all items."""
    all_items = {}
    all_items.update(GENERAL_GEAR)
    all_items.update(WEAPONS)
    all_items.update(ARMOR)
    all_items.update(KITS)
    return all_items

def find_item_by_name(item_name: str) -> GearItem:
    """Find an item by name from all available gear."""
    all_items = get_all_items()
    return all_items.get(item_name)

def is_container(item: GearItem) -> bool:
    """Check if an item is a container."""
    return hasattr(item, 'name') and 'Backpack' in item.name

def get_equipment_slot(item: GearItem) -> str:
    """Determine which equipment slot an item goes in."""
    if isinstance(item, Weapon):
        return 'weapon'
    elif isinstance(item, Armor):
        if 'Shield' in item.name:
            return 'shield'
        else:
            return 'armor'
    elif item.name == 'Torch':
        return 'light'
    elif item.name == 'Lantern':
        return 'light'
    return None

def format_item_cost(item: GearItem) -> str:
    """Format item cost as a readable string."""
    if hasattr(item, 'cost_gp') and item.cost_gp > 0:
        return f"{item.cost_gp} gp"
    elif hasattr(item, 'cost_sp') and item.cost_sp > 0:
        return f"{item.cost_sp} sp"
    elif hasattr(item, 'cost_cp') and item.cost_cp > 0:
        return f"{item.cost_cp} cp"
    else:
        return "Priceless"