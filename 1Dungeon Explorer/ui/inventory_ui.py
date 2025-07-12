"""
Inventory and Equipment UI Components
Extracted and refactored from the original dungeon_viewer.py
"""

import pygame
from typing import List, Optional

# Import from new modular structure
from config.constants import *
from data.player import Player
from data.items import *
from data.containers import *
from ui.base_ui import wrap_text, draw_separator_line, center_text

class InventoryUI:
    """Inventory management UI component."""
    
    def __init__(self, screen_width: int, screen_height: int, font_file: str):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fonts
        self.font = pygame.font.Font(font_file, 20)
        self.small_font = pygame.font.Font(font_file, 16)
        
        # Layout
        self.separator_x = screen_width // 3 + 30
        self.list_x = 20
        self.list_width = screen_width // 3
        self.detail_x = self.separator_x + 20
        self.detail_width = screen_width - self.detail_x - 20
        
        # State
        self.selected_index = 0
        self.current_containers = []
    
    def set_containers(self, containers: List[Container]):
        """Set the list of containers to display."""
        self.current_containers = containers
        self.selected_index = 0
    
    def handle_navigation(self, direction: int) -> bool:
        """Handle up/down navigation. Returns True if selection changed."""
        if self.current_containers:
            old_index = self.selected_index
            self.selected_index = (self.selected_index + direction) % len(self.current_containers)
            return old_index != self.selected_index
        return False
    
    def get_selected_container(self) -> Optional[Container]:
        """Get the currently selected container."""
        if self.current_containers and 0 <= self.selected_index < len(self.current_containers):
            return self.current_containers[self.selected_index]
        return None
    
    def draw_inventory_screen(self, surface: pygame.Surface, player: Player):
        """Draw the main inventory screen."""
        surface.fill(COLOR_BLACK)
        
        # Title
        center_text(surface, f"{player.name}'s Inventory", self.font, COLOR_WHITE, 20)
        
        # Draw separator line
        draw_separator_line(surface, self.separator_x, 80, self.screen_height - 100)
        
        # Left side - container list
        y = 100
        
        if not self.current_containers:
            empty_surf = self.font.render("No containers found", True, COLOR_WHITE)
            surface.blit(empty_surf, (self.list_x, y))
        else:
            for i, container in enumerate(self.current_containers):
                # Highlight selected container
                if i == self.selected_index:
                    highlight_rect = pygame.Rect(self.list_x - 5, y - 5, self.list_width - 30, 60)
                    pygame.draw.rect(surface, COLOR_SELECTED_ITEM, highlight_rect)
                    pygame.draw.rect(surface, COLOR_WHITE, highlight_rect, 2)
                
                color = COLOR_BLACK if i == self.selected_index else COLOR_WHITE
                
                # Container name
                container_surf = self.font.render(container.name, True, color)
                surface.blit(container_surf, (self.list_x, y))
                
                # Container capacity info
                used_capacity = container.get_used_capacity()
                capacity_text = f"{used_capacity}/{container.capacity} slots"
                capacity_color = COLOR_RED if used_capacity > container.capacity else color
                capacity_surf = self.small_font.render(capacity_text, True, capacity_color)
                surface.blit(capacity_surf, (self.list_x, y + 25))
                
                # Item count
                item_count_text = f"{len(container.contents)} items"
                item_surf = self.small_font.render(item_count_text, True, color)
                surface.blit(item_surf, (self.list_x, y + 40))
                
                y += 70
        
        # Right side - container contents
        selected_container = self.get_selected_container()
        if selected_container:
            self.draw_container_contents(surface, selected_container)
        
        # Instructions
        self._draw_inventory_instructions(surface)
    
    def draw_container_contents(self, surface: pygame.Surface, container: Container):
        """Draw the contents of a container."""
        current_y = 100
        
        # Container header
        header_surf = self.font.render(f"Contents of {container.name}", True, COLOR_WHITE)
        surface.blit(header_surf, (self.detail_x, current_y))
        current_y += 30
        
        # Capacity bar
        used_capacity = container.get_used_capacity()
        capacity_text = f"Capacity: {used_capacity}/{container.capacity}"
        capacity_surf = self.small_font.render(capacity_text, True, COLOR_WHITE)
        surface.blit(capacity_surf, (self.detail_x, current_y))
        current_y += 20
        
        # Visual capacity bar
        bar_width = min(200, self.detail_width - 20)
        bar_height = 8
        pygame.draw.rect(surface, (50, 50, 50), (self.detail_x, current_y, bar_width, bar_height))
        
        if container.capacity > 0:
            fill_ratio = min(used_capacity / container.capacity, 1.0)
            fill_width = int(bar_width * fill_ratio)
            fill_color = COLOR_RED if used_capacity > container.capacity else COLOR_GREEN
            pygame.draw.rect(surface, fill_color, (self.detail_x, current_y, fill_width, bar_height))
        
        current_y += 25
        
        # Contents list
        if not container.contents:
            empty_surf = self.small_font.render("(Empty)", True, (150, 150, 150))
            surface.blit(empty_surf, (self.detail_x, current_y))
        else:
            for inv_item in container.contents:
                item_name = getattr(inv_item.item, 'name', 'Unknown Item')
                quantity = getattr(inv_item, 'quantity', 1)
                
                item_text = f"• {quantity}x {item_name}"
                item_surf = self.small_font.render(item_text, True, COLOR_WHITE)
                surface.blit(item_surf, (self.detail_x, current_y))
                current_y += 18
                
                # Show item properties briefly
                if hasattr(inv_item.item, 'damage'):
                    prop_text = f"    Damage: {inv_item.item.damage}"
                    prop_surf = self.small_font.render(prop_text, True, (150, 150, 150))
                    surface.blit(prop_surf, (self.detail_x, current_y))
                    current_y += 15
                elif hasattr(inv_item.item, 'ac_bonus'):
                    prop_text = f"    AC: {inv_item.item.ac_bonus}"
                    prop_surf = self.small_font.render(prop_text, True, (150, 150, 150))
                    surface.blit(prop_surf, (self.detail_x, current_y))
                    current_y += 15
                
                current_y += 5
    
    def _draw_inventory_instructions(self, surface: pygame.Surface):
        """Draw inventory screen instructions."""
        instructions = ["UP/DOWN: Navigate containers", "ENTER: View container contents", "ESC: Back to game"]
        inst_y = self.screen_height - 60
        for instruction in instructions:
            center_text(surface, instruction, self.small_font, COLOR_WHITE, inst_y)
            inst_y += 15

class ContainerViewUI:
    """Container detailed view UI component."""
    
    def __init__(self, screen_width: int, screen_height: int, font_file: str):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fonts
        self.font = pygame.font.Font(font_file, 20)
        self.small_font = pygame.font.Font(font_file, 16)
        
        # Layout
        self.separator_x = screen_width // 3 + 30
        self.list_x = 20
        self.list_width = screen_width // 3
        self.detail_x = self.separator_x + 20
        self.detail_width = screen_width - self.detail_x - 20
        
        # State
        self.selected_index = 0
    
    def handle_navigation(self, direction: int, container: Container) -> bool:
        """Handle up/down navigation. Returns True if selection changed."""
        if container and container.contents:
            old_index = self.selected_index
            self.selected_index = (self.selected_index + direction) % len(container.contents)
            return old_index != self.selected_index
        return False
    
    def get_selected_item(self, container: Container) -> Optional[InventoryItem]:
        """Get the currently selected item."""
        if container and container.contents and 0 <= self.selected_index < len(container.contents):
            return container.contents[self.selected_index]
        return None
    
    def draw_container_view_screen(self, surface: pygame.Surface, player: Player, container: Container):
        """Draw detailed container view for item management."""
        surface.fill(COLOR_BLACK)
        
        # Title
        center_text(surface, f"Contents: {container.name}", self.font, COLOR_WHITE, 20)
        
        # Draw separator line
        draw_separator_line(surface, self.separator_x, 80, self.screen_height - 100)
        
        # Left side - item list
        y = 100
        
        if not container.contents:
            empty_surf = self.font.render("Container is empty", True, COLOR_WHITE)
            surface.blit(empty_surf, (self.list_x, y))
        else:
            for i, inv_item in enumerate(container.contents):
                # Highlight selected item
                if i == self.selected_index:
                    highlight_rect = pygame.Rect(self.list_x - 5, y - 5, self.list_width - 30, 40)
                    pygame.draw.rect(surface, COLOR_SELECTED_ITEM, highlight_rect)
                    pygame.draw.rect(surface, COLOR_WHITE, highlight_rect, 2)
                
                color = COLOR_BLACK if i == self.selected_index else COLOR_WHITE
                
                item_name = getattr(inv_item.item, 'name', 'Unknown Item')
                quantity = getattr(inv_item, 'quantity', 1)
                
                item_text = f"{quantity}x {item_name}"
                item_surf = self.font.render(item_text, True, color)
                surface.blit(item_surf, (self.list_x, y))
                y += 45
        
        # Right side - item details
        selected_item = self.get_selected_item(container)
        if selected_item:
            self.draw_item_details(surface, selected_item.item)
        
        # Container info at bottom of left side
        info_y = self.screen_height - 120
        used_capacity = container.get_used_capacity()
        capacity_text = f"Capacity: {used_capacity}/{container.capacity}"
        capacity_surf = self.small_font.render(capacity_text, True, COLOR_WHITE)
        surface.blit(capacity_surf, (self.list_x, info_y))
        
        # Instructions
        self._draw_container_view_instructions(surface)
    
    def draw_item_details(self, surface: pygame.Surface, item):
        """Draw detailed information about an item."""
        current_y = 100
        
        # Item name
        item_name = getattr(item, 'name', 'Unknown Item')
        name_surf = self.font.render(item_name, True, COLOR_WHITE)
        surface.blit(name_surf, (self.detail_x, current_y))
        current_y += 35
        
        # Item type/category
        category = getattr(item, 'category', 'General')
        category_surf = self.small_font.render(f"Category: {category}", True, (200, 200, 200))
        surface.blit(category_surf, (self.detail_x, current_y))
        current_y += 25
        
        # Weapon-specific details
        if hasattr(item, 'damage'):
            damage_surf = self.small_font.render(f"Damage: {item.damage}", True, COLOR_WHITE)
            surface.blit(damage_surf, (self.detail_x, current_y))
            current_y += 20
            
            if hasattr(item, 'weapon_properties') and item.weapon_properties:
                props_surf = self.small_font.render(f"Properties: {', '.join(item.weapon_properties)}", True, COLOR_WHITE)
                surface.blit(props_surf, (self.detail_x, current_y))
                current_y += 20
        
        # Armor-specific details
        elif hasattr(item, 'ac_bonus'):
            ac_surf = self.small_font.render(f"Armor Class: {item.ac_bonus}", True, COLOR_WHITE)
            surface.blit(ac_surf, (self.detail_x, current_y))
            current_y += 20
            
            if hasattr(item, 'armor_properties') and item.armor_properties:
                props_surf = self.small_font.render(f"Properties: {', '.join(item.armor_properties)}", True, COLOR_WHITE)
                surface.blit(props_surf, (self.detail_x, current_y))
                current_y += 20
        
        # Gear slots
        gear_slots = getattr(item, 'gear_slots', 1)
        slots_surf = self.small_font.render(f"Gear Slots: {gear_slots}", True, COLOR_WHITE)
        surface.blit(slots_surf, (self.detail_x, current_y))
        current_y += 20
        
        # Cost (if available)
        cost_text = format_item_cost(item)
        if cost_text != "Priceless":
            cost_surf = self.small_font.render(f"Value: {cost_text}", True, COLOR_GOLD)
            surface.blit(cost_surf, (self.detail_x, current_y))
            current_y += 25
        
        # Description
        description = getattr(item, 'description', '')
        if description:
            desc_lines = wrap_text(description, self.detail_width - 20, self.small_font)
            for line in desc_lines:
                line_surf = self.small_font.render(line, True, COLOR_WHITE)
                surface.blit(line_surf, (self.detail_x, current_y))
                current_y += 18
    
    def _draw_container_view_instructions(self, surface: pygame.Surface):
        """Draw container view instructions."""
        instructions = ["UP/DOWN: Navigate items", "ENTER: Item actions", "ESC: Back to containers"]
        inst_y = self.screen_height - 60
        for instruction in instructions:
            center_text(surface, instruction, self.small_font, COLOR_WHITE, inst_y)
            inst_y += 15

class ItemActionUI:
    """Item action selection UI component."""
    
    def __init__(self, screen_width: int, screen_height: int, font_file: str):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fonts
        self.font = pygame.font.Font(font_file, 20)
        self.small_font = pygame.font.Font(font_file, 16)
        
        # State
        self.selected_action = 0
        self.actions = ["Use/Consume", "Equip", "Drop Here", "Throw", "Examine"]
    
    def handle_navigation(self, direction: int) -> bool:
        """Handle up/down navigation. Returns True if selection changed."""
        old_index = self.selected_action
        self.selected_action = (self.selected_action + direction) % len(self.actions)
        return old_index != self.selected_action
    
    def get_selected_action(self) -> str:
        """Get the currently selected action."""
        return self.actions[self.selected_action]
    
    def draw_item_action_screen(self, surface: pygame.Surface, item):
        """Draw item action selection screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Action selection box
        box_width = 300
        box_height = 200
        box_x = (self.screen_width - box_width) // 2
        box_y = (self.screen_height - box_height) // 2
        
        # Background
        pygame.draw.rect(surface, COLOR_BLACK, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(surface, COLOR_WHITE, (box_x, box_y, box_width, box_height), 2)
        
        # Title
        item_name = getattr(item, 'name', 'Unknown Item')
        title_surf = self.font.render(f"Actions: {item_name}", True, COLOR_WHITE)
        title_rect = title_surf.get_rect(centerx=box_x + box_width//2, top=box_y + 10)
        surface.blit(title_surf, title_rect)
        
        # Action options
        start_y = box_y + 50
        for i, action in enumerate(self.actions):
            action_y = start_y + i * 25
            
            if i == self.selected_action:
                highlight_rect = pygame.Rect(box_x + 10, action_y - 5, box_width - 20, 20)
                pygame.draw.rect(surface, COLOR_SELECTED_ITEM, highlight_rect)
            
            color = COLOR_BLACK if i == self.selected_action else COLOR_WHITE
            action_surf = self.small_font.render(action, True, color)
            surface.blit(action_surf, (box_x + 20, action_y))
        
        # Instructions
        inst_surf = self.small_font.render("UP/DOWN: Navigate  ENTER: Select  ESC: Cancel", True, COLOR_WHITE)
        inst_rect = inst_surf.get_rect(centerx=box_x + box_width//2, bottom=box_y + box_height - 10)
        surface.blit(inst_surf, inst_rect)

class EquipmentUI:
    """Equipment management UI component."""
    
    def __init__(self, screen_width: int, screen_height: int, font_file: str):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fonts
        self.font = pygame.font.Font(font_file, 20)
        self.small_font = pygame.font.Font(font_file, 16)
        
        # Layout
        self.separator_x = screen_width // 3 + 30
        self.list_x = 20
        self.list_width = screen_width // 3
        self.detail_x = self.separator_x + 20
        self.detail_width = screen_width - self.detail_x - 20
        
        # State
        self.selected_slot = 'weapon'
        self.equipment_slots = ['weapon', 'armor', 'shield', 'light']
        self.slot_names = {
            'weapon': 'Weapon',
            'armor': 'Armor', 
            'shield': 'Shield',
            'light': 'Light Source'
        }
    
    def handle_slot_navigation(self, direction: int) -> bool:
        """Handle equipment slot navigation. Returns True if selection changed."""
        old_index = self.equipment_slots.index(self.selected_slot)
        new_index = (old_index + direction) % len(self.equipment_slots)
        old_slot = self.selected_slot
        self.selected_slot = self.equipment_slots[new_index]
        return old_slot != self.selected_slot
    
    def get_selected_slot(self) -> str:
        """Get the currently selected equipment slot."""
        return self.selected_slot
    
    def draw_equipment_screen(self, surface: pygame.Surface, player: Player):
        """Draw equipment management screen."""
        surface.fill(COLOR_BLACK)
        
        # Title
        center_text(surface, f"{player.name}'s Equipment", self.font, COLOR_WHITE, 20)
        
        # Draw separator line
        draw_separator_line(surface, self.separator_x, 80, self.screen_height - 100)
        
        # Left side - equipment slots
        y = 100
        
        for slot in self.equipment_slots:
            # Highlight selected slot
            if slot == self.selected_slot:
                highlight_rect = pygame.Rect(self.list_x - 5, y - 5, self.list_width - 30, 60)
                pygame.draw.rect(surface, COLOR_SELECTED_ITEM, highlight_rect)
                pygame.draw.rect(surface, COLOR_WHITE, highlight_rect, 2)
            
            color = COLOR_BLACK if slot == self.selected_slot else COLOR_WHITE
            
            # Slot name
            slot_surf = self.font.render(self.slot_names[slot], True, color)
            surface.blit(slot_surf, (self.list_x, y))
            
            # Equipped item
            if slot in player.equipment:
                item_name = player.equipment[slot].item.name
                item_surf = self.small_font.render(f"  {item_name}", True, color)
                surface.blit(item_surf, (self.list_x, y + 25))
            else:
                empty_surf = self.small_font.render("  (Empty)", True, (150, 150, 150))
                surface.blit(empty_surf, (self.list_x, y + 25))
            
            y += 70
        
        # Right side - item details or available equipment
        if self.selected_slot in player.equipment:
            # Show equipped item details
            equipped_item = player.equipment[self.selected_slot]
            self._draw_equipped_item_details(surface, equipped_item.item)
        else:
            # Show available items for this slot
            self._draw_available_equipment(surface, player)
        
        # Instructions
        self._draw_equipment_instructions(surface)
    
    def _draw_equipped_item_details(self, surface: pygame.Surface, item):
        """Draw details for equipped item."""
        current_y = 100
        
        # Item name
        item_name = getattr(item, 'name', 'Unknown Item')
        name_surf = self.font.render(item_name, True, COLOR_WHITE)
        surface.blit(name_surf, (self.detail_x, current_y))
        current_y += 35
        
        # Item details (same as ContainerViewUI)
        category = getattr(item, 'category', 'General')
        category_surf = self.small_font.render(f"Category: {category}", True, (200, 200, 200))
        surface.blit(category_surf, (self.detail_x, current_y))
        current_y += 25
        
        # Weapon-specific details
        if hasattr(item, 'damage'):
            damage_surf = self.small_font.render(f"Damage: {item.damage}", True, COLOR_WHITE)
            surface.blit(damage_surf, (self.detail_x, current_y))
            current_y += 20
            
            if hasattr(item, 'weapon_properties') and item.weapon_properties:
                props_surf = self.small_font.render(f"Properties: {', '.join(item.weapon_properties)}", True, COLOR_WHITE)
                surface.blit(props_surf, (self.detail_x, current_y))
                current_y += 20
        
        # Armor-specific details
        elif hasattr(item, 'ac_bonus'):
            ac_surf = self.small_font.render(f"Armor Class: {item.ac_bonus}", True, COLOR_WHITE)
            surface.blit(ac_surf, (self.detail_x, current_y))
            current_y += 20
            
            if hasattr(item, 'armor_properties') and item.armor_properties:
                props_surf = self.small_font.render(f"Properties: {', '.join(item.armor_properties)}", True, COLOR_WHITE)
                surface.blit(props_surf, (self.detail_x, current_y))
                current_y += 20
        
        # Description
        description = getattr(item, 'description', '')
        if description:
            current_y += 10
            desc_lines = wrap_text(description, self.detail_width - 20, self.small_font)
            for line in desc_lines:
                line_surf = self.small_font.render(line, True, COLOR_WHITE)
                surface.blit(line_surf, (self.detail_x, current_y))
                current_y += 18
    
    def _draw_available_equipment(self, surface: pygame.Surface, player: Player):
        """Draw available items for the selected slot."""
        # Get available items directly from player inventory
        available_items = []
        for inv_item in player.inventory:
            item_slot = get_equipment_slot(inv_item.item)
            if item_slot == self.selected_slot:
                # Check class restrictions
                can_equip = True
                if isinstance(inv_item.item, Weapon):
                    restrictions = CLASS_WEAPON_RESTRICTIONS.get(player.character_class, [])
                    if restrictions and inv_item.item.name not in restrictions:
                        can_equip = False
                elif isinstance(inv_item.item, Armor):
                    restrictions = CLASS_ARMOR_RESTRICTIONS.get(player.character_class, [])
                    if restrictions and inv_item.item.name not in restrictions:
                        can_equip = False
                
                if can_equip:
                    available_items.append(inv_item)
        
        if available_items:
            avail_title = self.small_font.render("Available to equip:", True, COLOR_WHITE)
            surface.blit(avail_title, (self.detail_x, 100))
            
            item_y = 130
            for inv_item in available_items:
                item_surf = self.small_font.render(f"• {inv_item.item.name}", True, COLOR_WHITE)
                surface.blit(item_surf, (self.detail_x, item_y))
                item_y += 20
        else:
            no_items_surf = self.small_font.render("No items available for this slot", True, (150, 150, 150))
            surface.blit(no_items_surf, (self.detail_x, 100))
            
            # Debug info to help troubleshoot
            debug_y = 130
            debug_surf = self.small_font.render(f"Debug: Total inventory items: {len(player.inventory)}", True, (100, 100, 100))
            surface.blit(debug_surf, (self.detail_x, debug_y))
            
            debug_y += 20
            debug_surf = self.small_font.render(f"Looking for slot: {self.selected_slot}", True, (100, 100, 100))
            surface.blit(debug_surf, (self.detail_x, debug_y))
            
            # Show what items we found and their slots
            debug_y += 20
            for i, inv_item in enumerate(player.inventory[:5]):  # Show first 5 items
                item_slot = get_equipment_slot(inv_item.item)
                debug_text = f"  {inv_item.item.name} -> slot: {item_slot}"
                debug_surf = self.small_font.render(debug_text, True, (100, 100, 100))
                surface.blit(debug_surf, (self.detail_x, debug_y))
                debug_y += 15
    
    def _draw_equipment_instructions(self, surface: pygame.Surface):
        """Draw equipment screen instructions."""
        instructions = ["UP/DOWN: Navigate slots", "ENTER: Change equipment", "ESC: Back to game"]
        inst_y = self.screen_height - 60
        for instruction in instructions:
            center_text(surface, instruction, self.small_font, COLOR_WHITE, inst_y)
            inst_y += 15

class EquipmentSelectionUI:
    """Equipment selection overlay UI component."""
    
    def __init__(self, screen_width: int, screen_height: int, font_file: str):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fonts
        self.font = pygame.font.Font(font_file, 20)
        self.small_font = pygame.font.Font(font_file, 16)
        
        # State
        self.selected_index = 0
    
    def handle_navigation(self, direction: int, available_items: list) -> bool:
        """Handle equipment selection navigation. Returns True if selection changed."""
        if available_items:
            old_index = self.selected_index
            self.selected_index = (self.selected_index + direction) % len(available_items)
            return old_index != self.selected_index
        return False
    
    def get_selected_item(self, available_items: list):
        """Get the currently selected item."""
        if available_items and 0 <= self.selected_index < len(available_items):
            return available_items[self.selected_index]
        return None
    
    def draw_equipment_selection(self, surface: pygame.Surface, player: Player, slot: str):
        """Show selection screen for equipment slot."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Equipment selection box
        box_width = 400
        box_height = 300
        box_x = (self.screen_width - box_width) // 2
        box_y = (self.screen_height - box_height) // 2
        
        # Background
        pygame.draw.rect(surface, COLOR_INVENTORY_BG, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(surface, COLOR_WHITE, (box_x, box_y, box_width, box_height), 2)
        
        # Title
        slot_names = {
            'weapon': 'Select Weapon',
            'armor': 'Select Armor', 
            'shield': 'Select Shield',
            'light': 'Select Light Source'
        }
        title_surf = self.font.render(slot_names.get(slot, f"Select {slot}"), True, COLOR_WHITE)
        title_rect = title_surf.get_rect(centerx=box_x + box_width//2, top=box_y + 10)
        surface.blit(title_surf, title_rect)
        
        # Get available items
        available_items = self._get_available_items_for_slot(player, slot)
        available_items.insert(0, None)  # Add "Unequip" option
        
        start_y = box_y + 50
        for i, inv_item in enumerate(available_items):
            item_y = start_y + i * 30
            
            if i == self.selected_index:
                highlight_rect = pygame.Rect(box_x + 10, item_y - 5, box_width - 20, 25)
                pygame.draw.rect(surface, COLOR_SELECTED_ITEM, highlight_rect)
            
            color = COLOR_BLACK if i == self.selected_index else COLOR_WHITE
            
            if inv_item is None:
                item_text = "(Unequip)"
            else:
                item_text = inv_item.item.name
            
            item_surf = self.small_font.render(item_text, True, color)
            surface.blit(item_surf, (box_x + 20, item_y))
        
        # Instructions
        inst_surf = self.small_font.render("UP/DOWN: Navigate  ENTER: Select  ESC: Cancel", True, COLOR_WHITE)
        inst_rect = inst_surf.get_rect(centerx=box_x + box_width//2, bottom=box_y + box_height - 10)
        surface.blit(inst_surf, inst_rect)
        
        return available_items
    
    def _get_available_items_for_slot(self, player: Player, slot: str):
        """Get inventory items that can be equipped in the given slot."""
        available = []
        print(f"\nDEBUG: Looking for items for slot '{slot}'")
        print(f"DEBUG: Player has {len(player.inventory)} items in inventory")
        
        for i, inv_item in enumerate(player.inventory):
            item_name = getattr(inv_item.item, 'name', 'Unknown')
            class_name = type(inv_item.item).__name__
            print(f"DEBUG: Item {i}: {item_name} (class: {class_name})")
            
            item_slot = get_equipment_slot(inv_item.item)
            print(f"DEBUG: get_equipment_slot returned: {item_slot}")
            
            if item_slot == slot:
                print(f"DEBUG: Slot matches! Checking class restrictions...")
                # Check class restrictions based on class name string
                can_equip = True
                
                if class_name == 'Weapon':
                    restrictions = CLASS_WEAPON_RESTRICTIONS.get(player.character_class, [])
                    if restrictions and item_name not in restrictions:
                        can_equip = False
                        print(f"DEBUG: Weapon restriction failed for {item_name}")
                elif class_name == 'Armor':
                    restrictions = CLASS_ARMOR_RESTRICTIONS.get(player.character_class, [])
                    if restrictions and item_name not in restrictions:
                        can_equip = False
                        print(f"DEBUG: Armor restriction failed for {item_name}")
                
                if can_equip:
                    print(f"DEBUG: Adding {item_name} to available items")
                    available.append(inv_item)
                else:
                    print(f"DEBUG: Cannot equip {item_name} due to class restrictions")
            else:
                print(f"DEBUG: Slot doesn't match ('{item_slot}' != '{slot}')")
        
        print(f"DEBUG: Found {len(available)} available items for slot '{slot}'")
        return available

def get_equipment_slot_debug(item) -> str:
    """Debug version of get_equipment_slot that shows what's happening."""
    print(f"Debug: Checking equipment slot for item: {getattr(item, 'name', 'Unknown')}")
    print(f"Debug: Item type: {type(item)}")
    print(f"Debug: Is Weapon? {isinstance(item, Weapon)}")
    print(f"Debug: Is Armor? {isinstance(item, Armor)}")
    
    if isinstance(item, Weapon):
        print(f"Debug: Weapon -> returning 'weapon'")
        return 'weapon'
    elif isinstance(item, Armor):
        if 'Shield' in item.name:
            print(f"Debug: Shield -> returning 'shield'")
            return 'shield'
        else:
            print(f"Debug: Armor -> returning 'armor'")
            return 'armor'
    elif hasattr(item, 'name'):
        if item.name == 'Torch':
            print(f"Debug: Torch -> returning 'light'")
            return 'light'
        elif item.name == 'Lantern':
            print(f"Debug: Lantern -> returning 'light'")
            return 'light'
    
    print(f"Debug: No slot found -> returning None")
    return None

def handle_item_action(player: Player, inv_item, action: str, dungeon_game=None) -> bool:
    """Handle item actions like equip, use, drop, etc."""
    if action == "Equip":
        slot = get_equipment_slot(inv_item.item)
        if slot and dungeon_game:
            return dungeon_game.equip_item(inv_item, slot)
        return False
    
    elif action == "Use/Consume":
        # TODO: Implement item usage
        print(f"Used {inv_item.item.name}")
        return True
    
    elif action == "Drop Here":
        # TODO: Implement item dropping
        print(f"Dropped {inv_item.item.name}")
        return True
    
    elif action == "Throw":
        # TODO: Implement item throwing
        print(f"Threw {inv_item.item.name}")
        return True
    
    elif action == "Examine":
        # TODO: Implement detailed examination
        print(f"Examined {inv_item.item.name}")
        return True
    
    return False

def organize_player_inventory(player: Player) -> List[Container]:
    """Organize player's inventory into containers for UI display."""
    return organize_inventory_into_containers(player)