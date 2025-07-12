"""
Complete Updated Player Data Structures
Enhanced with birth sign system and spell casting integration.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import time

# Import the new systems
try:
    from data.birth_sign_system import BirthSign
    from data.updated_spell_systems import Spellcaster
except ImportError:
    # Fallback for when the new systems aren't available yet
    BirthSign = Any
    Spellcaster = Any

@dataclass
class Player:
    """Enhanced player character data structure with birth sign and spellcasting."""
    # Core character information
    name: str
    title: str
    race: str
    alignment: str
    character_class: str
    level: int
    
    # Health and experience
    hp: int
    max_hp: int
    xp: int
    xp_to_next_level: int
    ac: int
    
    # Light/torch system
    light_duration: float
    light_start_time: float
    
    # Core ability scores
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    
    # Religious affiliation
    god: str = ""
    
    # Spell system
    starting_spells: List[str] = field(default_factory=list)
    spellcaster: Optional[Spellcaster] = None
    
    # Inventory and equipment
    inventory: List = field(default_factory=list)
    equipment: Dict = field(default_factory=dict)  # equipped items
    gold: float = 0.0
    gear_slots_used: int = 0
    max_gear_slots: int = 10
    
    # NEW: Birth sign and cosmic destiny system
    birth_sign: Optional[BirthSign] = None
    birth_sign_title: str = ""
    birth_sign_prophecy: str = ""
    birth_year: int = 721
    age: int = 33
    birth_month: str = "Duskwane"
    birth_day: int = 17
    birth_day_of_week: str = "Moonday"
    
    # NEW: Special abilities and enhanced traits
    special_abilities: List[str] = field(default_factory=list)
    birth_sign_bonuses: Dict[str, int] = field(default_factory=dict)
    cosmic_affinities: List[str] = field(default_factory=list)
    
    # NEW: Enhanced magic system
    spell_slots_per_day: Dict[int, int] = field(default_factory=dict)
    spell_slots_used: Dict[int, int] = field(default_factory=dict)
    known_spells: List[str] = field(default_factory=list)
    prepared_spells: List[str] = field(default_factory=list)
    
    # NEW: Character background and personality
    personality_traits: List[str] = field(default_factory=list)
    ideals: List[str] = field(default_factory=list)
    bonds: List[str] = field(default_factory=list)
    flaws: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize computed values after creation."""
        # Initialize spell slots based on class and level
        self._initialize_spell_slots()
        
        # Apply racial bonuses
        self._apply_racial_bonuses()
        
        # Apply class features
        self._apply_class_features()
    
    def _initialize_spell_slots(self):
        """Initialize spell slots based on character class and level."""
        if self.character_class == "Wizard":
            self.spell_slots_per_day = {
                1: 3, 2: 2, 3: 1, 4: 0, 5: 0
            }
        elif self.character_class == "Priest":
            self.spell_slots_per_day = {
                1: 2, 2: 1, 3: 1, 4: 0, 5: 0
            }
        else:
            self.spell_slots_per_day = {}
        
        # Initialize used slots to 0
        self.spell_slots_used = {tier: 0 for tier in self.spell_slots_per_day.keys()}
    
    def _apply_racial_bonuses(self):
        """Apply racial bonuses to stats and abilities."""
        racial_bonuses = {
            "Human": {"stat_bonus": 1, "extra_skill": True},
            "Elf": {"dexterity": 2, "night_vision": True, "magic_resistance": True},
            "Dwarf": {"constitution": 2, "poison_resistance": True, "stone_cunning": True},
            "Halfling": {"dexterity": 2, "luck": True, "brave": True},
            "Half-Orc": {"strength": 2, "constitution": 1, "relentless": True},
            "Goblin": {"dexterity": 2, "constitution": -1, "stealth_bonus": 2}
        }
        
        bonuses = racial_bonuses.get(self.race, {})
        for bonus_type, bonus_value in bonuses.items():
            if bonus_type in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
                current_value = getattr(self, bonus_type)
                setattr(self, bonus_type, current_value + bonus_value)
            elif isinstance(bonus_value, bool) and bonus_value:
                self.special_abilities.append(bonus_type)
            elif isinstance(bonus_value, int) and bonus_type not in ["stat_bonus"]:
                # Handle special numeric bonuses
                pass
    
    def _apply_class_features(self):
        """Apply class-specific features and bonuses."""
        if self.character_class == "Fighter":
            # Fighters get constitution bonus to gear slots
            constitution_bonus = get_stat_modifier(self.constitution)
            if constitution_bonus > 0:
                self.max_gear_slots += constitution_bonus
            
            # Combat bonuses
            self.special_abilities.append("second_wind")
            self.special_abilities.append("weapon_master")
        
        elif self.character_class == "Priest":
            # Divine magic abilities
            self.special_abilities.append("channel_divinity")
            self.special_abilities.append("divine_magic")
            
            # Healing bonus
            wisdom_bonus = get_stat_modifier(self.wisdom)
            if wisdom_bonus > 0:
                self.special_abilities.append(f"healing_bonus_{wisdom_bonus}")
        
        elif self.character_class == "Wizard":
            # Arcane magic abilities
            self.special_abilities.append("arcane_magic")
            self.special_abilities.append("spellbook")
            
            # Intelligence-based bonuses
            intelligence_bonus = get_stat_modifier(self.intelligence)
            if intelligence_bonus > 0:
                self.special_abilities.append(f"spell_power_bonus_{intelligence_bonus}")
        
        elif self.character_class == "Thief":
            # Stealth and thievery
            self.special_abilities.append("sneak_attack")
            self.special_abilities.append("lockpicking")
            self.special_abilities.append("stealth_expert")
    
    def apply_birth_sign_bonuses(self, birth_sign: BirthSign):
        """Apply birth sign bonuses to the character."""
        self.birth_sign = birth_sign
        self.birth_sign_title = birth_sign.combined_title
        self.birth_sign_prophecy = birth_sign.prophecy_text
        
        # Apply stat bonuses
        for stat, bonus in birth_sign.stat_bonuses.items():
            if hasattr(self, stat):
                current_value = getattr(self, stat)
                setattr(self, stat, current_value + bonus)
                self.birth_sign_bonuses[stat] = bonus
        
        # Add special abilities
        self.special_abilities.extend(birth_sign.special_abilities)
        
        # Store cosmic affinities
        for moon_name, (imprint, phase_value) in birth_sign.lunar_imprints.items():
            if imprint.name in ["EMPOWERED", "CHAOTIC"]:
                self.cosmic_affinities.append(f"{moon_name}_{imprint.name}")
    
    def get_total_ac(self) -> int:
        """Calculate total AC including all bonuses."""
        base_ac = self.ac
        
        # Add birth sign bonuses
        if "ac_bonus" in self.birth_sign_bonuses:
            base_ac += self.birth_sign_bonuses["ac_bonus"]
        
        # Add special ability bonuses
        for ability in self.special_abilities:
            if ability.startswith("ac_bonus_"):
                bonus = int(ability.split("_")[-1])
                base_ac += bonus
        
        return base_ac
    
    def can_cast_spell(self, spell_name: str, tier: int) -> bool:
        """Check if the character can cast a spell."""
        if not self.spellcaster:
            return False
        
        # Check if spell is known
        if spell_name not in self.known_spells:
            return False
        
        # Check spell slots
        return self.spell_slots_used.get(tier, 0) < self.spell_slots_per_day.get(tier, 0)
    
    def cast_spell(self, spell_name: str, tier: int) -> bool:
        """Cast a spell, consuming a spell slot."""
        if not self.can_cast_spell(spell_name, tier):
            return False
        
        self.spell_slots_used[tier] += 1
        
        if self.spellcaster:
            return self.spellcaster.cast_spell(spell_name)
        
        return True
    
    def rest(self, rest_type: str = "long"):
        """Rest to recover resources."""
        if rest_type == "long":
            # Recover all spell slots
            self.spell_slots_used = {tier: 0 for tier in self.spell_slots_per_day.keys()}
            
            # Recover hit points
            self.hp = self.max_hp
            
            if self.spellcaster:
                self.spellcaster.rest()
        
        elif rest_type == "short":
            # Recover some hit points
            self.hp = min(self.max_hp, self.hp + (self.max_hp // 4))
    
    def gain_experience(self, xp_amount: int):
        """Gain experience and potentially level up."""
        self.xp += xp_amount
        
        while self.xp >= self.xp_to_next_level:
            self.level_up()
    
    def level_up(self):
        """Level up the character."""
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = self._calculate_xp_to_next_level()
        
        # Increase hit points
        hp_gain = self._calculate_hp_gain()
        self.max_hp += hp_gain
        self.hp = self.max_hp
        
        # Update spell slots for spellcasters
        if self.character_class in ["Wizard", "Priest"]:
            self._update_spell_slots_for_level()
        
        print(f"🎉 {self.name} reached level {self.level}! (+{hp_gain} HP)")
    
    def _calculate_xp_to_next_level(self) -> int:
        """Calculate XP needed for next level."""
        return self.level * 100  # Simple progression
    
    def _calculate_hp_gain(self) -> int:
        """Calculate HP gain on level up."""
        constitution_bonus = get_stat_modifier(self.constitution)
        
        if self.character_class == "Fighter":
            base_hp = 10
        elif self.character_class == "Priest":
            base_hp = 8
        elif self.character_class in ["Wizard", "Thief"]:
            base_hp = 6
        else:
            base_hp = 8
        
        return max(1, base_hp + constitution_bonus)
    
    def _update_spell_slots_for_level(self):
        """Update spell slots based on new level."""
        # This would be expanded based on class progression tables
        if self.level >= 3 and 2 not in self.spell_slots_per_day:
            self.spell_slots_per_day[2] = 1
            self.spell_slots_used[2] = 0
        
        if self.level >= 5 and 3 not in self.spell_slots_per_day:
            self.spell_slots_per_day[3] = 1
            self.spell_slots_used[3] = 0
    
    def get_character_summary(self) -> List[str]:
        """Get a formatted character summary."""
        lines = [
            f"=== {self.name} ===",
            f"{self.title}",
            f"Level {self.level} {self.alignment} {self.race} {self.character_class}",
            "",
            f"HP: {self.hp}/{self.max_hp}",
            f"AC: {self.get_total_ac()}",
            f"XP: {self.xp}/{self.xp_to_next_level}",
            "",
            "ABILITIES:",
            f"STR: {self.strength} ({get_stat_modifier(self.strength):+d})",
            f"DEX: {self.dexterity} ({get_stat_modifier(self.dexterity):+d})",
            f"CON: {self.constitution} ({get_stat_modifier(self.constitution):+d})",
            f"INT: {self.intelligence} ({get_stat_modifier(self.intelligence):+d})",
            f"WIS: {self.wisdom} ({get_stat_modifier(self.wisdom):+d})",
            f"CHA: {self.charisma} ({get_stat_modifier(self.charisma):+d})",
            ""
        ]
        
        if self.birth_sign_title:
            lines.extend([
                "BIRTH SIGN:",
                self.birth_sign_title,
                f"Born: {self.birth_day} {self.birth_month} {self.birth_year} (Age {self.age})",
                f"Day: {self.birth_day_of_week}",
                ""
            ])
        
        if self.birth_sign_prophecy:
            lines.extend([
                "COSMIC DESTINY:",
                self.birth_sign_prophecy,
                ""
            ])
        
        if self.special_abilities:
            lines.append("SPECIAL ABILITIES:")
            for ability in self.special_abilities:
                lines.append(f"• {ability.replace('_', ' ').title()}")
            lines.append("")
        
        if self.known_spells:
            lines.append("KNOWN SPELLS:")
            for spell in self.known_spells:
                lines.append(f"• {spell}")
            lines.append("")
        
        if self.spell_slots_per_day:
            lines.append("SPELL SLOTS:")
            for tier, max_slots in self.spell_slots_per_day.items():
                used_slots = self.spell_slots_used.get(tier, 0)
                if max_slots > 0:
                    lines.append(f"Tier {tier}: {used_slots}/{max_slots}")
            lines.append("")
        
        lines.extend([
            f"Gold: {self.gold:.1f} gp",
            f"Gear Slots: {self.gear_slots_used}/{self.max_gear_slots}",
            f"Items: {len(self.inventory)}"
        ])
        
        if self.god:
            lines.append(f"Deity: {self.god}")
        
        return lines
    
    def to_dict(self) -> Dict:
        """Convert player to dictionary for saving."""
        return {
            "name": self.name,
            "title": self.title,
            "race": self.race,
            "alignment": self.alignment,
            "character_class": self.character_class,
            "level": self.level,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "xp": self.xp,
            "xp_to_next_level": self.xp_to_next_level,
            "ac": self.ac,
            "light_duration": self.light_duration,
            "light_start_time": self.light_start_time,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "charisma": self.charisma,
            "god": self.god,
            "starting_spells": self.starting_spells,
            "gold": self.gold,
            "gear_slots_used": self.gear_slots_used,
            "max_gear_slots": self.max_gear_slots,
            "birth_sign_title": self.birth_sign_title,
            "birth_sign_prophecy": self.birth_sign_prophecy,
            "birth_year": self.birth_year,
            "age": self.age,
            "birth_month": self.birth_month,
            "birth_day": self.birth_day,
            "birth_day_of_week": self.birth_day_of_week,
            "special_abilities": self.special_abilities,
            "birth_sign_bonuses": self.birth_sign_bonuses,
            "cosmic_affinities": self.cosmic_affinities,
            "spell_slots_per_day": self.spell_slots_per_day,
            "spell_slots_used": self.spell_slots_used,
            "known_spells": self.known_spells,
            "prepared_spells": self.prepared_spells,
            "personality_traits": self.personality_traits,
            "ideals": self.ideals,
            "bonds": self.bonds,
            "flaws": self.flaws
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Player':
        """Create player from dictionary."""
        # Remove non-field keys and create player
        player_data = {k: v for k, v in data.items() 
                      if k in cls.__dataclass_fields__}
        return cls(**player_data)

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

def create_enhanced_player(name: str, race: str, character_class: str, 
                          alignment: str, stats: List[int], 
                          birth_month: str, birth_day: int, age: int) -> Player:
    """Create a fully enhanced player with all new systems."""
    player = Player(
        name=name,
        title=get_character_title(character_class, alignment, 1),
        race=race,
        alignment=alignment,
        character_class=character_class,
        level=1,
        hp=calculate_starting_hp(character_class, stats[2]),  # Constitution
        max_hp=calculate_starting_hp(character_class, stats[2]),
        xp=0,
        xp_to_next_level=100,
        ac=calculate_starting_ac(stats[1]),  # Dexterity
        light_duration=3600,
        light_start_time=time.time(),
        strength=stats[0],
        dexterity=stats[1],
        constitution=stats[2],
        intelligence=stats[3],
        wisdom=stats[4],
        charisma=stats[5],
        max_gear_slots=max(stats[0], 10),  # Strength-based carrying capacity
        birth_month=birth_month,
        birth_day=birth_day,
        age=age,
        birth_year=754 - age  # Current year - age
    )
    
    return player

def calculate_starting_hp(character_class: str, constitution: int) -> int:
    """Calculate starting hit points."""
    constitution_bonus = get_stat_modifier(constitution)
    
    if character_class == "Fighter":
        base_hp = 10
    elif character_class == "Priest":
        base_hp = 8
    elif character_class in ["Wizard", "Thief"]:
        base_hp = 6
    else:
        base_hp = 8
    
    return max(1, base_hp + constitution_bonus)

def calculate_starting_ac(dexterity: int) -> int:
    """Calculate starting AC (unarmored)."""
    dexterity_bonus = get_stat_modifier(dexterity)
    return 10 + dexterity_bonus

def get_character_title(character_class: str, alignment: str, level: int) -> str:
    """Get appropriate title for character class/alignment/level."""
    titles = {
        "Fighter": {
            "Lawful": {(1, 3): "Guardian", (4, 6): "Defender", (7, 10): "Champion"},
            "Chaotic": {(1, 3): "Warrior", (4, 6): "Berserker", (7, 10): "Warlord"},
            "Neutral": {(1, 3): "Soldier", (4, 6): "Veteran", (7, 10): "Commander"}
        },
        "Priest": {
            "Lawful": {(1, 3): "Acolyte", (4, 6): "Cleric", (7, 10): "High Priest"},
            "Chaotic": {(1, 3): "Zealot", (4, 6): "Fanatic", (7, 10): "Prophet"},
            "Neutral": {(1, 3): "Initiate", (4, 6): "Priest", (7, 10): "Elder"}
        },
        "Wizard": {
            "Lawful": {(1, 3): "Apprentice", (4, 6): "Mage", (7, 10): "Arch-Mage"},
            "Chaotic": {(1, 3): "Hedge Wizard", (4, 6): "Sorcerer", (7, 10): "Archmage"},
            "Neutral": {(1, 3): "Student", (4, 6): "Scholar", (7, 10): "Sage"}
        },
        "Thief": {
            "Lawful": {(1, 3): "Scout", (4, 6): "Agent", (7, 10): "Spymaster"},
            "Chaotic": {(1, 3): "Rogue", (4, 6): "Thief", (7, 10): "Master Thief"},
            "Neutral": {(1, 3): "Burglar", (4, 6): "Infiltrator", (7, 10): "Shadow"}
        }
    }
    
    class_titles = titles.get(character_class, {})
    alignment_titles = class_titles.get(alignment, {})
    
    for level_range, title in alignment_titles.items():
        if level_range[0] <= level <= level_range[1]:
            return title
    
    return "Adventurer"

# Example usage and testing
if __name__ == "__main__":
    # Create a test character
    player = create_enhanced_player(
        name="Lyralei Moonweaver",
        race="Elf",
        character_class="Wizard",
        alignment="Chaotic",
        stats=[10, 16, 12, 17, 14, 13],  # STR, DEX, CON, INT, WIS, CHA
        birth_month="Duskwane",
        birth_day=17,
        age=120
    )
    
    # Display character summary
    summary = player.get_character_summary()
    for line in summary:
        print(line)
    
    # Test experience gain
    print("\n=== GAINING EXPERIENCE ===")
    player.gain_experience(150)
    
    # Test spell casting (would work with full spell system)
    print(f"\nSpell slots: {player.spell_slots_per_day}")
    print(f"Can cast Tier 1 spell: {player.can_cast_spell('Magic Missile', 1)}")