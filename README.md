[README_P2.md](https://github.com/user-attachments/files/29813840/README_P2.md)
# 🔐 Basic Encryption & Decryption
### DecodeLabs Cybersecurity Internship | Batch 2026 | Project 2

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python&logoColor=white)
![Track](https://img.shields.io/badge/Track-Cybersecurity-red?style=flat)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat)
![Internship](https://img.shields.io/badge/DecodeLabs-Batch%202026-orange?style=flat)

---

## 📌 Overview

This is **Project 2** of the DecodeLabs Cybersecurity Industrial Training Kit — the cryptographic phase. The goal is to implement a working encryption and decryption engine in Python using the **Caesar Cipher**, backed by a deep understanding of the ASCII model, modular arithmetic, and cryptographic vulnerability analysis.

> *"We don't shift letters; we shift integers."*
> — DecodeLabs, Batch 2026 Kit

---

## 🎯 Project Goals

| Requirement | Status |
|---|---|
| Encrypt user text using Caesar Cipher logic | ✅ |
| Decrypt the encrypted text | ✅ |
| Display both encrypted and decrypted output | ✅ |
| Handle edge cases — spaces, digits, punctuation | ✅ |
| Validate with round-trip symmetry test | ✅ |
| Bonus: User-selectable shift key | ✅ |
| Bonus: Brute-force vulnerability demonstration | ✅ |
| Bonus: Vigenère Cipher (poly-alphabetic) | ✅ |

---

## 🧠 Core Concepts Applied

### The IPO Model
Every cryptographic system follows the same universal architecture:

```
INPUT              PROCESS                    OUTPUT
──────────       ─────────────────────       ──────────────
Plaintext   →    Algorithm + Key        →    Ciphertext
Ciphertext  →    Reverse Algorithm      →    Plaintext
```

### ASCII — Shifting Integers, Not Letters

Text must become numbers before it can become math.

| Character | ASCII Value |
|---|---|
| `A` | 65 |
| `Z` | 90 |
| `a` | 97 |
| `z` | 122 |

### The Caesar Cipher Formula

**Encryption:** `E_n(x) = (x + n) % 26`

**Decryption:** `D_n(x) = (x - n) % 26`

Where `x` = character position (0–25), `n` = shift key.

The `% 26` handles wrap-around — so `Z + 3 = C`, not a character that doesn't exist.

### The 6-Step Algorithm

```
Step 1 → receive character          'A'
Step 2 → ASCII conversion           ord('A') = 65
Step 3 → subtract base              65 - 65  = 0
Step 4 → add key                    0  + 3   = 3
Step 5 → modulo wrap                3  % 26  = 3
Step 6 → restore + convert          3  + 65  = 68 → chr(68) = 'D'
```

### Symmetry — One Key, Two Directions

Decryption is not a separate algorithm. It's encryption with a negative shift. The same key that locks, unlocks.

```python
def decrypt(ciphertext, shift):
    return encrypt(ciphertext, -shift)  # D_n(x) = (x - n) % 26
```

---

## ⚙️ Modes

### Mode 1 — Caesar Cipher (Core)
Encrypts and decrypts any text with a user-selected shift key (1–25). Performs a round-trip symmetry test to verify correctness.

### Mode 2 — Brute Force Analysis
Tries all 25 possible shift values against a ciphertext and prints every result. Demonstrates exactly why Caesar is a lockbox, not a vault — a human or script simply reads which result makes English sense.

### Mode 3 — Vigenère Cipher (Bonus)
A poly-alphabetic upgrade. Uses a keyword instead of a single shift, assigning a different shift value to each character of the text. Breaks frequency analysis — the primary weakness of Caesar.

| | Caesar | Vigenère |
|---|---|---|
| Key type | Single number | Keyword |
| Key space | 25 | 26^len(keyword) |
| Frequency analysis | Vulnerable | Resistant |
| Real-world use | None | Historical |

---

## 💻 Sample Output

```
  ╔══════════════════════════════════════════════════════╗
  ║     DecodeLabs Cybersecurity  |  Batch 2026          ║
  ║     Project 2: Basic Encryption & Decryption         ║
  ║     "We don't shift letters; we shift integers."     ║
  ╚══════════════════════════════════════════════════════╝

  [1] Caesar Cipher     — Encrypt & Decrypt
  [2] Brute Force Demo  — Show all 25 decryptions
  [3] Vigenère Cipher   — Bonus mode
  [q] Quit

  Enter text to encrypt: Hello, World!
  Enter shift key [1–25]: 3

  ══════════════════════════════════════════════════════════
  DecodeLabs | Cryptographic Report — Caesar Cipher
  ══════════════════════════════════════════════════════════
  Algorithm          : Caesar Cipher
  Shift Key (n)      : 3
  ──────────────────────────────────────────────────────────
  [INPUT]  Plaintext  : Hello, World!
  [OUTPUT] Ciphertext : Khoor, Zruog!
  [CHECK]  Decrypted  : Hello, World!
  ──────────────────────────────────────────────────────────
  Symmetry test       : ✓  ROUND-TRIP VERIFIED
  ══════════════════════════════════════════════════════════
```

---

## 🔓 Security Analysis

### Why Caesar Is Broken

Caesar Cipher has **only 25 possible keys**. A brute-force attack that tries all of them runs in microseconds. Beyond that, it preserves the **frequency distribution** of the original language — the letter `E` is still the most common character in the ciphertext, just under a different symbol. This makes it trivially breakable with frequency analysis, even without knowing the key.

```
[Brute Force on "Khoor"]
[ 1] Jgnnq
[ 2] Ifmmp
[ 3] Hello  ← recovered instantly
[ 4] Gdkkn
...
```

### The Real-World Standard

Modern encryption (AES-256) solves both problems:
- Key space: **2²⁵⁶** — computationally infeasible to brute-force
- Confusion + diffusion — no frequency patterns survive

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- No external libraries required

### Installation

```bash
git clone https://github.com/Shovon30/DecodeLabs-Internship-Project2.git
cd DecodeLabs-Internship-Project2
```

### Run

```bash
python3 encryption_tool.py
```

---

## 🧪 Test Cases

| Input | Shift | Ciphertext | Decrypted | Verified |
|---|---|---|---|---|
| `Hello, World!` | 3 | `Khoor, Zruog!` | `Hello, World!` | ✅ |
| `A` | 3 | `D` | `A` | ✅ |
| `Y` | 3 | `B` | `Y` | ✅ (wrap) |
| `Z` | 1 | `A` | `Z` | ✅ (wrap) |
| `Abc 123!` | 3 | `Def 123!` | `Abc 123!` | ✅ (edge) |
| `Hello` (Vigenère, key: KEY) | — | `Rijvs` | `Hello` | ✅ |

---

## 📁 Project Structure

```
DecodeLabs-Internship-Project2/
│
├── encryption_tool.py    # Main program
└── README.md             # Project documentation
```

---

## 🔗 Project Chain

This project is part of a sequential internship track:

| Project | Focus | Status |
|---|---|---|
| Project 1 — Password Strength Checker | Validation & Entropy | ✅ Completed |
| Project 2 — Basic Encryption & Decryption | Cryptography & Confidentiality | ✅ Completed |
| Project 3 — Hashing & Encryption (Argon2id) | Secure Storage | 🔜 Next |

Project 1 established the **Gatekeeper Rule**: validate before you encrypt. Project 2 implements the encryption layer itself. Project 3 will secure that data at rest using production-grade hashing.

---

## 👤 Author

**Shovon** — Cybersecurity Track Intern
DecodeLabs Industrial Training Kit | Batch 2026

---

## 📜 License

Built as part of the DecodeLabs Internship Program for educational and portfolio purposes.
