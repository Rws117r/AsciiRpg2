"""
Status Effect and Buff/Debuff System
Comprehensive system for managing temporary character modifications.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import time

class StatusType(Enum):
    """Types of status effects."""
    BUFF = "buff"
    DEBUFF = "debuff"
    NEUTRAL = "neutral"

class StatusCategory(Enum):
    """Categories of status effects."""
    COMBAT = "combat"
    MOVEMENT = "movement"
    MENTAL = "mental"
    PHYSICAL = "physical"
    MAGICAL = "magical"
    ENVIRONMENTAL = "environmental"

class StatusDuration(Enum):
    """Duration types for status effects."""
    INSTANT = "instant"
    TEMPORARY = "temporary"
    PERMANENT = "permanent"
    CONDITIONAL = "conditional"

@dataclass
class StatusEffect:
    """Base class for all status effects."""
    name: str
    type: StatusType
    category: StatusCategory
    duration_type: StatusDuration
    duration: float = 0.0  # In rounds/turns for temporary effects
    max_duration: float = 0.0  # Original duration for reference
    stacks: int = 1
    max_stacks: int = 1
    description: str = ""
    icon: str = ""
    
    # Effect modifiers
    stat_modifiers: Dict[str, float] = field(default_factory=dict)
    percentage_modifiers: Dict[str, float] = field(default_factory=dict)
    special_effects: Dict[str, Any] = field(default_factory=dict)
    
    # Callbacks
    on_apply: Optional[Callable] = None
    on_remove: Optional[Callable] = None
    on_tick: Optional[Callable] = None
    
    def apply_to_character(self, character):
        """Apply this status effect to a character."""
        if self.on_apply:
            self.on_apply(character, self)
    
    def remove_from_character(self, character):
        """Remove this status effect from a character.""" 
        if self.on_remove:
            self.on_remove(character, self)
    
    def tick(self, character):
        """Called each turn/round for ongoing effects."""
        if self.duration_type == StatusDuration.TEMPORARY:
            self.duration -= 1
        
        if self.on_tick:
            self.on_tick(character, self)
        
        return self.duration > 0 if self.duration_type == StatusDuration.TEMPORARY else True
    
    def can_stack_with(self, other_effect: 'StatusEffect') -> bool:
        """Check if this effect can stack with another effect."""
        return (self.name == other_effect.name and 
                self.stacks < self.max_stacks)

class StatusEffectManager:
    """Manages status effects on a character."""
    
    def __init__(self, character):
        self.character = character
        self.active_effects: Dict[str, StatusEffect] = {}
        self.effect_history: List[StatusEffect] = []
    
    def add_effect(self, effect: StatusEffect) -> bool:
        """Add a status effect to the character."""
        existing_effect = self.active_effects.get(effect.name)
        
        if existing_effect:
            if existing_effect.can_stack_with(effect):
                # Stack the effect
                existing_effect.stacks += effect.stacks
                existing_effect.stacks = min(existing_effect.stacks, existing_effect.max_stacks)
                # Refresh duration
                if effect.duration > existing_effect.duration:
                    existing_effect.duration = effect.duration
                return True
            else:
                # Replace with new effect
                self.remove_effect(effect.name)
        
        # Add new effect
        self.active_effects[effect.name] = effect
        effect.apply_to_character(self.character)
        self.effect_history.append(effect)
        
        print(f"✨ {effect.name} applied to {self.character.name}")
        return True
    
    def remove_effect(self, effect_name: str) -> bool:
        """Remove a status effect by name."""
        if effect_name in self.active_effects:
            effect = self.active_effects[effect_name]
            effect.remove_from_character(self.character)
            del self.active_effects[effect_name]
            print(f"🔄 {effect_name} removed from {self.character.name}")
            return True
        return False
    
    def has_effect(self, effect_name: str) -> bool:
        """Check if character has a specific effect."""
        return effect_name in self.active_effects
    
    def get_effect(self, effect_name: str) -> Optional[StatusEffect]:
        """Get a specific active effect."""
        return self.active_effects.get(effect_name)
    
    def tick_all_effects(self):
        """Update all active effects (called each turn)."""
        effects_to_remove = []
        
        for effect_name, effect in self.active_effects.items():
            if not effect.tick(self.character):
                effects_to_remove.append(effect_name)
        
        # Remove expired effects
        for effect_name in effects_to_remove:
            self.remove_effect(effect_name)
    
    def get_stat_modifier(self, stat_name: str) -> float:
        """Get total modifier for a stat from all active effects."""
        total_modifier = 0.0
        percentage_modifier = 1.0
        
        for effect in self.active_effects.values():
            # Flat modifiers
            if stat_name in effect.stat_modifiers:
                total_modifier += effect.stat_modifiers[stat_name] * effect.stacks
            
            # Percentage modifiers
            if stat_name in effect.percentage_modifiers:
                percentage_modifier *= (1.0 + effect.percentage_modifiers[stat_name]) ** effect.stacks
        
        return total_modifier * percentage_modifier
    
    def has_special_effect(self, effect_name: str) -> bool:
        """Check if any active effect provides a special effect."""
        return any(effect_name in effect.special_effects 
                  for effect in self.active_effects.values())
    
    def get_all_special_effects(self) -> Dict[str, Any]:
        """Get all special effects from active status effects."""
        special_effects = {}
        for effect in self.active_effects.values():
            special_effects.update(effect.special_effects)
        return special_effects
    
    def clear_all_effects(self):
        """Remove all status effects."""
        for effect_name in list(self.active_effects.keys()):
            self.remove_effect(effect_name)
    
    def clear_debuffs(self):
        """Remove all debuff effects."""
        debuffs_to_remove = [name for name, effect in self.active_effects.items() 
                           if effect.type == StatusType.DEBUFF]
        for effect_name in debuffs_to_remove:
            self.remove_effect(effect_name)
    
    def get_effects_summary(self) -> List[str]:
        """Get a summary of all active effects."""
        return [f"{effect.name} ({effect.stacks})" + 
                (f" - {effect.duration:.0f} turns" if effect.duration_type == StatusDuration.TEMPORARY else "")
                for effect in self.active_effects.values()]

# Status Effect Factory - Creates predefined status effects
class StatusEffectFactory:
    """Factory for creating common status effects."""
    
    @staticmethod
    def create_haste() -> StatusEffect:
        """Create HASTE status effect."""
        return StatusEffect(
            name="HASTE",
            type=StatusType.BUFF,
            category=StatusCategory.COMBAT,
            duration_type=StatusDuration.TEMPORARY,
            duration=5,
            max_duration=5,
            description="Grants extra action, +2 AC, advantage on DEX checks",
            stat_modifiers={"ac": 2},
            special_effects={
                "extra_action": True,
                "dex_advantage": True
            }
        )
    
    @staticmethod
    def create_paralyzed() -> StatusEffect:
        """Create PARALYZED status effect."""
        return StatusEffect(
            name="PARALYZED",
            type=StatusType.DEBUFF,
            category=StatusCategory.PHYSICAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=3,
            max_duration=3,
            description="Cannot take physical actions; attacks against are critical hits",
            special_effects={
                "cannot_act": True,
                "vulnerable_to_crits": True
            }
        )
    
    @staticmethod
    def create_frostbitten() -> StatusEffect:
        """Create FROSTBITTEN status effect."""
        return StatusEffect(
            name="FROSTBITTEN",
            type=StatusType.DEBUFF,
            category=StatusCategory.PHYSICAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=2,
            max_duration=2,
            description="Disadvantage on next action",
            special_effects={
                "next_action_disadvantage": True
            }
        )
    
    @staticmethod
    def create_rooted() -> StatusEffect:
        """Create ROOTED status effect."""
        return StatusEffect(
            name="ROOTED",
            type=StatusType.DEBUFF,
            category=StatusCategory.MOVEMENT,
            duration_type=StatusDuration.TEMPORARY,
            duration=3,
            max_duration=3,
            description="Movement speed is zero, but can still act",
            stat_modifiers={"movement_speed": -999}
        )
    
    @staticmethod
    def create_invisible() -> StatusEffect:
        """Create INVISIBLE status effect."""
        return StatusEffect(
            name="INVISIBLE",
            type=StatusType.BUFF,
            category=StatusCategory.MAGICAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=10,
            max_duration=10,
            description="Cannot be targeted by most attacks and spells",
            special_effects={
                "untargetable": True,
                "stealth_bonus": True
            }
        )
    
    @staticmethod
    def create_confused() -> StatusEffect:
        """Create CONFUSED status effect."""
        return StatusEffect(
            name="CONFUSED",
            type=StatusType.DEBUFF,
            category=StatusCategory.MENTAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=2,
            max_duration=2,
            description="Attacks nearest creature, friend or foe",
            special_effects={
                "random_targeting": True
            }
        )
    
    @staticmethod
    def create_weakened() -> StatusEffect:
        """Create WEAKENED status effect."""
        return StatusEffect(
            name="WEAKENED",
            type=StatusType.DEBUFF,
            category=StatusCategory.COMBAT,
            duration_type=StatusDuration.TEMPORARY,
            duration=3,
            max_duration=3,
            description="All damage dealt reduced by 2",
            stat_modifiers={"damage": -2}
        )
    
    @staticmethod
    def create_vulnerable(damage_type: str = "all") -> StatusEffect:
        """Create VULNERABLE status effect."""
        return StatusEffect(
            name="VULNERABLE",
            type=StatusType.DEBUFF,
            category=StatusCategory.COMBAT,
            duration_type=StatusDuration.TEMPORARY,
            duration=3,
            max_duration=3,
            description=f"Takes increased damage from {damage_type}",
            special_effects={
                f"vulnerable_{damage_type}": True
            }
        )
    
    @staticmethod
    def create_slow() -> StatusEffect:
        """Create SLOW status effect."""
        return StatusEffect(
            name="SLOW",
            type=StatusType.DEBUFF,
            category=StatusCategory.MOVEMENT,
            duration_type=StatusDuration.TEMPORARY,
            duration=3,
            max_duration=3,
            description="Movement speed halved, one less action",
            percentage_modifiers={"movement_speed": -0.5},
            special_effects={
                "reduced_actions": True
            }
        )
    
    @staticmethod
    def create_stunned() -> StatusEffect:
        """Create STUNNED status effect."""
        return StatusEffect(
            name="STUNNED",
            type=StatusType.DEBUFF,
            category=StatusCategory.PHYSICAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=1,
            max_duration=1,
            description="Cannot take any actions (physical or mental)",
            special_effects={
                "cannot_act": True,
                "cannot_move": True
            }
        )
    
    @staticmethod
    def create_frightened() -> StatusEffect:
        """Create FRIGHTENED status effect."""
        return StatusEffect(
            name="FRIGHTENED",
            type=StatusType.DEBUFF,
            category=StatusCategory.MENTAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=3,
            max_duration=3,
            description="Disadvantage on attacks, must move away from fear source",
            special_effects={
                "attack_disadvantage": True,
                "forced_movement": True
            }
        )
    
    @staticmethod
    def create_sleep() -> StatusEffect:
        """Create SLEEP status effect."""
        return StatusEffect(
            name="SLEEP",
            type=StatusType.DEBUFF,
            category=StatusCategory.MENTAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=5,
            max_duration=5,
            description="Unconscious and helpless; wakes upon taking damage",
            special_effects={
                "unconscious": True,
                "helpless": True,
                "wake_on_damage": True
            }
        )
    
    @staticmethod
    def create_burning() -> StatusEffect:
        """Create BURNING status effect."""
        def burn_tick(character, effect):
            # Deal fire damage each turn
            damage = 1 * effect.stacks
            character.take_damage(damage, "fire")
            print(f"🔥 {character.name} takes {damage} fire damage from burning")
        
        return StatusEffect(
            name="BURNING",
            type=StatusType.DEBUFF,
            category=StatusCategory.ENVIRONMENTAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=4,
            max_duration=4,
            max_stacks=5,
            description="Takes fire damage each turn",
            on_tick=burn_tick
        )
    
    @staticmethod
    def create_poisoned() -> StatusEffect:
        """Create POISONED status effect."""
        def poison_tick(character, effect):
            # Deal poison damage each turn
            damage = 2 * effect.stacks
            character.take_damage(damage, "poison")
            print(f"☠️ {character.name} takes {damage} poison damage")
        
        return StatusEffect(
            name="POISONED",
            type=StatusType.DEBUFF,
            category=StatusCategory.ENVIRONMENTAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=5,
            max_duration=5,
            max_stacks=3,
            description="Takes poison damage each turn",
            on_tick=poison_tick
        )
    
    @staticmethod
    def create_blessed() -> StatusEffect:
        """Create BLESSED status effect."""
        return StatusEffect(
            name="BLESSED",
            type=StatusType.BUFF,
            category=StatusCategory.MAGICAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=10,
            max_duration=10,
            description="Bonus to all saving throws and divine magic",
            stat_modifiers={"saving_throws": 2},
            percentage_modifiers={"divine_magic": 0.2}
        )
    
    @staticmethod
    def create_cursed() -> StatusEffect:
        """Create CURSED status effect."""
        return StatusEffect(
            name="CURSED",
            type=StatusType.DEBUFF,
            category=StatusCategory.MAGICAL,
            duration_type=StatusDuration.PERMANENT,
            description="Penalty to all rolls until removed",
            stat_modifiers={"all_rolls": -1}
        )
    
    @staticmethod
    def create_ethereal() -> StatusEffect:
        """Create ETHEREAL status effect."""
        return StatusEffect(
            name="ETHEREAL",
            type=StatusType.BUFF,
            category=StatusCategory.MAGICAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=5,
            max_duration=5,
            description="Can move through solid objects, immune to physical damage",
            special_effects={
                "phase_through_walls": True,
                "immune_physical": True
            }
        )
    
    @staticmethod
    def create_dominated() -> StatusEffect:
        """Create DOMINATED status effect."""
        return StatusEffect(
            name="DOMINATED",
            type=StatusType.DEBUFF,
            category=StatusCategory.MENTAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=5,
            max_duration=5,
            description="Controlled by another creature",
            special_effects={
                "mind_controlled": True,
                "controlled_by": None  # Set to controller when applied
            }
        )
    
    @staticmethod
    def create_regenerating() -> StatusEffect:
        """Create REGENERATING status effect."""
        def regen_tick(character, effect):
            # Heal each turn
            heal_amount = 3 * effect.stacks
            character.heal(heal_amount)
            print(f"💚 {character.name} regenerates {heal_amount} HP")
        
        return StatusEffect(
            name="REGENERATING",
            type=StatusType.BUFF,
            category=StatusCategory.MAGICAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=10,
            max_duration=10,
            max_stacks=3,
            description="Regains health each turn",
            on_tick=regen_tick
        )
    
    @staticmethod
    def create_mana_burn() -> StatusEffect:
        """Create MANA_BURN status effect."""
        return StatusEffect(
            name="MANA_BURN",
            type=StatusType.DEBUFF,
            category=StatusCategory.MAGICAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=3,
            max_duration=3,
            description="Next spell costs 50% more",
            percentage_modifiers={"spell_cost": 0.5}
        )
    
    @staticmethod
    def create_armor_decay() -> StatusEffect:
        """Create ARMOR_DECAY status effect."""
        def decay_tick(character, effect):
            # Reduce AC each turn
            if hasattr(character, 'ac'):
                character.ac = max(0, character.ac - 1)
                print(f"🛡️ {character.name}'s armor decays (AC: {character.ac})")
        
        return StatusEffect(
            name="ARMOR_DECAY",
            type=StatusType.DEBUFF,
            category=StatusCategory.PHYSICAL,
            duration_type=StatusDuration.TEMPORARY,
            duration=5,
            max_duration=5,
            description="Armor Class reduces by 1 each turn",
            on_tick=decay_tick
        )
    
    @staticmethod
    def create_custom_effect(name: str, effect_type: StatusType, category: StatusCategory,
                           duration: float = 3, description: str = "",
                           stat_mods: Dict[str, float] = None,
                           percentage_mods: Dict[str, float] = None,
                           special_effects: Dict[str, Any] = None) -> StatusEffect:
        """Create a custom status effect with specified parameters."""
        return StatusEffect(
            name=name,
            type=effect_type,
            category=category,
            duration_type=StatusDuration.TEMPORARY,
            duration=duration,
            max_duration=duration,
            description=description,
            stat_modifiers=stat_mods or {},
            percentage_modifiers=percentage_mods or {},
            special_effects=special_effects or {}
        )

# Predefined status effect instances for easy access
PREDEFINED_EFFECTS = {
    "HASTE": StatusEffectFactory.create_haste,
    "PARALYZED": StatusEffectFactory.create_paralyzed,
    "FROSTBITTEN": StatusEffectFactory.create_frostbitten,
    "ROOTED": StatusEffectFactory.create_rooted,
    "INVISIBLE": StatusEffectFactory.create_invisible,
    "CONFUSED": StatusEffectFactory.create_confused,
    "WEAKENED": StatusEffectFactory.create_weakened,
    "VULNERABLE": StatusEffectFactory.create_vulnerable,
    "SLOW": StatusEffectFactory.create_slow,
    "STUNNED": StatusEffectFactory.create_stunned,
    "FRIGHTENED": StatusEffectFactory.create_frightened,
    "SLEEP": StatusEffectFactory.create_sleep,
    "BURNING": StatusEffectFactory.create_burning,
    "POISONED": StatusEffectFactory.create_poisoned,
    "BLESSED": StatusEffectFactory.create_blessed,
    "CURSED": StatusEffectFactory.create_cursed,
    "ETHEREAL": StatusEffectFactory.create_ethereal,
    "DOMINATED": StatusEffectFactory.create_dominated,
    "REGENERATING": StatusEffectFactory.create_regenerating,
    "MANA_BURN": StatusEffectFactory.create_mana_burn,
    "ARMOR_DECAY": StatusEffectFactory.create_armor_decay
}

def create_status_effect(effect_name: str, **kwargs) -> Optional[StatusEffect]:
    """Create a predefined status effect by name."""
    if effect_name in PREDEFINED_EFFECTS:
        return PREDEFINED_EFFECTS[effect_name]()
    return None