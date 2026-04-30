"""
PainMap — Project #7
Cross-condition neurological pain self-management with body-map-driven recommendations.

Author: Samuel Tobi Oluwakoya
Repo: github.com/samexdgs/painmap
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import auth
import db
import bodymap
import ontology
import recommender
import exercises
import resources
import notifier
import reports
from i18n import t

st.set_page_config(
    page_title="PainMap — Neurological Pain Self-Management",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialise database on first run
db.init_db()

# Session state defaults
for key, default in [
    ("user", None),
    ("page", "log"),
    ("language", "English"),
    ("selected_region", None),
    ("selected_pain_type", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def render_sidebar():
    with st.sidebar:
        st.markdown("### 🩺 PainMap")
        st.caption("Neurological pain self-management")

        if st.session_state.user:
            st.success(f"Signed in: {st.session_state.user['username']}")
            st.session_state.language = st.selectbox(
                t("language", st.session_state.language),
                ["English", "Yoruba", "Igbo", "Hausa", "Nigerian Pidgin",
                 "Spanish", "French", "Portuguese", "Arabic"],
                index=["English", "Yoruba", "Igbo", "Hausa", "Nigerian Pidgin",
                       "Spanish", "French", "Portuguese", "Arabic"].index(st.session_state.language)
            )

            st.divider()
            page = st.radio(
                t("navigation", st.session_state.language),
                [
                    ("log", "🗺️ " + t("log_pain", st.session_state.language)),
                    ("history", "📈 " + t("history", st.session_state.language)),
                    ("recommendations", "💡 " + t("recommendations", st.session_state.language)),
                    ("resources", "📍 " + t("local_resources", st.session_state.language)),
                    ("reminders", "🔔 " + t("reminders", st.session_state.language)),
                    ("export", "📄 " + t("export", st.session_state.language)),
                    ("profile", "👤 " + t("profile", st.session_state.language)),
                ],
                format_func=lambda x: x[1],
                key="nav_radio",
            )
            st.session_state.page = page[0]

            st.divider()
            if st.button(t("sign_out", st.session_state.language), use_container_width=True):
                auth.sign_out()
                st.rerun()
        else:
            st.info(t("sign_in_prompt", st.session_state.language))


def render_auth():
    st.title("🩺 PainMap")
    st.caption(t("tagline", st.session_state.language))

    tab1, tab2 = st.tabs([t("sign_in", st.session_state.language),
                           t("sign_up", st.session_state.language)])

    with tab1:
        with st.form("signin_form"):
            u = st.text_input(t("username_or_email", st.session_state.language))
            p = st.text_input(t("password", st.session_state.language), type="password")
            if st.form_submit_button(t("sign_in", st.session_state.language), use_container_width=True):
                user = auth.sign_in(u, p)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error(t("invalid_credentials", st.session_state.language))

    with tab2:
        with st.form("signup_form"):
            su = st.text_input(t("username", st.session_state.language))
            se = st.text_input(t("email", st.session_state.language))
            sp = st.text_input(t("password", st.session_state.language), type="password",
                                help="Minimum 8 characters")
            sc = st.selectbox(
                t("primary_condition", st.session_state.language),
                ["stroke", "multiple_sclerosis", "parkinsons", "spinal_cord_injury",
                 "peripheral_neuropathy", "cerebral_palsy", "other"],
            )
            sg = st.selectbox(t("gender", st.session_state.language),
                              ["prefer_not_to_say", "male", "female", "other"])
            sa = st.number_input(t("age", st.session_state.language),
                                  min_value=10, max_value=110, value=40)
            sl = st.text_input(t("city", st.session_state.language) +
                                " (e.g. Lagos, Surulere)")
            agree = st.checkbox(t("agree_research_use", st.session_state.language))
            if st.form_submit_button(t("create_account", st.session_state.language),
                                      use_container_width=True):
                if not agree:
                    st.error(t("must_agree", st.session_state.language))
                elif len(sp) < 8:
                    st.error(t("password_too_short", st.session_state.language))
                else:
                    ok, msg = auth.sign_up(su, se, sp, sc, sg, sa, sl)
                    if ok:
                        st.success(t("account_created", st.session_state.language))
                    else:
                        st.error(msg)


def render_log_pain():
    st.header("🗺️ " + t("log_pain", st.session_state.language))
    st.caption(t("log_pain_caption", st.session_state.language))

    col1, col2 = st.columns([3, 2])

    with col1:
        view = st.radio(t("body_view", st.session_state.language),
                         [t("front", st.session_state.language),
                          t("back", st.session_state.language)],
                         horizontal=True)
        view_key = "front" if view == t("front", st.session_state.language) else "back"

        clicked_region = bodymap.render_interactive_body(view_key)
        if clicked_region:
            st.session_state.selected_region = clicked_region
            st.session_state.selected_pain_type = None

    with col2:
        if st.session_state.selected_region:
            region = st.session_state.selected_region
            st.markdown(f"### {bodymap.region_name(region, st.session_state.language)}")

            condition = st.session_state.user["primary_condition"]
            pain_types = ontology.get_pain_types(region, condition)

            if not pain_types:
                st.info(t("no_specific_types", st.session_state.language))
                pain_types = ontology.get_generic_pain_types()

            options = [pt["label"] for pt in pain_types]
            choice = st.selectbox(t("pain_type", st.session_state.language), options)
            chosen = next(pt for pt in pain_types if pt["label"] == choice)

            intensity = st.slider(t("intensity", st.session_state.language), 0, 10, 5)

            quality = st.multiselect(
                t("pain_quality", st.session_state.language),
                ["sharp", "dull", "burning", "throbbing", "stabbing", "tingling",
                 "numbness", "wobble_without_pain", "spasm", "stiff"]
            )

            trigger = st.text_input(t("trigger_optional", st.session_state.language),
                                     placeholder=t("trigger_placeholder", st.session_state.language))

            duration_min = st.number_input(
                t("duration_minutes", st.session_state.language),
                min_value=0, max_value=1440, value=30
            )

            note = st.text_area(t("notes_optional", st.session_state.language), height=80)

            if st.button(t("save_log", st.session_state.language), type="primary",
                          use_container_width=True):
                db.insert_pain_log(
                    user_id=st.session_state.user["id"],
                    region=region,
                    pain_type=chosen["key"],
                    intensity=intensity,
                    quality=",".join(quality),
                    trigger=trigger,
                    duration_min=duration_min,
                    note=note,
                )
                st.success(t("log_saved", st.session_state.language))

                recs = recommender.get_recommendations(
                    region, chosen["key"], intensity, quality,
                    st.session_state.user["primary_condition"]
                )
                st.markdown("---")
                st.markdown("### 💡 " + t("what_to_do_now", st.session_state.language))
                for r in recs:
                    with st.expander(f"**{r['title']}**", expanded=True):
                        st.write(r["body"])
                        # Show exercise demo if available — videos + step cues
                        demo = exercises.find_demo(r["title"])
                        if demo:
                            cols = st.columns([1, 4]) if demo.get("image") else [None, st]
                            if demo.get("image"):
                                cols[0].markdown(
                                    f"<div style='font-size:54px;text-align:center'>{demo['image']}</div>",
                                    unsafe_allow_html=True,
                                )
                            target = cols[1] if demo.get("image") else st
                            if demo.get("video"):
                                target.markdown(
                                    f"📹 [{t('watch_demo', st.session_state.language)}]({demo['video']})"
                                )
                            if demo.get("steps"):
                                target.markdown("**" + t("how_to", st.session_state.language) + "**")
                                for i, step in enumerate(demo["steps"], 1):
                                    target.markdown(f"{i}. {step}")

                red_flags = recommender.get_red_flags(region, chosen["key"], intensity)
                if red_flags:
                    st.error("⚠️ " + t("red_flag_header", st.session_state.language))
                    for f in red_flags:
                        st.markdown(f"- {f}")
        else:
            st.info(t("tap_region_prompt", st.session_state.language))


def render_history():
    st.header("📈 " + t("history", st.session_state.language))
    logs = db.get_user_logs(st.session_state.user["id"])
    if not logs:
        st.info(t("no_logs_yet", st.session_state.language))
        return

    df = pd.DataFrame(logs)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp", ascending=False)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("total_logs", st.session_state.language), len(df))
    c2.metric(t("avg_intensity", st.session_state.language), f"{df['intensity'].mean():.1f}")
    c3.metric(t("days_tracked", st.session_state.language), df["timestamp"].dt.date.nunique())
    most_common = df["region"].mode().iloc[0] if len(df) else "—"
    c4.metric(t("top_region", st.session_state.language),
              bodymap.region_name(most_common, st.session_state.language))

    st.subheader(t("intensity_over_time", st.session_state.language))
    daily = df.groupby(df["timestamp"].dt.date)["intensity"].mean().reset_index()
    daily.columns = ["date", "avg_intensity"]
    st.line_chart(daily.set_index("date"))

    st.subheader(t("pain_by_region", st.session_state.language))
    by_region = df.groupby("region").size().reset_index(name="count").sort_values("count", ascending=False)
    by_region["region"] = by_region["region"].apply(
        lambda r: bodymap.region_name(r, st.session_state.language))
    st.bar_chart(by_region.set_index("region"))

    st.subheader(t("recent_entries", st.session_state.language))
    display_df = df.head(20).copy()
    display_df["region"] = display_df["region"].apply(
        lambda r: bodymap.region_name(r, st.session_state.language))
    display_df["timestamp"] = display_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
    st.dataframe(display_df[["timestamp", "region", "pain_type", "intensity", "quality"]],
                  use_container_width=True, hide_index=True)


def render_recommendations():
    st.header("💡 " + t("recommendations", st.session_state.language))
    st.caption(t("recommendations_caption", st.session_state.language))

    logs = db.get_user_logs(st.session_state.user["id"], limit=30)
    if not logs:
        st.info(t("log_first_for_recs", st.session_state.language))
        return

    patterns = recommender.detect_patterns(logs)
    if patterns:
        st.subheader("🔎 " + t("patterns_detected", st.session_state.language))
        for p in patterns:
            st.info(p)

    st.subheader("📋 " + t("personalised_plan", st.session_state.language))
    plan = recommender.build_personalised_plan(
        logs, st.session_state.user["primary_condition"]
    )
    for section in plan:
        st.markdown(f"#### {section['heading']}")
        for item in section["items"]:
            st.markdown(f"- {item}")


def render_resources():
    st.header("📍 " + t("local_resources", st.session_state.language))
    st.caption(t("resources_caption", st.session_state.language))

    user_city = st.session_state.user.get("city", "")
    city = st.text_input(t("city", st.session_state.language), value=user_city)
    category = st.selectbox(
        t("category", st.session_state.language),
        ["physiotherapist", "neurology_clinic", "rehab_centre", "orthotist",
         "fes_provider", "hydrotherapy", "home_visit_therapist", "support_group"]
    )

    results = resources.search(city, category)
    if not results:
        st.warning(t("no_resources_found", st.session_state.language))
        st.markdown(t("contribute_resources", st.session_state.language))
        return

    st.markdown(f"**{len(results)}** " + t("results_found", st.session_state.language))
    for r in sorted(results, key=lambda x: -x.get("rating", 0)):
        with st.container(border=True):
            cols = st.columns([3, 1])
            cols[0].markdown(f"**{r['name']}**")
            cols[0].caption(f"📍 {r['address']}")
            cols[1].metric(t("rating", st.session_state.language),
                            f"{r.get('rating', 0):.1f}/5")
            st.caption(
                f"📞 {r.get('phone', '—')}  |  💰 {r.get('price_range', '—')}  |  "
                f"🗣️ {', '.join(r.get('languages', []))}"
            )
            if r.get("notes"):
                st.write(r["notes"])


def render_reminders():
    st.header("🔔 " + t("reminders", st.session_state.language))

    existing = db.get_reminders(st.session_state.user["id"])
    st.subheader(t("active_reminders", st.session_state.language))
    if existing:
        for rem in existing:
            cols = st.columns([4, 1])
            cols[0].markdown(f"**{rem['label']}** — {rem['time_of_day']} ({rem['frequency']})")
            if cols[1].button(t("delete", st.session_state.language), key=f"del_{rem['id']}"):
                db.delete_reminder(rem["id"])
                st.rerun()
    else:
        st.info(t("no_reminders", st.session_state.language))

    st.subheader(t("add_reminder", st.session_state.language))
    with st.form("rem_form"):
        label = st.text_input(t("reminder_label", st.session_state.language),
                                placeholder=t("reminder_placeholder", st.session_state.language))
        time_of_day = st.time_input(t("time", st.session_state.language)).strftime("%H:%M")
        frequency = st.selectbox(t("frequency", st.session_state.language),
                                  ["daily", "weekdays", "weekly"])
        email_alert = st.checkbox(t("also_email_me", st.session_state.language), value=True)
        if st.form_submit_button(t("save_reminder", st.session_state.language)):
            db.insert_reminder(st.session_state.user["id"], label, time_of_day,
                                frequency, email_alert)
            st.success(t("reminder_saved", st.session_state.language))
            st.rerun()

    st.divider()
    st.subheader(t("test_notification", st.session_state.language))
    if st.button(t("send_test_email", st.session_state.language)):
        ok, msg = notifier.send_test_email(st.session_state.user["email"])
        if ok:
            st.success(msg)
        else:
            st.warning(msg)


def render_export():
    st.header("📄 " + t("export", st.session_state.language))
    st.caption(t("export_caption", st.session_state.language))

    days = st.selectbox(t("date_range", st.session_state.language), [7, 14, 30, 60, 90], index=2)
    logs = db.get_user_logs(st.session_state.user["id"], days=days)
    if not logs:
        st.info(t("nothing_to_export", st.session_state.language))
        return

    st.write(f"**{len(logs)}** " + t("logs_in_range", st.session_state.language))

    if st.button(t("generate_pdf", st.session_state.language), type="primary"):
        pdf_bytes = reports.build_pdf_report(st.session_state.user, logs, days)
        st.download_button(
            t("download_pdf", st.session_state.language),
            data=pdf_bytes,
            file_name=f"painmap_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
        )

    csv_bytes = reports.build_csv(logs)
    st.download_button(
        t("download_csv", st.session_state.language),
        data=csv_bytes,
        file_name=f"painmap_logs_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )


def render_profile():
    st.header("👤 " + t("profile", st.session_state.language))
    u = st.session_state.user

    with st.form("profile_form"):
        new_email = st.text_input(t("email", st.session_state.language), value=u["email"])
        new_city = st.text_input(t("city", st.session_state.language),
                                   value=u.get("city", ""))
        new_condition = st.selectbox(
            t("primary_condition", st.session_state.language),
            ["stroke", "multiple_sclerosis", "parkinsons", "spinal_cord_injury",
             "peripheral_neuropathy", "cerebral_palsy", "other"],
            index=["stroke", "multiple_sclerosis", "parkinsons", "spinal_cord_injury",
                   "peripheral_neuropathy", "cerebral_palsy", "other"].index(u["primary_condition"])
        )
        if st.form_submit_button(t("save_changes", st.session_state.language)):
            db.update_user(u["id"], email=new_email, city=new_city,
                            primary_condition=new_condition)
            st.session_state.user = db.get_user_by_id(u["id"])
            st.success(t("profile_updated", st.session_state.language))

    st.divider()
    st.subheader(t("change_password", st.session_state.language))
    with st.form("pwd_form"):
        old = st.text_input(t("current_password", st.session_state.language), type="password")
        new = st.text_input(t("new_password", st.session_state.language), type="password")
        if st.form_submit_button(t("update_password", st.session_state.language)):
            ok = auth.change_password(u["id"], old, new)
            if ok:
                st.success(t("password_updated", st.session_state.language))
            else:
                st.error(t("wrong_current_password", st.session_state.language))

    st.divider()
    st.subheader(t("danger_zone", st.session_state.language))
    if st.button(t("delete_account", st.session_state.language)):
        st.warning(t("confirm_delete_account", st.session_state.language))
        if st.button(t("yes_delete", st.session_state.language)):
            db.delete_user(u["id"])
            auth.sign_out()
            st.rerun()


# ──────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────
render_sidebar()

if st.session_state.user is None:
    render_auth()
else:
    page = st.session_state.page
    {
        "log": render_log_pain,
        "history": render_history,
        "recommendations": render_recommendations,
        "resources": render_resources,
        "reminders": render_reminders,
        "export": render_export,
        "profile": render_profile,
    }[page]()

# Research-tool footer (single, page-level, not on every screen)
st.markdown("---")
st.caption(
    "PainMap is an open research prototype for cross-condition neurological "
    "pain self-management. It is not a medical device, does not diagnose, and "
    "is not a substitute for professional care. Built by Samuel Tobi Oluwakoya "
    "(soluwakoyat@gmail.com) as Project #7 of the open-source neurological "
    "rehabilitation AI series. © 2026 — MIT License."
)
