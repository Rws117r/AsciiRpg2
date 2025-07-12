"""
Birth Sign and Astrology System
Comprehensive birth sign system based on month, day, moon phases, and year.
Integrates with the existing calendar system.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum
import random

from data.calendar import WorldCalendar, CalendarDate, MoonPhase

class SolarArchetype(Enum):
    """Month-based archetypal personalities."""
    THE_ENDURER = ("The Endurer", "Stoic, self-reliant, tough in crisis")
    THE_REKINDLED = ("The Rekindled", "Optimistic, fiery, drawn to rebirth")
    THE_AWAKENER = ("The Awakener", "Curious, restless, energetic")
    THE_VERDANT = ("The Verdant", "Compassionate, social, nurturing")
    THE_BLOOMING = ("The Blooming", "Expressive, dramatic, creative")
    THE_RADIANT = ("The Radiant", "Bold, confident, leadership-bound")
    THE_BURNED = ("The Burned", "Intense, volatile, passionate")
    THE_SHIFTING = ("The Shifting", "Elusive, clever, dual-natured")
    THE_WATCHER = ("The Watcher", "Reflective, wise, cautious")
    THE_VEILED = ("The Veiled", "Secretive, spiritual, mystical")
    THE_QUIET = ("The Quiet", "Thoughtful, loyal, reserved")
    THE_CROWNED = ("The Crowned", "Ambitious, legacy-driven, proud")

class SpiritualNature(Enum):
    """Day-of-week based spiritual nature."""
    EMPATH = ("Empath", "Healer, listener, compassionate soul")
    DREAMER = ("Dreamer", "Seer, wanderer, vision-seeker")
    FIGHTER = ("Fighter", "Activist, leader, warrior spirit")
    SCHOLAR = ("Scholar", "Trickster, thinker, knowledge-seeker")
    BUILDER = ("Builder", "Anchor, survivor, foundation-maker")
    FREE_SPIRIT = ("Free Spirit", "Traveler, talker, wanderer")
    MYSTIC = ("Mystic", "Rogue, oracle, shadow-walker")

class CelestialImprint(Enum):
    """Moon phase meanings."""
    DORMANT = ("Dormant Potential", "Hidden powers, secrets, new beginnings")
    AMBITIOUS = ("Ambitious Growth", "Drive, expansion, rising power")
    EMPOWERED = ("Empowered Blessing", "Active power, divine favor, peak ability")
    INTROSPECTIVE = ("Introspective Wisdom", "Reflection, learning, inner sight")
    CHAOTIC = ("Chaotic Intensity", "Unstable power, wild magic, unpredictable")

@dataclass
class GenerationalOmen:
    """Represents the meaning of birth year/decade."""
    decade_name: str
    theme: str
    description: str
    special_years: Dict[int, str] = field(default_factory=dict)

@dataclass
class BirthSign:
    """Complete birth sign calculation."""
    birth_date: CalendarDate
    birth_year: int
    age: int
    
    # Core sign components
    solar_archetype: SolarArchetype
    spiritual_nature: SpiritualNature
    lunar_imprints: Dict[str, Tuple[CelestialImprint, float]]  # moon_name -> (imprint, phase_value)
    generational_omen: GenerationalOmen
    
    # Calculated properties
    combined_title: str
    prophecy_text: str
    
    # Mechanical bonuses
    stat_bonuses: Dict[str, int] = field(default_factory=dict)
    skill_bonuses: Dict[str, int] = field(default_factory=dict)
    special_abilities: List[str] = field(default_factory=list)

class BirthSignCalculator:
    """Calculates birth signs from calendar data."""
    
    # Month to archetype mapping
    MONTH_ARCHETYPES = {
        "Frostwane": SolarArchetype.THE_ENDURER,
        "Embermarch": SolarArchetype.THE_REKINDLED,
        "Thawmere": SolarArchetype.THE_AWAKENER,
        "Greentide": SolarArchetype.THE_VERDANT,
        "Blossarch": SolarArchetype.THE_BLOOMING,
        "Suncrest": SolarArchetype.THE_RADIANT,
        "Highflare": SolarArchetype.THE_BURNED,
        "Duskwane": SolarArchetype.THE_SHIFTING,
        "Mournfall": SolarArchetype.THE_WATCHER,
        "Hallowdeep": SolarArchetype.THE_VEILED,
        "Snowrest": SolarArchetype.THE_QUIET,
        "Starhearth": SolarArchetype.THE_CROWNED
    }
    
    # Day of week to spiritual nature mapping
    DAY_NATURES = {
        "Soulday": SpiritualNature.EMPATH,
        "Moonday": SpiritualNature.DREAMER,
        "Flameday": SpiritualNature.FIGHTER,
        "Wyrmday": SpiritualNature.SCHOLAR,
        "Stonehold": SpiritualNature.BUILDER,
        "Windmere": SpiritualNature.FREE_SPIRIT,
        "Shadoweve": SpiritualNature.MYSTIC
    }
    
    # Generational themes by decade
    GENERATIONAL_OMENS = {
        720: GenerationalOmen("The Ash Decade", "Destruction and Renewal", 
                             "Born in times of great change, marked by endings that birth new beginnings"),
        721: GenerationalOmen("The Whispering Year", "Omens in Dreams", 
                             "Fated to hear what others cannot, destined to lift hidden truths"),
        730: GenerationalOmen("The Decade of Broken Oaths", "Betrayal and Honor", 
                             "Witnesses to broken promises, called to restore lost honor"),
        740: GenerationalOmen("The Silent War", "Hidden Conflicts", 
                             "Children of shadow conflicts, knowing sacrifice and hidden struggle"),
        750: GenerationalOmen("The Rising Dawn", "New Hope", 
                             "Born as hope returns, destined to herald new golden ages")
    }
    
    @classmethod
    def calculate_phase_imprint(cls, phase_value: float) -> CelestialImprint:
        """Convert moon phase to celestial imprint."""
        if 0.00 <= phase_value <= 0.10:
            return CelestialImprint.DORMANT
        elif 0.11 <= phase_value <= 0.40:
            return CelestialImprint.AMBITIOUS
        elif 0.41 <= phase_value <= 0.59:
            return CelestialImprint.EMPOWERED
        elif 0.60 <= phase_value <= 0.89:
            return CelestialImprint.INTROSPECTIVE
        else:  # 0.90-1.00
            return CelestialImprint.CHAOTIC
    
    @classmethod
    def calculate_birth_sign(cls, birth_year: int, birth_day_of_year: int, current_year: int = 754) -> BirthSign:
        """Calculate complete birth sign from birth data."""
        # Create calendar for birth year
        calendar = WorldCalendar(birth_year, birth_day_of_year)
        birth_date = calendar.get_current_date()
        age = current_year - birth_year
        
        # Calculate core components
        solar_archetype = cls.MONTH_ARCHETYPES[birth_date.month]
        spiritual_nature = cls.DAY_NATURES[birth_date.day_of_week]
        
        # Calculate lunar imprints
        lunar_imprints = {}
        for moon_name, phase_value in calendar.moon_phases.items():
            imprint = cls.calculate_phase_imprint(phase_value)
            lunar_imprints[moon_name] = (imprint, phase_value)
        
        # Get generational omen
        decade = (birth_year // 10) * 10
        year_omen = cls.GENERATIONAL_OMENS.get(birth_year)
        decade_omen = cls.GENERATIONAL_OMENS.get(decade)
        generational_omen = year_omen or decade_omen or GenerationalOmen(
            f"The {decade}s", "Unknown Era", "Born in times of mystery"
        )
        
        # Create combined title and prophecy
        combined_title = cls._create_combined_title(solar_archetype, spiritual_nature, lunar_imprints)
        prophecy_text = cls._create_prophecy_text(solar_archetype, spiritual_nature, lunar_imprints, generational_omen)
        
        # Calculate mechanical bonuses
        stat_bonuses, skill_bonuses, special_abilities = cls._calculate_bonuses(
            solar_archetype, spiritual_nature, lunar_imprints
        )
        
        return BirthSign(
            birth_date=birth_date,
            birth_year=birth_year,
            age=age,
            solar_archetype=solar_archetype,
            spiritual_nature=spiritual_nature,
            lunar_imprints=lunar_imprints,
            generational_omen=generational_omen,
            combined_title=combined_title,
            prophecy_text=prophecy_text,
            stat_bonuses=stat_bonuses,
            skill_bonuses=skill_bonuses,
            special_abilities=special_abilities
        )
    
    @classmethod
    def _create_combined_title(cls, solar: SolarArchetype, spiritual: SpiritualNature, lunar: Dict) -> str:
        """Create a combined title from the sign components."""
        archetype_name = solar.value[0].replace("The ", "")
        spirit_name = spiritual.value[0]
        
        # Add notable moon influences
        moon_influences = []
        for moon_name, (imprint, phase_value) in lunar.items():
            if imprint in [CelestialImprint.EMPOWERED, CelestialImprint.CHAOTIC]:
                moon_influences.append(f"{moon_name}-{imprint.value[0].split()[0]}")
        
        if moon_influences:
            return f"The {archetype_name} {spirit_name} of {', '.join(moon_influences)}"
        else:
            return f"The {archetype_name} {spirit_name}"
    
    @classmethod
    def _create_prophecy_text(cls, solar: SolarArchetype, spiritual: SpiritualNature, 
                            lunar: Dict, generational: GenerationalOmen) -> str:
        """Create prophecy text describing the character's destiny."""
        archetype_desc = solar.value[1].lower()
        spirit_desc = spiritual.value[1].lower()
        
        # Describe dominant moon influences
        moon_descriptions = []
        for moon_name, (imprint, phase_value) in lunar.items():
            if phase_value >= 0.4:  # Significant influence
                moon_descriptions.append(f"{moon_name}'s {imprint.value[0].lower()}")
        
        moon_text = f"under {', '.join(moon_descriptions)}" if moon_descriptions else "touched by celestial forces"
        
        return (f"You are {archetype_desc}, born {moon_text}. "
                f"Your spirit shows as {spirit_desc}. "
                f"{generational.description}.")
    
    @classmethod
    def _calculate_bonuses(cls, solar: SolarArchetype, spiritual: SpiritualNature, 
                         lunar: Dict) -> Tuple[Dict[str, int], Dict[str, int], List[str]]:
        """Calculate mechanical bonuses from birth sign."""
        stat_bonuses = {}
        skill_bonuses = {}
        special_abilities = []
        
        # Solar archetype bonuses
        archetype_bonuses = {
            SolarArchetype.THE_ENDURER: {"constitution": 1, "cold_resistance": 5},
            SolarArchetype.THE_REKINDLED: {"charisma": 1, "fire_affinity": True},
            SolarArchetype.THE_AWAKENER: {"dexterity": 1, "movement_bonus": 5},
            SolarArchetype.THE_VERDANT: {"wisdom": 1, "healing_bonus": 2},
            SolarArchetype.THE_BLOOMING: {"charisma": 1, "charm_bonus": 2},
            SolarArchetype.THE_RADIANT: {"charisma": 1, "leadership_bonus": 2},
            SolarArchetype.THE_BURNED: {"strength": 1, "fire_damage_bonus": 1},
            SolarArchetype.THE_SHIFTING: {"intelligence": 1, "illusion_bonus": 2},
            SolarArchetype.THE_WATCHER: {"wisdom": 1, "perception_bonus": 2},
            SolarArchetype.THE_VEILED: {"intelligence": 1, "stealth_bonus": 2},
            SolarArchetype.THE_QUIET: {"constitution": 1, "mental_resistance": 2},
            SolarArchetype.THE_CROWNED: {"charisma": 1, "wealth_bonus": 10}
        }
        
        # Apply solar bonuses
        for bonus_type, bonus_value in archetype_bonuses.get(solar, {}).items():
            if bonus_type in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
                stat_bonuses[bonus_type] = bonus_value
            elif isinstance(bonus_value, bool):
                special_abilities.append(bonus_type)
            else:
                skill_bonuses[bonus_type] = bonus_value
        
        # Spiritual nature bonuses
        spirit_bonuses = {
            SpiritualNature.EMPATH: {"healing_spells": 1, "empathy_bonus": 2},
            SpiritualNature.DREAMER: {"divination_bonus": 2, "dream_walker": True},
            SpiritualNature.FIGHTER: {"combat_bonus": 1, "intimidation_bonus": 2},
            SpiritualNature.SCHOLAR: {"lore_bonus": 2, "language_bonus": 1},
            SpiritualNature.BUILDER: {"crafting_bonus": 2, "fortification_bonus": 1},
            SpiritualNature.FREE_SPIRIT: {"travel_bonus": 2, "social_bonus": 1},
            SpiritualNature.MYSTIC: {"magic_resistance": 1, "occult_bonus": 2}
        }
        
        # Apply spiritual bonuses
        for bonus_type, bonus_value in spirit_bonuses.get(spiritual, {}).items():
            if isinstance(bonus_value, bool):
                special_abilities.append(bonus_type)
            else:
                skill_bonuses[bonus_type] = skill_bonuses.get(bonus_type, 0) + bonus_value
        
        # Lunar imprint bonuses
        for moon_name, (imprint, phase_value) in lunar.items():
            if imprint == CelestialImprint.EMPOWERED:
                if moon_name == "Myrr":
                    special_abilities.append("chaos_magic_affinity")
                elif moon_name == "Caelyra":
                    special_abilities.append("divine_magic_affinity")
                elif moon_name == "Velmara":
                    special_abilities.append("ancient_wisdom_access")
            elif imprint == CelestialImprint.CHAOTIC:
                special_abilities.append(f"{moon_name.lower()}_unpredictability")
        
        return stat_bonuses, skill_bonuses, special_abilities

class BirthSignGenerator:
    """Generates random birth signs for NPCs or random characters."""
    
    @classmethod
    def generate_random_birth_sign(cls, age_range: Tuple[int, int] = (18, 60), 
                                 current_year: int = 754) -> BirthSign:
        """Generate a random birth sign."""
        age = random.randint(*age_range)
        birth_year = current_year - age
        birth_day_of_year = random.randint(1, 365)
        
        return BirthSignCalculator.calculate_birth_sign(birth_year, birth_day_of_year, current_year)
    
    @classmethod
    def generate_birth_sign_from_date(cls, month: str, day: int, age: int, 
                                    current_year: int = 754) -> BirthSign:
        """Generate birth sign from specific date components."""
        birth_year = current_year - age
        
        # Convert month/day to day of year
        months = ["Frostwane", "Embermarch", "Thawmere", "Greentide", "Blossarch", "Suncrest",
                 "Highflare", "Duskwane", "Mournfall", "Hallowdeep", "Snowrest", "Starhearth"]
        month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        try:
            month_index = months.index(month)
            day_of_year = sum(month_lengths[:month_index]) + day
            return BirthSignCalculator.calculate_birth_sign(birth_year, day_of_year, current_year)
        except (ValueError, IndexError):
            return cls.generate_random_birth_sign((age, age), current_year)

# Integration functions for character creation
def add_birth_sign_to_player(player, birth_sign: BirthSign):
    """Add birth sign bonuses to a player character."""
    # Apply stat bonuses
    for stat, bonus in birth_sign.stat_bonuses.items():
        current_value = getattr(player, stat, 10)
        setattr(player, stat, current_value + bonus)
    
    # Store birth sign data on player
    player.birth_sign = birth_sign
    player.birth_sign_title = birth_sign.combined_title
    player.birth_sign_prophecy = birth_sign.prophecy_text
    
    # Add special abilities to starting abilities list
    if not hasattr(player, 'special_abilities'):
        player.special_abilities = []
    player.special_abilities.extend(birth_sign.special_abilities)

def format_birth_sign_for_display(birth_sign: BirthSign) -> List[str]:
    """Format birth sign for character creation display."""
    lines = [
        f"Birth Sign: {birth_sign.combined_title}",
        "",
        f"Born: {birth_sign.birth_date.day_of_month} {birth_sign.birth_date.month} {birth_sign.birth_year}",
        f"Age: {birth_sign.age} years",
        f"Day: {birth_sign.birth_date.day_of_week} ({birth_sign.spiritual_nature.value[0]})",
        "",
        "Lunar Influences:",
    ]
    
    for moon_name, (imprint, phase_value) in birth_sign.lunar_imprints.items():
        lines.append(f"  {moon_name}: {imprint.value[0]} ({phase_value:.2f})")
    
    lines.extend([
        "",
        f"Era: {birth_sign.generational_omen.decade_name}",
        "",
        "Prophecy:",
        birth_sign.prophecy_text
    ])
    
    if birth_sign.stat_bonuses:
        lines.append("")
        lines.append("Stat Bonuses:")
        for stat, bonus in birth_sign.stat_bonuses.items():
            lines.append(f"  {stat.title()}: +{bonus}")
    
    if birth_sign.special_abilities:
        lines.append("")
        lines.append("Special Abilities:")
        for ability in birth_sign.special_abilities:
            lines.append(f"  {ability.replace('_', ' ').title()}")
    
    return lines

# Example usage
if __name__ == "__main__":
    # Generate example birth sign
    birth_sign = BirthSignCalculator.calculate_birth_sign(721, 229, 754)  # Aug 17, 721 (age 33 in 754)
    
    print("=== BIRTH SIGN EXAMPLE ===")
    for line in format_birth_sign_for_display(birth_sign):
        print(line)