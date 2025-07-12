"""
Birth Sign Integration into Character Creation
Shows how to integrate the new birth sign system and spell systems 
into your existing character creation flow.
"""

import pygame
from typing import Optional, Tuple
import random

# Your existing imports
from config.constants import *
from data.player import Player
from game.states import CharCreationState
from ui.base_ui import wrap_text

# New systems
from birth_sign_system import (
    BirthSignCalculator, BirthSignGenerator, add_birth_sign_to_player,
    format_birth_sign_for_display
)
from updated_spell_systems import add_spellcasting_to_character

class BirthSignCharacterCreator:
    """Enhanced character creator with birth sign integration."""
    
    def __init__(self, existing_creator):
        """Wrap the existing character creator with birth sign functionality."""
        self.creator = existing_creator
        self.birth_date_input = None
        self.age_input = None
        self.birth_sign = None
        self.birth_sign_calculated = False
        
        # Add new states to the creation flow
        self.BIRTH_DATE_INPUT = "BIRTH_DATE_INPUT"
        self.BIRTH_SIGN_REVIEW = "BIRTH_SIGN_REVIEW"
    
    def handle_birth_date_input(self, event: pygame.event.Event) -> bool:
        """Handle birth date input during character creation."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Calculate birth sign
                if self.birth_date_input and self.age_input:
                    try:
                        # Parse birth date (format: "month day")
                        parts = self.birth_date_input.strip().split()
                        if len(parts) >= 2:
                            month = parts[0].title()
                            day = int(parts[1])
                            age = int(self.age_input)
                            
                            self.birth_sign = BirthSignGenerator.generate_birth_sign_from_date(
                                month, day, age
                            )
                            self.birth_sign_calculated = True
                            return True
                    except (ValueError, IndexError):
                        # Generate random birth sign on invalid input
                        age = int(self.age_input) if self.age_input else random.randint(18, 60)
                        self.birth_sign = BirthSignGenerator.generate_random_birth_sign((age, age))
                        self.birth_sign_calculated = True
                        return True
            
            elif event.key == pygame.K_r:
                # Generate random birth sign
                age = int(self.age_input) if self.age_input else random.randint(18, 60)
                self.birth_sign = BirthSignGenerator.generate_random_birth_sign((age, age))
                self.birth_sign_calculated = True
                return True
        
        return False
    
    def draw_birth_date_input(self, surface: pygame.Surface):
        """Draw birth date input screen."""
        font = pygame.font.Font(FONT_FILE, 20)
        small_font = pygame.font.Font(FONT_FILE, 16)
        
        # Title
        title_surf = font.render("Birth Sign Calculation", True, COLOR_WHITE)
        title_rect = title_surf.get_rect(centerx=surface.get_width() // 2, top=50)
        surface.blit(title_surf, title_rect)
        
        # Instructions
        instructions = [
            "Enter your birth details for cosmic alignment:",
            "",
            "Birth Month and Day (e.g., 'Duskwane 17'):",
            self.birth_date_input or "(enter month and day)",
            "",
            "Age:",
            self.age_input or "(enter age)",
            "",
            "Press ENTER to calculate birth sign",
            "Press R for random birth sign",
            "",
            "Available months:",
            "Frostwane, Embermarch, Thawmere, Greentide",
            "Blossarch, Suncrest, Highflare, Duskwane", 
            "Mournfall, Hallowdeep, Snowrest, Starhearth"
        ]
        
        y = title_rect.bottom + 30
        for instruction in instructions:
            color = COLOR_GOLD if instruction.startswith("Birth Month") or instruction.startswith("Age") else COLOR_WHITE
            if instruction in [self.birth_date_input or "(enter month and day)", self.age_input or "(enter age)"]:
                color = COLOR_TEXT_INPUT
            
            inst_surf = small_font.render(instruction, True, color)
            inst_rect = inst_surf.get_rect(centerx=surface.get_width() // 2, top=y)
            surface.blit(inst_surf, inst_rect)
            y += 25
    
    def draw_birth_sign_review(self, surface: pygame.Surface):
        """Draw birth sign review screen."""
        if not self.birth_sign:
            return
        
        font = pygame.font.Font(FONT_FILE, 20)
        small_font = pygame.font.Font(FONT_FILE, 16)
        
        # Title
        title_surf = font.render("Your Cosmic Destiny", True, COLOR_GOLD)
        title_rect = title_surf.get_rect(centerx=surface.get_width() // 2, top=30)
        surface.blit(title_surf, title_rect)
        
        # Birth sign details
        lines = format_birth_sign_for_display(self.birth_sign)
        y = title_rect.bottom + 20
        
        for line in lines:
            if line.startswith("Birth Sign:"):
                color = COLOR_GOLD
                current_font = font
            elif line.startswith("Prophecy:") or line.startswith("Stat Bonuses:") or line.startswith("Special Abilities:"):
                color = COLOR_GOLD
                current_font = small_font
            elif line.strip() == "":
                y += 10
                continue
            else:
                color = COLOR_WHITE
                current_font = small_font
            
            line_surf = current_font.render(line, True, color)
            line_rect = line_surf.get_rect(centerx=surface.get_width() // 2, top=y)
            surface.blit(line_surf, line_rect)
            y += current_font.get_height() + 2
        
        # Instructions
        inst_surf = small_font.render("Press ENTER to continue or ESC to recalculate", True, COLOR_WHITE)
        inst_rect = inst_surf.get_rect(centerx=surface.get_width() // 2, bottom=surface.get_height() - 20)
        surface.blit(inst_surf, inst_rect)
    
    def create_enhanced_player(self) -> Optional[Player]:
        """Create player with birth sign and enhanced spell system."""
        # Create base player using existing system
        base_player = self.creator.create_player()
        
        if self.birth_sign:
            # Apply birth sign bonuses
            add_birth_sign_to_player(base_player, self.birth_sign)
        
        # Add spellcasting system
        add_spellcasting_to_character(base_player)
        
        # Learn starting spells based on class and birth sign
        self._assign_starting_spells(base_player)
        
        return base_player
    
    def _assign_starting_spells(self, player: Player):
        """Assign starting spells based on class and birth sign."""
        if not hasattr(player, 'spellcaster') or not player.spellcaster:
            return
        
        # Base starting spells by class
        if player.character_class == "Wizard":
            base_spells = ["Force Bolt", "Arcane Sight", "Shifting Shadow"]
        elif player.character_class == "Priest":
            base_spells = ["Serentha's Touch", "Caedros's Aegis"]
        else:
            return
        
        # Learn base spells
        for spell_name in base_spells:
            player.spellcaster.learn_spell(spell_name)
        
        # Add birth sign influenced spells
        if self.birth_sign:
            bonus_spells = self._get_birth_sign_bonus_spells(player, self.birth_sign)
            for spell_name in bonus_spells:
                player.spellcaster.learn_spell(spell_name)
    
    def _get_birth_sign_bonus_spells(self, player: Player, birth_sign) -> List[str]:
        """Get bonus spells based on birth sign."""
        bonus_spells = []
        
        # Solar archetype bonuses
        archetype_spells = {
            "The Endurer": ["Runic Ward"] if player.character_class == "Wizard" else ["Velmari's Hearthlight"],
            "The Rekindled": ["Embermarch Coals"] if player.character_class == "Wizard" else ["Zyrix's Fury"],
            "The Awakener": ["Feather Fall"] if player.character_class == "Wizard" else ["Nymbril's Call"],
            "The Verdant": ["Greentide's Grasp"] if player.character_class == "Wizard" else ["Serentha's Touch"],
            "The Shifting": ["Shifting Shadow"] if player.character_class == "Wizard" else ["Olvenar's Whisper"],
            "The Veiled": ["Arcane Sight"] if player.character_class == "Wizard" else ["Vhalor's Weariness"]
        }
        
        archetype_name = birth_sign.solar_archetype.value[0]
        if archetype_name in archetype_spells:
            bonus_spells.extend(archetype_spells[archetype_name])
        
        # Lunar influence bonuses
        for moon_name, (imprint, phase_value) in birth_sign.lunar_imprints.items():
            if imprint.name == "EMPOWERED":
                if moon_name == "Myrr" and player.character_class == "Wizard":
                    bonus_spells.append("Duskwane Drowse")
                elif moon_name == "Caelyra" and player.character_class == "Priest":
                    bonus_spells.append("Caedros's Aegis")
                elif moon_name == "Velmara":
                    bonus_spells.append("Continual Flame" if player.character_class == "Wizard" else "Mercy's Relief")
        
        return bonus_spells

# Integration functions for the main character creation system

def enhance_character_creation_with_birth_signs(character_creator):
    """Enhance existing character creator with birth sign system."""
    # This would be called in your main character creation flow
    enhanced_creator = BirthSignCharacterCreator(character_creator)
    return enhanced_creator

def update_character_creation_flow():
    """Example of how to update your character creation flow."""
    # This shows where to insert the birth sign steps in your existing flow
    
    # In your existing CharacterCreator class, add these states:
    # - After ALIGNMENT_SELECTION, add BIRTH_DATE_INPUT
    # - After BIRTH_DATE_INPUT, add BIRTH_SIGN_REVIEW
    # - Then continue to GOD_SELECTION or SPELL_SELECTION
    
    creation_flow_example = {
        CharCreationState.NAME_INPUT: "Enter character name",
        CharCreationState.STAT_ROLLING: "Roll character stats", 
        CharCreationState.RACE_SELECTION: "Choose race",
        CharCreationState.CLASS_SELECTION: "Choose class",
        CharCreationState.ALIGNMENT_SELECTION: "Choose alignment",
        # NEW: Insert birth sign calculation here
        "BIRTH_DATE_INPUT": "Enter birth date and age",
        "BIRTH_SIGN_REVIEW": "Review cosmic destiny",
        # CONTINUE: Rest of existing flow
        CharCreationState.GOD_SELECTION: "Choose deity (if priest)",
        CharCreationState.SPELL_SELECTION: "Choose starting spells",
        CharCreationState.GEAR_SELECTION: "Select equipment",
        CharCreationState.STATS_REVIEW: "Final review"
    }
    
    return creation_flow_example

# Modified character creation handler
def handle_enhanced_character_creation_input(creator, event):
    """Enhanced input handler that includes birth sign steps."""
    
    if creator.state == "BIRTH_DATE_INPUT":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Go back to alignment selection
                creator.state = CharCreationState.ALIGNMENT_SELECTION
                return
            
            # Handle text input for birth date and age
            if hasattr(event, 'unicode') and event.unicode:
                if not creator.birth_date_input:
                    creator.birth_date_input = ""
                if event.key == pygame.K_BACKSPACE:
                    creator.birth_date_input = creator.birth_date_input[:-1]
                elif len(creator.birth_date_input) < 30:  # Reasonable limit
                    creator.birth_date_input += event.unicode
            
            elif event.key == pygame.K_TAB:
                # Switch to age input (simple implementation)
                if not creator.age_input:
                    creator.age_input = ""
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_r:
                # Calculate birth sign
                if creator.handle_birth_date_input(event):
                    creator.state = "BIRTH_SIGN_REVIEW"
    
    elif creator.state == "BIRTH_SIGN_REVIEW":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Go back to birth date input
                creator.state = "BIRTH_DATE_INPUT"
                creator.birth_sign_calculated = False
            elif event.key == pygame.K_RETURN:
                # Continue to next step (god selection or spell selection)
                if creator.character_class == "Priest":
                    creator.state = CharCreationState.GOD_SELECTION
                else:
                    creator.state = CharCreationState.SPELL_SELECTION

# Integration with existing main.py
def integrate_with_main_game():
    """Shows how to integrate with your main.py file."""
    
    # In your DungeonExplorer.start_character_creation method:
    
    example_integration = """
    def start_character_creation(self):
        # Store current display state
        current_fullscreen = self.fullscreen
        
        pygame.display.set_caption("Character Creation")
        
        # Create enhanced character creator
        from birth_sign_integration import enhance_character_creation_with_birth_signs
        from character_creation import CharacterCreator  # Your existing creator
        
        base_creator = CharacterCreator(self.screen, FONT_FILE)
        enhanced_creator = enhance_character_creation_with_birth_signs(base_creator)
        
        # Run enhanced character creation
        created_player = run_enhanced_character_creation(
            enhanced_creator, self.screen
        )
        
        if created_player is None:
            self.running = False
            return
        
        # Player now has birth sign and enhanced spell system
        self.player = created_player
        
        # Continue with dungeon initialization...
        self.dungeon_game = DungeonGame(self.dungeon_data, self.player)
        self.game_state = GameState.PLAYING
    """
    
    return example_integration

def run_enhanced_character_creation(enhanced_creator, screen):
    """Run the enhanced character creation with birth signs."""
    clock = pygame.time.Clock()
    
    running = True
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            # Handle enhanced creation input
            handle_enhanced_character_creation_input(enhanced_creator, event)
            
            # Handle base creator events
            result = enhanced_creator.creator.handle_event(event)
            if result is True:
                # Character creation complete
                return enhanced_creator.create_enhanced_player()
            elif result is None:
                return None  # Cancelled
        
        # Update
        enhanced_creator.creator.update(dt)
        
        # Draw
        screen.fill(COLOR_BLACK)
        
        if enhanced_creator.creator.state == "BIRTH_DATE_INPUT":
            enhanced_creator.draw_birth_date_input(screen)
        elif enhanced_creator.creator.state == "BIRTH_SIGN_REVIEW":
            enhanced_creator.draw_birth_sign_review(screen)
        else:
            # Draw normal character creation
            enhanced_creator.creator.draw(screen)
        
        pygame.display.flip()
    
    return None

# Example of how spells work with the new system
def example_spell_usage():
    """Example of how the new spell system works in practice."""
    
    # Create a test character
    from data.player import create_default_player
    player = create_default_player()
    player.character_class = "Wizard"
    player.alignment = "Chaotic"
    
    # Add spellcasting
    spellcaster = add_spellcasting_to_character(player)
    
    # Learn some spells
    spellcaster.learn_spell("Fireball")
    spellcaster.learn_spell("Embermarch Coals")
    spellcaster.learn_spell("Mirror Image")
    
    print("=== SPELL CASTING EXAMPLE ===")
    
    # Cast Mirror Image (shows alignment effect)
    print("Casting Mirror Image...")
    spellcaster.cast_spell("Mirror Image")
    
    # Cast Embermarch Coals (shows lore-fueled effect if conditions met)
    print("\nCasting Embermarch Coals...")
    spellcaster.cast_spell("Embermarch Coals")
    
    # Show spell slots remaining
    print(f"\nSpell slots remaining: {spellcaster.spells_per_day}")
    print(f"Spells used today: {spellcaster.spells_used_today}")

if __name__ == "__main__":
    # Run the example
    example_spell_usage()
    
    # Show integration flow
    flow = update_character_creation_flow()
    print("\n=== CHARACTER CREATION FLOW ===")
    for state, description in flow.items():
        print(f"{state}: {description}")