ENHANCED_ALIGNMENTS = {
    "Lawful": {
        "description": "Believes in order, tradition, and following established rules.",
        "traits": "Honorable, reliable, structured thinking",
        "divine_favor": "Favored by gods of order and justice",
        "spell_effects": "Enhanced lawful divine magic, order-based spell bonuses"
    },
    "Chaotic": {
        "description": "Values freedom, change, and individual expression over rules.",
        "traits": "Independent, unpredictable, innovative",
        "divine_favor": "Favored by gods of change and freedom",
        "spell_effects": "Enhanced chaotic magic, wild magic surges, creative spellcasting"
    },
    "Neutral": {
        "description": "Seeks balance between order and chaos, pragmatic approach.",
        "traits": "Balanced, pragmatic, adaptable",
        "divine_favor": "Favored by gods of balance and nature",
        "spell_effects": "Balanced magic, nature affinity, adaptive spellcasting"
    }
}

# Enhanced Gods with detailed information
ENHANCED_GODS = {
    # Lawful Gods
    "Caedros": {
        "title": "The Hand of Judgment",
        "alignment": "Lawful",
        "domain": "Justice, protection, oaths",
        "symbol": "Balanced scales over a sword",
        "description": "Said to have carved the laws of mortals in stone with a blade of starlight. His temples double as courts.",
        "worshippers": "Judges, paladins, lawmakers",
        "divine_magic": "Enhanced protection and judgment spells"
    },
    "Velmari": {
        "title": "Keeper of the First Flame",
        "alignment": "Lawful",
        "domain": "Civilization, tradition, knowledge",
        "symbol": "A flame within a stylized tower",
        "description": "Taught mortals the secrets of architecture, fire, and speech. Believed to have laid the foundation for the first cities.",
        "worshippers": "Architects, scribes, elders, nobles",
        "divine_magic": "Enhanced knowledge and civilization spells"
    },
    "Serentha": {
        "title": "The Mother of Mercy",
        "alignment": "Lawful",
        "domain": "Healing, compassion, endurance",
        "symbol": "A blooming flower held in open hands",
        "description": "Walks among mortals in times of great suffering, disguised as a beggar or healer. Her breath is said to soothe pain.",
        "worshippers": "Clerics, midwives, caretakers",
        "divine_magic": "Enhanced healing and compassion spells"
    },
    
    # Neutral Gods
    "Thalen": {
        "title": "The Silent Watcher",
        "alignment": "Neutral",
        "domain": "Fate, time, the stars",
        "symbol": "Three intersecting orbits",
        "description": "Never speaks, never intervenes. Some believe Thalen is time itself — not a god, but a force in the shape of one.",
        "worshippers": "Oracles, astrologers, monks",
        "divine_magic": "Enhanced divination and fate spells"
    },
    "Nymbril": {
        "title": "The Shifting Path",
        "alignment": "Neutral",
        "domain": "Nature, change, beasts",
        "symbol": "A leaf turning into a claw",
        "description": "Takes the form of various beasts across the lands. Said to be neither male nor female, nor one being at all.",
        "worshippers": "Druids, travelers, rangers",
        "divine_magic": "Enhanced nature and transformation spells"
    },
    "Olvenar": {
        "title": "The Deep Well",
        "alignment": "Neutral",
        "domain": "Secrets, memory, inner strength",
        "symbol": "A closed eye over a spiral",
        "description": "Keeps the memories of all souls in a hidden vault beneath the world. Some say dreams are fragments he leaks out.",
        "worshippers": "Scholars, introverts, inquisitors",
        "divine_magic": "Enhanced memory and secret spells"
    },
    
    # Chaotic Gods
    "Zyrix": {
        "title": "The Devouring Flame",
        "alignment": "Chaotic",
        "domain": "War, conquest, chaos",
        "symbol": "A cracked helm engulfed in fire",
        "description": "Born in the heart of the first battlefield. His voice is said to drive men to war and ruin.",
        "worshippers": "Warlords, berserkers, tyrants",
        "divine_magic": "Enhanced war and destruction spells"
    },
    "Myrraketh": {
        "title": "The Unraveler",
        "alignment": "Chaotic",
        "domain": "Madness, arcane corruption, forbidden knowledge",
        "symbol": "A spiraled tentacle piercing an open eye",
        "description": "Believed to have once been a god of magic who went mad staring too long at the stars. Now sows chaos through cursed insight.",
        "worshippers": "Cultists, warlocks, mad prophets",
        "divine_magic": "Enhanced chaos and madness spells"
    },
    "Vhalor": {
        "title": "Lord of Hunger",
        "alignment": "Chaotic",
        "domain": "Destruction, entropy, death without rebirth",
        "symbol": "A gaping black maw surrounded by broken circles",
        "description": "Said to be the void made flesh — the inevitable end of all things. Prayers to him are bargains, not devotions.",
        "worshippers": "Necromancers, doomsayers, nihilists",
        "divine_magic": "Enhanced entropy and death spells"
    }
}

# Spell lists for starting characters
ENHANCED_PRIEST_SPELLS = {
    "Tier 1": [
        "Serentha's Touch", "Caedros's Aegis", "Zyrix's Fury", 
        "Velmari's Hearthlight", "Nymbril's Call", "Vhalor's Weariness"
    ],
    "Tier 2": [
        "Blade of Judgment", "Mercy's Relief", "Olvenar's Whisper"
    ]
}

ENHANCED_WIZARD_SPELLS = {
    "Tier 1": [
        "Frostwane Bite", "Embermarch Coals", "Greentide's Grasp", "Force Bolt",
        "Architect's Seal", "Continual Flame", "Feather Fall", "Runic Ward",
        "Shifting Shadow", "Arcane Sight", "Sentry Rune", "Duskwane Drowse"
    ],
    "Tier 2": [
        "Acid Arrow", "Mirror Image", "Web", "Misty Step", "Invisibility", "Suncrest Scorch"
    ],
    "Tier 3": [
        "Fireball", "Lightning Bolt", "Haste"
    ]
}

# Name generation lists
ENHANCED_NAMES = {
    "Human": {
        "male": ["Aldric", "Bran", "Gareth", "Theron", "Marcus", "Daven", "Kael", "Roderick"],
        "female": ["Lyanna", "Seraphina", "Mara", "Elara", "Vera", "Cordelia", "Isla", "Rhiannon"],
        "surname": ["Blackwood", "Stormwind", "Ironforge", "Goldleaf", "Ravencrest", "Thornfield"]
    },
    "Elf": {
        "male": ["Aelindra", "Silvyr", "Thalion", "Erevan", "Galanodel", "Miriel", "Soveliss"],
        "female": ["Arwen", "Galadriel", "Silaqui", "Nimrodel", "Elaria", "Vaelynn", "Lyralei"],
        "surname": ["Moonweaver", "Stargazer", "Nightbreeze", "Silverleaf", "Dawnstrider"]
    },
    "Dwarf": {
        "male": ["Thorin", "Gimli", "Balin", "Dwalin", "Groin", "Nain", "Bombur", "Bofur"],
        "female": ["Disa", "Nala", "Vera", "Mira", "Gunnlod", "Asta", "Brynja"],
        "surname": ["Ironbeard", "Stonebreaker", "Golddigger", "Axebreaker", "Shieldwall"]
    },
    "Halfling": {
        "male": ["Frodo", "Samwise", "Peregrin", "Meriadoc", "Bilbo", "Bandobras", "Mungo"],
        "female": ["Rosie", "Lily", "Daisy", "Poppy", "Pearl", "Ruby", "Belladonna"],
        "surname": ["Baggins", "Took", "Brandybuck", "Gamgee", "Proudfoot", "Bolger"]
    },
    "Half-Orc": {
        "male": ["Grokk", "Thragg", "Urgoth", "Grimjaw", "Skarr", "Vorgath", "Bragg"],
        "female": ["Grasha", "Ursa", "Morghul", "Skarla", "Varga", "Gotha", "Brenna"],
        "surname": ["Bloodfang", "Ironskull", "Ragebeast", "Warcry", "Bonecrusher"]
    },
    "Goblin": {
        "male": ["Grix", "Snark", "Blix", "Zook", "Gizzard", "Nix", "Skitter"],
        "female": ["Grizelda", "Snix", "Blixa", "Zara", "Nixa", "Skittara", "Glim"],
        "surname": ["Shadowcreep", "Quickstab", "Nightsneak", "Gloomwhisper", "Darkbane"]
    }
}

class EnhancedCharacterCreator:
    """Enhanced character creation with birth sign and cosmic destiny."""
    
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
        self.state = EnhancedCharCreationState.NAME_INPUT
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
        
        # NEW: Birth sign data
        self.birth_month = ""
        self.birth_day = 1
        self.age = 25
        self.birth_sign = None
        self.birth_date_input = ""
        self.age_input = ""
        
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
        return get_stat_modifier(stat_value)
    
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
        
        if self.state == EnhancedCharCreationState.NAME_INPUT:
            self._setup_name_input()
        elif self.state == EnhancedCharCreationState.STAT_ROLLING:
            self._setup_stat_rolling()
        elif self.state == EnhancedCharCreationState.BIRTH_DATE_INPUT:
            self._setup_birth_date_input()
    
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
    
    def _setup_birth_date_input(self):
        """Setup birth date input UI."""
        # Simple setup for birth date input
        pass
    
    def _get_current_options(self):
        """Get options for current selection state."""
        if self.state == EnhancedCharCreationState.RACE_SELECTION:
            return list(ENHANCED_RACES.keys())
        elif self.state == EnhancedCharCreationState.CLASS_SELECTION:
            return list(ENHANCED_CLASSES.keys())
        elif self.state == EnhancedCharCreationState.ALIGNMENT_SELECTION:
            return list(ENHANCED_ALIGNMENTS.keys())
        elif self.state == EnhancedCharCreationState.GOD_SELECTION:
            if self.alignment:
                return [name for name, god in ENHANCED_GODS.items() if god["alignment"] == self.alignment]
            return list(ENHANCED_GODS.keys())
        elif self.state == EnhancedCharCreationState.SPELL_SELECTION:
            if self.character_class == "Priest":
                return ENHANCED_PRIEST_SPELLS["Tier 1"]
            elif self.character_class == "Wizard":
                return ENHANCED_WIZARD_SPELLS["Tier 1"]
        return []
    
    def _get_current_details(self):
        """Get details for currently selected option."""
        options = self._get_current_options()
        if not options or self.selected_index >= len(options):
            return None
            
        selected_option = options[self.selected_index]
        
        if self.state == EnhancedCharCreationState.RACE_SELECTION:
            return ENHANCED_RACES.get(selected_option)
        elif self.state == EnhancedCharCreationState.CLASS_SELECTION:
            return ENHANCED_CLASSES.get(selected_option)
        elif self.state == EnhancedCharCreationState.ALIGNMENT_SELECTION:
            return ENHANCED_ALIGNMENTS.get(selected_option)
        elif self.state == EnhancedCharCreationState.GOD_SELECTION:
            return ENHANCED_GODS.get(selected_option)
        elif self.state == EnhancedCharCreationState.SPELL_SELECTION:
            # Return simple spell info for now
            return {"description": f"A powerful {selected_option} spell"}
        return None
    
    def handle_event(self, event: pygame.event.Event) -> Optional[bool]:
        """Handle input events. Returns True to complete, None to cancel, False to continue."""
        # Handle text input
        if self.text_input and self.state == EnhancedCharCreationState.NAME_INPUT:
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
            if self.state == EnhancedCharCreationState.STAT_ROLLING:
                self._next_state()
        
        if self.reroll_button and self.reroll_button.handle_event(event):
            if not self.has_high_stat(self.stats):
                self._roll_new_stats()
        
        # Handle keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state != EnhancedCharCreationState.NAME_INPUT:
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
                if self.state == EnhancedCharCreationState.STAT_ROLLING:
                    self._roll_new_stats()
                elif self.state == EnhancedCharCreationState.BIRTH_DATE_INPUT:
                    self._generate_random_birth_date()
            
            # Handle birth date input
            elif self.state == EnhancedCharCreationState.BIRTH_DATE_INPUT:
                self._handle_birth_date_input(event)
        
        return False
    
    def _handle_birth_date_input(self, event):
        """Handle birth date input."""
        if event.type == pygame.KEYDOWN:
            if event.unicode and event.unicode.isprintable():
                if not self.birth_date_input:
                    self.birth_date_input = ""
                if event.key == pygame.K_BACKSPACE:
                    self.birth_date_input = self.birth_date_input[:-1]
                elif len(self.birth_date_input) < 50:
                    self.birth_date_input += event.unicode
    
    def _generate_random_birth_date(self):
        """Generate random birth date."""
        months = ["Frostwane", "Embermarch", "Thawmere", "Greentide", "Blossarch", "Suncrest",
                 "Highflare", "Duskwane", "Mournfall", "Hallowdeep", "Snowrest", "Starhearth"]
        self.birth_month = random.choice(months)
        self.birth_day = random.randint(1, 30)
        self.age = random.randint(18, 60)
        self.birth_date_input = f"{self.birth_month} {self.birth_day}, Age {self.age}"
    
    def _calculate_birth_sign(self):
        """Calculate birth sign from input."""
        if ENHANCED_SYSTEMS_AVAILABLE:
            try:
                # Parse birth date input
                if "," in self.birth_date_input:
                    date_part, age_part = self.birth_date_input.split(",")
                    parts = date_part.strip().split()
                    if len(parts) >= 2:
                        month = parts[0].title()
                        day = int(parts[1])
                        age = int(age_part.replace("Age", "").strip())
                        
                        self.birth_month = month
                        self.birth_day = day
                        self.age = age
                        
                        self.birth_sign = BirthSignGenerator.generate_birth_sign_from_date(
                            month, day, age
                        )
                        return True
            except (ValueError, IndexError):
                pass
        
        # Fallback - generate random
        self._generate_random_birth_date()
        if ENHANCED_SYSTEMS_AVAILABLE:
            self.birth_sign = BirthSignGenerator.generate_random_birth_sign((self.age, self.age))
        return True
    
    def _handle_enter_key(self) -> Optional[bool]:
        """Handle Enter key press."""
        if self.state == EnhancedCharCreationState.NAME_INPUT:
            if self.text_input and self.text_input.text.strip():
                self._next_state()
        elif self.state == EnhancedCharCreationState.STAT_ROLLING:
            self._next_state()
        elif self.state == EnhancedCharCreationState.BIRTH_DATE_INPUT:
            if self._calculate_birth_sign():
                self._next_state()
        elif self.state == EnhancedCharCreationState.BIRTH_SIGN_REVIEW:
            self._next_state()
        elif self.state in [EnhancedCharCreationState.RACE_SELECTION, EnhancedCharCreationState.CLASS_SELECTION, 
                           EnhancedCharCreationState.ALIGNMENT_SELECTION, EnhancedCharCreationState.GOD_SELECTION,
                           EnhancedCharCreationState.SPELL_SELECTION]:
            if self._make_selection(self.selected_index):
                self._next_state()
            elif self.state != EnhancedCharCreationState.SPELL_SELECTION:
                self._next_state()
        elif self.state == EnhancedCharCreationState.STATS_REVIEW:
            self.state = EnhancedCharCreationState.GEAR_SELECTION
        
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
        if self.state == EnhancedCharCreationState.NAME_INPUT:
            self._draw_name_input(surface)
        elif self.state == EnhancedCharCreationState.STAT_ROLLING:
            self._draw_stat_rolling(surface)
        elif self.state == EnhancedCharCreationState.BIRTH_DATE_INPUT:
            self._draw_birth_date_input(surface)
        elif self.state == EnhancedCharCreationState.BIRTH_SIGN_REVIEW:
            self._draw_birth_sign_review(surface)
        elif self.state in [EnhancedCharCreationState.RACE_SELECTION, EnhancedCharCreationState.CLASS_SELECTION, 
                           EnhancedCharCreationState.ALIGNMENT_SELECTION, EnhancedCharCreationState.GOD_SELECTION,
                           EnhancedCharCreationState.SPELL_SELECTION]:
            self._draw_selection_screen(surface)
        elif self.state == EnhancedCharCreationState.STATS_REVIEW:
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
        stat_names = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        
        for i, (stat_name, stat_value) in enumerate(zip(stat_names, self.stats)):
            y = left_start_y + i * 60
            modifier = self.get_stat_modifier(stat_value)
            modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)
            
            name_surf = self.large_font.render(f"{stat_name}:", True, COLOR_WHITE)
            surface.blit(name_surf, (self.list_x, y))
            
            value_text = f"{stat_value} ({modifier_str})"
            value_surf = self.large_font.render(value_text, True, COLOR_WHITE)
            surface.blit(value_surf, (self.list_x, y + 25))
        
        # Right side - descriptions
        stat_descriptions = {
            "Strength": "Physical power, melee damage, carrying capacity",
            "Dexterity": "Agility, ranged attacks, armor class, stealth",
            "Constitution": "Health, hit points, stamina, poison resistance",
            "Intelligence": "Reasoning, wizard spells, skill points, lore",
            "Wisdom": "Perception, priest spells, insight, willpower",
            "Charisma": "Personality, leadership, divine favor, social skills"
        }
        
        right_start_y = 150
        for i, stat_name in enumerate(stat_names):
            y = right_start_y + i * 60
            desc = stat_descriptions.get(stat_name, "")
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
    
    def _draw_birth_date_input(self, surface: pygame.Surface):
        """Draw birth date input screen."""
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Instructions
        instructions = [
            "Enter your birth details to calculate your cosmic destiny:",
            "",
            "Format: 'Month Day, Age ##' (e.g., 'Duskwane 17, Age 25')",
            "",
            "Available months:",
            "Frostwane, Embermarch, Thawmere, Greentide, Blossarch, Suncrest",
            "Highflare, Duskwane, Mournfall, Hallowdeep, Snowrest, Starhearth",
            "",
            "Current input:",
            self.birth_date_input or "(type your birth date)",
            "",
            "Press SPACE for random birth date",
            "Press ENTER to calculate birth sign"
        ]
        
        y = center_y - 200
        for i, instruction in enumerate(instructions):
            if instruction == self.birth_date_input or "(type your birth date)":
                color = COLOR_GOLD if self.birth_date_input else COLOR_WHITE
                font = self.medium_font
            elif instruction.startswith("Format:") or instruction.startswith("Available"):
                color = COLOR_GOLD
                font = self.small_font
            elif instruction.startswith("Press"):
                color = (150, 150, 255)
                font = self.small_font
            else:
                color = COLOR_WHITE
                font = self.small_font
            
            if instruction:
                inst_surf = font.render(instruction, True, color)
                inst_rect = inst_surf.get_rect(centerx=center_x, top=y)
                surface.blit(inst_surf, inst_rect)
            
            y += font.get_height() + 5
    
    def _draw_birth_sign_review(self, surface: pygame.Surface):
        """Draw birth sign review screen."""
        if not self.birth_sign and ENHANCED_SYSTEMS_AVAILABLE:
            # Fallback display
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2
            
            fallback_surf = self.large_font.render("Birth sign calculated!", True, COLOR_GOLD)
            fallback_rect = fallback_surf.get_rect(centerx=center_x, centery=center_y)
            surface.blit(fallback_surf, fallback_rect)
            return
        
        center_x = self.screen_width // 2
        
        # Title
        title_surf = self.title_font.render("Your Cosmic Destiny", True, COLOR_GOLD)
        title_rect = title_surf.get_rect(centerx=center_x, top=50)
        surface.blit(title_surf, title_rect)
        
        if ENHANCED_SYSTEMS_AVAILABLE and self.birth_sign:
            # Birth sign details
            lines = format_birth_sign_for_display(self.birth_sign)
            y = title_rect.bottom + 20
            
            for line in lines:
                if line.startswith("Birth Sign:"):
                    color = COLOR_GOLD
                    current_font = self.large_font
                elif line.startswith("Prophecy:") or line.startswith("Stat Bonuses:") or line.startswith("Special Abilities:"):
                    color = COLOR_GOLD
                    current_font = self.medium_font
                elif line.strip() == "":
                    y += 10
                    continue
                else:
                    color = COLOR_WHITE
                    current_font = self.small_font
                
                line_surf = current_font.render(line, True, color)
                line_rect = line_surf.get_rect(centerx=center_x, top=y)
                surface.blit(line_surf, line_rect)
                y += current_font.get_height() + 2
        else:
            # Fallback display without enhanced systems
            basic_info = [
                f"Born: {self.birth_day} {self.birth_month}, Age {self.age}",
                "",
                "Your cosmic destiny shapes your character's fate.",
                "The stars and moons influence your magical abilities",
                "and grant you special insights into the world.",
                "",
                f"Birth Month: {self.birth_month}",
                f"This grants you affinity with the season's energies."
            ]
            
            y = title_rect.bottom + 30
            for info in basic_info:
                if info.strip():
                    info_surf = self.medium_font.render(info, True, COLOR_WHITE)
                    info_rect = info_surf.get_rect(centerx=center_x, top=y)
                    surface.blit(info_surf, info_rect)
                y += self.medium_font.get_height() + 5
    
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
            
            if self.state == EnhancedCharCreationState.SPELL_SELECTION and option in self.selected_spells:
                selected_surf = self.small_font.render("✓ SELECTED", True, (0, 255, 0))
                surface.blit(selected_surf, (self.list_x, y + 25))
        
        # Spell selection progress
        if self.state == EnhancedCharCreationState.SPELL_SELECTION:
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
        title = details.get("title", details.get("description", ""))
        if self.state == EnhancedCharCreationState.GOD_SELECTION:
            title = f"{details.get('title', '')} - {details.get('domain', '')}"
        
        title_surf = self.large_font.render(title, True, COLOR_WHITE)
        surface.blit(title_surf, (self.detail_x, detail_y))
        detail_y += 40
        
        # Description
        description = details.get("description", "")
        wrapped_lines = wrap_text(description, self.detail_width - 40, self.medium_font)
        for line in wrapped_lines:
            line_surf = self.medium_font.render(line, True, COLOR_WHITE)
            surface.blit(line_surf, (self.detail_x, detail_y))
            detail_y += line_height
        
        detail_y += 20
        
        # Additional details
        if "traits" in details:
            trait_surf = self.small_font.render(f"Traits: {details['traits']}", True, COLOR_WHITE)
            surface.blit(trait_surf, (self.detail_x, detail_y))
            detail_y += 20
        
        if "stats" in details:
            detail_y += 10
            for stat in details["stats"]:
                stat_surf = self.small_font.render(stat, True, COLOR_WHITE)
                surface.blit(stat_surf, (self.detail_x, detail_y))
                detail_y += 18
            detail_y += 15
            
            for ability in details["abilities"]:
                wrapped_ability = wrap_text(ability, self.detail_width - 40, self.small_font)
                for line in wrapped_ability:
                    line_surf = self.small_font.render(line, True, COLOR_WHITE)
                    surface.blit(line_surf, (self.detail_x, detail_y))
                    detail_y += 16
                detail_y += 10
        
        # God-specific details
        if self.state == EnhancedCharCreationState.GOD_SELECTION:
            god_details = [
                f"Alignment: {details.get('alignment', 'Unknown')}",
                f"Symbol: {details.get('symbol', 'Unknown')}",
                f"Worshippers: {details.get('worshippers', 'Unknown')}",
                f"Divine Magic: {details.get('divine_magic', 'Standard divine spells')}"
            ]
            
            for detail in god_details:
                detail_surf = self.small_font.render(detail, True, COLOR_WHITE)
                surface.blit(detail_surf, (self.detail_x, detail_y))
                detail_y += 18
    
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
        
        if self.birth_month:
            char_info.append(f"Birth: {self.birth_day} {self.birth_month}, Age {self.age}")
        
        if self.selected_spells:
            char_info.append(f"Starting Spells: {', '.join(self.selected_spells)}")
        
        char_info.extend([
            "",
            "STATISTICS:",
        ])
        
        stat_names = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        for i, (stat_name, stat_value) in enumerate(zip(stat_names, self.stats)):
            modifier = self.get_stat_modifier(stat_value)
            modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)
            char_info.append(f"{stat_name}: {stat_value} ({modifier_str})")
        
        char_info.extend([
            "",
            "Level: 1",
            f"Hit Points: {self._calculate_starting_hp()}/{self._calculate_starting_hp()}",
            f"Armor Class: {self._calculate_starting_ac()}",
            "Experience: 0/100"
        ])
        
        for i, info in enumerate(char_info):
            if info:
                font = self.large_font if info in ["STATISTICS:"] else self.medium_font
                color = COLOR_GOLD if info.startswith("Name:") or info in ["STATISTICS:"] else COLOR_WHITE
                info_surf = font.render(info, True, color)
                info_rect = info_surf.get_rect(centerx=center_x, y=start_y + i * line_height)
                surface.blit(info_surf, info_rect)
    
    def _calculate_starting_hp(self) -> int:
        """Calculate starting hit points."""
        constitution_bonus = self.get_stat_modifier(self.stats[2])
        
        if self.character_class == "Fighter":
            base_hp = 10
        elif self.character_class == "Priest":
            base_hp = 8
        elif self.character_class in ["Wizard", "Thief"]:
            base_hp = 6
        else:
            base_hp = 8
        
        return max(1, base_hp + constitution_bonus)
    
    def _calculate_starting_ac(self) -> int:
        """Calculate starting AC."""
        dexterity_bonus = self.get_stat_modifier(self.stats[1])
        return 10 + dexterity_bonus
    
    def _draw_instructions(self, surface: pygame.Surface):
        """Draw instruction text."""
        instructions = []
        
        if self.state == EnhancedCharCreationState.NAME_INPUT:
            instructions = ["Enter your name and press ENTER", "Click Random for a random name"]
        elif self.state == EnhancedCharCreationState.STAT_ROLLING:
            instructions = ["SPACE or Roll Stats button to roll", "Press ENTER or Accept to continue", "Reroll if no stat is 14+"]
        elif self.state == EnhancedCharCreationState.BIRTH_DATE_INPUT:
            instructions = ["Type your birth month, day, and age", "SPACE for random", "ENTER to continue"]
        elif self.state == EnhancedCharCreationState.BIRTH_SIGN_REVIEW:
            instructions = ["Press ENTER to continue", "Press ESC to change birth date"]
        elif self.state in [EnhancedCharCreationState.RACE_SELECTION, EnhancedCharCreationState.CLASS_SELECTION, 
                           EnhancedCharCreationState.ALIGNMENT_SELECTION, EnhancedCharCreationState.GOD_SELECTION]:
            instructions = ["Use UP/DOWN arrows to navigate", "Press ENTER to select", "Press ESC to go back"]
        elif self.state == EnhancedCharCreationState.SPELL_SELECTION:
            if len(self.selected_spells) < self.spells_to_select:
                instructions = ["Use UP/DOWN arrows to navigate", "Press ENTER to select spell", f"Select {self.spells_to_select - len(self.selected_spells)} more spells"]
            else:
                instructions = ["Press ENTER to continue", "Press ESC to go back"]
        elif self.state == EnhancedCharCreationState.STATS_REVIEW:
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
            EnhancedCharCreationState.NAME_INPUT: "Enter Your Name",
            EnhancedCharCreationState.STAT_ROLLING: "Roll Your Statistics",
            EnhancedCharCreationState.RACE_SELECTION: "Choose Your Ancestry", 
            EnhancedCharCreationState.CLASS_SELECTION: "Choose Your Class",
            EnhancedCharCreationState.ALIGNMENT_SELECTION: "Choose Your Alignment",
            EnhancedCharCreationState.BIRTH_DATE_INPUT: "Calculate Your Birth Sign",
            EnhancedCharCreationState.BIRTH_SIGN_REVIEW: "Your Cosmic Destiny",
            EnhancedCharCreationState.GOD_SELECTION: "Choose Your Deity",
            EnhancedCharCreationState.SPELL_SELECTION: "Choose Your Starting Spells",
            EnhancedCharCreationState.GEAR_SELECTION: "Select Your Gear",
            EnhancedCharCreationState.STATS_REVIEW: "Character Summary"
        }
        return titles.get(self.state, "Character Creation")
    
    def _get_character_title(self) -> str:
        """Get character title based on class and alignment."""
        if not all([self.character_class, self.alignment]):
            return "Adventurer"
        
        titles = {
            "Fighter": {
                "Lawful": "Guardian",
                "Chaotic": "Warrior", 
                "Neutral": "Soldier"
            },
            "Priest": {
                "Lawful": "Acolyte",
                "Chaotic": "Zealot",
                "Neutral": "Initiate"
            },
            "Wizard": {
                "Lawful": "Apprentice",
                "Chaotic": "Hedge Wizard",
                "Neutral": "Student"
            },
            "Thief": {
                "Lawful": "Scout",
                "Chaotic": "Rogue",
                "Neutral": "Burglar"
            }
        }
        
        return titles.get(self.character_class, {}).get(self.alignment, "Adventurer")
    
    def create_player(self) -> Player:
        """Create a Player object from the character creation data."""
        # Create enhanced player with all new systems
        player = create_enhanced_player(
            name=self.name,
            race=self.race,
            character_class=self.character_class,
            alignment=self.alignment,
            stats=self.stats,
            birth_month=self.birth_month,
            birth_day=self.birth_day,
            age=self.age
        )
        
        # Set title
        player.title = self._get_character_title()
        
        # Set god
        player.god = self.god
        
        # Set starting spells
        player.starting_spells = self.selected_spells[:]
        player.known_spells = self.selected_spells[:]
        
        # Apply birth sign if available
        if ENHANCED_SYSTEMS_AVAILABLE and self.birth_sign:
            add_birth_sign_to_player(player, self.birth_sign)
        
        # Add spellcasting system
        if ENHANCED_SYSTEMS_AVAILABLE:
            add_spellcasting_to_character(player)
            
            # Learn starting spells
            if player.spellcaster:
                for spell_name in self.selected_spells:
                    player.spellcaster.learn_spell(spell_name)
        
        return player

def run_enhanced_character_creation_with_existing_display(screen: pygame.Surface, font_file: str) -> Optional[Player]:
    """Main function to run enhanced character creation process using existing display."""
    clock = pygame.time.Clock()
    
    creator = EnhancedCharacterCreator(screen, font_file)
    
    running = True
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and creator.state == EnhancedCharCreationState.NAME_INPUT:
                    return None
            
            result = creator.handle_event(event)
            if result is True:
                return creator.create_player()
            elif result is None:
                return None
            
            # Handle gear selection transition
            if creator.state == EnhancedCharCreationState.GEAR_SELECTION:
                # Import and run gear selection using existing display
                try:
                    from ui.gear_selection import run_gear_selection_with_existing_display
                    temp_player = creator.create_player()
                    gear_result = run_gear_selection_with_existing_display(temp_player, screen, font_file)
                    if gear_result:
                        # Gear selection completed successfully
                        return gear_result
                    else:
                        # Gear selection was cancelled, go back
                        creator._previous_state()
                except ImportError:
                    print("Error: gear_selection.py not found. Skipping gear selection.")
                    creator.state = EnhancedCharCreationState.STATS_REVIEW
                    creator._setup_ui()
        
        creator.update(dt)
        creator.draw(screen)
        pygame.display.flip()
    
    return None

# Example usage
if __name__ == "__main__":
    # Test the enhanced character creation
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Enhanced Character Creation Test")
    
    player = run_enhanced_character_creation_with_existing_display(screen, FONT_FILE)
    
    if player:
        print("=== CHARACTER CREATED ===")
        summary = player.get_character_summary()
        for line in summary:
            print(line)
    
    pygame.quit()
            return True  # Complete character creation
        
        return False
    
    def _handle_navigation(self, direction: int):
        """Handle up/down navigation."""
        if self.state in [EnhancedCharCreationState.RACE_SELECTION, EnhancedCharCreationState.CLASS_SELECTION, 
                         EnhancedCharCreationState.ALIGNMENT_SELECTION, EnhancedCharCreationState.GOD_SELECTION,
                         EnhancedCharCreationState.SPELL_SELECTION]:
            options = self._get_current_options()
            if options:
                self.selected_index = (self.selected_index + direction) % len(options)
    
    def _make_selection(self, index: int) -> bool:
        """Make a selection for current state."""
        options = self._get_current_options()
        if index < len(options):
            if self.state == EnhancedCharCreationState.RACE_SELECTION:
                self.race = options[index]
            elif self.state == EnhancedCharCreationState.CLASS_SELECTION:
                self.character_class = options[index]
            elif self.state == EnhancedCharCreationState.ALIGNMENT_SELECTION:
                self.alignment = options[index]
            elif self.state == EnhancedCharCreationState.GOD_SELECTION:
                self.god = options[index]
            elif self.state == EnhancedCharCreationState.SPELL_SELECTION:
                spell = options[index]
                if spell not in self.selected_spells:
                    self.selected_spells.append(spell)
                    if len(self.selected_spells) >= self.spells_to_select:
                        return True
        return False
    
    def _randomize_current_selection(self):
        """Randomize current selection."""
        if self.state == EnhancedCharCreationState.NAME_INPUT:
            # Generate random name based on race (if known) or human default
            race_for_name = self.race if self.race else "Human"
            gender = random.choice(["male", "female"])
            names = ENHANCED_NAMES.get(race_for_name, ENHANCED_NAMES["Human"])
            
            first_name = random.choice(names[gender])
            last_name = random.choice(names["surname"]) if "surname" in names else ""
            
            self.text_input.text = f"{first_name} {last_name}".strip()
    
    def _roll_new_stats(self):
        """Roll new stats."""
        new_stats = self.roll_stats()
        self.stat_rolls_history.append(new_stats)
        self.current_roll_set = len(self.stat_rolls_history) - 1
        self.stats = new_stats[:]
    
    def _next_state(self):
        """Advance to next state."""
        if self.state == EnhancedCharCreationState.NAME_INPUT:
            self.name = self.text_input.text.strip()
            self.state = EnhancedCharCreationState.STAT_ROLLING
        elif self.state == EnhancedCharCreationState.STAT_ROLLING:
            self.state = EnhancedCharCreationState.RACE_SELECTION
        elif self.state == EnhancedCharCreationState.RACE_SELECTION:
            self.state = EnhancedCharCreationState.CLASS_SELECTION
        elif self.state == EnhancedCharCreationState.CLASS_SELECTION:
            self.state = EnhancedCharCreationState.ALIGNMENT_SELECTION
        elif self.state == EnhancedCharCreationState.ALIGNMENT_SELECTION:
            # NEW: Go to birth date input
            self.state = EnhancedCharCreationState.BIRTH_DATE_INPUT
        elif self.state == EnhancedCharCreationState.BIRTH_DATE_INPUT:
            # NEW: Go to birth sign review
            self.state = EnhancedCharCreationState.BIRTH_SIGN_REVIEW
        elif self.state == EnhancedCharCreationState.BIRTH_SIGN_REVIEW:
            # Continue to god selection if priest
            if self.character_class == "Priest":
                self.state = EnhancedCharCreationState.GOD_SELECTION
            elif self.character_class in ["Priest", "Wizard"]:
                self._setup_spell_selection()
                self.state = EnhancedCharCreationState.SPELL_SELECTION
            else:
                self.state = EnhancedCharCreationState.GEAR_SELECTION
        elif self.state == EnhancedCharCreationState.GOD_SELECTION:
            if self.character_class in ["Priest", "Wizard"]:
                self._setup_spell_selection()
                self.state = EnhancedCharCreationState.SPELL_SELECTION
            else:
                self.state = EnhancedCharCreationState.GEAR_SELECTION
        elif self.state == EnhancedCharCreationState.SPELL_SELECTION:
            self.state = EnhancedCharCreationState.GEAR_SELECTION
        elif self.state == EnhancedCharCreationState.GEAR_SELECTION:
            self.state = EnhancedCharCreationState.STATS_REVIEW
        elif self.state == EnhancedCharCreationState.STATS_REVIEW:
            self.state = EnhancedCharCreationState.COMPLETE
        
        self._setup_ui()
    
    def _previous_state(self):
        """Go back to previous state."""
        if self.state == EnhancedCharCreationState.STAT_ROLLING:
            self.state = EnhancedCharCreationState.NAME_INPUT
        elif self.state == EnhancedCharCreationState.RACE_SELECTION:
            self.state = EnhancedCharCreationState.STAT_ROLLING
        elif self.state == EnhancedCharCreationState.CLASS_SELECTION:
            self.state = EnhancedCharCreationState.RACE_SELECTION
        elif self.state == EnhancedCharCreationState.ALIGNMENT_SELECTION:
            self.state = EnhancedCharCreationState.CLASS_SELECTION
        elif self.state == EnhancedCharCreationState.BIRTH_DATE_INPUT:
            self.state = EnhancedCharCreationState.ALIGNMENT_SELECTION
        elif self.state == EnhancedCharCreationState.BIRTH_SIGN_REVIEW:
            self.state = EnhancedCharCreationState.BIRTH_DATE_INPUT
        elif self.state == EnhancedCharCreationState.GOD_SELECTION:
            self.state = EnhancedCharCreationState.BIRTH_SIGN_REVIEW
        elif self.state == EnhancedCharCreationState.SPELL_SELECTION:
            if self.character_class == "Priest":
                self.state = EnhancedCharCreationState.GOD_SELECTION
            else:
                self.state = EnhancedCharCreationState.BIRTH_SIGN_REVIEW
        elif self.state == EnhancedCharCreationState.GEAR_SELECTION:
            if self.character_class in ["Priest", "Wizard"]:
                self.state = EnhancedCharCreationState.SPELL_SELECTION
            elif self.character_class == "Priest":
                self.state = EnhancedCharCreationState.GOD_SELECTION
            else:
                self.state = EnhancedCharCreationState.BIRTH_SIGN_REVIEW
        elif self.state == EnhancedCharCreationState.STATS_REVIEW:"""
Complete Enhanced Character Creation UI
Integrated with birth sign system, updated spell system, and cosmic destiny.
"""

import pygame
import random
import time
from typing import List, Tuple, Optional, Dict
from enum import Enum

# Import from modular structure
from config.constants import *
from data.player import Player, get_stat_modifier, create_enhanced_player
from game.states import CharCreationState
from ui.base_ui import Button, TextInput, wrap_text

# New systems integration
try:
    from data.birth_sign_system import (
        BirthSignCalculator, BirthSignGenerator, add_birth_sign_to_player,
        format_birth_sign_for_display
    )
    from data.updated_spell_systems import add_spellcasting_to_character
    ENHANCED_SYSTEMS_AVAILABLE = True
except ImportError:
    # Graceful fallback if enhanced systems aren't available yet
    ENHANCED_SYSTEMS_AVAILABLE = False
    print("Enhanced systems not available - using basic character creation")

# Enhanced Character Creation States
class EnhancedCharCreationState(Enum):
    """Enhanced character creation states including birth sign calculation."""
    NAME_INPUT = 0
    STAT_ROLLING = 1
    RACE_SELECTION = 2
    CLASS_SELECTION = 3
    ALIGNMENT_SELECTION = 4
    BIRTH_DATE_INPUT = 5      # NEW: Birth date and age input
    BIRTH_SIGN_REVIEW = 6     # NEW: Review cosmic destiny
    GOD_SELECTION = 7
    SPELL_SELECTION = 8
    GEAR_SELECTION = 9
    STATS_REVIEW = 10
    COMPLETE = 11

# Character creation data with enhanced details
ENHANCED_RACES = {
    "Human": {
        "description": "Versatile and ambitious, humans adapt quickly to any situation.",
        "traits": "Bonus skill point, extra feat, versatile",
        "stats": ["+1 to any stat of choice"],
        "abilities": ["Bonus skill point", "Extra starting feat", "Diplomatic bonus"]
    },
    "Elf": {
        "description": "Graceful and long-lived, with natural magical affinity.",
        "traits": "Keen senses, magic resistance, night vision",
        "stats": ["+2 Dexterity"],
        "abilities": ["Night vision", "Magic resistance", "Keen hearing and sight"]
    },
    "Dwarf": {
        "description": "Sturdy and resilient, masters of stone and metal.",
        "traits": "Poison resistance, stone cunning, combat training",
        "stats": ["+2 Constitution"],
        "abilities": ["Poison resistance", "Stone cunning", "Weapon familiarity"]
    },
    "Halfling": {
        "description": "Small but brave, with remarkable luck and stealth.",
        "traits": "Lucky, brave, nimble",
        "stats": ["+2 Dexterity"],
        "abilities": ["Lucky re-rolls", "Brave (fear resistance)", "Small size benefits"]
    },
    "Half-Orc": {
        "description": "Strong and fierce, caught between two worlds.",
        "traits": "Relentless endurance, savage attacks",
        "stats": ["+2 Strength", "+1 Constitution"],
        "abilities": ["Relentless endurance", "Savage critical hits", "Darkvision"]
    },
    "Goblin": {
        "description": "Small, clever, and mischievous creatures of shadow.",
        "traits": "Nimble escape, stealth mastery",
        "stats": ["+2 Dexterity", "-1 Constitution"],
        "abilities": ["Stealth expertise", "Small size", "Nimble escape"]
    }
}

ENHANCED_CLASSES = {
    "Fighter": {
        "description": "Master of weapons and armor, born for battle.",
        "traits": "Combat expertise, weapon mastery, high hit points",
        "stats": ["High Strength or Dexterity recommended"],
        "abilities": ["Second Wind", "Weapon specialization", "Combat maneuvers", "Extra gear slots from Constitution"]
    },
    "Priest": {
        "description": "Divine spellcaster serving the gods with healing and holy magic.",
        "traits": "Divine magic, healing powers, undead turning",
        "stats": ["High Wisdom for spellcasting"],
        "abilities": ["Divine spellcasting", "Channel divinity", "Healing touch", "Holy magic resistance"]
    },
    "Wizard": {
        "description": "Arcane spellcaster wielding reality-bending magic through study.",
        "traits": "Arcane magic, spell research, magical knowledge",
        "stats": ["High Intelligence for spellcasting"],
        "abilities": ["Arcane spellcasting", "Spell research", "Magical item creation", "Lore mastery"]
    },
    "Thief": {
        "description": "Stealthy scout skilled in locks, traps, and shadows.",
        "traits": "Stealth, lockpicking, sneak attacks",
        "stats": ["High Dexterity for skills"],
        "abilities": ["Sneak attack", "Lockpicking", "Trap detection", "Stealth mastery"]
    }
}

ENHANCED_ALIGNMENTS = {
    "Lawful": {
        "description": "Believes in order, tradition, and following established rules.",
        "traits": "Honorable, reliable, structured thinking",
        "divine_favor": "Fav