"""
Updated Wizard and Priest Spell Systems
Based on the new spell documents with lore-fueled and divine mechanics.
Replaces the old spell system implementations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import random

from data.calendar import get_world_calendar, MoonPhase

class SpellTier(Enum):
    """Spell power tiers."""
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3
    TIER_4 = 4
    TIER_5 = 5

class SpellRange(Enum):
    """Spell range categories."""
    CLOSE = "Close"      # 5 feet = 1 cell
    NEAR = "Near"        # 30 feet = 6 cells
    FAR = "Far"          # Within sight = 20 cells

class AlignmentType(Enum):
    """Character alignment types."""
    LAWFUL = "Lawful"
    CHAOTIC = "Chaotic"
    NEUTRAL = "Neutral"

@dataclass
class SpellEffect:
    """Represents the result of casting a spell."""
    damage: str = ""
    damage_type: str = ""
    healing: int = 0
    status_effects: List[str] = field(default_factory=list)
    special_effects: Dict[str, Any] = field(default_factory=dict)
    area_of_effect: int = 0  # Size in cells
    duration: int = 0  # In rounds
    requires_save: str = ""  # DEX, CON, WIS, etc.
    
    def __str__(self):
        parts = []
        if self.damage:
            parts.append(f"Damage: {self.damage} {self.damage_type}")
        if self.healing:
            parts.append(f"Healing: {self.healing}")
        if self.status_effects:
            parts.append(f"Effects: {', '.join(self.status_effects)}")
        if self.duration:
            parts.append(f"Duration: {self.duration} rounds")
        return "; ".join(parts) if parts else "No effect"

@dataclass
class Spell:
    """Base spell class for both wizard and priest spells."""
    name: str
    tier: SpellTier
    description: str
    range: SpellRange
    base_effect: SpellEffect
    requires_focus: bool = False
    
    # Lore-fueled conditions and effects
    lore_condition_text: str = ""
    lore_fueled_effect: Optional[SpellEffect] = None
    
    # Alignment-based effects for wizards
    alignment_effects: Dict[AlignmentType, SpellEffect] = field(default_factory=dict)
    
    def check_lore_condition(self) -> bool:
        """Check if lore-fueled conditions are met."""
        if not self.lore_condition_text:
            return False
            
        calendar = get_world_calendar()
        current_date = calendar.get_current_date()
        
        # Parse common conditions
        if "Frostwane" in self.lore_condition_text:
            return current_date.month == "Frostwane"
        elif "Flameday" in self.lore_condition_text:
            return current_date.day_of_week == "Flameday"
        elif "Greentide" in self.lore_condition_text or "Blossarch" in self.lore_condition_text:
            return current_date.month in ["Greentide", "Blossarch"]
        elif "Wyrmday" in self.lore_condition_text:
            return current_date.day_of_week == "Wyrmday"
        elif "Velmara" in self.lore_condition_text and "Waxing" in self.lore_condition_text:
            return calendar.get_moon_phase_name("Velmara") in [MoonPhase.WAXING, MoonPhase.FULL]
        elif "Velmara" in self.lore_condition_text and "Full" in self.lore_condition_text:
            return calendar.is_moon_full("Velmara")
        elif "Windmere" in self.lore_condition_text:
            return current_date.day_of_week == "Windmere"
        elif "Caelyra" in self.lore_condition_text and "Full" in self.lore_condition_text:
            return calendar.is_moon_full("Caelyra")
        elif "Shadoweve" in self.lore_condition_text:
            return current_date.day_of_week == "Shadoweve"
        elif "Myrr" in self.lore_condition_text and "visible" in self.lore_condition_text:
            return calendar.get_moon_phase_name("Myrr") in [MoonPhase.WAXING, MoonPhase.FULL, MoonPhase.DARK]
        elif "Stonehold" in self.lore_condition_text:
            return current_date.day_of_week == "Stonehold"
        elif "Duskwane" in self.lore_condition_text:
            return current_date.month == "Duskwane"
        elif "Mournfall" in self.lore_condition_text:
            return current_date.month == "Mournfall"
        elif "Hallowdeep" in self.lore_condition_text:
            return current_date.month == "Hallowdeep"
        elif "Suncrest" in self.lore_condition_text or "Highflare" in self.lore_condition_text:
            return current_date.month in ["Suncrest", "Highflare"]
        elif "Moonday" in self.lore_condition_text:
            return current_date.day_of_week == "Moonday"
        elif "Triune Gaze" in self.lore_condition_text:
            return calendar.is_triune_gaze()
        elif "Myrr" in self.lore_condition_text and ("Full" in self.lore_condition_text or "Dark" in self.lore_condition_text):
            return calendar.get_moon_phase_name("Myrr") in [MoonPhase.FULL, MoonPhase.DARK]
        
        return False
    
    def cast(self, caster, target=None, target_position=None) -> SpellEffect:
        """Cast the spell and return the combined effect."""
        effect = self.base_effect
        
        # Check for lore-fueled enhancement
        if self.check_lore_condition() and self.lore_fueled_effect:
            effect = self._combine_effects(effect, self.lore_fueled_effect)
            print(f"✨ {self.name} is empowered by cosmic forces!")
        
        # Check for alignment-based modifications (wizards)
        if hasattr(caster, 'alignment') and caster.alignment in self.alignment_effects:
            alignment_effect = self.alignment_effects[caster.alignment]
            effect = self._combine_effects(effect, alignment_effect)
            print(f"🔮 {self.name} modified by {caster.alignment} alignment!")
        
        return effect
    
    def _combine_effects(self, base: SpellEffect, modifier: SpellEffect) -> SpellEffect:
        """Combine two spell effects."""
        # Create new effect with combined properties
        combined = SpellEffect(
            damage=modifier.damage or base.damage,
            damage_type=modifier.damage_type or base.damage_type,
            healing=base.healing + modifier.healing,
            status_effects=base.status_effects + modifier.status_effects,
            special_effects={**base.special_effects, **modifier.special_effects},
            area_of_effect=max(base.area_of_effect, modifier.area_of_effect),
            duration=max(base.duration, modifier.duration),
            requires_save=modifier.requires_save or base.requires_save
        )
        return combined

# ===== WIZARD SPELLS =====

class WizardSpellbook:
    """Complete wizard spell collection organized by tier."""
    
    def __init__(self):
        self.spells_by_tier = {
            SpellTier.TIER_1: self._create_wizard_tier_1(),
            SpellTier.TIER_2: self._create_wizard_tier_2(),
            SpellTier.TIER_3: self._create_wizard_tier_3(),
            SpellTier.TIER_4: self._create_wizard_tier_4(),
            SpellTier.TIER_5: self._create_wizard_tier_5()
        }
        
        # Flatten for easy lookup
        self.all_spells = {}
        for tier_spells in self.spells_by_tier.values():
            for spell in tier_spells:
                self.all_spells[spell.name] = spell
    
    def get_spell(self, spell_name: str) -> Optional[Spell]:
        """Get a spell by name."""
        return self.all_spells.get(spell_name)
    
    def get_spells_by_tier(self, tier: SpellTier) -> List[Spell]:
        """Get all spells of a specific tier."""
        return self.spells_by_tier.get(tier, [])
    
    def _create_wizard_tier_1(self) -> List[Spell]:
        """Create Tier 1 wizard spells."""
        return [
            Spell(
                name="Frostwane Bite",
                tier=SpellTier.TIER_1,
                description="Deals 1d6 cold damage and applies FROSTBITTEN",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    damage="1d6",
                    damage_type="cold",
                    status_effects=["FROSTBITTEN"]
                ),
                lore_condition_text="In Frostwane",
                lore_fueled_effect=SpellEffect(status_effects=["SLOW"], duration=1)
            ),
            
            Spell(
                name="Embermarch Coals",
                tier=SpellTier.TIER_1,
                description="Creates a Close-sized area of 1d4 fire damage per round for 5 rounds",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    damage="1d4",
                    damage_type="fire",
                    area_of_effect=1,
                    duration=5,
                    special_effects={"damage_per_round": True}
                ),
                lore_condition_text="On Flameday",
                lore_fueled_effect=SpellEffect(duration=10)
            ),
            
            Spell(
                name="Greentide's Grasp",
                tier=SpellTier.TIER_1,
                description="Applies ROOTED to one target",
                range=SpellRange.NEAR,
                base_effect=SpellEffect(status_effects=["ROOTED"]),
                lore_condition_text="During Greentide or Blossarch",
                lore_fueled_effect=SpellEffect(special_effects={"str_check_disadvantage": True})
            ),
            
            Spell(
                name="Force Bolt",
                tier=SpellTier.TIER_1,
                description="Automatically hits one target for 1d4+1 force damage",
                range=SpellRange.NEAR,
                base_effect=SpellEffect(
                    damage="1d4+1",
                    damage_type="force",
                    special_effects={"auto_hit": True}
                ),
                lore_condition_text="On Wyrmday",
                lore_fueled_effect=SpellEffect(status_effects=["MANA_BURN"])
            ),
            
            Spell(
                name="Architect's Seal",
                tier=SpellTier.TIER_1,
                description="Magically locks a door or container for 1 hour",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    duration=60,
                    special_effects={"magical_lock": True}
                ),
                lore_condition_text="When Velmara is Waxing/Full",
                lore_fueled_effect=SpellEffect(special_effects={"str_break_disadvantage": True})
            ),
            
            Spell(
                name="Continual Flame",
                tier=SpellTier.TIER_1,
                description="Object glows with bright, heatless light that reveals invisible creatures",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    duration=-1,
                    special_effects={"light_source": True, "reveal_invisible": True}
                ),
                lore_condition_text="When Velmara is Full",
                lore_fueled_effect=SpellEffect(special_effects={"no_material_component": True})
            ),
            
            Spell(
                name="Feather Fall",
                tier=SpellTier.TIER_1,
                description="Negates all fall damage when cast as a reaction",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(special_effects={"negate_fall_damage": True}),
                lore_condition_text="On Windmere",
                lore_fueled_effect=SpellEffect(status_effects=["HASTE"], duration=1)
            ),
            
            Spell(
                name="Runic Ward",
                tier=SpellTier.TIER_1,
                description="Sets AC to 14 for 5 rounds",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    duration=5,
                    special_effects={"set_ac": 14}
                ),
                lore_condition_text="If Caelyra is Full",
                lore_fueled_effect=SpellEffect(special_effects={"set_ac": 15})
            ),
            
            Spell(
                name="Shifting Shadow",
                tier=SpellTier.TIER_1,
                description="Become INVISIBLE until you move or act",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    status_effects=["INVISIBLE"],
                    special_effects={"breaks_on_action": True}
                ),
                lore_condition_text="On Shadoweve",
                lore_fueled_effect=SpellEffect(special_effects={"persists_after_move": True})
            ),
            
            Spell(
                name="Arcane Sight",
                tier=SpellTier.TIER_1,
                description="See magical auras within Near range",
                range=SpellRange.NEAR,
                base_effect=SpellEffect(
                    duration=10,
                    special_effects={"detect_magic": True}
                ),
                lore_condition_text="When Myrr is visible",
                lore_fueled_effect=SpellEffect(special_effects={"reveal_alignment": True})
            ),
            
            Spell(
                name="Sentry Rune",
                tier=SpellTier.TIER_1,
                description="Invisible rune alerts when touched",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    duration=8,
                    special_effects={"invisible_alarm": True}
                ),
                lore_condition_text="On Stonehold",
                lore_fueled_effect=SpellEffect(duration=24)
            ),
            
            Spell(
                name="Duskwane Drowse",
                tier=SpellTier.TIER_1,
                description="Puts creatures with 5 HP or less to SLEEP in Near area",
                range=SpellRange.NEAR,
                base_effect=SpellEffect(
                    area_of_effect=6,
                    status_effects=["SLEEP"],
                    special_effects={"hp_threshold": 5}
                ),
                lore_condition_text="During Duskwane",
                lore_fueled_effect=SpellEffect(special_effects={"hp_threshold": 10})
            )
        ]
    
    def _create_wizard_tier_2(self) -> List[Spell]:
        """Create Tier 2 wizard spells."""
        return [
            Spell(
                name="Acid Arrow",
                tier=SpellTier.TIER_2,
                description="Bolt deals 1d4 acid damage per round",
                range=SpellRange.NEAR,
                base_effect=SpellEffect(
                    damage="1d4",
                    damage_type="acid",
                    duration=3,
                    special_effects={"damage_per_round": True}
                ),
                requires_focus=True,
                lore_condition_text="During Mournfall",
                lore_fueled_effect=SpellEffect(status_effects=["ARMOR_DECAY"])
            ),
            
            Spell(
                name="Mirror Image",
                tier=SpellTier.TIER_2,
                description="Create illusory duplicates that absorb attacks",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    duration=10,
                    special_effects={"mirror_images": 3, "hits_per_image": 1}
                ),
                alignment_effects={
                    AlignmentType.LAWFUL: SpellEffect(special_effects={"mirror_images": 2, "hits_per_image": 2}),
                    AlignmentType.CHAOTIC: SpellEffect(special_effects={"mirror_images": 4, "hits_per_image": 1}),
                    AlignmentType.NEUTRAL: SpellEffect(special_effects={"mirror_images": 3, "hits_per_image": 1})
                }
            ),
            
            Spell(
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
                lore_condition_text="During Hallowdeep",
                lore_fueled_effect=SpellEffect(status_effects=["ROOTED", "BLIND"])
            ),
            
            Spell(
                name="Misty Step",
                tier=SpellTier.TIER_2,
                description="Instantly teleport to visible spot within Near range",
                range=SpellRange.NEAR,
                base_effect=SpellEffect(special_effects={"teleport": True}),
                lore_condition_text="On Moonday",
                lore_fueled_effect=SpellEffect(special_effects={"dream_cloud": True})
            ),
            
            Spell(
                name="Invisibility",
                tier=SpellTier.TIER_2,
                description="Target becomes INVISIBLE for 10 rounds",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    duration=10,
                    status_effects=["INVISIBLE"],
                    special_effects={"breaks_on_attack": True}
                ),
                lore_condition_text="On Shadoweve",
                lore_fueled_effect=SpellEffect(special_effects={"utility_spells_safe": True})
            ),
            
            Spell(
                name="Suncrest Scorch",
                tier=SpellTier.TIER_2,
                description="Ray of light deals 2d8 radiant damage",
                range=SpellRange.FAR,
                base_effect=SpellEffect(
                    damage="2d8",
                    damage_type="radiant"
                ),
                lore_condition_text="During Suncrest or Highflare",
                lore_fueled_effect=SpellEffect(status_effects=["BLIND"], duration=3, requires_save="CON")
            )
        ]
    
    def _create_wizard_tier_3(self) -> List[Spell]:
        """Create Tier 3 wizard spells."""
        return [
            Spell(
                name="Fireball",
                tier=SpellTier.TIER_3,
                description="Explosion deals 5d6 fire damage in Near radius",
                range=SpellRange.FAR,
                base_effect=SpellEffect(
                    damage="5d6",
                    damage_type="fire",
                    area_of_effect=6,
                    requires_save="DEX"
                ),
                lore_condition_text="During Highflare",
                lore_fueled_effect=SpellEffect(
                    duration=3,
                    special_effects={"burning_ground": True, "ground_damage": "1d6"}
                )
            ),
            
            Spell(
                name="Lightning Bolt",
                tier=SpellTier.TIER_3,
                description="100-foot line deals 6d6 lightning damage",
                range=SpellRange.FAR,
                base_effect=SpellEffect(
                    damage="6d6",
                    damage_type="lightning",
                    special_effects={"line_area": 100},
                    requires_save="DEX"
                ),
                lore_condition_text="During a storm",
                lore_fueled_effect=SpellEffect(special_effects={"maximum_damage": True})
            ),
            
            Spell(
                name="Haste",
                tier=SpellTier.TIER_3,
                description="Target gains HASTE for 5 rounds",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    duration=5,
                    status_effects=["HASTE"]
                ),
                lore_condition_text="During Suncrest",
                lore_fueled_effect=SpellEffect(special_effects={"slow_immunity": True})
            )
        ]
    
    def _create_wizard_tier_4(self) -> List[Spell]:
        """Create Tier 4 wizard spells."""
        return [
            Spell(
                name="Ice Storm",
                tier=SpellTier.TIER_4,
                description="Hailstorm deals bludgeoning and cold damage over Far area",
                range=SpellRange.FAR,
                base_effect=SpellEffect(
                    damage="2d8+4d6",
                    damage_type="cold",
                    area_of_effect=20,
                    special_effects={"difficult_terrain": True}
                ),
                lore_condition_text="During Frostwane or Snowrest",
                lore_fueled_effect=SpellEffect(
                    special_effects={"ice_slick": True, "dex_save_prone": True},
                    requires_save="DEX"
                )
            )
        ]
    
    def _create_wizard_tier_5(self) -> List[Spell]:
        """Create Tier 5 wizard spells."""
        return [
            Spell(
                name="Meteor Swarm",
                tier=SpellTier.TIER_5,
                description="Meteors crash dealing 20d6 fire damage over massive area",
                range=SpellRange.FAR,
                base_effect=SpellEffect(
                    damage="20d6",
                    damage_type="fire",
                    area_of_effect=40,
                    special_effects={"massive_destruction": True}
                ),
                lore_condition_text="During Highflare",
                lore_fueled_effect=SpellEffect(
                    status_effects=["STUNNED"],
                    special_effects={"shockwave": True}
                )
            )
        ]

# ===== PRIEST SPELLS =====

class PriestSpellbook:
    """Complete priest spell collection organized by tier."""
    
    def __init__(self):
        self.spells_by_tier = {
            SpellTier.TIER_1: self._create_priest_tier_1(),
            SpellTier.TIER_2: self._create_priest_tier_2(),
            SpellTier.TIER_3: self._create_priest_tier_3(),
            SpellTier.TIER_4: self._create_priest_tier_4(),
            SpellTier.TIER_5: self._create_priest_tier_5()
        }
        
        # Flatten for easy lookup
        self.all_spells = {}
        for tier_spells in self.spells_by_tier.values():
            for spell in tier_spells:
                self.all_spells[spell.name] = spell
    
    def get_spell(self, spell_name: str) -> Optional[Spell]:
        """Get a spell by name."""
        return self.all_spells.get(spell_name)
    
    def get_spells_by_tier(self, tier: SpellTier) -> List[Spell]:
        """Get all spells of a specific tier."""
        return self.spells_by_tier.get(tier, [])
    
    def _create_priest_tier_1(self) -> List[Spell]:
        """Create Tier 1 priest spells."""
        return [
            Spell(
                name="Serentha's Touch",
                tier=SpellTier.TIER_1,
                description="A gentle, healing touch. Restores 1d8+2 hit points",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(healing=8),  # Simplified as average
                lore_condition_text="During Greentide or Blossarch",
                lore_fueled_effect=SpellEffect(special_effects={"remove_poisoned": True})
            ),
            
            Spell(
                name="Caedros's Aegis",
                tier=SpellTier.TIER_1,
                description="Divine protection. +2 bonus to Armor Class for 5 rounds",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    duration=5,
                    special_effects={"ac_bonus": 2}
                ),
                lore_condition_text="If Caelyra moon is Full",
                lore_fueled_effect=SpellEffect(special_effects={"reflect_damage": "1d4"})
            ),
            
            Spell(
                name="Zyrix's Fury",
                tier=SpellTier.TIER_1,
                description="Channel battlefield rage. +2 bonus to all damage rolls for 3 rounds",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    duration=3,
                    special_effects={"damage_bonus": 2}
                ),
                lore_condition_text="On Flameday",
                lore_fueled_effect=SpellEffect(duration=5)
            ),
            
            Spell(
                name="Velmari's Hearthlight",
                tier=SpellTier.TIER_1,
                description="Create a stationary flame that deters weak enemies",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    duration=10,
                    special_effects={"light_source": True, "deter_weak_enemies": 10}
                ),
                lore_condition_text="On Stonehold",
                lore_fueled_effect=SpellEffect(special_effects={"safe_camp_benefit": True})
            ),
            
            Spell(
                name="Nymbril's Call",
                tier=SpellTier.TIER_1,
                description="Magically beseech one beast of LV 2 or less",
                range=SpellRange.NEAR,
                base_effect=SpellEffect(
                    duration=1,
                    special_effects={"charm_beast": 2},
                    requires_save="WIS"
                ),
                lore_condition_text="During Duskwane",
                lore_fueled_effect=SpellEffect(special_effects={"charm_beast": 4})
            ),
            
            Spell(
                name="Vhalor's Weariness",
                tier=SpellTier.TIER_1,
                description="Touch inflicts entropy. Target gains WEAKENED for 3 rounds",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    duration=3,
                    status_effects=["WEAKENED"]
                ),
                lore_condition_text="During Hallowdeep",
                lore_fueled_effect=SpellEffect(status_effects=["WEAKENED", "SLOW"])
            )
        ]
    
    def _create_priest_tier_2(self) -> List[Spell]:
        """Create Tier 2 priest spells."""
        return [
            Spell(
                name="Blade of Judgment",
                tier=SpellTier.TIER_2,
                description="Weapon deals additional 1d6 radiant damage for 5 rounds",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    duration=5,
                    special_effects={"weapon_enchant": "1d6", "double_vs_chaotic": True}
                ),
                lore_condition_text="If target has OATHBREAKER flag",
                lore_fueled_effect=SpellEffect(special_effects={"maximize_radiant": True})
            ),
            
            Spell(
                name="Mercy's Relief",
                tier=SpellTier.TIER_2,
                description="Remove BLIND, DEAFENED, DISEASED, or PARALYZED",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    special_effects={"remove_conditions": ["BLIND", "DEAFENED", "DISEASED", "PARALYZED"]}
                ),
                lore_condition_text="On Soulday",
                lore_fueled_effect=SpellEffect(special_effects={"remove_two_conditions": True})
            ),
            
            Spell(
                name="Olvenar's Whisper",
                tier=SpellTier.TIER_2,
                description="Reveal enemy's lowest resistance and make them vulnerable",
                range=SpellRange.NEAR,
                base_effect=SpellEffect(
                    duration=3,
                    special_effects={"reveal_weakness": True, "make_vulnerable": True}
                ),
                lore_condition_text="On Shadoweve",
                lore_fueled_effect=SpellEffect(special_effects={"reveal_abilities": True})
            )
        ]
    
    def _create_priest_tier_3(self) -> List[Spell]:
        """Create Tier 3 priest spells."""
        return [
            Spell(
                name="Circle of Succor",
                tier=SpellTier.TIER_3,
                description="Create healing circle for 3 rounds",
                range=SpellRange.NEAR,
                base_effect=SpellEffect(
                    duration=3,
                    area_of_effect=6,
                    special_effects={"healing_circle": "1d6"}
                ),
                lore_condition_text="During Greentide",
                lore_fueled_effect=SpellEffect(special_effects={"ac_bonus": 1})
            ),
            
            Spell(
                name="Chains of Law",
                tier=SpellTier.TIER_3,
                description="Gleaming chains bind one creature with STUNNED",
                range=SpellRange.NEAR,
                base_effect=SpellEffect(
                    duration=3,
                    status_effects=["STUNNED"],
                    requires_save="STR"
                ),
                requires_focus=True,
                lore_condition_text="Against chaotic-aligned target",
                lore_fueled_effect=SpellEffect(special_effects={"no_focus_required": True})
            )
        ]
    
    def _create_priest_tier_4(self) -> List[Spell]:
        """Create Tier 4 priest spells."""
        return [
            Spell(
                name="Serentha's Rebirth",
                tier=SpellTier.TIER_4,
                description="Return dead ally to life with half hit points",
                range=SpellRange.CLOSE,
                base_effect=SpellEffect(
                    special_effects={"resurrect": 0.5}
                ),
                lore_condition_text="On Soulday",
                lore_fueled_effect=SpellEffect(special_effects={"resurrect": 1.0})
            ),
            
            Spell(
                name="Curse of Entropy",
                tier=SpellTier.TIER_4,
                description="Powerful curse prevents healing and reduces armor",
                range=SpellRange.NEAR,
                base_effect=SpellEffect(
                    duration=10,
                    special_effects={
                        "no_healing": True,
                        "armor_reduction": 2,
                        "weapon_destruction_chance": 0.25
                    }
                ),
                lore_condition_text="If target dies while cursed",
                lore_fueled_effect=SpellEffect(special_effects={"prevent_resurrection": True})
            )
        ]
    
    def _create_priest_tier_5(self) -> List[Spell]:
        """Create Tier 5 priest spells."""
        return [
            Spell(
                name="Wellspring of Life",
                tier=SpellTier.TIER_5,
                description="Massive zone of divine healing",
                range=SpellRange.FAR,
                base_effect=SpellEffect(
                    area_of_effect=20,
                    special_effects={
                        "heal_to_max": True,
                        "resurrect_recent_dead": 0.25
                    }
                ),
                lore_condition_text="Permanently consecrates ground",
                lore_fueled_effect=SpellEffect(special_effects={"consecrated_ground": True})
            ),
            
            Spell(
                name="Vhalor's Final Hunger",
                tier=SpellTier.TIER_5,
                description="Mark target with inevitable doom",
                range=SpellRange.NEAR,
                base_effect=SpellEffect(
                    duration=3,
                    special_effects={"doom_mark": 100}
                ),
                lore_condition_text="If target is slain by this spell",
                lore_fueled_effect=SpellEffect(
                    special_effects={
                        "consume_soul": True,
                        "caster_hp_bonus": 5
                    }
                )
            )
        ]

# Spellcasting management classes
class Spellcaster:
    """Base spellcasting manager for characters."""
    
    def __init__(self, character, spellbook_class):
        self.character = character
        self.spellbook = spellbook_class()
        self.known_spells = {}  # spell_name: spell_object
        self.spells_per_day = {tier: 0 for tier in SpellTier}
        self.spells_used_today = {tier: 0 for tier in SpellTier}
        
    def learn_spell(self, spell_name: str) -> bool:
        """Learn a new spell."""
        spell = self.spellbook.get_spell(spell_name)
        if spell:
            self.known_spells[spell_name] = spell
            return True
        return False
    
    def can_cast_spell(self, spell_name: str) -> bool:
        """Check if spell can be cast."""
        if spell_name not in self.known_spells:
            return False
        
        spell = self.known_spells[spell_name]
        return self.spells_used_today[spell.tier] < self.spells_per_day[spell.tier]
    
    def cast_spell(self, spell_name: str, target=None, target_position=None) -> bool:
        """Cast a spell."""
        if not self.can_cast_spell(spell_name):
            return False
        
        spell = self.known_spells[spell_name]
        self.spells_used_today[spell.tier] += 1
        
        # Cast the spell
        effect = spell.cast(self.character, target, target_position)
        print(f"✨ {self.character.name} casts {spell_name}!")
        print(f"   Effect: {effect}")
        
        return True
    
    def rest(self):
        """Rest to recover spell slots."""
        self.spells_used_today = {tier: 0 for tier in SpellTier}

class WizardSpellcaster(Spellcaster):
    """Wizard-specific spellcasting manager."""
    
    def __init__(self, character):
        super().__init__(character, WizardSpellbook)
        # Set wizard spell slots per day
        self.spells_per_day = {
            SpellTier.TIER_1: 3,
            SpellTier.TIER_2: 2,
            SpellTier.TIER_3: 1,
            SpellTier.TIER_4: 0,
            SpellTier.TIER_5: 0
        }

class PriestSpellcaster(Spellcaster):
    """Priest-specific spellcasting manager."""
    
    def __init__(self, character):
        super().__init__(character, PriestSpellbook)
        # Set priest spell slots per day
        self.spells_per_day = {
            SpellTier.TIER_1: 2,
            SpellTier.TIER_2: 1,
            SpellTier.TIER_3: 1,
            SpellTier.TIER_4: 0,
            SpellTier.TIER_5: 0
        }

# Integration function to add spellcasting to existing characters
def add_spellcasting_to_character(character):
    """Add appropriate spellcasting to a character based on their class."""
    if character.character_class == "Wizard":
        character.spellcaster = WizardSpellcaster(character)
    elif character.character_class == "Priest":
        character.spellcaster = PriestSpellcaster(character)
    else:
        character.spellcaster = None
    
    return character.spellcaster

# Example usage
if __name__ == "__main__":
    # Test the spell system
    from data.player import create_default_player
    
    player = create_default_player()
    player.character_class = "Wizard"
    player.alignment = "Chaotic"
    
    spellcaster = add_spellcasting_to_character(player)
    
    # Learn some spells
    spellcaster.learn_spell("Fireball")
    spellcaster.learn_spell("Mirror Image")
    
    # Cast spells
    spellcaster.cast_spell("Mirror Image")
    spellcaster.cast_spell("Fireball")