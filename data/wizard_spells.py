"""
Wizard Spell System with Lore-Fueled and Alignment-Based Effects
Implementation of all 39 wizard spells across 5 tiers.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import random
import math

from world_calendar_system import get_world_calendar, MoonPhase
from status_effect_system import StatusEffectManager, create_status_effect, StatusEffectFactory

class SpellTier(Enum):
    """Wizard spell tiers."""
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3
    TIER_4 = 4
    TIER_5 = 5

class WizardAlignment(Enum):
    """Wizard alignment types affecting spell behavior."""
    LAWFUL_CONJURER = "Lawful"
    CHAOTIC_CHANNELER = "Chaotic"
    NEUTRAL_SEER = "Neutral"

class SpellRange(Enum):
    """Spell range categories."""
    CLOSE = "Close"      # 5 feet = 1 cell
    NEAR = "Near"        # 30 feet = 6 cells
    FAR = "Far"          # Within sight = 20 cells

@dataclass
class SpellEffect:
    """Represents the effect of casting a spell."""
    damage: int = 0
    damage_type: str = ""
    healing: int = 0
    status_effects: List[str] = field(default_factory=list)
    special_effects: Dict[str, Any] = field(default_factory=dict)
    area_of_effect: int = 0  # Size in cells
    duration: int = 0  # In rounds
    
@dataclass
class WizardSpell:
    """Base wizard spell class."""
    name: str
    tier: SpellTier
    description: str
    range: SpellRange
    base_effect: SpellEffect
    requires_focus: bool = False
    lore_fueled_condition: Optional[Callable] = None
    lore_fueled_effect: Optional[SpellEffect] = None
    alignment_effects: Dict[WizardAlignment, SpellEffect] = field(default_factory=dict)
    
    def cast(self, caster, target=None, target_position=None) -> SpellEffect:
        """Cast the spell and return the combined effect."""
        calendar = get_world_calendar()
        effect = self.base_effect
        
        # Check for lore-fueled enhancement
        if self.lore_fueled_condition and self.lore_fueled_condition():
            if self.lore_fueled_effect:
                effect = self._combine_effects(effect, self.lore_fueled_effect)
                print(f"✨ {self.name} is empowered by cosmic forces!")
        
        # Check for alignment-based modifications
        caster_alignment = getattr(caster, 'alignment', WizardAlignment.NEUTRAL_SEER)
        if isinstance(caster_alignment, str):
            caster_alignment = WizardAlignment(caster_alignment)
        
        if caster_alignment in self.alignment_effects:
            alignment_effect = self.alignment_effects[caster_alignment]
            effect = self._combine_effects(effect, alignment_effect)
            print(f"🔮 {self.name} modified by {caster_alignment.value} alignment!")
        
        return effect
    
    def _combine_effects(self, base: SpellEffect, modifier: SpellEffect) -> SpellEffect:
        """Combine two spell effects."""
        combined = SpellEffect(
            damage=base.damage + modifier.damage,
            damage_type=modifier.damage_type or base.damage_type,
            healing=base.healing + modifier.healing,
            status_effects=base.status_effects + modifier.status_effects,
            special_effects={**base.special_effects, **modifier.special_effects},
            area_of_effect=max(base.area_of_effect, modifier.area_of_effect),
            duration=max(base.duration, modifier.duration)
        )
        return combined

class WizardSpellbook:
    """Collection of all wizard spells organized by tier."""
    
    def __init__(self):
        self.spells_by_tier = {
            SpellTier.TIER_1: self._create_tier_1_spells(),
            SpellTier.TIER_2: self._create_tier_2_spells(),
            SpellTier.TIER_3: self._create_tier_3_spells(),
            SpellTier.TIER_4: self._create_tier_4_spells(),
            SpellTier.TIER_5: self._create_tier_5_spells()
        }
        
        # Flatten for easy lookup
        self.all_spells = {}
        for tier_spells in self.spells_by_tier.values():
            for spell in tier_spells:
                self.all_spells[spell.name] = spell
    
    def get_spell(self, spell_name: str) -> Optional[WizardSpell]:
        """Get a spell by name."""
        return self.all_spells.get(spell_name)
    
    def get_spells_by_tier(self, tier: SpellTier) -> List[WizardSpell]:
        """Get all spells of a specific tier."""
        return self.spells_by_tier.get(tier, [])
    
    def _create_tier_1_spells(self) -> List[WizardSpell]:
        """Create all Tier 1 wizard spells."""
        calendar = get_world_calendar()
        
        spells = []
        
        # 1. FROSTWANE BITE
        spells.append(WizardSpell(
            name="Frostwane Bite",
            tier=SpellTier.TIER_1,
            description="Deals 1d6 cold damage and applies FROSTBITTEN",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                damage=random.randint(1, 6),
                damage_type="cold",
                status_effects=["FROSTBITTEN"]
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().month == "Frostwane",
            lore_fueled_effect=SpellEffect(status_effects=["SLOW"])
        ))
        
        # 2. EMBERMARCH COALS
        spells.append(WizardSpell(
            name="Embermarch Coals",
            tier=SpellTier.TIER_1,
            description="Creates a Close-sized area of 1d4 fire damage per round for 5 rounds",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                damage=random.randint(1, 4),
                damage_type="fire",
                area_of_effect=1,
                duration=5,
                special_effects={"damage_per_round": True}
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().day_of_week == "Flameday",
            lore_fueled_effect=SpellEffect(duration=10)
        ))
        
        # 3. GREENTIDE'S GRASP
        spells.append(WizardSpell(
            name="Greentide's Grasp",
            tier=SpellTier.TIER_1,
            description="Applies ROOTED to one target",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(status_effects=["ROOTED"]),
            lore_fueled_condition=lambda: calendar.get_current_date().month in ["Greentide", "Blossarch"],
            lore_fueled_effect=SpellEffect(special_effects={"str_check_disadvantage": True})
        ))
        
        # 4. FORCE BOLT
        spells.append(WizardSpell(
            name="Force Bolt",
            tier=SpellTier.TIER_1,
            description="Automatically hits one target for 1d4+1 force damage",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                damage=random.randint(1, 4) + 1,
                damage_type="force",
                special_effects={"auto_hit": True}
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().day_of_week == "Wyrmday",
            lore_fueled_effect=SpellEffect(status_effects=["MANA_BURN"])
        ))
        
        # 5. ARCHITECT'S SEAL
        spells.append(WizardSpell(
            name="Architect's Seal",
            tier=SpellTier.TIER_1,
            description="Magically locks a door or container for 1 hour",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                duration=60,  # 1 hour in minutes
                special_effects={"magical_lock": True}
            ),
            lore_fueled_condition=lambda: calendar.get_moon_phase_name("Velmara") in [MoonPhase.WAXING, MoonPhase.FULL],
            lore_fueled_effect=SpellEffect(special_effects={"str_break_disadvantage": True})
        ))
        
        # 6. CONTINUAL FLAME
        spells.append(WizardSpell(
            name="Continual Flame",
            tier=SpellTier.TIER_1,
            description="Object glows with bright, heatless light that reveals invisible creatures",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                duration=-1,  # Permanent until dispelled
                special_effects={
                    "light_source": True,
                    "reveal_invisible": True
                }
            ),
            lore_fueled_condition=lambda: calendar.is_moon_full("Velmara"),
            lore_fueled_effect=SpellEffect(special_effects={"no_material_component": True})
        ))
        
        # 7. FEATHER FALL
        spells.append(WizardSpell(
            name="Feather Fall",
            tier=SpellTier.TIER_1,
            description="Negates all fall damage when cast as a reaction",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(special_effects={"negate_fall_damage": True}),
            lore_fueled_condition=lambda: calendar.get_current_date().day_of_week == "Windmere",
            lore_fueled_effect=SpellEffect(status_effects=["HASTE"], duration=1)
        ))
        
        # 8. RUNIC WARD
        spells.append(WizardSpell(
            name="Runic Ward",
            tier=SpellTier.TIER_1,
            description="Sets AC to 14 for 5 rounds",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                duration=5,
                special_effects={"set_ac": 14}
            ),
            lore_fueled_condition=lambda: calendar.is_moon_full("Caelyra"),
            lore_fueled_effect=SpellEffect(special_effects={"set_ac": 15})
        ))
        
        # 9. SHIFTING SHADOW
        spells.append(WizardSpell(
            name="Shifting Shadow",
            tier=SpellTier.TIER_1,
            description="Become INVISIBLE until you move or act",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                status_effects=["INVISIBLE"],
                special_effects={"breaks_on_action": True}
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().day_of_week == "Shadoweve",
            lore_fueled_effect=SpellEffect(special_effects={"persists_after_move": True})
        ))
        
        # 10. ARCANE SIGHT
        spells.append(WizardSpell(
            name="Arcane Sight",
            tier=SpellTier.TIER_1,
            description="See magical auras within Near range",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                duration=10,
                special_effects={"detect_magic": True}
            ),
            lore_fueled_condition=lambda: calendar.get_moon_phase_name("Myrr") in [MoonPhase.WAXING, MoonPhase.FULL, MoonPhase.DARK],
            lore_fueled_effect=SpellEffect(special_effects={"reveal_alignment": True})
        ))
        
        # 11. SENTRY RUNE
        spells.append(WizardSpell(
            name="Sentry Rune",
            tier=SpellTier.TIER_1,
            description="Invisible rune alerts when touched",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                duration=8,  # Until next dawn
                special_effects={"invisible_alarm": True}
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().day_of_week == "Stonehold",
            lore_fueled_effect=SpellEffect(duration=24)  # Until next dawn extended
        ))
        
        # 12. DUSKWANE DROWSE
        spells.append(WizardSpell(
            name="Duskwane Drowse",
            tier=SpellTier.TIER_1,
            description="Puts creatures with 5 HP or less to SLEEP in Near area",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                area_of_effect=6,
                status_effects=["SLEEP"],
                special_effects={"hp_threshold": 5}
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().month == "Duskwane",
            lore_fueled_effect=SpellEffect(special_effects={"hp_threshold": 10})
        ))
        
        return spells
    
    def _create_tier_2_spells(self) -> List[WizardSpell]:
        """Create all Tier 2 wizard spells."""
        calendar = get_world_calendar()
        spells = []
        
        # 1. ACID ARROW
        spells.append(WizardSpell(
            name="Acid Arrow",
            tier=SpellTier.TIER_2,
            description="Bolt deals 1d4 acid damage per round",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                damage=random.randint(1, 4),
                damage_type="acid",
                duration=3,
                special_effects={"damage_per_round": True}
            ),
            requires_focus=True,
            lore_fueled_condition=lambda: calendar.get_current_date().month == "Mournfall",
            lore_fueled_effect=SpellEffect(status_effects=["ARMOR_DECAY"])
        ))
        
        # 2. MIRROR IMAGE
        spells.append(WizardSpell(
            name="Mirror Image",
            tier=SpellTier.TIER_2,
            description="Create illusory duplicates that absorb attacks",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                duration=10,
                special_effects={"mirror_images": 3, "hits_per_image": 1}
            ),
            alignment_effects={
                WizardAlignment.LAWFUL_CONJURER: SpellEffect(special_effects={"mirror_images": 2, "hits_per_image": 2}),
                WizardAlignment.CHAOTIC_CHANNELER: SpellEffect(special_effects={"mirror_images": 4, "hits_per_image": 1}),
                WizardAlignment.NEUTRAL_SEER: SpellEffect(special_effects={"mirror_images": 3, "hits_per_image": 1})
            }
        ))
        
        # 3. WEB
        spells.append(WizardSpell(
            name="Web",
            tier=SpellTier.TIER_2,
            description="Creates sticky webs applying STUCK status",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                area_of_effect=6,
                duration=10,
                status_effects=["ROOTED"],
                special_effects={"str_check_to_move": True}
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().month == "Hallowdeep",
            lore_fueled_effect=SpellEffect(status_effects=["ROOTED", "BLIND"])
        ))
        
        # 4. MISTY STEP
        spells.append(WizardSpell(
            name="Misty Step",
            tier=SpellTier.TIER_2,
            description="Instantly teleport to visible spot within Near range",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(special_effects={"teleport": True}),
            lore_fueled_condition=lambda: calendar.get_current_date().day_of_week == "Moonday",
            lore_fueled_effect=SpellEffect(special_effects={"dream_cloud": True})
        ))
        
        # 5. INVISIBILITY
        spells.append(WizardSpell(
            name="Invisibility",
            tier=SpellTier.TIER_2,
            description="Target becomes INVISIBLE for 10 rounds",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                duration=10,
                status_effects=["INVISIBLE"],
                special_effects={"breaks_on_attack": True}
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().day_of_week == "Shadoweve",
            lore_fueled_effect=SpellEffect(special_effects={"utility_spells_safe": True})
        ))
        
        # 6. SUNCREST SCORCH
        spells.append(WizardSpell(
            name="Suncrest Scorch",
            tier=SpellTier.TIER_2,
            description="Ray of light deals 2d8 radiant damage",
            range=SpellRange.FAR,
            base_effect=SpellEffect(
                damage=random.randint(2, 16),
                damage_type="radiant"
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().month in ["Suncrest", "Highflare"],
            lore_fueled_effect=SpellEffect(status_effects=["BLIND"], duration=3)
        ))
        
        # 7. MENTAL LOCK
        spells.append(WizardSpell(
            name="Mental Lock",
            tier=SpellTier.TIER_2,
            description="PARALYZE humanoid LV 4 or less",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                status_effects=["PARALYZED"],
                duration=5,
                special_effects={"max_level": 4, "humanoid_only": True}
            ),
            requires_focus=True,
            lore_fueled_condition=lambda: True,  # If target has CONFUSED or FRIGHTENED
            lore_fueled_effect=SpellEffect(special_effects={"resistance_disadvantage": True})
        ))
        
        # 8. SHATTER
        spells.append(WizardSpell(
            name="Shatter",
            tier=SpellTier.TIER_2,
            description="Loud boom deals 2d6 sonic damage in Near area",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                damage=random.randint(2, 12),
                damage_type="sonic",
                area_of_effect=6
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().day_of_week == "Stonehold",
            lore_fueled_effect=SpellEffect(special_effects={"double_construct_damage": True})
        ))
        
        # 9. OBSCURING VAPOR
        spells.append(WizardSpell(
            name="Obscuring Vapor",
            tier=SpellTier.TIER_2,
            description="Creates thick fog that obscures vision",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                area_of_effect=6,
                duration=10,
                special_effects={"heavy_obscurement": True}
            ),
            lore_fueled_condition=lambda: calendar.get_moon_phase_name("Myrr") in [MoonPhase.FULL, MoonPhase.DARK],
            lore_fueled_effect=SpellEffect(status_effects=["CONFUSED"], special_effects={"confusion_chance": 0.25})
        ))
        
        # 10. LEVITATE
        spells.append(WizardSpell(
            name="Levitate",
            tier=SpellTier.TIER_2,
            description="Float vertically up to Near distance per round",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                duration=10,
                special_effects={"vertical_movement": True}
            ),
            requires_focus=True,
            lore_fueled_condition=lambda: calendar.get_current_date().day_of_week == "Windmere",
            lore_fueled_effect=SpellEffect(special_effects={"horizontal_flight": True})
        ))
        
        # 11. MAGE HAND
        spells.append(WizardSpell(
            name="Mage Hand",
            tier=SpellTier.TIER_2,
            description="Floating hand manipulates objects from Far distance",
            range=SpellRange.FAR,
            base_effect=SpellEffect(
                duration=10,
                special_effects={"telekinetic_hand": True, "carry_weight": 10}
            ),
            lore_fueled_condition=lambda: calendar.is_triune_gaze(),
            lore_fueled_effect=SpellEffect(special_effects={"carry_weight": 50})
        ))
        
        # 12. COUNTERSPELL
        spells.append(WizardSpell(
            name="Counterspell",
            tier=SpellTier.TIER_2,
            description="Reaction to nullify enemy spell",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(special_effects={"counter_spell": True}),
            lore_fueled_condition=lambda: True,  # If countering mastered school
            lore_fueled_effect=SpellEffect(special_effects={"advantage_on_check": True})
        ))
        
        return spells
    
    def _create_tier_3_spells(self) -> List[WizardSpell]:
        """Create all Tier 3 wizard spells."""
        calendar = get_world_calendar()
        spells = []
        
        # 1. FIREBALL
        spells.append(WizardSpell(
            name="Fireball",
            tier=SpellTier.TIER_3,
            description="Explosion deals 5d6 fire damage in Near radius",
            range=SpellRange.FAR,
            base_effect=SpellEffect(
                damage=random.randint(5, 30),
                damage_type="fire",
                area_of_effect=6,
                special_effects={"dex_save_half": True}
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().month == "Highflare",
            lore_fueled_effect=SpellEffect(
                duration=3,
                special_effects={"burning_ground": True, "ground_damage": random.randint(1, 6)}
            )
        ))
        
        # 2. SUMMON ELEMENTAL
        spells.append(WizardSpell(
            name="Summon Elemental",
            tier=SpellTier.TIER_3,
            description="Summon elemental being for 1 minute",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                duration=10,  # 1 minute = 10 rounds
                special_effects={"summon_elemental": True}
            ),
            alignment_effects={
                WizardAlignment.LAWFUL_CONJURER: SpellEffect(special_effects={"elemental_type": "earth", "taunt_ability": True}),
                WizardAlignment.CHAOTIC_CHANNELER: SpellEffect(special_effects={"elemental_type": "fire", "burning_attacks": True}),
                WizardAlignment.NEUTRAL_SEER: SpellEffect(special_effects={"elemental_type": "air", "stun_attacks": True})
            }
        ))
        
        # 3. HASTE
        spells.append(WizardSpell(
            name="Haste",
            tier=SpellTier.TIER_3,
            description="Target gains HASTE for 5 rounds",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                duration=5,
                status_effects=["HASTE"]
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().month == "Suncrest",
            lore_fueled_effect=SpellEffect(special_effects={"slow_immunity": True})
        ))
        
        # 4. BLINK
        spells.append(WizardSpell(
            name="Blink",
            tier=SpellTier.TIER_3,
            description="50% chance each turn to teleport and avoid damage",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                duration=5,
                special_effects={"blink_chance": 0.5, "random_teleport": True}
            ),
            lore_fueled_condition=lambda: calendar.get_moon_phase_name("Myrr") in [MoonPhase.WAXING, MoonPhase.FULL, MoonPhase.DARK],
            lore_fueled_effect=SpellEffect(special_effects={"voluntary_control": True})
        ))
        
        # 5. LIGHTNING BOLT
        spells.append(WizardSpell(
            name="Lightning Bolt",
            tier=SpellTier.TIER_3,
            description="100-foot line deals 6d6 lightning damage",
            range=SpellRange.FAR,
            base_effect=SpellEffect(
                damage=random.randint(6, 36),
                damage_type="lightning",
                special_effects={"line_area": 100, "dex_save_half": True}
            ),
            lore_fueled_condition=lambda: calendar.is_weather_storm,
            lore_fueled_effect=SpellEffect(special_effects={"maximum_damage": True})
        ))
        
        # 6. SUMMON WRAITH
        spells.append(WizardSpell(
            name="Summon Wraith",
            tier=SpellTier.TIER_3,
            description="Spirit attacks with psychic damage and fear",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                damage=random.randint(2, 16),
                damage_type="psychic",
                status_effects=["FRIGHTENED"],
                special_effects={"wis_save_fear": True}
            ),
            requires_focus=True,
            lore_fueled_condition=lambda: calendar.is_night or calendar.get_current_date().month == "Hallowdeep",
            lore_fueled_effect=SpellEffect(special_effects={"can_cast": True})
        ))
        
        # 7. BANISHMENT
        spells.append(WizardSpell(
            name="Banishment",
            tier=SpellTier.TIER_3,
            description="Shunt creature to harmless demiplane for 3 rounds",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                duration=3,
                special_effects={"banished": True, "native_plane_only": False}
            ),
            lore_fueled_condition=lambda: calendar.is_triune_gaze() or calendar.is_eclipserite(),
            lore_fueled_effect=SpellEffect(duration=6)
        ))
        
        # 8. TELEPORT
        spells.append(WizardSpell(
            name="Teleport",
            tier=SpellTier.TIER_3,
            description="Transport up to 5 creatures to visited city",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                special_effects={"long_distance_teleport": True, "mishap_chance": 0.1, "max_targets": 5}
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().day_of_week == "Windmere",
            lore_fueled_effect=SpellEffect(special_effects={"mishap_chance": 0.0})
        ))
        
        return spells
    
    def _create_tier_4_spells(self) -> List[WizardSpell]:
        """Create all Tier 4 wizard spells."""
        calendar = get_world_calendar()
        spells = []
        
        # 1. ICE STORM
        spells.append(WizardSpell(
            name="Ice Storm",
            tier=SpellTier.TIER_4,
            description="Hailstorm deals bludgeoning and cold damage over Far area",
            range=SpellRange.FAR,
            base_effect=SpellEffect(
                damage=random.randint(2, 16) + random.randint(4, 24),  # 2d8 + 4d6
                damage_type="cold",
                area_of_effect=20,
                special_effects={"difficult_terrain": True}
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().month in ["Frostwane", "Snowrest"],
            lore_fueled_effect=SpellEffect(special_effects={"ice_slick": True, "dex_save_prone": True})
        ))
        
        # 2. DOMINATE MIND
        spells.append(WizardSpell(
            name="Dominate Mind",
            tier=SpellTier.TIER_4,
            description="Control humanoid LV 8 or less for 1 minute",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                duration=10,
                status_effects=["DOMINATED"],
                special_effects={"max_level": 8, "humanoid_only": True}
            ),
            requires_focus=True,
            alignment_effects={
                WizardAlignment.LAWFUL_CONJURER: SpellEffect(special_effects={"no_self_harm": True}),
                WizardAlignment.CHAOTIC_CHANNELER: SpellEffect(special_effects={"absolute_control": True, "psychic_feedback": True}),
                WizardAlignment.NEUTRAL_SEER: SpellEffect(special_effects={"friendly_suggestion": True, "defend_caster": True})
            }
        ))
        
        # 3. PRISMATIC WALL
        spells.append(WizardSpell(
            name="Prismatic Wall",
            tier=SpellTier.TIER_4,
            description="Multi-colored wall with different damage effects",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                duration=10,
                special_effects={"prismatic_effects": True, "wall_length": 50}
            ),
            lore_fueled_condition=lambda: calendar.is_triune_gaze(),
            lore_fueled_effect=SpellEffect(special_effects={"protective_dome": True})
        ))
        
        # 4. WALL OF FORCE
        spells.append(WizardSpell(
            name="Wall of Force",
            tier=SpellTier.TIER_4,
            description="Invisible, indestructible wall for 5 rounds",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                duration=5,
                special_effects={"force_wall": True, "wall_length": 50, "indestructible": True}
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().day_of_week == "Stonehold",
            lore_fueled_effect=SpellEffect(duration=10)
        ))
        
        # 5. PLANAR ALLY
        spells.append(WizardSpell(
            name="Planar Ally",
            tier=SpellTier.TIER_4,
            description="Summon powerful being from another plane",
            range=SpellRange.NEAR,
            base_effect=SpellEffect(
                duration=10,
                special_effects={"planar_summon": True}
            ),
            alignment_effects={
                WizardAlignment.LAWFUL_CONJURER: SpellEffect(special_effects={"summon_type": "warden_of_mechanism"}),
                WizardAlignment.CHAOTIC_CHANNELER: SpellEffect(special_effects={"summon_type": "fiend_of_entropy"}),
                WizardAlignment.NEUTRAL_SEER: SpellEffect(special_effects={"summon_type": "warden_of_mechanism"})
            }
        ))
        
        # 6. ETHEREALNESS
        spells.append(WizardSpell(
            name="Etherealness",
            tier=SpellTier.TIER_4,
            description="Become ETHEREAL for 1 minute",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                duration=10,
                status_effects=["ETHEREAL"]
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().day_of_week == "Shadoweve",
            lore_fueled_effect=SpellEffect(special_effects={"see_spirits": True, "hidden_truths": True})
        ))
        
        return spells
    
    def _create_tier_5_spells(self) -> List[WizardSpell]:
        """Create all Tier 5 wizard spells."""
        calendar = get_world_calendar()
        spells = []
        
        # 1. METEOR SWARM
        spells.append(WizardSpell(
            name="Meteor Swarm",
            tier=SpellTier.TIER_5,
            description="Meteors crash dealing 20d6 fire damage over massive area",
            range=SpellRange.FAR,
            base_effect=SpellEffect(
                damage=random.randint(20, 120),
                damage_type="fire",
                area_of_effect=40,
                special_effects={"massive_destruction": True}
            ),
            lore_fueled_condition=lambda: calendar.get_current_date().month == "Highflare",
            lore_fueled_effect=SpellEffect(status_effects=["STUNNED"], special_effects={"shockwave": True})
        ))
        
        # 2. TEMPORAL STASIS
        spells.append(WizardSpell(
            name="Temporal Stasis",
            tier=SpellTier.TIER_5,
            description="Halt time around yourself for 3 rounds",
            range=SpellRange.CLOSE,
            base_effect=SpellEffect(
                duration=3,
                special_effects={"time_stop": True, "free_actions": True, "no_affect_others": True}
            ),
            lore_fueled_condition=lambda: calendar.is_triune_gaze(),
            lore_fueled_effect=SpellEffect(duration=5)
        ))
        
        # 3. SYNAPTIC OVERLOAD
        spells.append(WizardSpell(
            name="Synaptic Overload",
            tier=SpellTier.TIER_5,
            description="Wave of psychic information causes permanent INSANE status",
            range=SpellRange.FAR,
            base_effect=SpellEffect(
                area_of_effect=20,
                status_effects=["INSANE"],
                special_effects={"wis_save_insanity": True, "permanent_effect": True}
            ),
            alignment_effects={
                WizardAlignment.LAWFUL_CONJURER: SpellEffect(special_effects={"caster_madness": 10, "mental_wards": True}),
                WizardAlignment.CHAOTIC_CHANNELER: SpellEffect(special_effects={"caster_madness": 5, "ally_affect_chance": 0.1}),
                WizardAlignment.NEUTRAL_SEER: SpellEffect(special_effects={"caster_madness": 10, "mental_wards": True})
            }
        ))
        
        return spells

# Example usage and spell casting system
class WizardSpellcaster:
    """Manages wizard spellcasting for a character."""
    
    def __init__(self, character):
        self.character = character
        self.spellbook = WizardSpellbook()
        self.known_spells = {}  # spell_name: spell_object
        self.spells_per_day = {
            SpellTier.TIER_1: 3,
            SpellTier.TIER_2: 2,
            SpellTier.TIER_3: 1,
            SpellTier.TIER_4: 0,
            SpellTier.TIER_5: 0
        }
        self.spells_used_today = {tier: 0 for tier in SpellTier}
        self.mastered_schools = []  # For counterspell bonus
    
    def learn_spell(self, spell_name: str) -> bool:
        """Learn a new spell."""
        spell = self.spellbook.get_spell(spell_name)
        if spell:
            self.known_spells[spell_name] = spell
            print(f"📖 {self.character.name} learned {spell_name}")
            return True
        return False
    
    def can_cast_spell(self, spell_name: str) -> bool:
        """Check if spell can be cast."""
        if spell_name not in self.known_spells:
            return False
        
        spell = self.known_spells[spell_name]
        tier = spell.tier
        
        return self.spells_used_today[tier] < self.spells_per_day[tier]
    
    def cast_spell(self, spell_name: str, target=None, target_position=None) -> bool:
        """Cast a spell."""
        if not self.can_cast_spell(spell_name):
            print(f"❌ Cannot cast {spell_name} - insufficient spell slots or unknown spell")
            return False
        
        spell = self.known_spells[spell_name]
        
        # Use spell slot
        self.spells_used_today[spell.tier] += 1
        
        # Cast the spell
        effect = spell.cast(self.character, target, target_position)
        
        print(f"✨ {self.character.name} casts {spell_name}!")
        
        # Apply effects to target
        if target and hasattr(target, 'status_effects'):
            for status_name in effect.status_effects:
                status_effect = create_status_effect(status_name)
                if status_effect:
                    target.status_effects.add_effect(status_effect)
        
        # Apply damage
        if effect.damage > 0 and target:
            if hasattr(target, 'take_damage'):
                target.take_damage(effect.damage, effect.damage_type)
        
        # Apply healing
        if effect.healing > 0 and target:
            if hasattr(target, 'heal'):
                target.heal(effect.healing)
        
        return True
    
    def rest(self):
        """Rest to recover spell slots."""
        self.spells_used_today = {tier: 0 for tier in SpellTier}
        print(f"🛌 {self.character.name} rests and recovers all spell slots")
    
    def get_available_spells(self) -> Dict[SpellTier, List[str]]:
        """Get spells available to cast by tier."""
        available = {}
        for tier in SpellTier:
            if self.spells_used_today[tier] < self.spells_per_day[tier]:
                available[tier] = [name for name, spell in self.known_spells.items() 
                                 if spell.tier == tier]
        return available