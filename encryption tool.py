# ================================================================
# DecodeLabs | Cybersecurity Track | Batch 2026
# Project 2: Basic Encryption & Decryption (Caesar Cipher)
# ================================================================
# SLIDE MAP (every design decision references a slide):
#   Slide 7  → IPO Model    : Plaintext → (Algorithm + Key) → Ciphertext
#   Slide 8  → ASCII Logic  : "We don't shift letters; we shift integers."
#                             A=65, Z=90  |  a=97, z=122
#   Slide 9  → The Shift    : E_n(x) = (x + n)
#   Slide 10 → The Wrap     : E_n(x) = (x + n) % 26  ← modular arithmetic
#   Slide 11 → 6-Step Flow  : char→ASCII→-base→+key→%26→+base→char
#   Slide 12 → Decryption   : D_n(x) = (x - n) % 26  ← negative shift
#   Slide 13 → Code         : ord() = char→int | chr() = int→char
#   Slide 14 → Vulnerability: only 25 keys → instant brute force
#   Slide 16 → Deliverables : IPO + Math + Edge Cases + Validation
#   Slide 17 → Bonus        : user-selectable shift key + Vigenère hint
# ================================================================


# ================================================================
# THE CORE ALGORITHM  (Slides 9, 10, 11, 13)
# Implements the exact 6-step pipeline from the Algorithm
# Visualization slide:
#   Step 1 : receive character
#   Step 2 : ASCII Conversion  → ord(char)
#   Step 3 : Subtract Base     → - 65 (uppercase) or - 97 (lowercase)
#   Step 4 : Add Key           → + shift
#   Step 5 : Modulo            → % 26   (the wrap-around)
#   Step 6 : Add Base          → + base → chr() back to character
# ================================================================
def cipher_char(char: str, shift: int) -> str:
    """
    Transforms a single character using the Caesar Cipher formula.

    Encryption : E_n(x) = (x + n) % 26      
    Decryption : D_n(x) = (x - n) % 26     
      → Achieved by passing a negative shift.
      → Python's % operator handles negatives correctly:
         (-1) % 26 = 25  ✓

    Case-aware :
      Uppercase uses base 65  (A=65 ... Z=90)
      Lowercase uses base 97  (a=97 ... z=122)

    Edge cases  [Handle Spaces/Punctuation]:
      Non-alphabetic characters (spaces, digits, symbols) are
      returned unchanged. They are not part of the alphabet,
      so no shift applies.
    """
    if char.isupper():
        base = 65                          # ASCII anchor: 'A' [Slide 8]
    elif char.islower():
        base = 97                          # ASCII anchor: 'a' [Slide 8]
    else:
        return char                        # Pass-through: spaces, digits, symbols

    # ── The 6-step transformation (Slide 11) ──────────────────────
    ascii_val  = ord(char)                 # Step 2: char  → integer [Slide 13]
    normalized = ascii_val - base          # Step 3: map to 0–25 range
    shifted    = normalized + shift        # Step 4: apply shift key
    wrapped    = shifted % 26             # Step 5: modular wrap [Slide 10]
    result_val = wrapped + base           # Step 6: restore to ASCII range
    # ─────────────────────────────────────────────────────────────

    return chr(result_val)                 # Step 6 cont: integer → char [Slide 13]


# ================================================================
# ENCRYPT  —  IPO Process Stage (Slide 7)
# Applies cipher_char() to every character of the plaintext.
# Uses a generator expression (Pythonic, consistent with Project 1).
# ================================================================
def encrypt(plaintext: str, shift: int) -> str:
    """
    Encrypts full plaintext.
    IPO: Plaintext + Shift Key → Ciphertext 
    """
    return ''.join(cipher_char(char, shift) for char in plaintext)


# ================================================================
# DECRYPT  —  Reverse Engineering (Slide 12)
# D_n(x) = (x - n) % 26  →  same function, negative shift.
# "Symmetric Encryption: The same key locks and unlocks." — Slide 12
# ================================================================
def decrypt(ciphertext: str, shift: int) -> str:
    """
    Decrypts ciphertext by reversing the shift direction.
    Reuses encrypt() with a negative shift — proving symmetry.
    """
    return encrypt(ciphertext, -shift)


# ================================================================
# BRUTE FORCE ANALYSIS  —  The Vulnerability (Slide 14)
# Caesar has only 25 possible keys → instant brute-force.
# This function demonstrates exactly WHY it's a lockbox, not a vault.
# ================================================================
def brute_force(ciphertext: str) -> list[tuple[int, str]]:
    """
    Tries all 25 possible shift values and returns every decryption.
    This is the attack that makes Caesar trivially breakable.
    A human or computer simply reads which result makes English sense.
    """
    return [(shift, decrypt(ciphertext, shift)) for shift in range(1, 26)]


# ================================================================
# VIGENÈRE CIPHER  —  Bonus Challenge (Slide 17)
# The conclusion hints at this as a "more complex" upgrade.
# Instead of one shift key, a keyword sets a different shift per char.
# This breaks frequency analysis — each 'E' maps differently.
# ================================================================
def vigenere_cipher(text: str, keyword: str, mode: str = "encrypt") -> str:
    """
    Vigenère Cipher: poly-alphabetic substitution.

    How it works:
      keyword = "KEY"  →  K=10, E=4, Y=24  (positions in alphabet)
      Each plaintext letter is shifted by the corresponding keyword letter,
      cycling through the keyword: K, E, Y, K, E, Y, ...

    Why it's stronger:
      - 'E' (most common English letter) now maps to DIFFERENT ciphertext
        letters depending on its position → frequency analysis fails.
      - Key space grows exponentially with keyword length.
    """
    if not keyword.isalpha():
        return "ERROR: Keyword must contain only letters."

    keyword = keyword.lower()
    result  = []
    key_idx = 0  # cycles through the keyword independently of non-alpha chars

    for char in text:
        if char.isalpha():
            # shift = position of keyword letter in alphabet (0-25)
            key_shift = ord(keyword[key_idx % len(keyword)]) - 97
            if mode == "decrypt":
                key_shift = -key_shift
            result.append(cipher_char(char, key_shift))
            key_idx += 1          # advance keyword pointer only for alpha chars
        else:
            result.append(char)   # pass-through: spaces, punctuation

    return ''.join(result)


# ================================================================
# INPUT HELPERS
# ================================================================
def get_valid_shift() -> int:
    """Validates shift key input. Must be 1–25 (26 = no change)."""
    while True:
        try:
            shift = int(input("  Enter shift key [1–25]: "))
            if 1 <= shift <= 25:
                return shift
            print("  ✗ Shift must be between 1 and 25.")
        except ValueError:
            print("  ✗ Please enter a whole number.")


def get_non_empty(prompt: str) -> str:
    """Ensures the user provides non-empty input."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  ✗ Input cannot be empty.")


# ================================================================
# DISPLAY — Output Stage of IPO Model (Slide 7)
# ================================================================
def display_caesar_report(plaintext: str, shift: int,
                           ciphertext: str, decrypted: str):
    """Presents the full encryption/decryption report."""
    divider = "=" * 58
    thin    = "-" * 58
    verified = "✓  ROUND-TRIP VERIFIED" if decrypted == plaintext else "✗  MISMATCH — CHECK LOGIC"

    print()
    print(divider)
    print("  DecodeLabs | Cryptographic Report — Caesar Cipher")
    print(divider)
    print(f"  {'Algorithm':<18}: Caesar Cipher")
    print(f"  {'Shift Key (n)':<18}: {shift}")
    print(thin)
    print(f"  {'[INPUT]  Plaintext':<18}: {plaintext}")
    print(f"  {'[OUTPUT] Ciphertext':<18}: {ciphertext}")
    print(f"  {'[CHECK]  Decrypted':<18}: {decrypted}")
    print(thin)
    print(f"  Symmetry test        : {verified}")
    print(divider)
    print()
    # Vulnerability disclosure (Slide 14)
    print("  ⚠  SECURITY ANALYSIS:")
    print(f"     Key space   : only 25 possible shifts")
    print(f"     Attack cost : brute-force all 25 in microseconds")
    print(f"     Pattern     : letter frequency distribution PRESERVED")
    print(f"     Verdict     : lockbox, not a vault")
    print(f"     Real-world  : AES-256 uses 2^256 key space")
    print(divider)
    print()


def display_brute_force_report(ciphertext: str, results: list[tuple[int, str]]):
    """Displays all 25 brute-force decryption attempts."""
    divider = "=" * 58
    thin    = "-" * 58

    print()
    print(divider)
    print("  DecodeLabs | Brute Force Analysis — All 25 Keys")
    print(f"  Ciphertext: {ciphertext}")
    print(divider)
    print(f"  {'KEY':>5}  {'DECRYPTED OUTPUT'}")
    print(thin)
    for shift, result in results:
        print(f"  [{shift:>2}]   {result}")
    print(divider)
    print("  A human or script reads whichever line makes sense.")
    print("  This is why 25 keys = zero real security.")
    print(divider)
    print()


def display_vigenere_report(mode: str, keyword: str,
                             original: str, processed: str,
                             verified: bool = None):
    """Displays Vigenère cipher results."""
    divider = "=" * 58
    thin    = "-" * 58
    label   = "Ciphertext" if mode == "encrypt" else "Decrypted"

    print()
    print(divider)
    print("  DecodeLabs | Vigenère Cipher — Bonus Mode")
    print(divider)
    print(f"  {'Algorithm':<18}: Vigenère (poly-alphabetic)")
    print(f"  {'Keyword':<18}: {keyword.upper()}")
    print(thin)
    print(f"  {'[INPUT]':<18}: {original}")
    print(f"  {'['+label+']':<18}: {processed}")
    if verified is not None:
        status = "✓  VERIFIED" if verified else "✗  MISMATCH"
        print(f"  {'Round-trip':<18}: {status}")
    print(divider)
    print()
    print("  WHY THIS IS STRONGER:")
    print(f"  Each character shifts by a DIFFERENT amount (per keyword).")
    print(f"  Letter 'E' maps to multiple ciphertext chars → frequency")
    print(f"  analysis FAILS. Key space = 26^len(keyword) possibilities.")
    print(divider)
    print()


# ================================================================
# MAIN — Orchestrates the Full IPO Model (Slide 7)
# ================================================================
def main():
    BANNER = """
  ╔══════════════════════════════════════════════════════╗
  ║     DecodeLabs Cybersecurity  |  Batch 2026          ║
  ║     Project 2: Basic Encryption & Decryption         ║
  ║     "We don't shift letters; we shift integers."     ║
  ╚══════════════════════════════════════════════════════╝
    """
    print(BANNER)

    MENU = """  Select a mode:
  [1] Caesar Cipher     — Encrypt & Decrypt
  [2] Brute Force Demo  — Show all 25 decryptions
  [3] Vigenère Cipher   — Bonus mode
  [q] Quit
"""

    while True:
        print(MENU)
        choice = input("  Your choice: ").strip().lower()
        print()

        # ── MODE 1: Caesar Cipher (core deliverables) ─────────────
        if choice == "1":
            plaintext = get_non_empty("  Enter text to encrypt: ")
            shift     = get_valid_shift()

            # ── IPO Model (Slide 7) ──────────────────────────────
            ciphertext = encrypt(plaintext, shift)   # I → P → O
            decrypted  = decrypt(ciphertext, shift)  # O → P → I (validation)
            # ────────────────────────────────────────────────────

            display_caesar_report(plaintext, shift, ciphertext, decrypted)

        # ── MODE 2: Brute Force Analysis (Slide 14) ───────────────
        elif choice == "2":
            ciphertext = get_non_empty("  Enter ciphertext to brute-force: ")
            results    = brute_force(ciphertext)
            display_brute_force_report(ciphertext, results)

        # ── MODE 3: Vigenère Cipher Bonus (Slide 17) ──────────────
        elif choice == "3":
            print("  Vigenère Cipher — keyword sets a unique shift per character.")
            print()
            sub_choice = input("  [E]ncrypt or [D]ecrypt? ").strip().lower()
            print()

            if sub_choice not in ("e", "d"):
                print("  ✗ Invalid. Enter 'e' or 'd'.")
                continue

            keyword = get_non_empty("  Enter keyword (letters only): ")
            mode    = "encrypt" if sub_choice == "e" else "decrypt"

            if mode == "encrypt":
                plaintext  = get_non_empty("  Enter plaintext to encrypt: ")
                ciphertext = vigenere_cipher(plaintext, keyword, "encrypt")
                decrypted  = vigenere_cipher(ciphertext, keyword, "decrypt")
                verified   = (decrypted == plaintext)
                display_vigenere_report("encrypt", keyword, plaintext,
                                        ciphertext, verified)
            else:
                ciphertext = get_non_empty("  Enter ciphertext to decrypt: ")
                decrypted  = vigenere_cipher(ciphertext, keyword, "decrypt")
                display_vigenere_report("decrypt", keyword, ciphertext, decrypted)

        # ── Quit ──────────────────────────────────────────────────
        elif choice == "q":
            print("  Session ended. Stay encrypted.\n")
            break

        else:
            print("  ✗ Invalid choice. Please enter 1, 2, 3, or q.\n")


if __name__ == "__main__":
    main()