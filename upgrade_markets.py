from pathlib import Path
import shutil
import re
import ast

ROOT = Path(__file__).resolve().parent
FILE = ROOT / "pages" / "markets.py"

if not FILE.exists():
    raise FileNotFoundError(FILE)

BACKUP = FILE.with_suffix(".py.repair_v2_backup")

if not BACKUP.exists():
    shutil.copy2(FILE, BACKUP)

text = FILE.read_text(encoding="utf-8-sig")
changes = []


# ============================================================
# 1. TABLE = 7 COLUMNS
# ============================================================

count = text.count("for column in range(6):")

if count:
    text = text.replace(
        "for column in range(6):",
        "for column in range(7):",
    )
    changes.append(
        f"grid loops 6 -> 7 x{count}"
    )


count = text.count("columnspan=6,")

if count:
    text = text.replace(
        "columnspan=6,",
        "columnspan=7,",
    )
    changes.append(
        f"columnspan 6 -> 7 x{count}"
    )


# ============================================================
# 2. HEADER
# ============================================================

old_header = '''        headers = (
            "Asset",
            "Name",
            "Exchange",
            "Type",
            "Price",
            "Action",
        )
'''

new_header = '''        headers = (
            "Asset",
            "Name",
            "Exchange",
            "Type",
            "Price",
            "24h",
            "Action",
        )
'''

if old_header in text:
    text = text.replace(
        old_header,
        new_header,
        1,
    )
    changes.append("added 24h header")


# ============================================================
# 3. CREATE change_label
# ============================================================

if "change_label = ctk.CTkLabel(" not in text:

    marker = '''        # ========================================================
        # ACTION
        # ========================================================
        action_frame = ctk.CTkFrame(
'''

    replacement = '''        # ========================================================
        # 24H CHANGE
        # ========================================================

        change_label = ctk.CTkLabel(
            frame,
            text="—",
            anchor="e",
            font=ctk.CTkFont(
                size=10,
                weight="bold",
            ),
        )

        change_label.grid(
            row=0,
            column=5,
            sticky="ew",
            padx=8,
        )

        # ========================================================
        # ACTION
        # ========================================================
        action_frame = ctk.CTkFrame(
'''

    if marker not in text:
        raise RuntimeError(
            "Could not find ACTION section in _create_row()."
        )

    text = text.replace(
        marker,
        replacement,
        1,
    )

    changes.append(
        "created change_label"
    )


# ============================================================
# 4. ACTION -> COLUMN 6
# ============================================================

pattern = re.compile(
    r"(action_frame\.grid\(\s*"
    r"row=0,\s*"
    r"column=)5(,)",
    re.MULTILINE,
)

if pattern.search(text):

    text = pattern.sub(
        r"\g<1>6\2",
        text,
        count=1,
    )

    changes.append(
        "Action column 5 -> 6"
    )


# ============================================================
# 5. SAVE change_label IN self.rows
# ============================================================

if '"change_label": change_label' not in text:

    marker = '''            "price_label": price_label,
'''

    replacement = '''            "price_label": price_label,
            "change_label": change_label,
'''

    if marker not in text:
        raise RuntimeError(
            "Could not find price_label row storage."
        )

    text = text.replace(
        marker,
        replacement,
        1,
    )

    changes.append(
        "stored change_label in self.rows"
    )


# ============================================================
# 6. UPDATE realtime system
# ============================================================

if "def update_prices(" in text:

    # Read change_label from row.
    if 'data["change_label"]' not in text:

        marker = '''            price_label = (
                data["price_label"]
            )
'''

        replacement = '''            price_label = (
                data["price_label"]
            )

            change_label = (
                data["change_label"]
            )
'''

        if marker in text:
            text = text.replace(
                marker,
                replacement,
                1,
            )
            changes.append(
                "connected change_label to realtime updater"
            )

    # Current provider returns price only, so safely leave
    # 24h as "—" until provider exposes change_24h.
    if "change_label.configure(" not in text:

        marker = '''                price_label.configure(
                    text=self.format_price(
                        price,
                        instrument.currency,
                    )
                )
'''

        replacement = '''                price_label.configure(
                    text=self.format_price(
                        price,
                        instrument.currency,
                    )
                )

                # Provider currently exposes price only.
                # Keep 24h neutral until change_24h is available.
                change_label.configure(
                    text="—"
                )
'''

        if marker in text:
            text = text.replace(
                marker,
                replacement,
                1,
            )
            changes.append(
                "added safe 24h placeholder"
            )


# ============================================================
# 7. VALIDATE
# ============================================================

try:
    ast.parse(
        text,
        filename=str(FILE),
    )
except SyntaxError:
    shutil.copy2(
        BACKUP,
        FILE,
    )

    raise RuntimeError(
        "Repair generated invalid Python. "
        "Original markets.py was restored."
    )


FILE.write_text(
    text,
    encoding="utf-8",
)


print()
print("=" * 60)
print(" CRYTOPZ MARKETS REPAIR V2 COMPLETE")
print("=" * 60)

for change in changes:
    print("[OK]", change)

print()
print("Backup:")
print(BACKUP)

print()
print("NEXT:")
print("python -m py_compile pages\\markets.py")
print("python main.py")
print()