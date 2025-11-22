"""
password_strength.py

Usage:
    python password_strength.py        # runs quick interactive demo
    from password_strength import assess_password

Functions:
    assess_password(password: str) -> dict
"""

import math
import re
from typing import Dict, List

# Character classes
_UPPER = re.compile(r"[A-Z]")
_LOWER = re.compile(r"[a-z]")
_DIGIT = re.compile(r"\d")
_SPECIAL = re.compile(r"[^A-Za-z0-9]")

def _charset_size(password: str) -> int:
    """Estimate character set size based on which classes are present."""
    size = 0
    if _LOWER.search(password): size += 26
    if _UPPER.search(password): size += 26
    if _DIGIT.search(password): size += 10
    if _SPECIAL.search(password):
        # conservative estimate for printable special characters
        size += 32
    return size or 1

def _estimate_entropy_bits(password: str) -> float:
    """Shannon-style estimation: log2(charset_size ** length) = length * log2(charset_size)."""
    charset = _charset_size(password)
    return len(password) * math.log2(charset) if charset > 1 else 0.0

def assess_password(password: str) -> Dict:
    """
    Assess a password and return:
      - score: 0..100
      - verdict: 'Very weak' .. 'Very strong'
      - entropy_bits: estimated bits of entropy
      - checks: dict of individual boolean checks (length, upper, lower, digit, special)
      - feedback: list of human-readable suggestions
    """
    length = len(password)
    checks = {
        "length_8+": length >= 8,
        "length_12+": length >= 12,
        "has_upper": bool(_UPPER.search(password)),
        "has_lower": bool(_LOWER.search(password)),
        "has_digit": bool(_DIGIT.search(password)),
        "has_special": bool(_SPECIAL.search(password)),
    }

    entropy = _estimate_entropy_bits(password)

    # Base scoring from checks
    score = 0
    # length contribution
    if length == 0:
        score = 0
    else:
        # length band points
        if length < 8:
            score += 5
        elif length < 12:
            score += 20
        elif length < 16:
            score += 35
        else:
            score += 45

        # character variety points
        variety = sum([checks["has_upper"], checks["has_lower"], checks["has_digit"], checks["has_special"]])
        score += variety * 12  # up to 48

        # entropy bonus (small)
        if entropy >= 60:
            score += 7
        elif entropy >= 40:
            score += 4
        elif entropy >= 28:
            score += 2

    # clamp 0..100
    score = max(0, min(100, int(round(score))))

    # verdict thresholds
    if score < 20:
        verdict = "Very weak"
    elif score < 40:
        verdict = "Weak"
    elif score < 60:
        verdict = "Moderate"
    elif score < 80:
        verdict = "Strong"
    else:
        verdict = "Very strong"

    # feedback suggestions
    feedback: List[str] = []
    if length < 12:
        feedback.append("Make the password longer (12+ characters recommended).")
    if not checks["has_lower"]:
        feedback.append("Add lowercase letters.")
    if not checks["has_upper"]:
        feedback.append("Add uppercase letters.")
    if not checks["has_digit"]:
        feedback.append("Add digits (0-9).")
    if not checks["has_special"]:
        feedback.append("Add special characters (e.g. ! @ # $ %).")
    if entropy < 28:
        feedback.append("Avoid common words and predictable patterns; consider a 4+ word passphrase or a password manager.")
    if not feedback:
        feedback.append("Good password — keep it unique per account and consider using a password manager.")

    return {
        "password": password,
        "length": length,
        "score": score,
        "verdict": verdict,
        "entropy_bits": round(entropy, 2),
        "checks": checks,
        "feedback": feedback
    }


# Quick demo when run as script
if __name__ == "__main__":
    print("Password Strength Demo — type passwords (empty to exit)\n")
    try:
        while True:
            pw = input("Password> ")
            if pw == "":
                break
            out = assess_password(pw)
            print(f"Score: {out['score']} / 100  — {out['verdict']}")
            print(f"Length: {out['length']}, Entropy ≈ {out['entropy_bits']} bits")
            print("Checks:", ", ".join([k for k, v in out['checks'].items() if v]))
            print("Feedback:")
            for f in out['feedback']:
                print(" -", f)
            print()
    except (KeyboardInterrupt, EOFError):
        print("\nBye")
