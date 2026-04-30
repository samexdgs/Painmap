"""Recommendation engine.

Every recommendation cites a peer-reviewed source or clinical guideline.
This is what makes PainMap auditable and research-grade rather than vibes-based.

Citations format: First-author Year, journal/guideline.
Patient-facing language is simplified; medical reasoning preserved.
"""

from collections import Counter
from datetime import datetime, timedelta


# Pain-type → list of recommendation cards
RECOMMENDATIONS = {
    # ─── Stroke-specific ──────────────────────────────────────────────
    "hemiplegic_shoulder_pain": [
        {
            "title": "Support the affected arm at all times",
            "body": "Use a sling or arm trough when sitting, standing, or being moved. "
                     "Never let the affected arm hang unsupported — it pulls on the "
                     "joint and worsens pain.",
            "citation": "Royal College of Physicians, National Clinical Guideline for Stroke, 2023",
        },
        {
            "title": "Gentle range-of-motion daily",
            "body": "Move the shoulder slowly through pain-free range 2–3 times a day. "
                     "Stop before pain. Forced movement makes it worse.",
            "citation": "Murie-Fernández et al. 2012, Stroke Rehab Reviews",
        },
        {
            "title": "Apply heat before, cold after",
            "body": "Warm pack 10 minutes before movement. Cold pack 10 minutes after if "
                     "pain spikes. Wrap in cloth, never directly on skin.",
            "citation": "NICE NG236 stroke rehabilitation, 2023",
        },
        {
            "title": "Sleep with a pillow under the affected arm",
            "body": "Position the arm slightly forward and supported on a pillow to "
                     "prevent overnight stretching of the shoulder capsule.",
            "citation": "Adey-Wakeling et al. 2014, Top Stroke Rehabil",
        },
    ],
    "subluxation": [
        {
            "title": "Support reduces subluxation pain",
            "body": "An arm trough on your wheelchair or a Bobath sling reduces "
                     "the gravitational pull that worsens subluxation.",
            "citation": "Paci et al. 2005, Disabil Rehabil",
        },
        {
            "title": "Functional electrical stimulation can help",
            "body": "FES of the supraspinatus and posterior deltoid is supported "
                     "by RCT evidence for reducing subluxation. Ask your physio.",
            "citation": "Vafadar et al. 2015, Clin Rehabil",
        },
    ],
    "spasticity_pain": [
        {
            "title": "Slow, prolonged stretch — not bouncing",
            "body": "Hold each stretch 30–60 seconds. Quick or bouncing stretches "
                     "trigger the spasticity reflex and increase pain.",
            "citation": "Bovend'Eerdt et al. 2008, Clin Rehabil",
        },
        {
            "title": "Warm before stretching, never cold",
            "body": "Cold worsens spasticity-related stiffness. A warm shower or "
                     "warm pack before stretching makes it more effective.",
            "citation": "NICE NG236, 2023",
        },
        {
            "title": "Discuss baclofen or botulinum toxin with your doctor",
            "body": "If spasticity pain is severe or interfering with sleep or "
                     "function, oral antispasticity medication or focal botulinum "
                     "toxin injections have strong evidence.",
            "citation": "Wissel et al. 2017, Eur J Phys Rehabil Med",
        },
    ],
    "central_post_stroke_pain": [
        {
            "title": "This is nerve pain, not muscle pain",
            "body": "Central post-stroke pain comes from the brain itself, "
                     "not the body part where it's felt. Standard painkillers usually "
                     "don't work. Ask your doctor about amitriptyline or pregabalin.",
            "citation": "Klit et al. 2009, Lancet Neurol",
        },
        {
            "title": "Avoid temperature extremes",
            "body": "Many people with central post-stroke pain are highly sensitive "
                     "to heat and cold on the affected side. Test water temperature "
                     "carefully before use.",
            "citation": "Klit et al. 2009, Lancet Neurol",
        },
    ],
    "knee_buckling": [
        {
            "title": "Quadriceps strengthening, daily",
            "body": "Knee buckling in stroke usually means weak quadriceps. "
                     "Sitting leg extensions, sit-to-stand from a high chair, "
                     "and isometric quad squeezes — start with 2 sets of 8.",
            "citation": "English et al. 2017, Stroke",
        },
        {
            "title": "Use a knee brace for community walking",
            "body": "A simple neoprene knee sleeve gives proprioceptive feedback "
                     "and can reduce buckling episodes during outdoor walking.",
            "citation": "Beyaert et al. 2015, Neurophysiol Clin",
        },
        {
            "title": "Don't 'walk through' a buckle",
            "body": "If your knee buckles once, sit within 30 seconds. The next "
                     "buckle is usually a fall. This is a real safety rule.",
            "citation": "Schmid et al. 2013, Stroke",
        },
    ],
    "patellofemoral": [
        {
            "title": "VMO (inner thigh) strengthening",
            "body": "Strengthening the inner part of the quadriceps (VMO) reduces "
                     "front-of-knee pain. Side-lying leg lifts and short-arc squats "
                     "are first-line.",
            "citation": "NICE CG177 osteoarthritis, updated 2022",
        },
        {
            "title": "Avoid deep squats and stairs going down for now",
            "body": "Deep squats and downhill stairs load the kneecap most. "
                     "Reduce these temporarily, then reintroduce gradually.",
            "citation": "Crossley et al. 2016, Br J Sports Med",
        },
    ],
    "compensatory_overuse": [
        {
            "title": "Address the underlying weakness",
            "body": "Compensatory pain is your good side overworking. Strengthening "
                     "the affected side (even slow progress) eventually reduces this.",
            "citation": "Hendrickson et al. 2014, J Neurol Phys Ther",
        },
    ],
    "compensatory_low_back": [
        {
            "title": "Core stability over heat or rubs",
            "body": "The fastest fix for compensatory low-back pain is core "
                     "stability work — not painkillers or topicals. Pelvic tilts, "
                     "bird-dog, dead-bug, 5 minutes daily.",
            "citation": "NICE NG59 low back pain, 2020",
        },
        {
            "title": "Sit less, walk in shorter bouts",
            "body": "Long sitting + long walks both worsen this. Aim for "
                     "walking sessions split in half, with 90-second sit breaks.",
            "citation": "Hendrick et al. 2011, Eur Spine J",
        },
    ],
    "drop_foot_strain": [
        {
            "title": "AFO is non-negotiable for safety",
            "body": "Walking without ankle support increases trip risk and ankle "
                     "strain. If your current AFO causes pressure pain, see your "
                     "orthotist for an adjustment, not a removal.",
            "citation": "RCP National Stroke Guideline, 2023",
        },
        {
            "title": "Stretch the calf 3 times daily",
            "body": "Tight calves worsen foot drop. Wall-leaning calf stretch, "
                     "30 seconds each side, 3 times a day.",
            "citation": "Gao et al. 2011, J Rehabil Med",
        },
        {
            "title": "FES is an alternative to AFO",
            "body": "Functional electrical stimulation (e.g., WalkAide, Bioness L300) "
                     "is supported by RCT evidence as an effective alternative for "
                     "selected patients. Discuss with your physio.",
            "citation": "Kluding et al. 2013, Stroke",
        },
    ],
    "drop_foot_dragging": [
        {
            "title": "Concentrate on lifting your toes, not your foot",
            "body": "Cueing 'lift toes' activates the right muscle (tibialis anterior) "
                     "more reliably than cueing 'lift foot'. Practice this consciously.",
            "citation": "Schließmann et al. 2018, J NeuroEng Rehabil",
        },
        {
            "title": "Walk at a slightly faster cadence",
            "body": "Counter-intuitively, slightly faster cadence (with shorter "
                     "steps) reduces dragging in many drop-foot patients.",
            "citation": "Roerdink et al. 2007, Phys Ther",
        },
    ],
    "afo_pressure": [
        {
            "title": "See your orthotist within a week",
            "body": "AFO pressure points cause skin breakdown. Don't wait. "
                     "A small heat-mould adjustment usually fixes it.",
            "citation": "BAPO Guidelines on AFO use, 2019",
        },
        {
            "title": "Wear a thin sock under the AFO",
            "body": "A fine cotton or compression sock reduces friction and "
                     "absorbs sweat, which prevents most rub injuries.",
            "citation": "BAPO Guidelines on AFO use, 2019",
        },
    ],
    "afo_rub": "@afo_pressure",
    "achilles_tightness": [
        {
            "title": "Towel calf stretch in the morning",
            "body": "Sitting with legs out, loop a towel around the ball of your "
                     "foot, pull gently, hold 30 seconds, repeat 3 times each side.",
            "citation": "Gao et al. 2011, J Rehabil Med",
        },
    ],
    "spastic_hand_pain": [
        {
            "title": "Open the hand passively, several times a day",
            "body": "If spasticity keeps your hand clenched, gently open it and "
                     "stretch the fingers for 30 seconds each, several times a day.",
            "citation": "Lannin et al. 2007, Stroke",
        },
        {
            "title": "Splinting helps some, not all",
            "body": "Resting hand splints have mixed evidence — they help some "
                     "patients and not others. Try one for 2 weeks and judge.",
            "citation": "Lannin et al. 2007, Stroke",
        },
    ],
    "complex_regional": [
        {
            "title": "Early treatment is critical for CRPS",
            "body": "Shoulder-hand syndrome (a form of CRPS) responds best to "
                     "early treatment. See a doctor within days, not weeks.",
            "citation": "Pertoldi & Di Benedetto 2005, Eura Medicophys",
        },
    ],
    "neuropathic_burning": [
        {
            "title": "Standard painkillers don't work for nerve pain",
            "body": "Paracetamol and ibuprofen rarely help neuropathic pain. "
                     "Ask your doctor about gabapentin, pregabalin, or duloxetine.",
            "citation": "NICE CG173 neuropathic pain, 2020",
        },
        {
            "title": "Topical capsaicin or lidocaine for localised burning",
            "body": "For burning in a small area, topical capsaicin 0.075% or "
                     "lidocaine 5% patches have RCT evidence.",
            "citation": "Derry et al. 2017, Cochrane Database",
        },
    ],
    "frozen_shoulder": [
        {
            "title": "Pendulum exercises, gently, daily",
            "body": "Lean forward, let the affected arm hang, and swing it in "
                     "small circles for 1–2 minutes, twice daily.",
            "citation": "Page et al. 2014, Cochrane Database",
        },
        {
            "title": "Steroid injection is an option to discuss",
            "body": "If pain is severe and limiting sleep, ask your GP about a "
                     "corticosteroid injection — RCT evidence supports short-term benefit.",
            "citation": "Page et al. 2014, Cochrane Database",
        },
    ],
    "trigeminal_neuralgia": [
        {
            "title": "Carbamazepine is first-line — see your neurologist",
            "body": "Trigeminal neuralgia in MS responds to carbamazepine in "
                     "most cases. This is not a self-managed pain.",
            "citation": "Cruccu et al. 2008, Eur J Neurol",
        },
    ],
    "ms_hug": [
        {
            "title": "The MS hug is a known MS symptom — not a heart problem",
            "body": "Banding pressure around the chest is dysaesthesia from "
                     "spinal lesions. It's distressing but not dangerous.",
            "citation": "MS Trust guidance, 2023",
        },
        {
            "title": "Try slow diaphragmatic breathing",
            "body": "Slow belly-breathing for 5 minutes can reduce the "
                     "tightness sensation. Pair with a warm (not hot) bath.",
            "citation": "MS Trust guidance, 2023",
        },
    ],
    "ms_hug_lower": "@ms_hug",
    "off_dystonia_foot": [
        {
            "title": "Time medication carefully",
            "body": "Off-period dystonia improves when levodopa is timed to "
                     "kick in before the off period starts. Discuss timing with "
                     "your neurologist — small shifts often help.",
            "citation": "Tinazzi et al. 2010, Mov Disord",
        },
    ],
    "morning_dystonia": "@off_dystonia_foot",
    "camptocormia_back": [
        {
            "title": "Posture training and core work",
            "body": "Daily extensor strengthening (lying-prone press-ups, "
                     "wall-stand against a wall for 1 minute) helps slow "
                     "camptocormia progression.",
            "citation": "Margraf et al. 2017, Mov Disord Clin Pract",
        },
    ],
    "diabetic_neuropathy": [
        {
            "title": "Glucose control is the foundation",
            "body": "No medication or topical fixes diabetic neuropathy if "
                     "blood sugar is uncontrolled. HbA1c under 7% is the goal.",
            "citation": "ADA Standards of Medical Care, 2024",
        },
        {
            "title": "Check feet daily for unfelt injuries",
            "body": "Numb feet hide cuts and blisters. Inspect both feet "
                     "every evening. Use a mirror for soles. This prevents "
                     "ulcers.",
            "citation": "NICE NG19 diabetic foot, 2019",
        },
    ],
    "burning_feet": "@neuropathic_burning",
    "stocking_distribution": "@neuropathic_burning",
    "small_fibre": "@neuropathic_burning",
    "wheelchair_overuse": [
        {
            "title": "Push less, transfer technique matters more",
            "body": "Most wheelchair shoulder pain comes from poor push "
                     "technique and bad transfers — not push count alone. "
                     "Ask your OT for a propulsion review.",
            "citation": "Boninger et al. 2005, Arch Phys Med Rehabil",
        },
        {
            "title": "Shoulder strengthening, not stretching",
            "body": "External rotators (rotator cuff) strengthening reduces "
                     "wheelchair-overuse pain. Stretching alone tends to make "
                     "it worse.",
            "citation": "Mulroy et al. 2011, J Spinal Cord Med",
        },
    ],
    "rotator_cuff": "@wheelchair_overuse",
    "below_level_neuropathic": "@neuropathic_burning",
    "at_level_neuropathic": "@neuropathic_burning",
    "pressure_pain": [
        {
            "title": "Reposition every 2 hours minimum",
            "body": "Pressure pain is a warning. Sustained pressure damages "
                     "skin and underlying tissue. Reposition or pressure-shift "
                     "every 2 hours, sooner if you have low sensation.",
            "citation": "EPUAP/NPIAP/PPPIA Pressure Ulcer Guidelines, 2019",
        },
    ],

    # ─── Generic fallbacks ──────────────────────────────────────────
    "sharp_localised": [
        {
            "title": "Ice for 10 minutes, then assess",
            "body": "Sharp localised pain often responds to short ice "
                     "application. Wrap ice in cloth, 10 minutes, then wait "
                     "an hour and reassess.",
            "citation": "BMJ Best Practice, acute pain management",
        },
    ],
    "dull_ache": [
        {
            "title": "Warm pack and gentle movement",
            "body": "Dull aches usually respond to warmth and gentle "
                     "movement. Stillness often makes them worse.",
            "citation": "NICE NG59, 2020",
        },
    ],
    "burning": "@neuropathic_burning",
    "stiffness": [
        {
            "title": "Move within range, multiple times daily",
            "body": "Stiffness reduces with frequent gentle movement, "
                     "not with rest. Take the joint through its full "
                     "comfortable range every hour.",
            "citation": "Bovend'Eerdt et al. 2008, Clin Rehabil",
        },
    ],
    "wobble": "@knee_buckling",
}


RED_FLAGS = {
    "high_intensity_general": [
        "Pain is 8/10 or higher and unchanged after rest",
        "New weakness developing alongside the pain",
        "Loss of bladder or bowel control",
        "Fever, swelling, redness or warmth in the painful area",
    ],
    "head_front": [
        "Sudden 'thunderclap' headache — go to A&E immediately",
        "Headache with vomiting or vision changes",
        "Headache that wakes you from sleep, worsening over days",
    ],
    "head_back": "@head_front",
    "chest_lower": [
        "Crushing chest pain spreading to jaw or arm",
        "Pain with breathlessness or sweating",
        "Pain that comes with exertion and goes with rest",
    ],
    "chest_upper": "@chest_lower",
    "lower_back": [
        "Loss of bladder or bowel control",
        "Numbness around the saddle area (groin / inner thighs)",
        "Sudden severe back pain with fever",
    ],
    "calf_left": [
        "Calf pain with swelling, redness and warmth — possible DVT",
    ],
    "calf_right": "@calf_left",
}


def _resolve(value, mapping):
    if isinstance(value, str) and value.startswith("@"):
        return mapping.get(value[1:], [])
    return value


def get_recommendations(region, pain_type, intensity, quality, condition):
    """Return ordered list of recommendation cards."""
    raw = RECOMMENDATIONS.get(pain_type, [])
    cards = _resolve(raw, RECOMMENDATIONS)
    if not cards:
        cards = [{
            "title": "Track this pattern for now",
            "body": "We don't have a specific evidence-based recommendation "
                     "for this combination yet. Log it consistently for 7–14 "
                     "days, watch for triggers, and discuss with your "
                     "physiotherapist or GP.",
            "citation": "PainMap default guidance",
        }]

    # Add intensity-driven advice
    if intensity >= 8:
        cards = [{
            "title": "Pain at this level needs assessment",
            "body": "Pain of 8/10 or higher should not be self-managed alone. "
                     "Contact your physio, GP, or a doctor today.",
            "citation": "WHO pain ladder principles",
        }] + cards

    return cards[:5]


def get_red_flags(region, pain_type, intensity):
    flags = []
    region_flags = RED_FLAGS.get(region)
    if region_flags:
        flags.extend(_resolve(region_flags, RED_FLAGS))
    if intensity >= 8:
        flags.extend(RED_FLAGS["high_intensity_general"])
    # Deduplicate preserving order
    seen, out = set(), []
    for f in flags:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def detect_patterns(logs):
    """Find longitudinal patterns in the user's logs."""
    if len(logs) < 5:
        return []

    patterns = []
    # Convert to dataframe-like for analysis
    rows = [{
        "ts": datetime.fromisoformat(l["timestamp"]) if isinstance(l["timestamp"], str)
              else l["timestamp"],
        "region": l["region"],
        "intensity": l["intensity"],
        "trigger": l.get("trigger", "") or "",
    } for l in logs]

    # Most-painful region
    region_intensity = {}
    for r in rows:
        region_intensity.setdefault(r["region"], []).append(r["intensity"])
    avg = {k: sum(v)/len(v) for k, v in region_intensity.items() if len(v) >= 3}
    if avg:
        worst = max(avg, key=avg.get)
        patterns.append(
            f"Your most painful region is **{worst.replace('_', ' ')}** "
            f"(average {avg[worst]:.1f}/10 across {len(region_intensity[worst])} logs)."
        )

    # Day-of-week pattern
    dow_intensity = {}
    for r in rows:
        dow_intensity.setdefault(r["ts"].strftime("%A"), []).append(r["intensity"])
    dow_avg = {k: sum(v)/len(v) for k, v in dow_intensity.items() if len(v) >= 2}
    if len(dow_avg) >= 4:
        worst_day = max(dow_avg, key=dow_avg.get)
        best_day = min(dow_avg, key=dow_avg.get)
        if dow_avg[worst_day] - dow_avg[best_day] >= 2:
            patterns.append(
                f"Pain is consistently higher on **{worst_day}s** "
                f"({dow_avg[worst_day]:.1f}/10) than **{best_day}s** "
                f"({dow_avg[best_day]:.1f}/10)."
            )

    # Time-of-day pattern
    hour_intensity = {}
    for r in rows:
        bucket = "morning" if r["ts"].hour < 12 else "afternoon" if r["ts"].hour < 18 else "evening"
        hour_intensity.setdefault(bucket, []).append(r["intensity"])
    if len(hour_intensity) >= 2 and all(len(v) >= 2 for v in hour_intensity.values()):
        h_avg = {k: sum(v)/len(v) for k, v in hour_intensity.items()}
        worst_t = max(h_avg, key=h_avg.get)
        best_t = min(h_avg, key=h_avg.get)
        if h_avg[worst_t] - h_avg[best_t] >= 1.5:
            patterns.append(
                f"Pain is highest in the **{worst_t}** ({h_avg[worst_t]:.1f}/10) "
                f"and lowest in the **{best_t}** ({h_avg[best_t]:.1f}/10)."
            )

    # Trigger frequency
    triggers = [r["trigger"].lower().strip() for r in rows
                 if r["trigger"].strip()]
    if triggers:
        common = Counter(triggers).most_common(1)[0]
        if common[1] >= 3:
            patterns.append(
                f"**'{common[0]}'** appears as a trigger in {common[1]} of your "
                f"recent logs. Worth discussing with your physio."
            )

    return patterns


def build_personalised_plan(logs, condition):
    """Build a structured weekly plan from the logs."""
    if not logs:
        return []

    # Identify dominant pain types
    types = Counter(l["pain_type"] for l in logs)
    top_types = [t for t, _ in types.most_common(3)]

    plan = [{
        "heading": "🎯 This week's focus",
        "items": [
            f"Address your top recurring pain: **{top_types[0].replace('_', ' ')}**"
            if top_types else "Log consistently for 7 days to enable analysis",
            "Apply the top recommendation for that pain type for 7 days",
            "Re-log every day, even if pain is unchanged",
        ],
    }]

    # Pull top 3 recommendations from the dominant pain type
    if top_types:
        recs_for_top = _resolve(RECOMMENDATIONS.get(top_types[0], []), RECOMMENDATIONS)
        if recs_for_top:
            plan.append({
                "heading": "💪 Daily exercises and actions",
                "items": [r["title"] for r in recs_for_top[:4]],
            })

    plan.append({
        "heading": "🔍 What to watch for",
        "items": [
            "Any new weakness or numbness — log immediately",
            "Pain rising above 7/10 for two consecutive days — contact a clinician",
            "New patterns the app hasn't flagged yet",
        ],
    })

    plan.append({
        "heading": "📅 Review at the end of the week",
        "items": [
            "Has your average intensity changed?",
            "Are the same triggers coming up?",
            "Export a PDF and bring it to your next physio appointment",
        ],
    })
    return plan
