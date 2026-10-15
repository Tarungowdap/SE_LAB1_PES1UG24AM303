# Lab 5: Issue Table (energy_system.py)

Scores: Pylint 6.14/10 → 10.00/10 | Bandit 1 Medium issue → 0 | Flake8 12 warnings → 0.
Line numbers refer to the original file (see `before/` reports).

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `eval()` on user input (Bandit B307, Pylint W0123) | Security (Medium) | 63 | `eval(adjustment)` runs whatever the user types, so it allows arbitrary code execution. | Replaced with `ast.literal_eval()`, which only accepts literals, and wrapped it in `try/except (ValueError, SyntaxError)` so bad input prints a message instead of crashing. |
| Mutable default argument `history=[]` (Pylint W0102) | Bug | 12 | The default list is created once and shared across every call, so readings from different calls pile up in one hidden list. | Removed the shared `history` parameter. Readings are now stored per meter in a dict of lists and created when first needed. |
| Bare `except:` (Pylint W0702, Flake8 E722) | Bug / bad practice | 44 | Catches every error, including `KeyboardInterrupt`, and silently resets the data to `{}`. | Catch only `json.JSONDecodeError`, and check `os.path.exists()` for the missing-file case. |
| Files opened without `with` (Pylint R1732) | Resource leak | 42, 48 | If an error occurs before `close()`, the file handle is never closed. | Used `with open(...) as file_obj:` so the file always closes. |
| `open()` without encoding (Pylint W1514) | Portability | 42, 48 | The default encoding depends on the operating system. | Added `encoding="utf-8"`. |
| `global` statements (Pylint W0603) | Design | 27, 40 | Functions change module state through `global`, which is hard to follow and test. | Removed the `global` statements. The functions now mutate the shared `meter_data` dict instead of reassigning it. |
| Unused import `sys` (Flake8 F401, Pylint W0611) | Style | 2 | Imported but never used. | Removed the import. |
| Missing docstrings (Pylint C0114, C0116) | Documentation | 1, 12, 17, 26, 32, 39, 47, 52 | The module and every function lack docstrings. | Added a module docstring and a one-line docstring to each function. |
| Unnecessary `elif` after `return` (Pylint R1705) | Style | 19 | `elif` after a `return` is redundant. | Simplified the billing logic so no `elif` chain remains. |
| `%` string formatting (Pylint C0209) | Style | 59, 60, 66 | Old-style formatting. | Converted to f-strings. |
| Wrong blank-line spacing (Flake8 E302, E305) | Style (PEP 8) | 12, 17, 26, 32, 39, 47, 52, 68 | Two blank lines are required around top-level definitions. | Reformatted. |
| Lines over 79 characters (Flake8 E501) | Style (PEP 8) | 24, 62 | Lines of 88 and 86 characters. | Wrapped the long lines. |
