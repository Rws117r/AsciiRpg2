"""
Tile Rendering System
Extracted and refactored from the original dungeon_viewer.py
"""

import pygame
from typing import List, Tuple, Set, Dict
import random

# Import from new modular structure
from config.constants import *
from game.states import TileType

class TileRenderer:
    """Handles rendering of dungeon tiles and terrain features."""
    
    def __init__(self):
        pass
    
    def draw_tile(self, surface: pygame.Surface, tile_type: TileType, x: int, y: int, cell_size: int):
        """Draw a single tile at the specified grid position."""
        left = x * cell_size
        top = y * cell_size
        center_x = left + cell_size // 2
        center_y = top + cell_size // 2
        
        if tile_type == TileType.VOID:
            pygame.draw.rect(surface, COLOR_VOID, (left, top, cell_size, cell_size))
        
        elif tile_type == TileType.FLOOR or tile_type == TileType.DOOR_OPEN:
            # Draw cream floor for floor, open doors, and passages
            pygame.draw.rect(surface, COLOR_FLOOR, (left, top, cell_size, cell_size))
            self._draw_floor_grid(surface, left, top, cell_size)
        
        elif tile_type in [TileType.DOOR_HORIZONTAL, TileType.DOOR_VERTICAL]:
            # Draw floor base
            pygame.draw.rect(surface, COLOR_FLOOR, (left, top, cell_size, cell_size))
            self._draw_floor_grid(surface, left, top, cell_size)
            
            # The outline thickness is 1 to match the floor grid
            outline_thickness = 1
            
            if tile_type == TileType.DOOR_HORIZONTAL:
                door_width = int(cell_size * 0.8)
                door_height = int(cell_size * 0.3)
                door_rect = pygame.Rect(center_x - door_width // 2, center_y - door_height // 2, door_width, door_height)
            else: # DOOR_VERTICAL
                door_width = int(cell_size * 0.3)
                door_height = int(cell_size * 0.8)
                door_rect = pygame.Rect(center_x - door_width // 2, center_y - door_height // 2, door_width, door_height)

            # Draw the filled interior of the door
            pygame.draw.rect(surface, COLOR_DOOR, door_rect)
            # Draw the black outline
            pygame.draw.rect(surface, COLOR_WALL, door_rect, width=outline_thickness)

        elif tile_type in [TileType.STAIRS_HORIZONTAL, TileType.STAIRS_VERTICAL]:
            # Draw floor base
            pygame.draw.rect(surface, COLOR_FLOOR, (left, top, cell_size, cell_size))
            self._draw_floor_grid(surface, left, top, cell_size)

            line_thickness = 1
            line_color = COLOR_FLOOR_GRID # Match grid color for subtle effect

            if tile_type == TileType.STAIRS_HORIZONTAL:
                # 3 horizontal lines for stairs in a vertical hallway
                spacing = cell_size // 4
                y1 = top + spacing
                y2 = top + 2 * spacing
                y3 = top + 3 * spacing
                pygame.draw.line(surface, line_color, (left, y1), (left + cell_size, y1), line_thickness)
                pygame.draw.line(surface, line_color, (left, y2), (left + cell_size, y2), line_thickness)
                pygame.draw.line(surface, line_color, (left, y3), (left + cell_size, y3), line_thickness)
            else: # STAIRS_VERTICAL
                # 3 vertical lines for stairs in a horizontal hallway
                spacing = cell_size // 4
                x1 = left + spacing
                x2 = left + 2 * spacing
                x3 = left + 3 * spacing
                pygame.draw.line(surface, line_color, (x1, top), (x1, top + cell_size), line_thickness)
                pygame.draw.line(surface, line_color, (x2, top), (x2, top + cell_size), line_thickness)
                pygame.draw.line(surface, line_color, (x3, top), (x3, top + cell_size), line_thickness)

        elif tile_type == TileType.NOTE:
            # Draw cream floor
            pygame.draw.rect(surface, COLOR_FLOOR, (left, top, cell_size, cell_size))
            # Draw grid on floor
            self._draw_floor_grid(surface, left, top, cell_size)
            # Note indicator (could be enhanced with better graphics)
            note_size = max(2, cell_size // 8)
            note_rect = pygame.Rect(center_x - note_size//2, center_y - note_size//2, note_size, note_size)
            pygame.draw.rect(surface, COLOR_NOTE, note_rect)

    def _draw_floor_grid(self, surface: pygame.Surface, left: int, top: int, cell_size: int):
        """Draw a grid pattern that aligns with character movement."""
        # Very thin lines for the grid
        line_thickness = 1
        
        # The grid should match the cell_size used for character movement
        # Each character movement cell should have its own grid square
        grid_spacing = cell_size  # One grid square = one movement cell
        
        # Draw vertical grid lines at cell boundaries
        # Start from the left edge and draw lines at cell_size intervals
        x = left
        while x <= left + cell_size:
            pygame.draw.line(surface, COLOR_FLOOR_GRID, 
                            (x, top), (x, top + cell_size), line_thickness)
            x += grid_spacing
        
        # Draw horizontal grid lines at cell boundaries
        y = top
        while y <= top + cell_size:
            pygame.draw.line(surface, COLOR_FLOOR_GRID,
                            (left, y), (left + cell_size, y), line_thickness)
            y += grid_spacing

class WallRenderer:
    """Handles rendering of dungeon walls and boundaries."""
    
    def __init__(self):
        pass
    
    def draw_boundary_walls(self, surface: pygame.Surface, dungeon, 
                           viewport_x: int, viewport_y: int, cell_size: int,
                           viewport_width_cells: int, viewport_height_cells: int):
        """Draw walls around the perimeter of revealed areas with drop shadow effect."""
        # Make walls much thicker for the hand-drawn aesthetic
        line_thickness = max(4, cell_size // 4)  # Much thicker walls
        shadow_offset = max(2, cell_size // 12)  # Drop shadow offset
        
        # Get all revealed cells  
        revealed_cells = self._get_revealed_cells(dungeon)
        
        if not revealed_cells:
            return
        
        # Pre-calculate secret door locations for faster lookup
        secret_horizontal_doors = {(d.x, d.y) for d in dungeon.doors if d.type == 6 and d.is_horizontal and not d.is_open}
        secret_vertical_doors = {(d.x, d.y) for d in dungeon.doors if d.type == 6 and not d.is_horizontal and not d.is_open}
        
        # Collect all wall segments for both shadow and main walls
        wall_segments = self._collect_wall_segments(
            revealed_cells, secret_horizontal_doors, secret_vertical_doors,
            viewport_x, viewport_y, viewport_width_cells, viewport_height_cells, cell_size
        )
        
        # Extend line segments to fill corners properly
        extended_segments = self._extend_wall_segments(wall_segments, line_thickness)
        
        # Draw drop shadows first (offset down and right)
        for start_pos, end_pos in extended_segments:
            shadow_start = (start_pos[0] + shadow_offset, start_pos[1] + shadow_offset)
            shadow_end = (end_pos[0] + shadow_offset, end_pos[1] + shadow_offset)
            pygame.draw.line(surface, COLOR_WALL_SHADOW, shadow_start, shadow_end, line_thickness)
        
        # Draw main black walls on top
        for start_pos, end_pos in extended_segments:
            pygame.draw.line(surface, COLOR_WALL, start_pos, end_pos, line_thickness)
    
    def _get_revealed_cells(self, dungeon) -> Set[Tuple[int, int]]:
        """Get all revealed cells including rooms and doors."""
        revealed_cells = set()
        
        # Add revealed room cells
        for room_id in dungeon.revealed_rooms:
            room = dungeon.rooms[room_id]
            for x, y in room.get_cells():
                revealed_cells.add((x, y))
        
        # Also add revealed doors (only if they connect to revealed rooms)
        for door in dungeon.doors:
            # Do not add secret doors to revealed cells for wall drawing purposes
            if door.type == 6 and not door.is_open:
                continue
            if (door.room1_id in dungeon.revealed_rooms or 
                door.room2_id in dungeon.revealed_rooms):
                revealed_cells.add((door.x, door.y))
        
        return revealed_cells
    
    def _collect_wall_segments(self, revealed_cells: Set[Tuple[int, int]], 
                              secret_horizontal_doors: Set[Tuple[int, int]],
                              secret_vertical_doors: Set[Tuple[int, int]],
                              viewport_x: int, viewport_y: int, 
                              viewport_width_cells: int, viewport_height_cells: int,
                              cell_size: int) -> List[Tuple[str, Tuple[int, int], Tuple[int, int]]]:
        """Collect all wall segments that need to be drawn."""
        wall_segments = []
        
        # For each revealed cell, check if it's on the boundary and collect wall segments
        for cell_x, cell_y in revealed_cells:
            # Check if this cell is within viewport bounds (with some margin)
            if (cell_x < viewport_x - 1 or cell_x > viewport_x + viewport_width_cells + 1 or
                cell_y < viewport_y - 1 or cell_y > viewport_y + viewport_height_cells + 1):
                continue
            
            # Convert to screen coordinates
            screen_x = (cell_x - viewport_x) * cell_size
            screen_y = (cell_y - viewport_y) * cell_size
            
            # Check each direction for boundaries and collect wall segments
            # Bottom wall (of current cell)
            if (cell_x, cell_y + 1) not in revealed_cells or (cell_x, cell_y + 1) in secret_horizontal_doors:
                start_pos = (screen_x, screen_y + cell_size)
                end_pos = (screen_x + cell_size, screen_y + cell_size)
                wall_segments.append(('horizontal', start_pos, end_pos))
            
            # Top wall (of current cell)
            if (cell_x, cell_y - 1) not in revealed_cells or (cell_x, cell_y) in secret_horizontal_doors:
                start_pos = (screen_x, screen_y)
                end_pos = (screen_x + cell_size, screen_y)
                wall_segments.append(('horizontal', start_pos, end_pos))
            
            # Right wall (of current cell)
            if (cell_x + 1, cell_y) not in revealed_cells or (cell_x + 1, cell_y) in secret_vertical_doors:
                start_pos = (screen_x + cell_size, screen_y)
                end_pos = (screen_x + cell_size, screen_y + cell_size)
                wall_segments.append(('vertical', start_pos, end_pos))
            
            # Left wall (of current cell)
            if (cell_x - 1, cell_y) not in revealed_cells or (cell_x, cell_y) in secret_vertical_doors:
                start_pos = (screen_x, screen_y)
                end_pos = (screen_x, screen_y + cell_size)
                wall_segments.append(('vertical', start_pos, end_pos))
        
        return wall_segments
    
    def _extend_wall_segments(self, wall_segments: List[Tuple[str, Tuple[int, int], Tuple[int, int]]], 
                             line_thickness: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Extend line segments to fill corners properly."""
        extended_segments = []
        half_thickness = line_thickness // 2
        
        for orientation, start_pos, end_pos in wall_segments:
            if orientation == 'horizontal':
                # Extend horizontal lines left and right by half thickness
                extended_start = (start_pos[0] - half_thickness, start_pos[1])
                extended_end = (end_pos[0] + half_thickness, end_pos[1])
            else:  # vertical
                # Extend vertical lines up and down by half thickness
                extended_start = (start_pos[0], start_pos[1] - half_thickness)
                extended_end = (end_pos[0], end_pos[1] + half_thickness)
            
            extended_segments.append((extended_start, extended_end))
        
        return extended_segments

class TerrainRenderer:
    """Handles rendering of terrain features like water and columns."""
    
    def __init__(self):
        pass
    
    def draw_terrain_features(self, surface: pygame.Surface, dungeon,
                             viewport_x: int, viewport_y: int, cell_size: int):
        """Draw water and other terrain features with organic polygon shapes."""
        
        # Collect all visible water tiles
        visible_water = []
        for water in dungeon.water_tiles:
            if dungeon.is_revealed(water.x, water.y):
                screen_x = (water.x - viewport_x) * cell_size
                screen_y = (water.y - viewport_y) * cell_size
                
                # Only include if roughly in viewport (with margin for blob effects)
                if (screen_x > -cell_size * 2 and screen_x < surface.get_width() + cell_size * 2 and
                    screen_y > -cell_size * 2 and screen_y < surface.get_height() + cell_size * 2):
                    visible_water.append((screen_x + cell_size // 2, screen_y + cell_size // 2, water.x, water.y))
        
        if not visible_water:
            return
        
        # Group connected water tiles into clusters
        water_clusters = self._group_water_clusters(visible_water, cell_size)
        
        # Draw each cluster as an organic polygon
        for cluster in water_clusters:
            if len(cluster) >= 3:  # Need at least 3 points for a polygon
                self._draw_organic_water_polygon(surface, cluster, cell_size)
            elif len(cluster) == 2:  # Draw connecting blob for 2 points
                self._draw_water_connection(surface, cluster, cell_size)
            else:  # Single water tile
                self._draw_single_water_blob(surface, cluster[0], cell_size)
    
    def _group_water_clusters(self, water_positions: list, cell_size: int):
        """Group nearby water tiles into connected clusters."""
        clusters = []
        unprocessed = water_positions.copy()
        
        while unprocessed:
            # Start new cluster with first unprocessed point
            current_cluster = [unprocessed.pop(0)]
            cluster_changed = True
            
            # Keep adding connected points until no more can be added
            while cluster_changed:
                cluster_changed = False
                to_remove = []
                
                for i, point in enumerate(unprocessed):
                    # Check if this point is adjacent to any point in current cluster
                    for cluster_point in current_cluster:
                        world_dist = max(abs(point[2] - cluster_point[2]), abs(point[3] - cluster_point[3]))
                        if world_dist <= 1.5:  # Adjacent or diagonal (allowing some tolerance)
                            current_cluster.append(point)
                            to_remove.append(i)
                            cluster_changed = True
                            break
                    if cluster_changed:
                        break
                
                # Remove processed points (in reverse order to maintain indices)
                for i in reversed(to_remove):
                    unprocessed.pop(i)
            
            clusters.append(current_cluster)
        
        return clusters

    def _draw_organic_water_polygon(self, surface: pygame.Surface, cluster: list, cell_size: int):
        """Draw an organic polygon for a cluster of water tiles."""
        if len(cluster) < 3:
            return
        
        # Create organic boundary points around the cluster
        boundary_points = self._create_organic_boundary(cluster, cell_size)
        
        if len(boundary_points) >= 3:
            # Draw the main water polygon
            pygame.draw.polygon(surface, COLOR_WATER, boundary_points)
            
            # Draw border for depth effect
            border_points = self._create_organic_boundary(cluster, cell_size, border_offset=3)
            if len(border_points) >= 3:
                pygame.draw.polygon(surface, (80, 120, 160), border_points, 2)

    def _create_organic_boundary(self, cluster: list, cell_size: int, border_offset: int = 0):
        """Create organic boundary points around a water cluster using convex hull with organic modifications."""
        if len(cluster) < 3:
            return []
        
        # Extract screen coordinates
        points = [(point[0], point[1]) for point in cluster]
        
        # Calculate the center of the cluster
        center_x = sum(p[0] for p in points) / len(points)
        center_y = sum(p[1] for p in points) / len(points)
        
        # Sort points by angle from center to create a rough hull
        def angle_from_center(point):
            import math
            return math.atan2(point[1] - center_y, point[0] - center_x)
        
        sorted_points = sorted(points, key=angle_from_center)
        
        # Create organic boundary by expanding points outward and adding smoothing
        boundary_points = []
        expansion = cell_size * 0.4 + border_offset  # How much to expand outward
        
        for i, (x, y) in enumerate(sorted_points):
            # Calculate direction from center to this point
            dx = x - center_x
            dy = y - center_y
            dist = (dx * dx + dy * dy) ** 0.5
            
            if dist > 0:
                # Normalize and expand
                nx = dx / dist
                ny = dy / dist
                
                # Add organic variation
                variation = 0.3 + 0.2 * abs((i % 3) - 1)  # Varies between 0.1 and 0.5
                expand_dist = expansion * variation
                
                new_x = x + nx * expand_dist
                new_y = y + ny * expand_dist
                boundary_points.append((int(new_x), int(new_y)))
        
        # Add intermediate points for smoother curves
        smooth_boundary = []
        for i in range(len(boundary_points)):
            current = boundary_points[i]
            next_point = boundary_points[(i + 1) % len(boundary_points)]
            
            smooth_boundary.append(current)
            
            # Add intermediate point for smoother curves
            mid_x = (current[0] + next_point[0]) // 2
            mid_y = (current[1] + next_point[1]) // 2
            smooth_boundary.append((mid_x, mid_y))
        
        return smooth_boundary

    def _draw_water_connection(self, surface: pygame.Surface, cluster: list, cell_size: int):
        """Draw connection between two water tiles."""
        if len(cluster) != 2:
            return
        
        point1, point2 = cluster[0], cluster[1]
        
        # Calculate connection parameters
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        dist = (dx * dx + dy * dy) ** 0.5
        
        if dist > 0:
            # Create capsule-like shape
            radius = cell_size * 0.35
            
            # Draw circles at endpoints
            pygame.draw.circle(surface, COLOR_WATER, (point1[0], point1[1]), int(radius))
            pygame.draw.circle(surface, COLOR_WATER, (point2[0], point2[1]), int(radius))
            
            # Draw connecting rectangle
            if dist > radius:
                # Calculate perpendicular vector for rectangle width
                perp_x = -dy / dist * radius
                perp_y = dx / dist * radius
                
                rect_points = [
                    (point1[0] + perp_x, point1[1] + perp_y),
                    (point1[0] - perp_x, point1[1] - perp_y),
                    (point2[0] - perp_x, point2[1] - perp_y),
                    (point2[0] + perp_x, point2[1] + perp_y)
                ]
                pygame.draw.polygon(surface, COLOR_WATER, rect_points)

    def _draw_single_water_blob(self, surface: pygame.Surface, point, cell_size: int):
        """Draw a single organic water blob."""
        x, y = point[0], point[1]
        radius = int(cell_size * 0.4)
        
        # Draw main blob
        pygame.draw.circle(surface, COLOR_WATER, (x, y), radius)
        
        # Draw border
        pygame.draw.circle(surface, (80, 120, 160), (x, y), radius, 2)

class EntityRenderer:
    """Handles rendering of game entities like players, monsters, and items."""
    
    def __init__(self):
        pass
    
    def draw_player(self, surface: pygame.Surface, player_pos: Tuple[int, int], 
                   viewport_x: int, viewport_y: int, cell_size: int, 
                   viewport_width_cells: int, viewport_height_cells: int, font: pygame.font.Font):
        """Draw the player character."""
        player_screen_x = (viewport_width_cells // 2) * cell_size + (cell_size // 2)
        player_screen_y = (viewport_height_cells // 2) * cell_size + (cell_size // 2)
        
        player_surf = font.render('@', True, COLOR_PLAYER)
        player_rect = player_surf.get_rect(center=(player_screen_x, player_screen_y))
        surface.blit(player_surf, player_rect)
    
    def draw_monsters(self, surface: pygame.Surface, monsters: List, dungeon,
                     viewport_x: int, viewport_y: int, cell_size: int, font: pygame.font.Font):
        """Draw all visible monsters."""
        for monster in monsters:
            if dungeon.is_revealed(monster.x, monster.y):
                monster_screen_x = (monster.x - viewport_x) * cell_size + (cell_size // 2)
                monster_screen_y = (monster.y - viewport_y) * cell_size + (cell_size // 2)
                monster_surf = font.render(UI_ICONS["MONSTER"], True, COLOR_MONSTER)
                monster_rect = monster_surf.get_rect(center=(monster_screen_x, monster_screen_y))
                surface.blit(monster_surf, monster_rect)
    
    def draw_spell_cursor(self, surface: pygame.Surface, spell_target_pos: Tuple[int, int],
                         viewport_x: int, viewport_y: int, cell_size: int, font: pygame.font.Font):
        """Draw the spell targeting cursor."""
        cursor_screen_x = (spell_target_pos[0] - viewport_x) * cell_size + (cell_size // 2)
        cursor_screen_y = (spell_target_pos[1] - viewport_y) * cell_size + (cell_size // 2)
        cursor_surf = font.render(UI_ICONS["SPELL_CURSOR"], True, COLOR_SPELL_CURSOR)
        cursor_rect = cursor_surf.get_rect(center=(cursor_screen_x, cursor_screen_y))
        surface.blit(cursor_surf, cursor_rect)
    
    def draw_spell_range_indicator(self, surface: pygame.Surface, player_pos: Tuple[int, int], 
                                  spell_name: str, viewport_x: int, viewport_y: int, 
                                  cell_size: int, viewport_width_cells: int, viewport_height_cells: int):
        """Draw spell range indicator around player."""
        max_range = self._get_spell_range_in_cells(spell_name)
        player_screen_x = (viewport_width_cells // 2) * cell_size + (cell_size // 2)
        player_screen_y = (viewport_height_cells // 2) * cell_size + (cell_size // 2)
        
        # Create transparent surface for range indicator
        range_size = max_range * cell_size
        if range_size > 0:
            range_surface = pygame.Surface((range_size * 2, range_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (255, 255, 0, 50), 
                              (range_size, range_size), range_size)
            
            range_rect = (player_screen_x - range_size, player_screen_y - range_size)
            surface.blit(range_surface, range_rect)
    
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

class DungeonRenderer:
    """Main renderer that coordinates all rendering systems."""
    
    def __init__(self):
        self.tile_renderer = TileRenderer()
        self.wall_renderer = WallRenderer()
        self.terrain_renderer = TerrainRenderer()
        self.entity_renderer = EntityRenderer()
    
    def render_viewport(self, surface: pygame.Surface, dungeon, player_pos: Tuple[int, int],
                       viewport_x: int, viewport_y: int, cell_size: int,
                       viewport_width_cells: int, viewport_height_cells: int,
                       game_state, spell_target_pos: Tuple[int, int], current_spell: str,
                       player_font: pygame.font.Font, spell_cursor_font: pygame.font.Font):
        """Render the entire dungeon viewport."""
        
        # Clear viewport
        surface.fill(COLOR_BG)
        
        # Draw tiles
        for screen_cell_y in range(viewport_height_cells + 2):
            for screen_cell_x in range(viewport_width_cells + 2):
                world_x = viewport_x + screen_cell_x
                world_y = viewport_y + screen_cell_y
                
                tile_type = dungeon.tiles.get((world_x, world_y), TileType.VOID)
                
                # Check visibility - fog of war rules
                if dungeon.is_revealed(world_x, world_y):
                    self.tile_renderer.draw_tile(surface, tile_type, screen_cell_x, screen_cell_y, cell_size)
        
        # Draw terrain features (water) on top of tiles but under walls
        self.terrain_renderer.draw_terrain_features(surface, dungeon, viewport_x, viewport_y, cell_size)
        
        # Draw walls using proper marching squares
        self.wall_renderer.draw_boundary_walls(surface, dungeon, viewport_x, viewport_y, cell_size, viewport_width_cells, viewport_height_cells)
        
        # Draw spell range indicator if targeting
        from game.states import GameState  # Import here to avoid circular import
        if game_state == GameState.SPELL_TARGETING:
            self.entity_renderer.draw_spell_range_indicator(surface, player_pos, current_spell, viewport_x, viewport_y, cell_size, viewport_width_cells, viewport_height_cells)
        
        # Draw monsters
        self.entity_renderer.draw_monsters(surface, dungeon.monsters, dungeon, viewport_x, viewport_y, cell_size, player_font)
        
        # Draw player
        self.entity_renderer.draw_player(surface, player_pos, viewport_x, viewport_y, cell_size, viewport_width_cells, viewport_height_cells, player_font)
        
        # Draw spell cursor if targeting
        if game_state == GameState.SPELL_TARGETING:
            self.entity_renderer.draw_spell_cursor(surface, spell_target_pos, viewport_x, viewport_y, cell_size, spell_cursor_font)
    
    def render_coordinates(self, surface: pygame.Surface, player_pos: Tuple[int, int], font: pygame.font.Font):
        """Render coordinate display."""
        coord_text = f"({player_pos[0]}, {player_pos[1]})"
        coord_surf = font.render(coord_text, True, COLOR_WALL)
        surface.blit(coord_surf, (10, 10))
    
    def render_timer_box(self, surface: pygame.Surface, player, font: pygame.font.Font):
        """Render the torch timer in its own box in the top right corner."""
        import time
        
        margin = 10
        screen_width, _ = surface.get_size()
        
        time_left = max(0, player.light_duration - (time.time() - player.light_start_time))
        minutes, seconds = divmod(int(time_left), 60)
        light_text = f'{UI_ICONS["SUN"]} {minutes:02d}:{seconds:02d}'
        
        light_surf = font.render(light_text, True, COLOR_TORCH_ICON)
        
        box_width = light_surf.get_width() + 20
        box_height = light_surf.get_height() + 10
        
        box_rect = pygame.Rect(screen_width - box_width - margin, margin, box_width, box_height)
        pygame.draw.rect(surface, COLOR_BLACK, box_rect)
        
        inner_rect = box_rect.inflate(-4, -4)
        pygame.draw.rect(surface, COLOR_WHITE, inner_rect, 1)
        
        light_rect = light_surf.get_rect(center=box_rect.center)
        surface.blit(light_surf, light_rect)

# Utility functions for rendering

def calculate_viewport_parameters(screen_width: int, screen_height: int, hud_height: int, 
                                 player_pos: Tuple[int, int], zoom_level: float) -> Dict:
    """Calculate viewport parameters for rendering."""
    cell_size = int(BASE_CELL_SIZE * zoom_level)
    game_area_height = screen_height - hud_height
    
    # Calculate viewport to fill entire screen
    viewport_width_cells = (screen_width + cell_size - 1) // cell_size  # Round up
    viewport_height_cells = (game_area_height + cell_size - 1) // cell_size  # Round up
    
    # Center viewport on player
    viewport_x = player_pos[0] - viewport_width_cells // 2
    viewport_y = player_pos[1] - viewport_height_cells // 2
    
    return {
        'cell_size': cell_size,
        'viewport_width_cells': viewport_width_cells,
        'viewport_height_cells': viewport_height_cells,
        'viewport_x': viewport_x,
        'viewport_y': viewport_y,
        'game_area_width': screen_width,
        'game_area_height': game_area_height
    }

def create_fonts_for_zoom(font_file: str, zoom_level: float) -> Dict[str, pygame.font.Font]:
    """Create appropriately sized fonts for the current zoom level."""
    return {
        'player': pygame.font.Font(font_file, max(8, int(BASE_FONT_SIZE * zoom_level))),
        'spell_cursor': pygame.font.Font(font_file, int(BASE_CELL_SIZE * zoom_level)),
        'coords': pygame.font.Font(font_file, 16),
        'timer': pygame.font.Font(font_file, 22)
    }