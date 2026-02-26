## Plan: New Random Wheel Generator (Python CLI)

**TL;DR:** Build a Python command-line random wheel generator with session-based entry management, spin limits per wheel, pre-spin exclusion rules, and result history logging. Users add entries via CLI, optionally exclude entries, set max spins, then spin sequentially with results tracked until limit is reached or user exits.

**Steps**

1. **Create core data structure** — Implement a `Wheel` class or dictionary structure to store:
   - entries (list of items)
   - excluded_entries (items to skip this session)
   - max_spins (limit per wheel)
   - spin_count (current count)
   - history (list of past results with timestamps)

2. **Build entry management module** — Implement functions for:
   - Add entry to wheel
   - Remove entry from wheel  
   - View all entries
   - View excluded entries
   - Mark entries as excluded/included

3. **Implement spin logic** — Create function that:
   - Checks if spin limit reached, halt if so
   - Filters out excluded entries
   - Uses `random.choice()` to select from available entries
   - Increments spin counter
   - Records result + timestamp to history

4. **Build CLI menu system** — Main loop with options:
   - Create new wheel
   - Add/remove entries
   - View wheel (all entries, excluded list)
   - Configure exclusions
   - Set max spins
   - Spin wheel (single or loop)
   - View history
   - Exit

5. **Add history/logging** — Track and display:
   - Each spin result with timestamp
   - Order of selections
   - Session summary (spins done, spins remaining)

6. **Error handling** — Validate:
   - Non-empty entry list before spinning
   - Valid spin limit (>0)
   - No spinning when limit reached
   - User input types

**Verification**
- Manually run through CLI: create wheel → add entries → exclude some → spin until limit
- Check history displays all results in order
- Verify excluded entries never get selected
- Confirm spin counter stops at max limit
- Test edge cases: empty wheel, all entries excluded, single entry

**Decisions**
- Chose session-based (no file persistence) to match requirements
- Spin limit applies per wheel instance, resets on new wheel
- Exclusion is pre-spin only (set once before spinning begins)
- History keeps all results indefinitely during session