from flask import Flask, request, jsonify
import random
import re

app = Flask(__name__)

MAX_LENGTH = 15

THEMES = {
    "nature": {
        "prefixes": ["River", "Forest", "Stone", "Cedar", "Maple"],
        "suffixes": ["trail", "breeze", "ridge", "grove", "leaf"]
    },
    "space": {
        "prefixes": ["Nova", "Cosmo", "Orbit", "Stellar", "Astro"],
        "suffixes": ["drift", "spark", "pulse", "beam", "core"]
    },
    "tech": {
        "prefixes": ["Cyber", "Quantum", "Data", "Code", "Nano"],
        "suffixes": ["node", "matrix", "byte", "logic", "system"]
    },
    "sports": {
        "prefixes": ["Swift", "Turbo", "Power", "Rapid", "Blaze"],
        "suffixes": ["runner", "striker", "dash", "kick", "drive"]
    },
    "food": {
        "prefixes": ["Honey", "Cocoa", "Berry", "Peach", "Sugar"],
        "suffixes": ["bite", "slice", "treat", "snack", "mix"]
    }
}

# Basic profanity filter
BANNED_WORDS = {
    "badword1",
    "badword2",
    "badword3"
}


def clean_text(text):
    """Remove characters other than letters, numbers, and underscores."""
    return re.sub(r'[^a-zA-Z0-9_]', '', text)


def trim_name(name):
    """Limit the generated name to the maximum allowed length."""
    return name[:MAX_LENGTH]


def contains_profanity(name):
    """Check whether the generated name contains a banned word."""
    lowered = name.lower()
    return any(bad_word in lowered for bad_word in BANNED_WORDS)


def build_name(theme):
    """
    Build a username from the selected theme.
    Tries several combinations and returns the first valid result.
    """
    prefix = random.choice(THEMES[theme]["prefixes"])
    suffix = random.choice(THEMES[theme]["suffixes"])
    number = str(random.randint(1, 99))

    possible_names = [
        f"{prefix}{suffix}",
        f"{prefix}{suffix}{number}",
        f"{prefix}_{suffix}",
        f"{prefix}{number}",
        f"{suffix}{number}"
    ]

    random.shuffle(possible_names)

    for name in possible_names:
        cleaned_name = clean_text(name)
        final_name = trim_name(cleaned_name)

        if final_name and not contains_profanity(final_name):
            return final_name

    return "user123"


@app.route("/generate_name", methods=["POST"])
def generate_name():
    """
    Generate a username based on an optional theme.
    If no theme is provided, default to 'tech'.
    """
    data = request.get_json(silent=True) or {}
    theme = data.get("theme", "tech").lower()

    if theme not in THEMES:
        return jsonify({
            "error": "Unsupported theme",
            "supported_themes": list(THEMES.keys())
        }), 400

    generated_name = build_name(theme)

    return jsonify({
        "generated_name": generated_name,
        "theme_used": theme,
        "max_length": MAX_LENGTH,
        "supported_themes": list(THEMES.keys())
    }), 200


@app.route("/", methods=["GET"])
def home():
    """Simple home route so users know the microservice is running."""
    return jsonify({
        "message": "Username Generator Microservice is running",
        "endpoint": "/generate_name",
        "method": "POST",
        "supported_themes": list(THEMES.keys())
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5002)