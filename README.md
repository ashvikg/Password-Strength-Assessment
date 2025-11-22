Overview

A small, standalone Python module that assesses password strength using a mix of heuristic checks (length, uppercase/lowercase, digits, special chars) and an entropy-based estimate. Returns a structured result (score, verdict, entropy, checks, feedback) suitable for CLI use, automation, or integration into other Python projects.

Features

Score from 0–100 and human-friendly verdict (Very weak → Very strong).

Entropy estimate in bits using length × log2(charset_size).

Individual boolean checks (length thresholds, has_upper, has_lower, has_digit, has_special).

Actionable feedback suggestions.

Small, dependency-free single-file module (password_strength.py).

CLI demo mode when run as script and programmatic API for integration.

Requirements

Python 3.8+ (should work on 3.7 but 3.8+ recommended)

No third-party packages required

Installation

Download password_strength.py into your project directory.

(Optional) Make it available as a module in your environment (e.g., place in your project or install into a virtualenv).

Usage
As a script (interactive demo)
python password_strength.py
# Type passwords at the prompt. Press Enter on an empty line to exit.

Programmatic API
from password_strength import assess_password

result = assess_password("Example123!")
print(result["score"])        # integer 0..100
print(result["verdict"])      # "Weak", "Strong", etc.
print(result["entropy_bits"]) # float
print(result["feedback"])     # list of suggestions

Example output
{
  "password": "Example123!",
  "length": 11,
  "score": 63,
  "verdict": "Strong",
  "entropy_bits": 57.17,
  "checks": {
    "length_8+": true,
    "length_12+": false,
    "has_upper": true,
    "has_lower": true,
    "has_digit": true,
    "has_special": true
  },
  "feedback": [
    "Make the password longer (12+ characters recommended).",
    "Good password — keep it unique per account and consider using a password manager."
  ]
}

Design & Scoring Notes

Charset size is estimated from which character classes appear:

lowercase = 26, uppercase = 26, digits = 10, specials ≈ 32

Entropy estimate: length × log2(charset_size) (a Shannon-style upper bound).

Score combines length band points, character variety, and a small entropy bonus.

The logic favors longer passphrases; you can change thresholds in the source.

Integrations & Extensions

Add a CLI flag to output JSON (easy to add argparse).

Expose as a Flask endpoint for web-based checks.

Hook into registration forms to provide server-side verification (always perform server-side check — never trust only client-side).

Security Considerations

Never log or store user passwords in plaintext. If you must persist examples for testing, use safe, synthetic data.

Use secure channels (HTTPS) if transmitting passwords to a server for assessment.

Prefer assessing strength client-side (using the HTML meter) and performing only server-side checks that don't persist or log the raw password.

For high-value accounts recommend passphrases (4+ random words) or a password manager.

Tests

Add unit tests for:

Various length bands

Each character-class detection

Entropy calculations with mocked charset sizes

Use pytest or unittest to automate tests.

License

MIT License — see LICENSE (or add license text).

Contribution

Contributions and improvements welcome. Open issues or send a PR to:

Improve scoring heuristics

Add JSON CLI output

Add localization for feedback messages