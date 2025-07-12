"""
Core Dungeon Game Logic
Extracted and refactored from the original dungeon_viewer.py
"""

import random
import time
from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass
from enum import Enum

# Import from new modular structure
from config.constants import *
from data.player import Player, get_stat_modifier
from data.items import *
from data.containers import *
from game.states import GameState, TileType

@dataclass
class Monster:
    """Monster entity in the dungeon."""
    x: int
    y: int
    room_id: int

@dataclass
class Room:
    """Room in the dungeon."""
    id: int
    x: int
    y: int
    width: int
    height: int
    
    def contains_point(self, x: int, y: int) -> bool:
        """Check if point is inside this room."""
        return (self.x <= x < self.x + self.width and 
                self.y <= y < self.y + self.height)
    
    def get_cells(self) -> List[Tuple[int, int]]:
        """Get all cells in this room."""
        cells = []
        for y in range(self.y, self.y + self.height):
            for x in range(self.x, self.x + self.width):
                cells.append((x, y))
        return cells

@dataclass 
class Door:
    """Door in the dungeon."""
    x: int
    y: int
    room1_id: int
    room2_id: int
    is_horizontal: bool
    type: int
    is_open: bool = False

@dataclass
class Note:
    """Note in the dungeon."""
    x: int
    y: int
    content: str

@dataclass
class Column:
    """Column/pillar in the dungeon."""
    x: int
    y: int

@dataclass
class WaterTile:
    """Water tile in the dungeon."""
    x: int
    y: int

class DungeonGame:
    """Core dungeon game logic and state management."""
    
    def __init__(self, dungeon_data: dict, player: Player):
        self.player = player
        self.rooms: Dict[int, Room] = {}
        self.doors: List[Door] = []
        self.notes: List[Note] = []
        self.columns: List[Column] = []
        self.water_tiles: List[WaterTile] = []
        self.tiles: Dict[Tuple[int, int], TileType] = {}
        self.revealed_rooms: Set[int] = set()
        self.monsters: List[Monster] = []
        
        # Game state
        self.player_pos = (0, 0)
        self.walkable_positions: Set[Tuple[int, int]] = set()
        self.current_spell = ""
        self.spell_target_pos = (0, 0)
        
        # Parse dungeon data and setup
        self._parse_data(dungeon_data)
        self._generate_tiles()
        self._spawn_monsters()
        self._setup_starting_position()
        
        # Update player stats
        self._update_player_stats()
    
    def _parse_data(self, data: dict):
        """Parse dungeon data from JSON."""
        # Parse rooms
        for i, rect in enumerate(data['rects']):
            self.rooms[i] = Room(i, rect['x'], rect['y'], rect['w'], rect['h'])
        
        # Parse doors
        for door_data in data['doors']:
            # Find which rooms this door connects
            connected_rooms = []
            for room_id, room in self.rooms.items():
                if room.contains_point(door_data['x'], door_data['y']):
                    connected_rooms.append(room_id)
                # Check if door is adjacent to room
                elif (abs(door_data['x'] - room.x) <= 1 and room.y <= door_data['y'] < room.y + room.height) or \
                     (abs(door_data['x'] - (room.x + room.width - 1)) <= 1 and room.y <= door_data['y'] < room.y + room.height) or \
                     (abs(door_data['y'] - room.y) <= 1 and room.x <= door_data['x'] < room.x + room.width) or \
                     (abs(door_data['y'] - (room.y + room.height - 1)) <= 1 and room.x <= door_data['x'] < room.x + room.width):
                    connected_rooms.append(room_id)
            
            # Determine orientation
            is_horizontal = True
            if len(connected_rooms) >= 2:
                room1 = self.rooms[connected_rooms[0]]
                room2 = self.rooms[connected_rooms[1]]
                # If rooms are vertically adjacent, door is horizontal
                if abs(room1.y - room2.y) > abs(room1.x - room2.x):
                    is_horizontal = True
                else:
                    is_horizontal = False
            
            door = Door(
                door_data['x'], door_data['y'],
                connected_rooms[0] if len(connected_rooms) > 0 else -1,
                connected_rooms[1] if len(connected_rooms) > 1 else -1,
                is_horizontal,
                door_data.get('type', 1)
            )
            self.doors.append(door)
        
        # Parse notes
        for note_data in data['notes']:
            self.notes.append(Note(
                int(note_data['pos']['x']),
                int(note_data['pos']['y']),
                note_data.get('text', 'Note')
            ))
        
        # Parse columns/pillars
        if 'columns' in data:
            for column_data in data['columns']:
                self.columns.append(Column(
                    column_data['x'],
                    column_data['y']
                ))
        
        # Parse water tiles
        if 'water' in data:
            for water_data in data['water']:
                self.water_tiles.append(WaterTile(
                    water_data['x'],
                    water_data['y']
                ))
    
    def _generate_tiles(self):
        """Generate tile map from room and door data."""
        # Calculate bounds
        min_x = min(room.x for room in self.rooms.values()) - 3
        max_x = max(room.x + room.width for room in self.rooms.values()) + 3
        min_y = min(room.y for room in self.rooms.values()) - 3
        max_y = max(room.y + room.height for room in self.rooms.values()) + 3
        
        self.bounds = (min_x, min_y, max_x - min_x, max_y - min_y)
        
        # Initialize as void
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                self.tiles[(x, y)] = TileType.VOID
        
        # Fill rooms with floors
        for room in self.rooms.values():
            for x, y in room.get_cells():
                self.tiles[(x, y)] = TileType.FLOOR
        
        # Place doors
        for door in self.doors:
            if door.is_open:
                self.tiles[(door.x, door.y)] = TileType.DOOR_OPEN
            # Types 0 (No Door) and 2 (Open Door) are just open passages
            elif door.type in [0, 2]:
                self.tiles[(door.x, door.y)] = TileType.DOOR_OPEN
            # Types 3, 7, and 9 are stairs
            elif door.type in [3, 7, 9]:
                self.tiles[(door.x, door.y)] = TileType.STAIRS_HORIZONTAL if door.is_horizontal else TileType.STAIRS_VERTICAL
            # Type 6 is a secret door, which initially appears as a wall.
            elif door.type == 6:
                # It's treated as a floor tile, but the wall drawing logic will draw a wall over it.
                continue
            # Types 1 (Door) and 5 (Locked Door) are standard doors
            elif door.type in [1, 5]:
                self.tiles[(door.x, door.y)] = TileType.DOOR_HORIZONTAL if door.is_horizontal else TileType.DOOR_VERTICAL
        
        # Place notes
        for note in self.notes:
            if (note.x, note.y) in self.tiles:
                self.tiles[(note.x, note.y)] = TileType.NOTE
    
    def _spawn_monsters(self):
        """Spawn monsters in rooms based on random chance."""
        start_pos = self.get_starting_position()
        start_room_id = -1
        for room_id, room in self.rooms.items():
            if room.contains_point(start_pos[0], start_pos[1]):
                start_room_id = room_id
                break

        door_locations = {(d.x, d.y) for d in self.doors}

        for room_id, room in self.rooms.items():
            # Don't spawn monsters in the starting room
            if room_id == start_room_id:
                continue

            if random.randint(1, 6) <= 3:
                # Spawn a monster in a random valid cell of the room
                valid_cells = [cell for cell in room.get_cells() if cell not in door_locations]
                if valid_cells:
                    x, y = random.choice(valid_cells)
                    self.monsters.append(Monster(x=x, y=y, room_id=room_id))
    
    def _setup_starting_position(self):
        """Setup starting position and reveal initial room."""
        start_pos = self.get_starting_position()
        self.player_pos = start_pos
        
        start_room_found = False
        for room_id, room in self.rooms.items():
            if room.contains_point(start_pos[0], start_pos[1]):
                self.reveal_room(room_id)
                start_room_found = True
                break
        
        # Fallback if starting position is not in any room
        if not start_room_found and self.rooms:
             first_room_id = list(self.rooms.keys())[0]
             self.reveal_room(first_room_id)
        
        self.walkable_positions = self.get_walkable_positions()
    
    def _update_player_stats(self):
        """Update player stats based on equipment and race."""
        # Calculate AC
        self.player.ac = self._calculate_armor_class()
        
        # Update gear slots if Fighter with Constitution bonus
        if self.player.character_class == "Fighter":
            constitution_bonus = get_stat_modifier(self.player.constitution)
            if constitution_bonus > 0:
                self.player.max_gear_slots += constitution_bonus
        
        # Calculate actual gear slots used from inventory
        self.player.gear_slots_used = 0
        for inv_item in self.player.inventory:
            item_slots = getattr(inv_item.item, 'gear_slots', 1)
            if hasattr(inv_item.item, 'quantity_per_slot') and inv_item.item.quantity_per_slot > 1:
                # Items that can stack
                slots_needed = (inv_item.quantity + inv_item.item.quantity_per_slot - 1) // inv_item.item.quantity_per_slot
                self.player.gear_slots_used += slots_needed * item_slots
            else:
                self.player.gear_slots_used += item_slots * inv_item.quantity
    
    def _calculate_armor_class(self) -> int:
        """Calculate player's AC based on equipped armor."""
        base_ac = 10
        dex_modifier = get_stat_modifier(self.player.dexterity)
        
        # Check for equipped armor
        if 'armor' in self.player.equipment:
            armor_name = self.player.equipment['armor'].item.name
            if 'Leather' in armor_name:
                base_ac = 11 + dex_modifier
            elif 'Chainmail' in armor_name:
                base_ac = 13 + dex_modifier
            elif 'Plate' in armor_name:
                base_ac = 15
        else:
            # No armor, just dex bonus
            base_ac = 10 + dex_modifier
        
        # Add shield bonus
        if 'shield' in self.player.equipment:
            base_ac += 2
        
        return base_ac
    
    def get_starting_position(self) -> Tuple[int, int]:
        """Get starting position for player."""
        return (0, 0)
    
    def reveal_room(self, room_id_to_reveal: int):
        """Reveal a room and recursively reveal connected open rooms."""
        if room_id_to_reveal < 0 or room_id_to_reveal in self.revealed_rooms:
            return

        # Use a queue for a breadth-first search of connected open rooms
        queue = [room_id_to_reveal]
        
        while queue:
            current_room_id = queue.pop(0)
            
            if current_room_id in self.revealed_rooms:
                continue
                
            self.revealed_rooms.add(current_room_id)
            
            # Find all doors connected to the newly revealed room
            for door in self.doors:
                neighbor_id = -1
                if door.room1_id == current_room_id:
                    neighbor_id = door.room2_id
                elif door.room2_id == current_room_id:
                    neighbor_id = door.room1_id
                
                # If it's a valid neighbor and the door is an open type, add to queue
                if neighbor_id >= 0 and door.type in [0, 2, 3, 7, 9]:
                    if neighbor_id not in self.revealed_rooms:
                        queue.append(neighbor_id)
    
    def get_walkable_positions(self) -> Set[Tuple[int, int]]:
        """Get all positions the player can walk to."""
        walkable = set()
        
        # Define which tiles are generally passable
        passable_tiles = {
            TileType.FLOOR, TileType.DOOR_OPEN, TileType.NOTE,
            TileType.STAIRS_HORIZONTAL, TileType.STAIRS_VERTICAL,
            TileType.DOOR_HORIZONTAL, TileType.DOOR_VERTICAL
        }
        
        for pos, tile_type in self.tiles.items():
            # A tile is walkable if its type is passable AND it's in a revealed area.
            if tile_type in passable_tiles and self.is_revealed(pos[0], pos[1]):
                 walkable.add(pos)
    
        return walkable
    
    def open_door_at_position(self, x: int, y: int) -> bool:
        """Try to open a door at the given position."""
        for door in self.doors:
            if door.x == x and door.y == y and not door.is_open:
                # Regular (1), locked (5), and secret (6) doors can be "opened"
                if door.type in [1, 5, 6]:
                    door.is_open = True
                    self.tiles[(door.x, door.y)] = TileType.DOOR_OPEN
                    
                    # Reveal connected rooms, which will cascade if they lead to more open areas
                    if door.room1_id >= 0:
                        self.reveal_room(door.room1_id)
                    if door.room2_id >= 0:
                        self.reveal_room(door.room2_id)
                    
                    return True
        return False
    
    def is_revealed(self, x: int, y: int) -> bool:
        """Check if a cell at given coordinates is revealed."""        
        # Check if in revealed room
        for room_id in self.revealed_rooms:
            room = self.rooms[room_id]
            if room.contains_point(x, y):
                return True
        
        # Check if it's a door that connects to at least one revealed room
        for door in self.doors:
            if door.x == x and door.y == y:
                # Secret doors are never revealed this way
                if door.type == 6 and not door.is_open:
                    return False
                # Door is visible if either connected room is revealed
                if (door.room1_id in self.revealed_rooms or 
                    door.room2_id in self.revealed_rooms):
                    return True
        
        return False
    
    def handle_player_movement(self, direction: Tuple[int, int]) -> bool:
        """Handle player movement in a direction. Returns True if moved."""
        next_pos = (self.player_pos[0] + direction[0], self.player_pos[1] + direction[1])
        
        if next_pos in self.walkable_positions:
            self.player_pos = next_pos
            
            # Auto-open regular/locked doors on move
            tile_at_pos = self.tiles.get(self.player_pos)
            if tile_at_pos in [TileType.DOOR_HORIZONTAL, TileType.DOOR_VERTICAL]:
                 if self.open_door_at_position(self.player_pos[0], self.player_pos[1]):
                    self.walkable_positions = self.get_walkable_positions()
            
            # Handle monster turns
            self._handle_monster_turns()
            
            return True
        
        return False
    
    def handle_door_interaction(self) -> bool:
        """Try to open doors around the player. Returns True if a door was opened."""
        for dx, dy in [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]:
            if self.open_door_at_position(self.player_pos[0] + dx, self.player_pos[1] + dy):
                self.walkable_positions = self.get_walkable_positions()
                return True
        return False
    
    def _handle_monster_turns(self):
        """Handle monster AI turns."""
        occupied_tiles = {(m.x, m.y) for m in self.monsters}
        occupied_tiles.add(self.player_pos)
        monster_walkable = self.get_walkable_positions()

        for monster in self.monsters:
            if monster.room_id in self.revealed_rooms:
                dx = self.player_pos[0] - monster.x
                dy = self.player_pos[1] - monster.y
                
                # Move monster one step closer to player
                next_monster_pos = monster.x, monster.y
                if abs(dx) > abs(dy):
                    next_monster_pos = (monster.x + (1 if dx > 0 else -1), monster.y)
                else:
                    next_monster_pos = (monster.x, monster.y + (1 if dy > 0 else -1))
                
                if next_monster_pos in monster_walkable and next_monster_pos not in occupied_tiles:
                    monster.x, monster.y = next_monster_pos
    
    def handle_spell_casting(self, spell_name: str, target_pos: Tuple[int, int]):
        """Handle casting a spell at a target position."""
        # Validate spell range
        if not self._is_valid_spell_target(target_pos, spell_name):
            return False
        
        # Cast the spell (implement spell effects here)
        print(f"Casting {spell_name} at {target_pos}!")
        
        # TODO: Implement actual spell effects
        
        return True
    
    def _is_valid_spell_target(self, target_pos: Tuple[int, int], spell_name: str) -> bool:
        """Check if spell target is within range."""
        max_range = self._get_spell_range_in_cells(spell_name)
        distance = max(abs(target_pos[0] - self.player_pos[0]), 
                       abs(target_pos[1] - self.player_pos[1]))
        return distance <= max_range
    
    def _get_spell_range_in_cells(self, spell_name: str) -> int:
        """Convert spell ranges to grid cells (5 feet per cell)."""
        # Based on the gear document: close=5ft, near=30ft, far=sight
        if spell_name in ["Cure Wounds", "Holy Weapon", "Light", "Protection From Evil", 
                          "Burning Hands", "Detect Magic", "Hold Portal", "Mage Armor", "Alarm"]:
            return 1  # Close range (5 feet = 1 cell)
        elif spell_name in ["Turn Undead", "Charm Person", "Floating Disk", "Sleep"]:
            return 6  # Near range (30 feet = 6 cells)
        elif spell_name in ["Magic Missile"]:
            return 20  # Far range (within sight, limited for gameplay)
        else:
            return 1  # Default to close range
    
    def handle_spell_targeting_movement(self, direction: Tuple[int, int], spell_name: str) -> bool:
        """Handle spell targeting cursor movement. Returns True if moved."""
        new_target = (self.spell_target_pos[0] + direction[0], self.spell_target_pos[1] + direction[1])
        if self._is_valid_spell_target(new_target, spell_name):
            self.spell_target_pos = new_target
            return True
        return False
    
    def get_equipped_weapon_damage(self) -> str:
        """Get damage of equipped weapon."""
        if 'weapon' in self.player.equipment:
            weapon = self.player.equipment['weapon'].item
            if hasattr(weapon, 'damage'):
                return weapon.damage
        return "1d4"  # Unarmed damage
    
    def can_equip_item(self, item) -> bool:
        """Check if player can equip an item based on class restrictions."""
        if isinstance(item, Weapon):
            restrictions = CLASS_WEAPON_RESTRICTIONS.get(self.player.character_class, [])
            if restrictions and item.name not in restrictions:
                return False
        elif isinstance(item, Armor):
            restrictions = CLASS_ARMOR_RESTRICTIONS.get(self.player.character_class, [])
            if restrictions and item.name not in restrictions:
                return False
        
        return True
    
    def equip_item(self, inv_item, slot: str = None) -> bool:
        """Equip an item to the appropriate slot."""
        if slot is None:
            slot = get_equipment_slot(inv_item.item)
        
        if slot and self.can_equip_item(inv_item.item):
            # Unequip current item in slot if any
            if slot in self.player.equipment:
                self.unequip_item(slot)
            
            # Equip new item
            self.player.equipment[slot] = inv_item
            
            # Update AC if armor/shield equipped
            if slot in ['armor', 'shield']:
                self.player.ac = self._calculate_armor_class()
            
            return True
        return False
    
    def unequip_item(self, slot: str) -> bool:
        """Unequip an item from the given slot."""
        if slot in self.player.equipment:
            del self.player.equipment[slot]
            
            # Update AC if armor/shield unequipped
            if slot in ['armor', 'shield']:
                self.player.ac = self._calculate_armor_class()
            
            return True
        return False
    
    def get_available_items_for_slot(self, slot: str):
        """Get inventory items that can be equipped in the given slot."""
        available = []
        for inv_item in self.player.inventory:
            item_slot = get_equipment_slot(inv_item.item)
            if item_slot == slot and self.can_equip_item(inv_item.item):
                available.append(inv_item)
        return available
    
    def update_light_timer(self):
        """Update the torch/light timer."""
        # This is handled in the UI drawing, but we could add logic here
        # for when light runs out
        time_left = max(0, self.player.light_duration - (time.time() - self.player.light_start_time))
        if time_left <= 0:
            # Handle torch running out
            pass
    
    def get_player_position(self) -> Tuple[int, int]:
        """Get current player position."""
        return self.player_pos
    
    def get_monsters_in_room(self, room_id: int) -> List[Monster]:
        """Get all monsters in a specific room."""
        return [m for m in self.monsters if m.room_id == room_id]
    
    def get_visible_monsters(self) -> List[Monster]:
        """Get all monsters in revealed areas."""
        return [m for m in self.monsters if self.is_revealed(m.x, m.y)]
    
    def get_notes_at_position(self, x: int, y: int) -> List[Note]:
        """Get notes at a specific position."""
        return [note for note in self.notes if note.x == x and note.y == y]
    
    def get_dungeon_bounds(self) -> Tuple[int, int, int, int]:
        """Get dungeon bounds (x, y, width, height)."""
        return self.bounds if hasattr(self, 'bounds') else (0, 0, 10, 10)
    
    def save_game_state(self) -> dict:
        """Save current game state to a dictionary."""
        return {
            'player_pos': self.player_pos,
            'revealed_rooms': list(self.revealed_rooms),
            'monsters': [(m.x, m.y, m.room_id) for m in self.monsters],
            'opened_doors': [(d.x, d.y) for d in self.doors if d.is_open],
            'player_data': {
                'name': self.player.name,
                'hp': self.player.hp,
                'xp': self.player.xp,
                'gold': self.player.gold,
                'inventory': [(item.item.name, item.quantity) for item in self.player.inventory],
                'equipment': {slot: item.item.name for slot, item in self.player.equipment.items()}
            }
        }
    
    def load_game_state(self, state_data: dict):
        """Load game state from a dictionary."""
        if 'player_pos' in state_data:
            self.player_pos = tuple(state_data['player_pos'])
        
        if 'revealed_rooms' in state_data:
            self.revealed_rooms = set(state_data['revealed_rooms'])
        
        if 'monsters' in state_data:
            self.monsters = [Monster(x, y, room_id) for x, y, room_id in state_data['monsters']]
        
        if 'opened_doors' in state_data:
            for door_x, door_y in state_data['opened_doors']:
                for door in self.doors:
                    if door.x == door_x and door.y == door_y:
                        door.is_open = True
                        self.tiles[(door.x, door.y)] = TileType.DOOR_OPEN
        
        # Recalculate walkable positions
        self.walkable_positions = self.get_walkable_positions()
    
    def get_game_statistics(self) -> dict:
        """Get various game statistics."""
        return {
            'rooms_discovered': len(self.revealed_rooms),
            'total_rooms': len(self.rooms),
            'monsters_remaining': len(self.monsters),
            'doors_opened': len([d for d in self.doors if d.is_open]),
            'total_doors': len(self.doors),
            'exploration_percentage': (len(self.revealed_rooms) / len(self.rooms)) * 100 if self.rooms else 0
        }