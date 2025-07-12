"""
Container system for managing backpacks and item storage.
"""

from dataclasses import dataclass, field
from typing import List
from .items import GearItem, InventoryItem, is_container

@dataclass
class Container:
    """Represents a container that can hold items."""
    name: str
    capacity: int  # Max gear slots it can hold
    contents: List[InventoryItem] = field(default_factory=list)
    
    def get_used_capacity(self) -> int:
        """Calculate how many gear slots are used in this container."""
        total = 0
        for inv_item in self.contents:
            if hasattr(inv_item.item, 'gear_slots'):
                slots_per_item = inv_item.item.gear_slots
                if hasattr(inv_item.item, 'quantity_per_slot') and inv_item.item.quantity_per_slot > 1:
                    # Items that can stack
                    slots_needed = (inv_item.quantity + inv_item.item.quantity_per_slot - 1) // inv_item.item.quantity_per_slot
                    total += slots_needed * slots_per_item
                else:
                    total += slots_per_item * inv_item.quantity
            else:
                total += inv_item.quantity
        return total
    
    def can_fit_item(self, item: GearItem, quantity: int = 1) -> bool:
        """Check if item can fit in this container."""
        if hasattr(item, 'gear_slots'):
            slots_needed = item.gear_slots * quantity
            if hasattr(item, 'quantity_per_slot') and item.quantity_per_slot > 1:
                slots_needed = (quantity + item.quantity_per_slot - 1) // item.quantity_per_slot
            return self.get_used_capacity() + slots_needed <= self.capacity
        else:
            return self.get_used_capacity() + quantity <= self.capacity
    
    def add_item(self, item: GearItem, quantity: int = 1) -> bool:
        """Add an item to this container if it fits."""
        if not self.can_fit_item(item, quantity):
            return False
        
        # Check if item already exists
        for inv_item in self.contents:
            if inv_item.item.name == item.name:
                inv_item.quantity += quantity
                return True
        
        # Add new item
        self.contents.append(InventoryItem(item, quantity))
        return True
    
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """Remove an item from this container."""
        for i, inv_item in enumerate(self.contents):
            if inv_item.item.name == item_name:
                if inv_item.quantity <= quantity:
                    # Remove entire stack
                    self.contents.pop(i)
                else:
                    # Reduce quantity
                    inv_item.quantity -= quantity
                return True
        return False

def get_containers_from_inventory(player) -> List[Container]:
    """Get all containers from player's inventory."""
    containers = []
    
    # Find backpacks and convert them to containers
    for inv_item in player.inventory:
        if is_container(inv_item.item):
            # Create container for each backpack
            for i in range(inv_item.quantity):
                container_name = f"{inv_item.item.name} {i+1}" if inv_item.quantity > 1 else inv_item.item.name
                # Standard backpack holds all items the character can carry
                capacity = player.max_gear_slots
                containers.append(Container(container_name, capacity))
    
    # If no backpacks, create a default "carried items" container
    if not containers:
        containers.append(Container("Carried Items", player.max_gear_slots))
    
    return containers

def organize_inventory_into_containers(player) -> List[Container]:
    """Organize player's inventory into containers."""
    containers = get_containers_from_inventory(player)
    
    if not containers:
        return containers
    
    # For now, put all non-container items in the first container
    main_container = containers[0]
    
    for inv_item in player.inventory:
        if not is_container(inv_item.item):
            # Check if item can fit
            if main_container.can_fit_item(inv_item.item, inv_item.quantity):
                main_container.contents.append(inv_item)
            else:
                # Try other containers or create overflow
                placed = False
                for container in containers[1:]:
                    if container.can_fit_item(inv_item.item, inv_item.quantity):
                        container.contents.append(inv_item)
                        placed = True
                        break
                
                if not placed:
                    # Create overflow container
                    overflow = Container("Overflow (No Backpack)", player.max_gear_slots)
                    overflow.contents.append(inv_item)
                    containers.append(overflow)
    
    return containers