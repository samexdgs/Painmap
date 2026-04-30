# PainMap

> **Project #7 of 10** — Open-source neurological rehabilitation AI series
> Cross-condition pain self-management with a body-map UI, neuro-specific recommendation engine, and clinician-ready reports.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--2126--0254-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0008-2126-0254)

---

## About this project

PainMap is the seventh app in an open-source rehabilitation AI series built solo by **Samuel Tobi Oluwakoya**, an independent AI health researcher based in Lagos, Nigeria. Like every other app in the series, it is born from lived experience — Samuel lives with foot drop — and from clinical problems witnessed firsthand in low-resource Nigerian neuro-rehab.

Existing pain-mapping tools (Stanford CHOIR, the Michigan eMBM, GeoPain) are validated for chronic pain logging but stop at data collection. None give condition-aware recommendations after the tap. None cover stroke, multiple sclerosis, Parkinson's, spinal cord injury, peripheral neuropathy and cerebral palsy in a single tool. None work offline. PainMap fills that gap.

This is a **research prototype**. It is not a medical device. The single in-app disclaimer lives in the page footer — not on every screen — because clinical-grade self-management tools should not lecture the user.

---

## What it does

- **Anatomical body-map entry** — front and back views, 53 anatomically curated regions matching Stanford CHOIR resolution. Tap a region to begin.
- **Condition-aware pain ontology** — each region surfaces pain types specific to the user's primary condition (e.g. *hemiplegic shoulder pain*, *L'hermitte's sign*, *off-period dystonia*, *diabetic small-fibre neuropathy*) drawn from IASP, NICE, Cochrane and condition-specific guidelines.
- **Cited recommendation engine** — every recommendation cites a peer-reviewed source or clinical guideline. Auditable. Research-grade.
- **Red-flag detection** — region- and intensity-driven safety prompts that tell the user when to stop self-managing and see a clinician.
- **Pattern detection** — longitudinal analysis of triggers, day-of-week, time-of-day, and dominant regions across the user's logs.
- **Personalised weekly plan** — built from the user's most recurring pain types.
- **Local resources directory** — physiotherapists, orthotists, neurology clinics, FES providers, hydrotherapy pools, support groups across Nigerian cities, with patient-rated entries, prices and languages spoken. City-level filtering.
- **Reminders** — in-app and Brevo email reminders, plus a weekly digest.
- **Clinical PDF export** — single-tap generation of a clinician-ready PDF summary including stats, region breakdown, and recent entries.
- **Persistent login** — PBKDF2-HMAC-SHA256 password hashing with per-user salt (100,000 iterations). User data persists across sessions.
- **Nine-language UI** — English, Yoruba, Igbo, Hausa, Nigerian Pidgin, Spanish, French, Portuguese, Arabic.
- **Offline-first** — SQLite local storage; no clinic IT integration required.

---

## Why this is the missing piece

Three independent systematic reviews flagged the same gap:

| Review | Finding |
|---|---|
| Lee et al. 2022 (PD self-care, *J Med Internet Res*) | "There is a lack of studies focusing on symptom **management**." |
| Triantafyllidis et al. 2023 (PD, MS, Stroke apps, *Sensors*) | Most apps focus on logging; few on what to do next. |
| Boege et al. 2024 (PD self-management, *J Parkinsons Dis*) | "Few studies have systematically examined the standardisation of acceptability and usability assessments for clinicians." |

The literature is full of **monitoring**. The literature is empty on **management**. PainMap targets the management gap with a transparent, auditable recommendation engine.

---

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| UI | Streamlit | Solo-buildable, deploys free, matches the rest of Samuel's portfolio |
| Body map | Inline SVG + Streamlit components | No external dependencies, fully customisable |
| Storage | SQLite | Free, persistent, zero-config |
| Auth | PBKDF2-HMAC-SHA256 (100k iterations) | Same security pattern as SpeakAgain |
| Reports | ReportLab | Native PDF generation |
| Email | Brevo SMTP (free tier, 300/day) | Same provider as SpeakAgain; verified sender already configured |
| Hosting | Streamlit Community Cloud | Free, GitHub-linked CI |

No paid services. No wearables. No clinic-side integration required.

---

## Running locally

```bash
# Clone
git clone https://github.com/samexdgs/painmap.git
cd painmap

# Install
pip install -r requirements.txt

# Run
streamlit run app.py
```

The app opens at `http://localhost:8501`. Sign up with any username, email, password, and condition. SQLite database is auto-created at `painmap.db`.

---

## Deploying on Streamlit Community Cloud

1. Push the repo to GitHub.
2. On [share.streamlit.io](https://share.streamlit.io), click **Deploy an app**.
3. **Important — set Python 3.11 in Advanced Settings before deploying.** Streamlit Cloud locks the Python version at first deploy. The default Python 3.14 will fail to compile some wheels.
4. Set the main file to `app.py`.
5. (Optional) Paste Brevo credentials into **Secrets** using the template at `.streamlit/secrets.toml.template`.
6. Deploy.

If you accidentally deploy on Python 3.14 and encounter wheel-compilation errors, **delete the app and redeploy with Python 3.11 selected in Advanced Settings**. Editing `runtime.txt` after the fact will not change the locked version. (Lesson learned painfully on SpeakAgain — see project history.)

---

## Project structure

```
painmap/
├── app.py            # Streamlit shell, routing, page renderers
├── auth.py           # PBKDF2 password hashing, sign in / up / out
├── db.py             # SQLite schema, all CRUD operations
├── bodymap.py        # 53-region SVG body map (front + back), localised labels
├── ontology.py       # Condition × region → pain types (IASP/NICE-derived)
├── recommender.py    # Cited recommendations, red flags, pattern detection
├── resources.py      # Local rehab provider directory (seeded for Nigeria)
├── notifier.py       # Brevo SMTP email reminders
├── reports.py        # PDF (ReportLab) + CSV export
├── i18n.py           # 9-language UI translations
├── requirements.txt  # Unpinned to allow Python-version-compatible wheels
├── runtime.txt       # python-3.11
└── .streamlit/
    ├── config.toml             # Theme + server config
    └── secrets.toml.template   # Brevo SMTP placeholders
```

---

## Author

**Samuel Tobi Oluwakoya** — Independent AI Health Researcher
BSc (Hons) Computer Science, Afe Babalola University, Ado-Ekiti, Nigeria
Lagos, Nigeria · CGPA 4.23/5.00

- Email: [soluwakoyat@gmail.com](mailto:soluwakoyat@gmail.com), [samueloluwakoyat@gmail.com](mailto:samueloluwakoyat@gmail.com)
- ORCID: [0009-0008-2126-0254](https://orcid.org/0009-0008-2126-0254)
- GitHub: [github.com/samexdgs](https://github.com/samexdgs)
- LinkedIn: [linkedin.com/in/samueloluwakoya](https://linkedin.com/in/samueloluwakoya)
- Portfolio: [samueloluwakoya.netlify.app](https://samueloluwakoya.netlify.app)

The Brevo verified sender domain `Samuel@bloomgatelaw.com` is used **only** for outbound emails. It is **not** a contact address — please use the Gmail addresses above.

---

## The series

PainMap is project #7 of a planned 10-app neurological rehabilitation AI series. Every app is open source, free to use, and built solo from a patient-centred design perspective.

| # | App | Stack | Status |
|---|---|---|---|
| 1 | [Drop Foot Manager](https://fdmapp.streamlit.app/) | Streamlit · scikit-learn | Live (90% accuracy) |
| 2 | [AFO Prescription Platform](https://afoplat.streamlit.app/) | Streamlit · LightGBM | Live (ROC-AUC 0.987) |
| 3 | [NeuroKinetics](https://neurokinetics.vercel.app/) | Next.js · MediaPipe | Live (21-point tracking) |
| 4 | [Daily Stroke Recovery Classifier](https://stroketracker.streamlit.app/) | Streamlit · LightGBM | Live (92.1% accuracy) |
| 5 | [Family-Connected Stroke Monitor](https://stroketracker2.streamlit.app/) | Streamlit · SMTP | Live (92.4% accuracy) |
| 6 | [SpeakAgain](https://speakagain2.streamlit.app/) | Streamlit · Anthropic API | Live (9 languages, 5 games) |
| 7 | **PainMap** | Streamlit · SQLite · ReportLab | **This repo** |
| 8 | TBD | — | — |
| 9 | TBD | — | — |
| 10 | TBD | — | — |

---

## Disclaimer

PainMap is an open research prototype. It is not a medical device, does not diagnose, and is not a substitute for professional clinical care. If you are experiencing severe or worsening symptoms, contact a qualified clinician. Anyone showing red-flag features described in the app should seek medical evaluation immediately.

## License

MIT — see [LICENSE](LICENSE).

## Citing PainMap

If you use PainMap in research or teaching, please cite the accompanying manuscript:

> Oluwakoya, S. T. (2026). PainMap: Cross-condition neurological pain self-management with body-map-driven recommendations — design and feasibility of a patient-led research prototype. *Manuscript in preparation.*
