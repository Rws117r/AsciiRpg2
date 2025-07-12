"""
Character Creation UI Components - FIXED VERSION
Extracted and refactored from the original character_creation.py
No more display recreation to prevent fullscreen issues
"""

import pygame
import random
import time
from typing import List, Tuple, Optional
from enum import Enum

# Import from new modular structure
from config.constants import *
from data.player import Player
from game.states import CharCreationState
from ui.base_ui import Button, TextInput, wrap_text

# Character creation data
from character_creation import (
    RACES, CLASSES, ALIGNMENTS, STATS, STAT_DESCRIPTIONS,
    PRIEST_SPELLS_TIER_1, WIZARD_SPELLS_TIER_1, GODS, NAMES, TITLES,
    RACE_DETAILS, CLASS_DETAILS, ALIGNMENT_DETAILS
)

class CharacterCreator:
    """Main character creation UI controller."""
    
    def __init__(self, screen: pygame.Surface, font_file: str):
        # Use existing screen instead of creating new one
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.font_file = font_file
        
        # Initialize fonts
        self.title_font = pygame.font.Font(font_file, 36)
        self.large_font = pygame.font.Font(font_file, 24)
        self.medium_font = pygame.font.Font(font_file, 20)
        self.small_font = pygame.font.Font(font_file, 16)
        self.tiny_font = pygame.font.Font(font_file, 14)
        
        # State management
        self.state = CharCreationState.NAME_INPUT
        self.selected_index = 0
        
        # Character data
        self.name = ""
        self.race = ""
        self.character_class = ""
        self.alignment = ""
        self.god = ""
        self.selected_spells = []
        self.spells_to_select = 0
        
        # Stats
        self.stats = [10, 10, 10, 10, 10, 10]
        self.stat_rolls_history = []
        self.current_roll_set = 0
        
        # UI components
        self.text_input = None
        self.random_button = None
        self.roll_button = None
        self.accept_button = None
        self.reroll_button = None
        
        # Layout
        self.list_width = self.screen_width // 3
        self.detail_width = (self.screen_width * 2) // 3
        self.list_x = 20
        self.detail_x = self.list_width + 40
        
        self._setup_ui()
    
    def update_screen_size(self):
        """Update screen size if window was resized."""
        new_size = self.screen.get_size()
        if new_size != (self.screen_width, self.screen_height):
            self.screen_width, self.screen_height = new_size
            # Recalculate layout
            self.list_width = self.screen_width // 3
            self.detail_width = (self.screen_width * 2) // 3
            self.detail_x = self.list_width + 40
            self._setup_ui()
    
    def get_stat_modifier(self, stat_value: int) -> int:
        """Calculate ability score modifier."""
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
    
    def roll_stats(self) -> List[int]:
        """Roll 3d6 for each stat."""
        return [sum(random.randint(1, 6) for _ in range(3)) for _ in range(6)]
    
    def has_high_stat(self, stats: List[int]) -> bool:
        """Check if any stat is 14 or higher."""
        return any(stat >= 14 for stat in stats)
    
    def _setup_ui(self):
        """Setup UI components for current state."""
        self.selected_index = 0
        
        # Clear existing UI
        self.text_input = None
        self.random_button = None
        self.roll_button = None
        self.accept_button = None
        self.reroll_button = None
        
        if self.state == CharCreationState.NAME_INPUT:
            self._setup_name_input()
        elif self.state == CharCreationState.STAT_ROLLING:
            self._setup_stat_rolling()
    
    def _setup_name_input(self):
        """Setup name input UI."""
        input_width = 300
        input_height = 40
        input_x = (self.screen_width - input_width) // 2
        input_y = self.screen_height // 2 - 20
        
        self.text_input = TextInput(input_x, input_y, input_width, input_height, self.large_font)
        self.random_button = Button(input_x + input_width + 20, input_y, 100, input_height, "Random", self.medium_font)
    
    def _setup_stat_rolling(self):
        """Setup stat rolling UI."""
        button_y = self.screen_height // 2 + 100
        self.roll_button = Button(self.screen_width // 2 - 150, button_y, 100, 40, "Roll Stats", self.medium_font)
        self.accept_button = Button(self.screen_width // 2 - 40, button_y, 80, 40, "Accept", self.medium_font)
        self.reroll_button = Button(self.screen_width // 2 + 50, button_y, 100, 40, "Reroll", self.medium_font)
        
        if not self.stat_rolls_history:
            initial_stats = self.roll_stats()
            self.stat_rolls_history.append(initial_stats)
            self.stats = initial_stats[:]
    
    def _get_current_options(self):
        """Get options for current selection state."""
        if self.state == CharCreationState.RACE_SELECTION:
            return RACES
        elif self.state == CharCreationState.CLASS_SELECTION:
            return CLASSES
        elif self.state == CharCreationState.ALIGNMENT_SELECTION:
            return ALIGNMENTS
        elif self.state == CharCreationState.GOD_SELECTION:
            if self.alignment:
                return [name for name, god in GODS.items() if god["alignment"] == self.alignment]
            return list(GODS.keys())
        elif self.state == CharCreationState.SPELL_SELECTION:
            if self.character_class == "Priest":
                return list(PRIEST_SPELLS_TIER_1.keys())
            elif self.character_class == "Wizard":
                return list(WIZARD_SPELLS_TIER_1.keys())
        return []
    
    def _get_current_details(self):
        """Get details for currently selected option."""
        options = self._get_current_options()
        if not options or self.selected_index >= len(options):
            return None
            
        selected_option = options[self.selected_index]
        
        if self.state == CharCreationState.RACE_SELECTION:
            return RACE_DETAILS.get(selected_option)
        elif self.state == CharCreationState.CLASS_SELECTION:
            return CLASS_DETAILS.get(selected_option)
        elif self.state == CharCreationState.ALIGNMENT_SELECTION:
            return ALIGNMENT_DETAILS.get(selected_option)
        elif self.state == CharCreationState.GOD_SELECTION:
            return GODS.get(selected_option)
        elif self.state == CharCreationState.SPELL_SELECTION:
            if self.character_class == "Priest":
                return PRIEST_SPELLS_TIER_1.get(selected_option)
            elif self.character_class == "Wizard":
                return WIZARD_SPELLS_TIER_1.get(selected_option)
        return None
    
    def handle_event(self, event: pygame.event.Event) -> Optional[bool]:
        """Handle input events. Returns True to complete, None to cancel, False to continue."""
        # Handle text input
        if self.text_input and self.state == CharCreationState.NAME_INPUT:
            if self.text_input.handle_event(event):
                if self.text_input.text.strip():
                    self._next_state()
                    return False
        
        # Handle button clicks
        if self.random_button and self.random_button.handle_event(event):
            self._randomize_current_selection()
        
        if self.roll_button and self.roll_button.handle_event(event):
            self._roll_new_stats()
        
        if self.accept_button and self.accept_button.handle_event(event):
            if self.state == CharCreationState.STAT_ROLLING:
                self._next_state()
        
        if self.reroll_button and self.reroll_button.handle_event(event):
            if not self.has_high_stat(self.stats):
                self._roll_new_stats()
        
        # Handle keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state != CharCreationState.NAME_INPUT:
                    self._previous_state()
                    return False
                else:
                    return None  # Cancel
            
            elif event.key == pygame.K_RETURN:
                return self._handle_enter_key()
            
            elif event.key == pygame.K_UP:
                self._handle_navigation(-1)
            
            elif event.key == pygame.K_DOWN:
                self._handle_navigation(1)
            
            elif event.key == pygame.K_SPACE:
                if self.state == CharCreationState.STAT_ROLLING:
                    self._roll_new_stats()
        
        return False
    
    def _handle_enter_key(self) -> Optional[bool]:
        """Handle Enter key press."""
        if self.state == CharCreationState.NAME_INPUT:
            if self.text_input and self.text_input.text.strip():
                self._next_state()
        elif self.state == CharCreationState.STAT_ROLLING:
            self._next_state()
        elif self.state in [CharCreationState.RACE_SELECTION, CharCreationState.CLASS_SELECTION, 
                           CharCreationState.ALIGNMENT_SELECTION, CharCreationState.GOD_SELECTION,
                           CharCreationState.SPELL_SELECTION]:
            if self._make_selection(self.selected_index):
                self._next_state()
            elif self.state != CharCreationState.SPELL_SELECTION:
                self._next_state()
        elif self.state == CharCreationState.STATS_REVIEW:
            return True  # Complete character creation
        
        return False
    
    def _handle_navigation(self, direction: int):
        """Handle up/down navigation."""
        if self.state in [CharCreationState.RACE_SELECTION, CharCreationState.CLASS_SELECTION, 
                         CharCreationState.ALIGNMENT_SELECTION, CharCreationState.GOD_SELECTION,
                         CharCreationState.SPELL_SELECTION]:
            options = self._get_current_options()
            if options:
                self.selected_index = (self.selected_index + direction) % len(options)
    
    def _make_selection(self, index: int) -> bool:
        """Make a selection for current state."""
        options = self._get_current_options()
        if index < len(options):
            if self.state == CharCreationState.RACE_SELECTION:
                self.race = options[index]
            elif self.state == CharCreationState.CLASS_SELECTION:
                self.character_class = options[index]
            elif self.state == CharCreationState.ALIGNMENT_SELECTION:
                self.alignment = options[index]
            elif self.state == CharCreationState.GOD_SELECTION:
                self.god = options[index]
            elif self.state == CharCreationState.SPELL_SELECTION:
                spell = options[index]
                if spell not in self.selected_spells:
                    self.selected_spells.append(spell)
                    if len(self.selected_spells) >= self.spells_to_select:
                        return True
        return False
    
    def _randomize_current_selection(self):
        """Randomize current selection."""
        if self.state == CharCreationState.NAME_INPUT:
            temp_race = random.choice(RACES)
            random_name = random.choice(NAMES[temp_race])
            self.text_input.text = random_name
    
    def _roll_new_stats(self):
        """Roll new stats."""
        new_stats = self.roll_stats()
        self.stat_rolls_history.append(new_stats)
        self.current_roll_set = len(self.stat_rolls_history) - 1
        self.stats = new_stats[:]
    
    def _next_state(self):
        """Advance to next state."""
        if self.state == CharCreationState.NAME_INPUT:
            self.name = self.text_input.text.strip()
            self.state = CharCreationState.STAT_ROLLING
        elif self.state == CharCreationState.STAT_ROLLING:
            self.state = CharCreationState.RACE_SELECTION
        elif self.state == CharCreationState.RACE_SELECTION:
            self.state = CharCreationState.CLASS_SELECTION
        elif self.state == CharCreationState.CLASS_SELECTION:
            self.state = CharCreationState.ALIGNMENT_SELECTION
        elif self.state == CharCreationState.ALIGNMENT_SELECTION:
            if self.character_class == "Priest":
                self.state = CharCreationState.GOD_SELECTION
            elif self.character_class in ["Priest", "Wizard"]:
                self._setup_spell_selection()
                self.state = CharCreationState.SPELL_SELECTION
            else:
                self.state = CharCreationState.GEAR_SELECTION
        elif self.state == CharCreationState.GOD_SELECTION:
            if self.character_class in ["Priest", "Wizard"]:
                self._setup_spell_selection()
                self.state = CharCreationState.SPELL_SELECTION
            else:
                self.state = CharCreationState.GEAR_SELECTION
        elif self.state == CharCreationState.SPELL_SELECTION:
            self.state = CharCreationState.GEAR_SELECTION
        elif self.state == CharCreationState.GEAR_SELECTION:
            self.state = CharCreationState.STATS_REVIEW
        elif self.state == CharCreationState.STATS_REVIEW:
            self.state = CharCreationState.COMPLETE
        
        self._setup_ui()
    
    def _previous_state(self):
        """Go back to previous state."""
        if self.state == CharCreationState.STAT_ROLLING:
            self.state = CharCreationState.NAME_INPUT
        elif self.state == CharCreationState.RACE_SELECTION:
            self.state = CharCreationState.STAT_ROLLING
        elif self.state == CharCreationState.CLASS_SELECTION:
            self.state = CharCreationState.RACE_SELECTION
        elif self.state == CharCreationState.ALIGNMENT_SELECTION:
            self.state = CharCreationState.CLASS_SELECTION
        elif self.state == CharCreationState.GOD_SELECTION:
            self.state = CharCreationState.ALIGNMENT_SELECTION
        elif self.state == CharCreationState.SPELL_SELECTION:
            if self.character_class == "Priest":
                self.state = CharCreationState.GOD_SELECTION
            else:
                self.state = CharCreationState.ALIGNMENT_SELECTION
        elif self.state == CharCreationState.GEAR_SELECTION:
            if self.character_class in ["Priest", "Wizard"]:
                self.state = CharCreationState.SPELL_SELECTION
            elif self.character_class == "Priest":
                self.state = CharCreationState.GOD_SELECTION
            else:
                self.state = CharCreationState.ALIGNMENT_SELECTION
        elif self.state == CharCreationState.STATS_REVIEW:
            self.state = CharCreationState.GEAR_SELECTION
        
        self._setup_ui()
    
    def _setup_spell_selection(self):
        """Setup spell selection."""
        self.selected_spells = []
        if self.character_class == "Priest":
            self.spells_to_select = 2
        elif self.character_class == "Wizard":
            self.spells_to_select = 3
    
    def update(self, dt: float):
        """Update components."""
        if self.text_input:
            self.text_input.update(dt)
        
        # Update screen size in case of resize
        self.update_screen_size()
    
    def draw(self, surface: pygame.Surface):
        """Draw the character creation interface."""
        surface.fill(COLOR_BLACK)
        
        # Draw title
        title = self._get_title()
        title_surf = self.title_font.render(title, True, COLOR_WHITE)
        title_rect = title_surf.get_rect(centerx=self.screen_width // 2, top=30)
        surface.blit(title_surf, title_rect)
        
        # Draw state-specific content
        if self.state == CharCreationState.NAME_INPUT:
            self._draw_name_input(surface)
        elif self.state == CharCreationState.STAT_ROLLING:
            self._draw_stat_rolling(surface)
        elif self.state in [CharCreationState.RACE_SELECTION, CharCreationState.CLASS_SELECTION, 
                           CharCreationState.ALIGNMENT_SELECTION, CharCreationState.GOD_SELECTION,
                           CharCreationState.SPELL_SELECTION]:
            self._draw_selection_screen(surface)
        elif self.state == CharCreationState.STATS_REVIEW:
            self._draw_stats_review(surface)
        
        # Draw UI components
        if self.text_input:
            self.text_input.draw(surface)
        if self.random_button:
            self.random_button.draw(surface)
        if self.roll_button:
            self.roll_button.draw(surface)
        if self.accept_button:
            self.accept_button.draw(surface)
        if self.reroll_button:
            self.reroll_button.draw(surface)
        
        # Draw instructions
        self._draw_instructions(surface)
    
    def _draw_name_input(self, surface: pygame.Surface):
        """Draw name input interface."""
        instruction = "Enter your character's name:"
        inst_surf = self.large_font.render(instruction, True, COLOR_WHITE)
        inst_rect = inst_surf.get_rect(centerx=self.screen_width // 2, y=self.screen_height // 2 - 80)
        surface.blit(inst_surf, inst_rect)
    
    def _draw_stat_rolling(self, surface: pygame.Surface):
        """Draw stat rolling interface."""
        separator_x = self.list_width + 30
        pygame.draw.line(surface, COLOR_WHITE, (separator_x, 100), (separator_x, self.screen_height - 100), 2)
        
        # Left side - stats
        left_start_y = 150
        for i, (stat_name, stat_value) in enumerate(zip(STATS, self.stats)):
            y = left_start_y + i * 60
            modifier = self.get_stat_modifier(stat_value)
            modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)
            
            name_surf = self.large_font.render(f"{stat_name}:", True, COLOR_WHITE)
            surface.blit(name_surf, (self.list_x, y))
            
            value_text = f"{stat_value} ({modifier_str})"
            value_surf = self.large_font.render(value_text, True, COLOR_WHITE)
            surface.blit(value_surf, (self.list_x, y + 25))
        
        # Right side - descriptions
        right_start_y = 150
        for i, stat_name in enumerate(STATS):
            y = right_start_y + i * 60
            desc = STAT_DESCRIPTIONS.get(stat_name, "")
            wrapped_lines = wrap_text(desc, self.detail_width - 40, self.small_font)
            for j, line in enumerate(wrapped_lines):
                line_surf = self.small_font.render(line, True, COLOR_WHITE)
                surface.blit(line_surf, (self.detail_x, y + j * 18))
        
        # Reroll notification
        if not self.has_high_stat(self.stats):
            reroll_text = "No stat is 14+ - Reroll available"
            reroll_surf = self.medium_font.render(reroll_text, True, (255, 255, 0))
            reroll_rect = reroll_surf.get_rect(centerx=self.screen_width // 2, y=self.screen_height - 200)
            surface.blit(reroll_surf, reroll_rect)
    
    def _draw_selection_screen(self, surface: pygame.Surface):
        """Draw selection interface."""
        options = self._get_current_options()
        if not options:
            return
        
        separator_x = self.list_width + 30
        pygame.draw.line(surface, COLOR_WHITE, (separator_x, 100), (separator_x, self.screen_height - 100), 2)
        
        # Left side - options
        list_start_y = 120
        for i, option in enumerate(options):
            y = list_start_y + i * 50
            
            if i == self.selected_index:
                highlight_rect = pygame.Rect(self.list_x - 5, y - 5, self.list_width - 30, 40)
                pygame.draw.rect(surface, COLOR_BUTTON_HOVER, highlight_rect)
                pygame.draw.rect(surface, COLOR_WHITE, highlight_rect, 2)
            
            color = COLOR_BLACK if i == self.selected_index else COLOR_WHITE
            option_surf = self.large_font.render(option, True, color)
            surface.blit(option_surf, (self.list_x, y))
            
            if self.state == CharCreationState.SPELL_SELECTION and option in self.selected_spells:
                selected_surf = self.small_font.render("✓ SELECTED", True, (0, 255, 0))
                surface.blit(selected_surf, (self.list_x, y + 25))
        
        # Spell selection progress
        if self.state == CharCreationState.SPELL_SELECTION:
            progress_text = f"Selected {len(self.selected_spells)}/{self.spells_to_select} spells"
            progress_surf = self.medium_font.render(progress_text, True, COLOR_WHITE)
            progress_rect = progress_surf.get_rect(centerx=self.list_width // 2, y=list_start_y + len(options) * 50 + 20)
            surface.blit(progress_surf, progress_rect)
        
        # Right side - details
        details = self._get_current_details()
        if details:
            self._draw_option_details(surface, details)
    
    def _draw_option_details(self, surface: pygame.Surface, details: dict):
        """Draw details for selected option."""
        detail_y = 120
        line_height = 25
        
        # Title
        title_surf = self.large_font.render(details.get("title", ""), True, COLOR_WHITE)
        surface.blit(title_surf, (self.detail_x, detail_y))
        detail_y += 40
        
        # Spell info
        if "tier" in details:
            spell_info = f"Tier {details['tier']} | Duration: {details['duration']} | Range: {details['range']}"
            info_surf = self.small_font.render(spell_info, True, (200, 200, 200))
            surface.blit(info_surf, (self.detail_x, detail_y))
            detail_y += 30
        
        # Description
        description = details.get("description", "")
        wrapped_lines = wrap_text(description, self.detail_width - 40, self.medium_font)
        for line in wrapped_lines:
            line_surf = self.medium_font.render(line, True, COLOR_WHITE)
            surface.blit(line_surf, (self.detail_x, detail_y))
            detail_y += line_height
        
        detail_y += 20
        
        # Additional info
        if "ability" in details:
            wrapped_ability = wrap_text(details["ability"], self.detail_width - 40, self.medium_font)
            for line in wrapped_ability:
                line_surf = self.medium_font.render(line, True, COLOR_WHITE)
                surface.blit(line_surf, (self.detail_x, detail_y))
                detail_y += line_height
        elif "traits" in details:
            wrapped_traits = wrap_text(f"Traits: {details['traits']}", self.detail_width - 40, self.small_font)
            for line in wrapped_traits:
                line_surf = self.small_font.render(line, True, COLOR_WHITE)
                surface.blit(line_surf, (self.detail_x, detail_y))
                detail_y += line_height - 5
        elif "stats" in details:
            detail_y += 10
            for stat in details["stats"]:
                stat_surf = self.small_font.render(stat, True, COLOR_WHITE)
                surface.blit(stat_surf, (self.detail_x, detail_y))
                detail_y += line_height - 5
            
            detail_y += 15
            
            for ability in details["abilities"]:
                wrapped_ability = wrap_text(ability, self.detail_width - 40, self.small_font)
                for line in wrapped_ability:
                    line_surf = self.small_font.render(line, True, COLOR_WHITE)
                    surface.blit(line_surf, (self.detail_x, detail_y))
                    detail_y += line_height - 5
                detail_y += 10
    
    def _draw_stats_review(self, surface: pygame.Surface):
        """Draw final character review."""
        center_x = self.screen_width // 2
        start_y = 120
        line_height = 25
        
        title = self._get_character_title()
        
        char_info = [
            f"Name: {self.name}",
            f"Title: {title}",
            f"Race: {self.race}",
            f"Class: {self.character_class}",
            f"Alignment: {self.alignment}",
        ]
        
        if self.god:
            char_info.append(f"Deity: {self.god}")
        
        if self.selected_spells:
            char_info.append(f"Starting Spells: {', '.join(self.selected_spells)}")
        
        char_info.extend([
            "",
            "STATISTICS:",
        ])
        
        for i, (stat_name, stat_value) in enumerate(zip(STATS, self.stats)):
            modifier = self.get_stat_modifier(stat_value)
            modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)
            char_info.append(f"{stat_name}: {stat_value} ({modifier_str})")
        
        char_info.extend([
            "",
            "Level: 1",
            "Hit Points: 10/10",
            "Armor Class: 11",
            "Experience: 0/100"
        ])
        
        for i, info in enumerate(char_info):
            if info:
                font = self.large_font if info in ["STATISTICS:"] else self.medium_font
                color = COLOR_WHITE
                info_surf = font.render(info, True, color)
                info_rect = info_surf.get_rect(centerx=center_x, y=start_y + i * line_height)
                surface.blit(info_surf, info_rect)
    
    def _draw_instructions(self, surface: pygame.Surface):
        """Draw instruction text."""
        instructions = []
        
        if self.state == CharCreationState.NAME_INPUT:
            instructions = ["Enter your name and press ENTER", "Click Random for a random name"]
        elif self.state == CharCreationState.STAT_ROLLING:
            instructions = ["SPACE or Roll Stats button to roll", "Press ENTER or Accept to continue", "Reroll if no stat is 14+"]
        elif self.state in [CharCreationState.RACE_SELECTION, CharCreationState.CLASS_SELECTION, 
                           CharCreationState.ALIGNMENT_SELECTION, CharCreationState.GOD_SELECTION]:
            instructions = ["Use UP/DOWN arrows to navigate", "Press ENTER to select", "Press ESC to go back"]
        elif self.state == CharCreationState.SPELL_SELECTION:
            if len(self.selected_spells) < self.spells_to_select:
                instructions = ["Use UP/DOWN arrows to navigate", "Press ENTER to select spell", f"Select {self.spells_to_select - len(self.selected_spells)} more spells"]
            else:
                instructions = ["Press ENTER to continue", "Press ESC to go back"]
        elif self.state == CharCreationState.STATS_REVIEW:
            instructions = ["Press ENTER to finish character creation", "Press ESC to go back"]
        
        y = self.screen_height - 80
        for instruction in instructions:
            inst_surf = self.small_font.render(instruction, True, COLOR_WHITE)
            inst_rect = inst_surf.get_rect(centerx=self.screen_width // 2, y=y)
            surface.blit(inst_surf, inst_rect)
            y += 20
    
    def _get_title(self) -> str:
        """Get title for current state."""
        titles = {
            CharCreationState.NAME_INPUT: "Enter Your Name",
            CharCreationState.STAT_ROLLING: "Roll Your Statistics",
            CharCreationState.RACE_SELECTION: "Choose Your Ancestry", 
            CharCreationState.CLASS_SELECTION: "Choose Your Class",
            CharCreationState.ALIGNMENT_SELECTION: "Choose Your Alignment",
            CharCreationState.GOD_SELECTION: "Choose Your Deity",
            CharCreationState.SPELL_SELECTION: "Choose Your Starting Spells",
            CharCreationState.GEAR_SELECTION: "Select Your Gear",
            CharCreationState.STATS_REVIEW: "Character Summary"
        }
        return titles.get(self.state, "Character Creation")
    
    def _get_character_title(self) -> str:
        """Get character title based on class and alignment."""
        if not all([self.character_class, self.alignment]):
            return "Adventurer"
        
        try:
            for level_range, title in TITLES[self.character_class][self.alignment].items():
                if 1 >= level_range[0] and 1 <= level_range[1]:
                    return title
        except KeyError:
            pass
        
        return "Adventurer"
    
    def create_player(self) -> Player:
        """Create a Player object from the character creation data."""
        title = self._get_character_title()
        
        return Player(
            name=self.name,
            title=title,
            race=self.race,
            alignment=self.alignment,
            character_class=self.character_class,
            level=1,
            hp=10,
            max_hp=10,
            xp=0,
            xp_to_next_level=100,
            ac=11,
            light_duration=TORCH_DURATION_SECONDS,
            light_start_time=time.time(),
            strength=self.stats[0],
            dexterity=self.stats[1],
            constitution=self.stats[2],
            intelligence=self.stats[3],
            wisdom=self.stats[4],
            charisma=self.stats[5],
            god=self.god,
            starting_spells=self.selected_spells[:],
            inventory=[],
            equipment={},
            gold=0.0,
            gear_slots_used=0,
            max_gear_slots=max(self.stats[0], 10)  # Strength or 10, whichever is higher
        )

def run_character_creation_with_existing_display(screen: pygame.Surface, font_file: str) -> Optional[Player]:
    """Main function to run character creation process using existing display."""
    clock = pygame.time.Clock()
    
    creator = CharacterCreator(screen, font_file)
    
    running = True
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and creator.state == CharCreationState.NAME_INPUT:
                    return None
            
            result = creator.handle_event(event)
            if result is True:
                # Check if we have a completed player from gear selection
                if hasattr(creator, 'completed_player'):
                    return creator.completed_player
                else:
                    return creator.create_player()
            elif result is None:
                return None
            
            # Handle gear selection transition
            if creator.state == CharCreationState.GEAR_SELECTION:
                # Import and run gear selection using existing display
                try:
                    from ui.gear_selection import run_gear_selection_with_existing_display
                    temp_player = creator.create_player()
                    gear_result = run_gear_selection_with_existing_display(temp_player, screen, font_file)
                    if gear_result:
                        # Gear selection completed successfully - store the result
                        creator.completed_player = gear_result
                        creator.state = CharCreationState.STATS_REVIEW
                        creator._setup_ui()
                    else:
                        # Gear selection was cancelled, go back
                        creator._previous_state()
                except ImportError:
                    print("Error: gear_selection.py not found. Skipping gear selection.")
                    creator.state = CharCreationState.STATS_REVIEW
                    creator._setup_ui()
        
        creator.update(dt)
        creator.draw(screen)
        pygame.display.flip()
    
    return None

# Keep the old function for backward compatibility but mark it as deprecated
def run_character_creation(screen_width: int, screen_height: int, font_file: str) -> Optional[Player]:
    """DEPRECATED: Use run_character_creation_with_existing_display instead."""
    print("WARNING: run_character_creation is deprecated. Use run_character_creation_with_existing_display.")
    # Fallback implementation that creates its own display
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Character Creation")
    return run_character_creation_with_existing_display(screen, font_file)