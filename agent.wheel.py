"""
New Random Wheel Generator - Python CLI Implementation
Implements the plan from agent.proposal.md

Features:
- Session-based entry management (no file persistence)
- Spin limits per wheel
- Pre-spin exclusion rules
- Result history with timestamps
"""

import random
from datetime import datetime
from typing import List, Dict, Optional


class Wheel:
    """Core wheel data structure with entries, exclusions, spin limits, and history."""
    
    def __init__(self, max_spins: int = 10):
        """
        Initialize a new wheel.
        
        Args:
            max_spins: Maximum number of spins allowed for this wheel (default: 10)
        """
        self.entries: List[str] = []
        self.excluded_entries: List[str] = []
        self.max_spins: int = max_spins
        self.spin_count: int = 0
        self.history: List[Dict] = []
    
    def add_entry(self, entry: str) -> bool:
        """
        Add an entry to the wheel.
        
        Args:
            entry: Entry text to add
            
        Returns:
            True if added successfully, False if entry already exists
        """
        entry = entry.strip()
        if not entry:
            return False
        if entry in self.entries:
            return False
        self.entries.append(entry)
        return True
    
    def remove_entry(self, entry: str) -> bool:
        """
        Remove an entry from the wheel.
        
        Args:
            entry: Entry text to remove
            
        Returns:
            True if removed, False if entry doesn't exist
        """
        entry = entry.strip()
        if entry in self.entries:
            self.entries.remove(entry)
            # Also remove from excluded if it was there
            if entry in self.excluded_entries:
                self.excluded_entries.remove(entry)
            return True
        return False
    
    def view_entries(self) -> List[str]:
        """Return all entries in the wheel."""
        return self.entries.copy()
    
    def view_excluded(self) -> List[str]:
        """Return all excluded entries."""
        return self.excluded_entries.copy()
    
    def exclude_entry(self, entry: str) -> bool:
        """
        Mark an entry as excluded from spins.
        
        Args:
            entry: Entry text to exclude
            
        Returns:
            True if excluded successfully, False if entry doesn't exist
        """
        entry = entry.strip()
        if entry in self.entries and entry not in self.excluded_entries:
            self.excluded_entries.append(entry)
            return True
        return False
    
    def include_entry(self, entry: str) -> bool:
        """
        Remove an entry from excluded list.
        
        Args:
            entry: Entry text to include
            
        Returns:
            True if included successfully, False if not in excluded list
        """
        entry = entry.strip()
        if entry in self.excluded_entries:
            self.excluded_entries.remove(entry)
            return True
        return False
    
    def get_available_entries(self) -> List[str]:
        """Return entries that are available to spin (not excluded)."""
        return [e for e in self.entries if e not in self.excluded_entries]
    
    def spin_limit_reached(self) -> bool:
        """Check if spin limit has been reached."""
        return self.spin_count >= self.max_spins
    
    def spin(self) -> Optional[str]:
        """
        Spin the wheel and select a random entry.
        
        Returns:
            Selected entry string, or None if spin limit reached or no entries available
        """
        if self.spin_limit_reached():
            return None
        
        available = self.get_available_entries()
        if not available:
            return None
        
        result = random.choice(available)
        self.spin_count += 1
        
        # Record in history
        self.history.append({
            'result': result,
            'timestamp': datetime.now(),
            'spin_number': self.spin_count
        })
        
        return result
    
    def view_history(self) -> List[Dict]:
        """Return spin history."""
        return self.history.copy()
    
    def get_session_summary(self) -> Dict:
        """Return summary of current session."""
        return {
            'total_entries': len(self.entries),
            'excluded_entries': len(self.excluded_entries),
            'available_entries': len(self.get_available_entries()),
            'max_spins': self.max_spins,
            'spins_done': self.spin_count,
            'spins_remaining': self.max_spins - self.spin_count
        }
    
    def reset(self):
        """Reset wheel for new session (keeps entries but clears exclusions, history, spin count)."""
        self.excluded_entries = []
        self.spin_count = 0
        self.history = []


class WheelGenerator:
    """CLI interface for the random wheel generator."""
    
    def __init__(self):
        """Initialize the generator with no wheel."""
        self.current_wheel: Optional[Wheel] = None
    
    def display_main_menu(self):
        """Display main menu options."""
        print("\n" + "="*50)
        print("RANDOM WHEEL GENERATOR")
        print("="*50)
        if self.current_wheel:
            summary = self.current_wheel.get_session_summary()
            print(f"Status: {summary['available_entries']} available entries, "
                  f"{summary['spins_done']}/{summary['max_spins']} spins done")
        print("\nOptions:")
        print("1. Create new wheel")
        print("2. Add entry")
        print("3. Remove entry")
        print("4. View wheel")
        print("5. Configure exclusions")
        print("6. Set max spins")
        print("7. Spin wheel")
        print("8. View history")
        print("9. Exit")
        print("="*50)
    
    def create_wheel(self):
        """Create a new wheel with specified max spins."""
        try:
            max_spins = int(input("Enter maximum spins allowed (default 10): ") or "10")
            if max_spins <= 0:
                print("❌ Max spins must be greater than 0.")
                return
            self.current_wheel = Wheel(max_spins)
            print(f"✓ New wheel created with {max_spins} max spins.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
    
    def add_entry(self):
        """Add entry to current wheel."""
        if not self.current_wheel:
            print("❌ No wheel created yet. Create one first.")
            return
        
        entry = input("Enter entry to add: ").strip()
        if self.current_wheel.add_entry(entry):
            print(f"✓ '{entry}' added to wheel.")
        else:
            print(f"❌ Entry is empty or already exists.")
    
    def remove_entry(self):
        """Remove entry from current wheel."""
        if not self.current_wheel:
            print("❌ No wheel created yet.")
            return
        
        self.view_wheel()
        entry = input("Enter entry to remove: ").strip()
        if self.current_wheel.remove_entry(entry):
            print(f"✓ '{entry}' removed from wheel.")
        else:
            print(f"❌ Entry not found.")
    
    def view_wheel(self):
        """Display current wheel entries and status."""
        if not self.current_wheel:
            print("❌ No wheel created yet.")
            return
        
        print("\n" + "-"*50)
        print("WHEEL STATUS")
        print("-"*50)
        
        summary = self.current_wheel.get_session_summary()
        print(f"Total entries: {summary['total_entries']}")
        print(f"Excluded entries: {summary['excluded_entries']}")
        print(f"Available entries: {summary['available_entries']}")
        print(f"Spins: {summary['spins_done']}/{summary['max_spins']}")
        
        entries = self.current_wheel.view_entries()
        if entries:
            print("\nAll Entries:")
            excluded = set(self.current_wheel.view_excluded())
            for idx, entry in enumerate(entries, 1):
                status = " (excluded)" if entry in excluded else ""
                print(f"  {idx}. {entry}{status}")
        else:
            print("\nNo entries yet.")
        print("-"*50 + "\n")
    
    def configure_exclusions(self):
        """Configure which entries to exclude from spins."""
        if not self.current_wheel:
            print("❌ No wheel created yet.")
            return
        
        entries = self.current_wheel.view_entries()
        if not entries:
            print("❌ No entries to exclude. Add entries first.")
            return
        
        print("\nExclusion Menu:")
        print("1. Exclude entry")
        print("2. Include entry (remove from exclusion)")
        print("3. Back")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            entry = input("Enter entry to exclude: ").strip()
            if self.current_wheel.exclude_entry(entry):
                print(f"✓ '{entry}' excluded.")
            else:
                print(f"❌ Entry not found or already excluded.")
        
        elif choice == "2":
            excluded = self.current_wheel.view_excluded()
            if not excluded:
                print("No excluded entries.")
                return
            print("Excluded entries:")
            for idx, entry in enumerate(excluded, 1):
                print(f"  {idx}. {entry}")
            entry = input("Enter entry to include: ").strip()
            if self.current_wheel.include_entry(entry):
                print(f"✓ '{entry}' included.")
            else:
                print(f"❌ Entry not found in excluded list.")
    
    def set_max_spins(self):
        """Change the maximum spins for current wheel."""
        if not self.current_wheel:
            print("❌ No wheel created yet.")
            return
        
        try:
            max_spins = int(input(f"Enter new max spins (current: {self.current_wheel.max_spins}): "))
            if max_spins <= 0:
                print("❌ Max spins must be greater than 0.")
                return
            self.current_wheel.max_spins = max_spins
            print(f"✓ Max spins set to {max_spins}.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
    
    def spin_wheel(self):
        """Spin the wheel."""
        if not self.current_wheel:
            print("❌ No wheel created yet.")
            return
        
        if self.current_wheel.spin_limit_reached():
            print(f"❌ Spin limit reached ({self.current_wheel.max_spins} spins).")
            return
        
        available = self.current_wheel.get_available_entries()
        if not available:
            print("❌ No available entries. All entries are excluded or wheel is empty.")
            return
        
        print("\nSpinning the wheel...")
        result = self.current_wheel.spin()
        
        if result:
            print(f"\n🎡 RESULT: {result}")
            summary = self.current_wheel.get_session_summary()
            print(f"   Spin {summary['spins_done']} of {summary['max_spins']}")
            
            if self.current_wheel.spin_limit_reached():
                print("⚠️  Spin limit reached!")
        else:
            print("❌ Error spinning wheel.")
    
    def view_history(self):
        """Display spin history."""
        if not self.current_wheel:
            print("❌ No wheel created yet.")
            return
        
        history = self.current_wheel.view_history()
        if not history:
            print("No spins recorded yet.")
            return
        
        print("\n" + "-"*50)
        print("SPIN HISTORY")
        print("-"*50)
        for record in history:
            timestamp = record['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            print(f"{record['spin_number']}. {record['result']} ({timestamp})")
        print("-"*50 + "\n")
    
    def run(self):
        """Main CLI loop."""
        print("Welcome to the Random Wheel Generator!")
        
        while True:
            self.display_main_menu()
            choice = input("Enter your choice (1-9): ").strip()
            
            if choice == "1":
                self.create_wheel()
            elif choice == "2":
                self.add_entry()
            elif choice == "3":
                self.remove_entry()
            elif choice == "4":
                self.view_wheel()
            elif choice == "5":
                self.configure_exclusions()
            elif choice == "6":
                self.set_max_spins()
            elif choice == "7":
                self.spin_wheel()
            elif choice == "8":
                self.view_history()
            elif choice == "9":
                print("Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-9.")


def main():
    """Entry point for the application."""
    generator = WheelGenerator()
    generator.run()


if __name__ == "__main__":
    main()
