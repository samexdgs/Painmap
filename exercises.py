"""Exercise demonstration library.

Maps recommendation card titles → demo content (video link, image, or
inline GIF) so patients can SEE the exercise, not just read about it.

Sources: NHS, American Stroke Association, Royal United Hospitals Bath,
Northern Care Alliance NHS Trust, Flint Rehab. All publicly accessible.
"""

# Map recommendation title (or keyword in title) → demo content
# Each entry: {"video": YouTube URL, "image": optional emoji/symbol,
#               "steps": list of short cues}

DEMOS = {
    # ─── Stretches ─────────────────────────────────────────────────
    "calf": {
        "video": "https://www.youtube.com/watch?v=j4ytUXLf_1w",
        "image": "🦵",
        "steps": [
            "Stand facing a wall, hands at shoulder height",
            "Step one foot back, keeping the heel on the floor",
            "Lean forward gently until you feel a stretch in the calf",
            "Hold 30 seconds, swap legs, repeat 3 times each",
        ],
    },
    "towel calf stretch": {
        "video": "https://www.youtube.com/watch?v=j4ytUXLf_1w",
        "image": "🦵",
        "steps": [
            "Sit with your legs straight in front of you",
            "Loop a towel around the ball of your affected foot",
            "Pull gently toward you until you feel the stretch",
            "Hold 30 seconds, repeat 3 times each side",
        ],
    },
    "pendulum": {
        "video": "https://www.youtube.com/watch?v=8SaDFbZGV0w",
        "image": "💪",
        "steps": [
            "Lean forward, supporting yourself with the unaffected hand",
            "Let the affected arm hang relaxed",
            "Swing it gently in small circles for 30 seconds",
            "Reverse the direction. Repeat 2× daily",
        ],
    },

    # ─── Strengthening ─────────────────────────────────────────────
    "quadriceps strengthening": {
        "video": "https://www.youtube.com/watch?v=GZbfZ033f74",
        "image": "🏋️",
        "steps": [
            "Sit upright on a firm chair, feet flat on the floor",
            "Slowly straighten one knee until leg is fully extended",
            "Hold for 3 seconds, lower slowly",
            "Start with 2 sets of 8 reps, build to 3 sets of 12",
        ],
    },
    "vmo": {
        "video": "https://www.youtube.com/watch?v=lHSTqWb9ck4",
        "image": "🦵",
        "steps": [
            "Lie on your side, lower leg slightly bent",
            "Lift the upper leg to about 30°, slow and controlled",
            "Hold 2 seconds, lower slowly",
            "10 reps each side, build daily",
        ],
    },
    "core stability": {
        "video": "https://www.youtube.com/watch?v=9lH2EzbJpXg",
        "image": "🧘",
        "steps": [
            "Lie on your back, knees bent, feet flat",
            "Tighten your tummy muscles, press lower back into floor",
            "Hold 5 seconds, release, repeat 10 times",
            "Add bird-dog and dead-bug as you progress",
        ],
    },
    "shoulder strengthening": {
        "video": "https://www.youtube.com/watch?v=fXz1jaxMlAQ",
        "image": "💪",
        "steps": [
            "Use a light resistance band or no weight at first",
            "Keep elbow at 90° tucked into your side",
            "Rotate forearm outward against resistance, slow",
            "10–15 reps, twice daily",
        ],
    },
    "extensor strengthening": {
        "video": "https://www.youtube.com/watch?v=hxxtZv2ZeFw",
        "image": "🧘",
        "steps": [
            "Lie face down on a firm surface",
            "Gently push up onto your forearms (sphinx position)",
            "Hold 10 seconds, lower slowly, repeat 8 times",
            "Work toward holding 30 seconds as you build",
        ],
    },

    # ─── Range of motion ───────────────────────────────────────────
    "range of motion": {
        "video": "https://www.youtube.com/watch?v=9P5RdzJqg-A",
        "image": "🤲",
        "steps": [
            "Move the joint slowly through pain-free range",
            "Stop just before pain — never push through",
            "5–10 repetitions, 2–3 times daily",
            "Keep the movement smooth, not jerky",
        ],
    },
    "open the hand": {
        "video": "https://www.youtube.com/watch?v=I6rg4cdqWJU",
        "image": "🖐️",
        "steps": [
            "Use your unaffected hand to gently open the spastic hand",
            "Spread the fingers fully if possible",
            "Hold 30 seconds, release slowly",
            "Repeat 5 times, several times a day",
        ],
    },
    "stretch": {
        "video": "https://www.youtube.com/watch?v=4BOTvaRaDjI",
        "image": "🧘",
        "steps": [
            "Move slowly into the stretched position",
            "Hold 30–60 seconds — never bounce",
            "Breathe normally throughout",
            "Stop if pain sharpens",
        ],
    },

    # ─── Positioning / safety ──────────────────────────────────────
    "support the affected arm": {
        "video": "https://www.youtube.com/watch?v=7v3oMIQEd6E",
        "image": "🤝",
        "steps": [
            "Use a sling or arm trough when sitting or standing",
            "Place a pillow under the arm when lying down",
            "Never let the affected arm hang unsupported",
            "Adjust positioning every 1–2 hours",
        ],
    },
    "sleep with a pillow": {
        "video": None,
        "image": "🛏️",
        "steps": [
            "Lie on your back or unaffected side",
            "Place a pillow under the affected arm, slightly forward",
            "Keep the elbow gently bent, hand higher than elbow",
            "This prevents overnight stretching of the shoulder",
        ],
    },
    "reposition every 2 hours": {
        "video": None,
        "image": "⏰",
        "steps": [
            "Set an alarm if needed",
            "Shift weight in chair: forward, side, back",
            "If in bed, change position fully every 2 hours",
            "Inspect skin during repositioning",
        ],
    },

    # ─── Sit-to-stand / functional ────────────────────────────────
    "sit-to-stand": {
        "video": "https://www.youtube.com/watch?v=xIwl4Mbij_Y",
        "image": "🪑",
        "steps": [
            "Sit on a firm, high chair, feet flat behind your knees",
            "Lean forward (nose over toes), push through both feet",
            "Stand fully, pause, lower slowly with control",
            "5 reps to start, build up to 10",
        ],
    },

    # ─── Heat / cold ───────────────────────────────────────────────
    "heat": {
        "video": None,
        "image": "♨️",
        "steps": [
            "Wrap a warm pack in a thin cloth — never directly on skin",
            "Apply for 10 minutes before exercise",
            "Remove and check skin colour every 5 minutes",
            "Skip if you have reduced sensation in that area",
        ],
    },
    "ice": {
        "video": None,
        "image": "❄️",
        "steps": [
            "Wrap ice in a damp cloth — never directly on skin",
            "Apply 10 minutes maximum",
            "Wait at least one hour before reapplying",
            "Stop if skin turns very red or numb",
        ],
    },

    # ─── Walking / cadence ─────────────────────────────────────────
    "concentrate on lifting your toes": {
        "video": "https://www.youtube.com/watch?v=zw4_YwRGOCs",
        "image": "🦶",
        "steps": [
            "Sit with feet flat, focus on lifting toes only",
            "Keep heel on floor; lift toes high 10 times",
            "Then practice with each step you take walking",
            "The cue 'lift toes' fires the right muscle",
        ],
    },
    "faster cadence": {
        "video": None,
        "image": "🚶",
        "steps": [
            "Take shorter, quicker steps — not longer ones",
            "Use a metronome app if helpful (start at 90 bpm)",
            "Match each step to the beat",
            "Counter-intuitive but reduces dragging",
        ],
    },

    # ─── Breathing ─────────────────────────────────────────────────
    "diaphragmatic breathing": {
        "video": "https://www.youtube.com/watch?v=JJTtRT1FSBE",
        "image": "🫁",
        "steps": [
            "Place one hand on chest, one on belly",
            "Breathe in slowly through nose — belly rises, chest still",
            "Breathe out slowly through pursed lips",
            "5 minutes daily, especially during MS hug",
        ],
    },

    # ─── Posture training ─────────────────────────────────────────
    "posture training": {
        "video": "https://www.youtube.com/watch?v=d3ZZc0ZSJNc",
        "image": "🧍",
        "steps": [
            "Stand with back against a wall, heels 4 inches out",
            "Push head, shoulders, and hips back to the wall",
            "Hold 60 seconds, breathe normally",
            "Repeat 3 times daily",
        ],
    },
}


def find_demo(title: str) -> dict | None:
    """Find the most relevant demo for a recommendation title."""
    if not title:
        return None
    t = title.lower()
    # Try exact and fuzzy matching against demo keys
    for key, demo in DEMOS.items():
        if key in t:
            return demo
    return None
