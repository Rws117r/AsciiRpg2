"""
Dynamic World Calendar and Time System
Implements the comprehensive calendar, lunar cycles, and world event system.
"""

import math
import time
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

class MoonPhase(Enum):
    """Moon phase classifications."""
    NEW = "New"           # 0.00-0.10
    WAXING = "Waxing"     # 0.11-0.40
    FULL = "Full"         # 0.41-0.59
    WANING = "Waning"     # 0.60-0.89
    DARK = "Dark"         # 0.90-1.00

@dataclass
class WorldEvent:
    """Represents a world event that can be triggered."""
    name: str
    description: str
    trigger_condition: Callable
    effects: Dict = field(default_factory=dict)
    is_active: bool = False
    duration: int = 1  # in days

@dataclass
class CalendarDate:
    """Represents a specific date in the world calendar."""
    year: int
    day_of_year: int
    
    def __post_init__(self):
        """Calculate derived values."""
        self.month, self.day_of_month = self._calculate_month_and_day()
        self.day_of_week = self._calculate_day_of_week()
    
    def _calculate_month_and_day(self) -> Tuple[str, int]:
        """Calculate month and day of month from day of year."""
        months = [
            ("Frostwane", 31), ("Embermarch", 28), ("Thawmere", 31),
            ("Greentide", 30), ("Blossarch", 31), ("Suncrest", 30),
            ("Highflare", 31), ("Duskwane", 31), ("Mournfall", 30),
            ("Hallowdeep", 31), ("Snowrest", 30), ("Starhearth", 31)
        ]
        
        current_day = self.day_of_year
        for month_name, days_in_month in months:
            if current_day <= days_in_month:
                return month_name, current_day
            current_day -= days_in_month
        
        # Fallback for invalid dates
        return "Starhearth", 31
    
    def _calculate_day_of_week(self) -> str:
        """Calculate day of week from total days."""
        weekdays = ["Soulday", "Moonday", "Flameday", "Wyrmday", "Stonehold", "Windmere", "Shadoweve"]
        # Assume year 754, day 1 starts on Soulday (index 0)
        total_days = (self.year - 754) * 365 + self.day_of_year - 1
        return weekdays[total_days % 7]

class WorldCalendar:
    """Main calendar system managing time, moons, and events."""
    
    # Calendar constants
    YEAR_LENGTH = 365
    WEEK_LENGTH = 7
    MONTHS = {
        "Frostwane": 31, "Embermarch": 28, "Thawmere": 31, "Greentide": 30,
        "Blossarch": 31, "Suncrest": 30, "Highflare": 31, "Duskwane": 31,
        "Mournfall": 30, "Hallowdeep": 31, "Snowrest": 30, "Starhearth": 31
    }
    WEEKDAYS = ["Soulday", "Moonday", "Flameday", "Wyrmday", "Stonehold", "Windmere", "Shadoweve"]
    
    # Lunar constants
    LUNAR_CYCLES = {
        "Myrr": 27.7,
        "Caelyra": 29.0,
        "Velmara": 32.0
    }
    LUNAR_SHIFTS = {
        "Myrr": 13,
        "Caelyra": 0,
        "Velmara": 5
    }
    
    def __init__(self, initial_year: int = 754, initial_day: int = 1):
        """Initialize the world calendar."""
        self.current_year = initial_year
        self.current_day_of_year = initial_day
        self.time_of_day = 0.0  # 0.0 to 1.0 representing a full day
        
        # Moon phases (0.0 to 1.0)
        self.moon_phases = {
            "Myrr": 0.0,
            "Caelyra": 0.0,
            "Velmara": 0.0
        }
        
        # Weather and conditions
        self.is_night = False
        self.is_weather_storm = False
        
        # Event system
        self.active_events: List[WorldEvent] = []
        self.event_registry: List[WorldEvent] = []
        
        # Initialize moon phases and events
        self._calculate_moon_phases()
        self._register_world_events()
    
    def get_current_date(self) -> CalendarDate:
        """Get the current calendar date."""
        return CalendarDate(self.current_year, self.current_day_of_year)
    
    def advance_time(self, hours: float = 1.0):
        """Advance time by specified hours."""
        days_to_advance = hours / 24.0
        self.time_of_day += days_to_advance
        
        # Handle day rollover
        while self.time_of_day >= 1.0:
            self.time_of_day -= 1.0
            self._advance_day()
        
        # Update day/night cycle
        self.is_night = self.time_of_day < 0.25 or self.time_of_day > 0.75
    
    def _advance_day(self):
        """Advance to the next day and update all systems."""
        self.current_day_of_year += 1
        
        # Handle year rollover
        if self.current_day_of_year > self.YEAR_LENGTH:
            self.current_day_of_year = 1
            self.current_year += 1
        
        # Update moon phases
        self._calculate_moon_phases()
        
        # Check for events
        self._check_events()
        
        # Update active events
        self._update_active_events()
    
    def _calculate_moon_phases(self):
        """Calculate current moon phases based on the date."""
        total_days = (self.current_year - 754) * self.YEAR_LENGTH + self.current_day_of_year
        
        for moon, cycle_length in self.LUNAR_CYCLES.items():
            shift = self.LUNAR_SHIFTS[moon]
            phase_position = ((total_days + shift) % cycle_length) / cycle_length
            self.moon_phases[moon] = phase_position
    
    def get_moon_phase_name(self, moon: str) -> MoonPhase:
        """Get the descriptive phase name for a moon."""
        phase = self.moon_phases[moon]
        if 0.00 <= phase <= 0.10:
            return MoonPhase.NEW
        elif 0.11 <= phase <= 0.40:
            return MoonPhase.WAXING
        elif 0.41 <= phase <= 0.59:
            return MoonPhase.FULL
        elif 0.60 <= phase <= 0.89:
            return MoonPhase.WANING
        else:  # 0.90-1.00
            return MoonPhase.DARK
    
    def is_moon_full(self, moon: str) -> bool:
        """Check if a specific moon is full."""
        return self.get_moon_phase_name(moon) == MoonPhase.FULL
    
    def is_moon_dark(self, moon: str) -> bool:
        """Check if a specific moon is dark."""
        return self.get_moon_phase_name(moon) == MoonPhase.DARK
    
    def is_triune_gaze(self) -> bool:
        """Check if all three moons are full (rare event)."""
        return all(self.is_moon_full(moon) for moon in ["Myrr", "Caelyra", "Velmara"])
    
    def is_eclipserite(self) -> bool:
        """Check if Myrr eclipses Caelyra (both full, special alignment)."""
        return (self.is_moon_full("Myrr") and self.is_moon_full("Caelyra") and 
                abs(self.moon_phases["Myrr"] - self.moon_phases["Caelyra"]) < 0.05)
    
    def _register_world_events(self):
        """Register all world events with their trigger conditions."""
        # The Burning Howl (Zyrix event)
        self.event_registry.append(WorldEvent(
            name="The Burning Howl",
            description="Zyrix's influence peaks, empowering chaotic magic and violence.",
            trigger_condition=lambda: (self.get_current_date().month == "Highflare" and 
                                     self.get_current_date().day_of_week == "Flameday" and 
                                     self.is_moon_full("Myrr")),
            effects={
                "chaos_magic_bonus": 2,
                "fire_damage_bonus": 1.5,
                "arena_tournaments": True
            },
            duration=3
        ))
        
        # The Triune Gaze (Thalen event)
        self.event_registry.append(WorldEvent(
            name="The Triune Gaze", 
            description="All three moons align in full phase, revealing cosmic truths.",
            trigger_condition=lambda: self.is_triune_gaze(),
            effects={
                "divination_bonus": 3,
                "spell_range_bonus": 2,
                "prophecy_available": True,
                "world_boss_spawn": True
            },
            duration=1
        ))
        
        # Mercy's Embrace (Serentha event)
        self.event_registry.append(WorldEvent(
            name="Mercy's Embrace",
            description="Serentha's compassion flows freely through the world.",
            trigger_condition=lambda: (self.get_current_date().month in ["Greentide", "Blossarch"] and 
                                     self.get_current_date().day_of_week == "Soulday"),
            effects={
                "healing_bonus": 2.0,
                "shrine_regeneration": True,
                "potion_discount": 0.5
            },
            duration=1
        ))
        
        # Eclipserite (Chaos vs Law)
        self.event_registry.append(WorldEvent(
            name="Eclipserite",
            description="Myrr eclipses Caelyra, chaos overwhelms order.",
            trigger_condition=lambda: self.is_eclipserite(),
            effects={
                "divine_law_disabled": True,
                "chaos_magic_empowered": True,
                "temple_vulnerability": True
            },
            duration=1
        ))
        
        # The Hunger's Toll (Vhalor event)
        self.event_registry.append(WorldEvent(
            name="The Hunger's Toll",
            description="Vhalor demands tribute, or entropy spreads.",
            trigger_condition=lambda: (self.get_current_date().month == "Hallowdeep" and 
                                     self.get_current_date().day_of_week == "Shadoweve"),
            effects={
                "entropy_spread": True,
                "sacrifice_required": True,
                "undead_empowered": True
            },
            duration=7
        ))
    
    def _check_events(self):
        """Check if any events should trigger today."""
        current_date = self.get_current_date()
        
        for event in self.event_registry:
            if event.trigger_condition() and not event.is_active:
                self._trigger_event(event)
    
    def _trigger_event(self, event: WorldEvent):
        """Trigger a world event."""
        event.is_active = True
        self.active_events.append(event)
        print(f"🌟 World Event Triggered: {event.name}")
        print(f"   {event.description}")
    
    def _update_active_events(self):
        """Update durations of active events and remove expired ones."""
        for event in self.active_events[:]:  # Copy list to avoid modification during iteration
            event.duration -= 1
            if event.duration <= 0:
                event.is_active = False
                self.active_events.remove(event)
                print(f"🌅 World Event Ended: {event.name}")
    
    def get_active_event_effects(self) -> Dict:
        """Get combined effects from all active events."""
        combined_effects = {}
        for event in self.active_events:
            combined_effects.update(event.effects)
        return combined_effects
    
    def is_event_active(self, event_name: str) -> bool:
        """Check if a specific event is currently active."""
        return any(event.name == event_name for event in self.active_events)
    
    def get_month_environmental_effects(self) -> Dict:
        """Get environmental effects based on current month."""
        current_date = self.get_current_date()
        month_effects = {
            "Frostwane": {
                "temperature": "freezing",
                "stamina_drain": 1.2,
                "cold_resistance_bonus": True,
                "frozen_water": True
            },
            "Embermarch": {
                "temperature": "cold",
                "fire_festival_goods": True,
                "ice_melting": True
            },
            "Thawmere": {
                "temperature": "cool",
                "spring_growth": True,
                "healing_herb_spawn": True
            },
            "Greentide": {
                "temperature": "mild",
                "plant_growth_accelerated": True,
                "nature_magic_bonus": 1.2
            },
            "Blossarch": {
                "temperature": "warm",
                "chaotic_growth": True,
                "romance_festival": True
            },
            "Suncrest": {
                "temperature": "hot",
                "solar_magic_bonus": 1.5,
                "endurance_trials": True
            },
            "Highflare": {
                "temperature": "scorching",
                "stamina_drain": 1.5,
                "fire_enemies_empowered": True,
                "water_sources_rare": True
            },
            "Duskwane": {
                "temperature": "warm",
                "illusion_magic_bonus": 1.3,
                "shifting_weather": True
            },
            "Mournfall": {
                "temperature": "cool",
                "melancholy_atmosphere": True,
                "spirit_encounters": True
            },
            "Hallowdeep": {
                "temperature": "cold",
                "veil_thinned": True,
                "undead_spawn_increased": True,
                "necromancy_empowered": True
            },
            "Snowrest": {
                "temperature": "freezing",
                "rest_bonus": True,
                "storytelling_bonus": True
            },
            "Starhearth": {
                "temperature": "cold",
                "divine_alignment": True,
                "ancestor_communion": True
            }
        }
        
        return month_effects.get(current_date.month, {})
    
    def format_date(self) -> str:
        """Format the current date as a readable string."""
        date = self.get_current_date()
        hour = int(self.time_of_day * 24)
        minute = int((self.time_of_day * 24 - hour) * 60)
        
        return f"{date.day_of_week}, {date.day_of_month} {date.month} {date.year} - {hour:02d}:{minute:02d}"
    
    def format_moon_phases(self) -> str:
        """Format current moon phases as a readable string."""
        phases = []
        for moon, phase_value in self.moon_phases.items():
            phase_name = self.get_moon_phase_name(moon)
            phases.append(f"{moon}: {phase_name.value} ({phase_value:.2f})")
        return " | ".join(phases)
    
    def get_calendar_state(self) -> Dict:
        """Get complete calendar state for save/load."""
        return {
            "current_year": self.current_year,
            "current_day_of_year": self.current_day_of_year,
            "time_of_day": self.time_of_day,
            "moon_phases": self.moon_phases.copy(),
            "is_night": self.is_night,
            "is_weather_storm": self.is_weather_storm,
            "active_events": [(event.name, event.duration) for event in self.active_events]
        }
    
    def load_calendar_state(self, state: Dict):
        """Load calendar state from save data."""
        self.current_year = state["current_year"]
        self.current_day_of_year = state["current_day_of_year"]
        self.time_of_day = state["time_of_day"]
        self.moon_phases = state["moon_phases"]
        self.is_night = state["is_night"]
        self.is_weather_storm = state.get("is_weather_storm", False)
        
        # Restore active events
        self.active_events = []
        for event_name, duration in state.get("active_events", []):
            for event in self.event_registry:
                if event.name == event_name:
                    event.is_active = True
                    event.duration = duration
                    self.active_events.append(event)
                    break

# Global calendar instance
world_calendar = WorldCalendar()

def get_world_calendar() -> WorldCalendar:
    """Get the global world calendar instance."""
    return world_calendar