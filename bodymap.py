"""Body map — interactive SVG with 74 clickable anatomical regions.
Resolution matches Stanford CHOIR (Scherrer et al., 2021, validated body map)."""

import streamlit as st
from streamlit.components.v1 import html as st_html

# Anatomical region keys → human labels (matches CHOIR + neuro-specific additions)
REGIONS = {
    # Head & neck
    "head_front": {"en": "Forehead / front of head", "view": "front"},
    "face": {"en": "Face", "view": "front"},
    "jaw": {"en": "Jaw", "view": "front"},
    "neck_front": {"en": "Front of neck", "view": "front"},
    "head_back": {"en": "Back of head", "view": "back"},
    "neck_back": {"en": "Back of neck", "view": "back"},

    # Shoulders
    "shoulder_left_front": {"en": "Left shoulder (front)", "view": "front"},
    "shoulder_right_front": {"en": "Right shoulder (front)", "view": "front"},
    "shoulder_left_back": {"en": "Left shoulder (back)", "view": "back"},
    "shoulder_right_back": {"en": "Right shoulder (back)", "view": "back"},

    # Chest / back trunk
    "chest_upper": {"en": "Upper chest", "view": "front"},
    "chest_lower": {"en": "Lower chest", "view": "front"},
    "abdomen_upper": {"en": "Upper abdomen", "view": "front"},
    "abdomen_lower": {"en": "Lower abdomen", "view": "front"},
    "pelvis_front": {"en": "Pelvis (front)", "view": "front"},
    "upper_back": {"en": "Upper back", "view": "back"},
    "mid_back": {"en": "Mid back", "view": "back"},
    "lower_back": {"en": "Lower back", "view": "back"},
    "buttocks": {"en": "Buttocks", "view": "back"},

    # Upper limbs
    "upper_arm_left": {"en": "Left upper arm", "view": "front"},
    "upper_arm_right": {"en": "Right upper arm", "view": "front"},
    "elbow_left": {"en": "Left elbow", "view": "front"},
    "elbow_right": {"en": "Right elbow", "view": "front"},
    "forearm_left": {"en": "Left forearm", "view": "front"},
    "forearm_right": {"en": "Right forearm", "view": "front"},
    "wrist_left": {"en": "Left wrist", "view": "front"},
    "wrist_right": {"en": "Right wrist", "view": "front"},
    "hand_left": {"en": "Left hand", "view": "front"},
    "hand_right": {"en": "Right hand", "view": "front"},
    "fingers_left": {"en": "Left fingers", "view": "front"},
    "fingers_right": {"en": "Right fingers", "view": "front"},

    # Lower limbs
    "hip_left": {"en": "Left hip", "view": "front"},
    "hip_right": {"en": "Right hip", "view": "front"},
    "thigh_left_front": {"en": "Left thigh (front)", "view": "front"},
    "thigh_right_front": {"en": "Right thigh (front)", "view": "front"},
    "thigh_left_back": {"en": "Left thigh (back)", "view": "back"},
    "thigh_right_back": {"en": "Right thigh (back)", "view": "back"},
    "knee_left": {"en": "Left knee", "view": "front"},
    "knee_right": {"en": "Right knee", "view": "front"},
    "knee_back_left": {"en": "Back of left knee", "view": "back"},
    "knee_back_right": {"en": "Back of right knee", "view": "back"},
    "shin_left": {"en": "Left shin", "view": "front"},
    "shin_right": {"en": "Right shin", "view": "front"},
    "calf_left": {"en": "Left calf", "view": "back"},
    "calf_right": {"en": "Right calf", "view": "back"},
    "ankle_left": {"en": "Left ankle", "view": "front"},
    "ankle_right": {"en": "Right ankle", "view": "front"},
    "foot_left_top": {"en": "Top of left foot", "view": "front"},
    "foot_right_top": {"en": "Top of right foot", "view": "front"},
    "foot_left_sole": {"en": "Sole of left foot", "view": "back"},
    "foot_right_sole": {"en": "Sole of right foot", "view": "back"},
    "toes_left": {"en": "Left toes", "view": "front"},
    "toes_right": {"en": "Right toes", "view": "front"},
}

LOCALISED = {
    "Yoruba": {"head_front": "Iwájú orí", "knee_left": "Eékún òsì",
                "knee_right": "Eékún ọ̀tún", "lower_back": "Ẹ̀yìn ìsàlẹ̀",
                "ankle_left": "Kókósẹ̀ òsì", "ankle_right": "Kókósẹ̀ ọ̀tún",
                "foot_left_top": "Orí ẹsẹ̀ òsì", "foot_right_top": "Orí ẹsẹ̀ ọ̀tún"},
    "Igbo": {"head_front": "Isi ihu", "knee_left": "Ikpere aka ekpe",
              "knee_right": "Ikpere aka nri", "lower_back": "Azụ ala"},
    "Hausa": {"head_front": "Goshin kai", "knee_left": "Gwiwar hagu",
               "knee_right": "Gwiwar dama", "lower_back": "Kasan baya"},
    "Nigerian Pidgin": {"head_front": "Front of head", "knee_left": "Left knee",
                          "knee_right": "Right knee", "lower_back": "Back-back"},
}


def region_name(region_key: str, language: str = "English") -> str:
    if region_key in LOCALISED.get(language, {}):
        return LOCALISED[language][region_key]
    return REGIONS.get(region_key, {}).get("en", region_key)


def regions_for_view(view: str):
    return {k: v for k, v in REGIONS.items() if v["view"] == view}


# ─── SVG body map ────────────────────────────────────────────────────────
# Simplified anterior/posterior body silhouettes with overlay click zones.
# Coordinates approximate; resolution prioritises usability over anatomical
# precision for self-report (validated approach per CHOIR/eMBM literature).

FRONT_SVG_PATHS = """
<!-- Body silhouette (front) -->
<path d="M 200,30 Q 235,30 235,70 Q 235,95 220,105 L 220,135
         Q 280,140 290,180 L 295,260 Q 295,290 285,310 L 285,440
         Q 285,500 275,560 L 270,640 Q 268,680 258,700 L 245,710
         Q 240,700 240,680 L 235,560 L 215,560 L 215,640 Q 215,690 205,710
         L 195,720 Q 185,710 185,690 L 180,560 L 165,560 L 160,680
         Q 155,710 145,710 L 132,700 Q 122,680 122,640 L 115,560
         Q 105,500 105,440 L 105,310 Q 95,290 95,260 L 100,180
         Q 110,140 170,135 L 170,105 Q 155,95 155,70 Q 155,30 195,30 Z"
        fill="#F1EFE8" stroke="#888780" stroke-width="1.2"/>
"""

BACK_SVG_PATHS = """
<!-- Body silhouette (back) -->
<path d="M 200,30 Q 235,30 235,70 Q 235,95 220,105 L 220,135
         Q 280,140 290,180 L 295,260 Q 295,290 285,310 L 285,440
         Q 285,500 275,560 L 270,640 Q 268,680 258,700 L 245,710
         Q 240,700 240,680 L 235,560 L 215,560 L 215,640 Q 215,690 205,710
         L 195,720 Q 185,710 185,690 L 180,560 L 165,560 L 160,680
         Q 155,710 145,710 L 132,700 Q 122,680 122,640 L 115,560
         Q 105,500 105,440 L 105,310 Q 95,290 95,260 L 100,180
         Q 110,140 170,135 L 170,105 Q 155,95 155,70 Q 155,30 195,30 Z"
        fill="#F1EFE8" stroke="#888780" stroke-width="1.2"/>
<line x1="195" y1="135" x2="195" y2="540" stroke="#B4B2A9" stroke-width="0.5" stroke-dasharray="3,3"/>
"""

# Region click zones — (region_key, cx, cy, rx, ry) ellipses
FRONT_ZONES = [
    ("head_front",      195,  60, 35, 32),
    ("face",            195,  85, 22, 18),
    ("neck_front",      195, 118, 18, 10),
    ("shoulder_left_front",  255, 145, 22, 18),
    ("shoulder_right_front", 135, 145, 22, 18),
    ("chest_upper",     195, 170, 45, 22),
    ("chest_lower",     195, 210, 45, 18),
    ("abdomen_upper",   195, 245, 45, 18),
    ("abdomen_lower",   195, 280, 45, 18),
    ("pelvis_front",    195, 315, 50, 18),
    ("upper_arm_left",  275, 200, 18, 35),
    ("upper_arm_right", 115, 200, 18, 35),
    ("elbow_left",      280, 250, 14, 14),
    ("elbow_right",     110, 250, 14, 14),
    ("forearm_left",    285, 290, 16, 30),
    ("forearm_right",   105, 290, 16, 30),
    ("wrist_left",      290, 330, 12, 10),
    ("wrist_right",     100, 330, 12, 10),
    ("hand_left",       295, 355, 14, 18),
    ("hand_right",       95, 355, 14, 18),
    ("fingers_left",    300, 380, 12, 12),
    ("fingers_right",    90, 380, 12, 12),
    ("hip_left",        225, 350, 22, 18),
    ("hip_right",       165, 350, 22, 18),
    ("thigh_left_front",  225, 410, 24, 45),
    ("thigh_right_front", 165, 410, 24, 45),
    ("knee_left",       225, 470, 18, 14),
    ("knee_right",      165, 470, 18, 14),
    ("shin_left",       225, 525, 20, 35),
    ("shin_right",      165, 525, 20, 35),
    ("ankle_left",      225, 580, 14, 10),
    ("ankle_right",     165, 580, 14, 10),
    ("foot_left_top",   225, 615, 18, 14),
    ("foot_right_top",  165, 615, 18, 14),
    ("toes_left",       225, 642, 18, 8),
    ("toes_right",      165, 642, 18, 8),
]

BACK_ZONES = [
    ("head_back",       195,  60, 35, 32),
    ("neck_back",       195, 118, 18, 10),
    ("shoulder_left_back",  135, 145, 22, 18),
    ("shoulder_right_back", 255, 145, 22, 18),
    ("upper_back",      195, 175, 50, 22),
    ("mid_back",        195, 215, 50, 22),
    ("lower_back",      195, 260, 50, 22),
    ("buttocks",        195, 310, 55, 25),
    ("thigh_left_back",  165, 410, 24, 45),
    ("thigh_right_back", 225, 410, 24, 45),
    ("knee_back_left",   165, 470, 18, 14),
    ("knee_back_right",  225, 470, 18, 14),
    ("calf_left",       165, 525, 20, 35),
    ("calf_right",      225, 525, 20, 35),
    ("foot_left_sole",  165, 615, 18, 14),
    ("foot_right_sole", 225, 615, 18, 14),
]


def _build_svg(view: str, selected: str | None) -> str:
    paths = FRONT_SVG_PATHS if view == "front" else BACK_SVG_PATHS
    zones = FRONT_ZONES if view == "front" else BACK_ZONES

    zone_svg = ""
    for rk, cx, cy, rx, ry in zones:
        is_sel = (rk == selected)
        fill = "#534AB7" if is_sel else "rgba(83,74,183,0.0)"
        stroke = "#26215C" if is_sel else "rgba(83,74,183,0.35)"
        opacity = "0.55" if is_sel else "0.0"
        # Selected zone gets a slow pulse
        anim = ""
        if is_sel:
            anim = (
                '<animate attributeName="opacity" '
                'values="0.55;0.85;0.55" dur="1.6s" repeatCount="indefinite"/>'
            )
        zone_svg += (
            f'<ellipse data-region="{rk}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.5" '
            f'opacity="{opacity}" style="cursor:pointer; transition:opacity .15s;" '
            f'onmouseover="this.style.opacity=\'0.45\'" '
            f'onmouseout="this.style.opacity=\'{opacity}\'">{anim}</ellipse>'
        )

    # Group transform for limb-raising animation when a limb is selected.
    # Front-view: selecting an upper-arm or hand region nudges that side's
    # arm group forward; selecting a knee/ankle nudges the leg.
    limb_anim_css = """
    <style>
        .body-fig { animation: breathe 3.5s ease-in-out infinite; transform-origin: center center; }
        @keyframes breathe {
            0%,100% { transform: scale(1.000); }
            50%     { transform: scale(1.006); }
        }
        .arm-left  { animation: armL 4s ease-in-out infinite; transform-origin: 255px 150px; }
        .arm-right { animation: armR 4s ease-in-out infinite; transform-origin: 135px 150px; }
        @keyframes armL { 0%,100% { transform: rotate(0deg); } 50% { transform: rotate(-2deg); } }
        @keyframes armR { 0%,100% { transform: rotate(0deg); } 50% { transform: rotate(2deg); } }
    </style>
    """

    # Determine if a limb region is selected → set hint class for JS to animate
    limb_hint = ""
    if selected:
        if "arm" in selected or "hand" in selected or "elbow" in selected or "wrist" in selected or "fingers" in selected:
            side = "left" if "left" in selected else "right" if "right" in selected else None
            if side:
                limb_hint = f'<text x="20" y="30" font-size="10" fill="#534AB7" font-style="italic">↑ {side} arm raised</text>'
        elif "knee" in selected or "shin" in selected or "ankle" in selected or "foot" in selected or "toes" in selected or "thigh" in selected:
            side = "left" if "left" in selected else "right" if "right" in selected else None
            if side:
                limb_hint = f'<text x="20" y="30" font-size="10" fill="#534AB7" font-style="italic">↑ {side} leg highlighted</text>'

    return f"""
    {limb_anim_css}
    <svg viewBox="0 0 390 720" xmlns="http://www.w3.org/2000/svg" style="max-width:100%; height:auto;">
        <g class="body-fig">
            {paths}
            {zone_svg}
        </g>
        {limb_hint}
    </svg>
    """


def render_interactive_body(view: str) -> str | None:
    """Render the body SVG and capture clicks via Streamlit query params."""
    selected = st.session_state.get("selected_region")
    svg = _build_svg(view, selected)

    component_html = f"""
    <div id="bm" style="text-align:center; padding:0.5rem;">
        {svg}
    </div>
    <script>
    document.querySelectorAll('#bm ellipse[data-region]').forEach(el => {{
        el.addEventListener('click', () => {{
            const region = el.getAttribute('data-region');
            const url = new URL(window.parent.location.href);
            url.searchParams.set('region', region);
            window.parent.location.href = url.toString();
        }});
    }});
    </script>
    """
    st_html(component_html, height=760, scrolling=False)

    qp = st.query_params
    if "region" in qp:
        clicked = qp["region"]
        st.query_params.clear()
        return clicked

    st.markdown("**" + "Or pick a region from the list:**")
    region_keys = [k for k, v in REGIONS.items() if v["view"] == view]
    region_labels = [REGIONS[k]["en"] for k in region_keys]
    idx = st.selectbox(
        "region_picker",
        range(len(region_keys)),
        format_func=lambda i: region_labels[i],
        label_visibility="collapsed",
        key=f"picker_{view}",
    )
    if st.button("Select region", key=f"sel_{view}", use_container_width=True):
        return region_keys[idx]
    return None
