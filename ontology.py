"""Pain ontology — neurological-condition-aware pain types per body region.

Sources cited per pain type:
  - IASP (International Association for the Study of Pain) classifications
  - Klit et al. 2009 (post-stroke central pain)
  - O'Connor & Dworkin 2009 (neuropathic pain)
  - NICE NG59, NG177 (neurological pain guidelines)
  - Treede et al. 2019 (chronic pain ICD-11)
"""

# Generic pain types available everywhere as fallback
GENERIC = [
    {"key": "sharp_localised", "label": "Sharp, localised pain"},
    {"key": "dull_ache", "label": "Dull ache"},
    {"key": "throbbing", "label": "Throbbing pain"},
    {"key": "burning", "label": "Burning sensation"},
    {"key": "tingling", "label": "Tingling / pins and needles"},
    {"key": "numbness", "label": "Numbness"},
    {"key": "stiffness", "label": "Stiffness"},
    {"key": "spasm", "label": "Muscle spasm"},
    {"key": "weakness_only", "label": "Weakness without pain"},
    {"key": "wobble", "label": "Instability / wobble"},
]

# Condition × region → curated list of likely pain types
ONTOLOGY = {
    # ───────────────────── STROKE ─────────────────────
    "stroke": {
        "shoulder_left_front": [
            {"key": "hemiplegic_shoulder_pain",
              "label": "Hemiplegic shoulder pain (post-stroke)"},
            {"key": "subluxation",
              "label": "Shoulder subluxation pain"},
            {"key": "spasticity_pain",
              "label": "Spasticity-driven pain"},
            {"key": "frozen_shoulder",
              "label": "Frozen shoulder (adhesive capsulitis)"},
            {"key": "central_post_stroke_pain",
              "label": "Central post-stroke pain"},
        ],
        "shoulder_right_front": "@shoulder_left_front",
        "shoulder_left_back": "@shoulder_left_front",
        "shoulder_right_back": "@shoulder_left_front",

        "knee_left": [
            {"key": "knee_buckling", "label": "Knee buckling / wobble"},
            {"key": "patellofemoral",
              "label": "Patellofemoral pain (front of knee)"},
            {"key": "compensatory_overuse",
              "label": "Compensatory overuse pain"},
            {"key": "osteoarthritis",
              "label": "Osteoarthritis pain"},
            {"key": "central_post_stroke_pain",
              "label": "Central post-stroke pain"},
        ],
        "knee_right": "@knee_left",

        "lower_back": [
            {"key": "compensatory_low_back",
              "label": "Compensatory low-back pain"},
            {"key": "muscular_strain",
              "label": "Muscular strain"},
            {"key": "spasticity_pain",
              "label": "Spasticity-driven pain"},
            {"key": "central_post_stroke_pain",
              "label": "Central post-stroke pain"},
        ],

        "ankle_left": [
            {"key": "drop_foot_strain",
              "label": "Foot-drop related ankle strain"},
            {"key": "afo_pressure",
              "label": "AFO pressure / discomfort"},
            {"key": "spasticity_pain",
              "label": "Calf spasticity referred pain"},
            {"key": "achilles_tightness",
              "label": "Achilles tightness"},
            {"key": "inversion_sprain",
              "label": "Inversion sprain history"},
        ],
        "ankle_right": "@ankle_left",

        "foot_left_top": [
            {"key": "drop_foot_dragging",
              "label": "Drop-foot related dragging pain"},
            {"key": "neuropathic_burning",
              "label": "Neuropathic burning"},
            {"key": "afo_rub",
              "label": "AFO rub / blister pain"},
            {"key": "footwear_pressure",
              "label": "Footwear pressure point"},
        ],
        "foot_right_top": "@foot_left_top",

        "hand_left": [
            {"key": "spastic_hand_pain",
              "label": "Spastic hand pain (clenched)"},
            {"key": "complex_regional",
              "label": "CRPS / shoulder-hand syndrome"},
            {"key": "neuropathic_burning",
              "label": "Neuropathic burning"},
            {"key": "joint_stiffness",
              "label": "Joint stiffness"},
        ],
        "hand_right": "@hand_left",

        "head_front": [
            {"key": "tension_headache", "label": "Tension headache"},
            {"key": "post_stroke_headache",
              "label": "Post-stroke headache"},
            {"key": "central_post_stroke_pain",
              "label": "Central post-stroke pain (face)"},
        ],
        "head_back": "@head_front",
    },

    # ───────────────────── MULTIPLE SCLEROSIS ─────────────────────
    "multiple_sclerosis": {
        "face": [
            {"key": "trigeminal_neuralgia",
              "label": "Trigeminal neuralgia (MS-related)"},
            {"key": "ms_facial_pain",
              "label": "MS facial pain"},
        ],
        "lower_back": [
            {"key": "ms_back_pain", "label": "MS-related back pain"},
            {"key": "spasticity_pain", "label": "Spasticity pain"},
            {"key": "compensatory_low_back",
              "label": "Compensatory low-back pain"},
        ],
        "thigh_left_front": [
            {"key": "lhermittes_sign",
              "label": "L'hermitte's sign (electric-shock)"},
            {"key": "spasticity_pain", "label": "Thigh spasticity pain"},
            {"key": "neuropathic_burning",
              "label": "Neuropathic burning"},
        ],
        "thigh_right_front": "@thigh_left_front",
        "shin_left": [
            {"key": "ms_hug_lower",
              "label": "MS hug (banding) — lower variant"},
            {"key": "neuropathic_burning",
              "label": "Neuropathic burning"},
            {"key": "spasticity_pain", "label": "Calf spasticity pain"},
        ],
        "shin_right": "@shin_left",
        "chest_lower": [
            {"key": "ms_hug",
              "label": "MS hug (banding around chest)"},
            {"key": "intercostal_neuralgia",
              "label": "Intercostal neuralgia"},
        ],
    },

    # ───────────────────── PARKINSON'S ─────────────────────
    "parkinsons": {
        "shoulder_left_front": [
            {"key": "parkinsonian_shoulder",
              "label": "Parkinsonian shoulder pain (early sign)"},
            {"key": "frozen_shoulder",
              "label": "Frozen shoulder"},
            {"key": "rigidity_pain", "label": "Rigidity-related pain"},
        ],
        "shoulder_right_front": "@shoulder_left_front",
        "lower_back": [
            {"key": "camptocormia_back",
              "label": "Camptocormia / forward-flexed back pain"},
            {"key": "rigidity_pain", "label": "Rigidity-related pain"},
            {"key": "dystonia_back", "label": "Axial dystonia pain"},
        ],
        "neck_back": [
            {"key": "antecollis", "label": "Antecollis / dropped-head pain"},
            {"key": "rigidity_pain", "label": "Cervical rigidity pain"},
        ],
        "foot_left_top": [
            {"key": "off_dystonia_foot",
              "label": "Off-period foot dystonia (claw toes)"},
            {"key": "morning_dystonia", "label": "Early-morning dystonia"},
        ],
        "foot_right_top": "@foot_left_top",
        "calf_left": [
            {"key": "rigidity_pain", "label": "Calf rigidity pain"},
            {"key": "off_period_pain", "label": "Off-period pain"},
        ],
        "calf_right": "@calf_left",
    },

    # ───────────────────── SPINAL CORD INJURY ─────────────────────
    "spinal_cord_injury": {
        "lower_back": [
            {"key": "at_level_neuropathic",
              "label": "At-level neuropathic pain"},
            {"key": "musculoskeletal_back",
              "label": "Musculoskeletal back pain"},
        ],
        "buttocks": [
            {"key": "pressure_pain", "label": "Pressure-area pain"},
            {"key": "below_level_neuropathic",
              "label": "Below-level neuropathic pain"},
        ],
        "thigh_left_back": [
            {"key": "below_level_neuropathic",
              "label": "Below-level neuropathic pain"},
            {"key": "spasticity_pain", "label": "Spasticity pain"},
        ],
        "thigh_right_back": "@thigh_left_back",
        "shoulder_left_front": [
            {"key": "wheelchair_overuse",
              "label": "Wheelchair-overuse shoulder pain"},
            {"key": "rotator_cuff", "label": "Rotator cuff tendinopathy"},
        ],
        "shoulder_right_front": "@shoulder_left_front",
    },

    # ───────────────────── PERIPHERAL NEUROPATHY ─────────────────────
    "peripheral_neuropathy": {
        "foot_left_top": [
            {"key": "diabetic_neuropathy",
              "label": "Diabetic neuropathy (feet)"},
            {"key": "burning_feet", "label": "Burning feet syndrome"},
            {"key": "small_fibre",
              "label": "Small-fibre neuropathy"},
            {"key": "stocking_distribution",
              "label": "Stocking-distribution numbness"},
        ],
        "foot_right_top": "@foot_left_top",
        "foot_left_sole": "@foot_left_top",
        "foot_right_sole": "@foot_left_top",
        "hand_left": [
            {"key": "carpal_tunnel", "label": "Carpal tunnel syndrome"},
            {"key": "glove_distribution",
              "label": "Glove-distribution numbness"},
            {"key": "small_fibre", "label": "Small-fibre neuropathy"},
        ],
        "hand_right": "@hand_left",
        "shin_left": [
            {"key": "neuropathic_burning",
              "label": "Neuropathic burning"},
            {"key": "restless_legs", "label": "Restless legs sensation"},
        ],
        "shin_right": "@shin_left",
    },

    # ───────────────────── CEREBRAL PALSY ─────────────────────
    "cerebral_palsy": {
        "lower_back": [
            {"key": "scoliosis_pain", "label": "Scoliosis-related pain"},
            {"key": "spasticity_pain", "label": "Trunk spasticity pain"},
        ],
        "knee_left": [
            {"key": "crouch_gait_knee",
              "label": "Crouch-gait knee pain"},
            {"key": "patellofemoral",
              "label": "Patellofemoral pain"},
        ],
        "knee_right": "@knee_left",
        "thigh_left_front": [
            {"key": "spasticity_pain", "label": "Quadriceps spasticity"},
            {"key": "hamstring_tightness", "label": "Hamstring tightness"},
        ],
        "thigh_right_front": "@thigh_left_front",
    },
}


def _resolve_alias(value, condition_map):
    """Resolve '@other_region_key' aliases to actual lists."""
    if isinstance(value, str) and value.startswith("@"):
        return condition_map.get(value[1:], [])
    return value


def get_pain_types(region: str, condition: str):
    """Return the curated pain types for a region+condition, plus 1-2 generic
    fallbacks so the user always has options."""
    cmap = ONTOLOGY.get(condition, {})
    raw = cmap.get(region, [])
    resolved = _resolve_alias(raw, cmap)

    generic_subset = [
        g for g in GENERIC
        if g["key"] in {"sharp_localised", "dull_ache", "burning",
                        "stiffness", "wobble"}
    ]
    seen = {p["key"] for p in resolved}
    for g in generic_subset:
        if g["key"] not in seen:
            resolved.append(g)
    return resolved


def get_generic_pain_types():
    return GENERIC.copy()
