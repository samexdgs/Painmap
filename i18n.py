"""Internationalisation — 9 languages, namespaced keys.
Same architecture as SpeakAgain (t(key, language)).
Falls back to English if translation missing.
"""

TRANSLATIONS = {
    # Navigation & shell
    "language": {
        "English": "Language",
        "Yoruba": "Èdè", "Igbo": "Asụsụ", "Hausa": "Harshe",
        "Nigerian Pidgin": "Language",
        "Spanish": "Idioma", "French": "Langue",
        "Portuguese": "Idioma", "Arabic": "اللغة",
    },
    "navigation": {
        "English": "Navigate", "Yoruba": "Lilọ kiri", "Igbo": "Gaa",
        "Hausa": "Tafiya", "Nigerian Pidgin": "Move",
        "Spanish": "Navegar", "French": "Naviguer",
        "Portuguese": "Navegar", "Arabic": "تنقّل",
    },
    "log_pain": {
        "English": "Log pain", "Yoruba": "Ṣàkọsílẹ̀ ìrora",
        "Igbo": "Dekoo ihe mgbu", "Hausa": "Rubuta ciwo",
        "Nigerian Pidgin": "Mark wia e dey pain you",
        "Spanish": "Registrar dolor", "French": "Noter la douleur",
        "Portuguese": "Registar dor", "Arabic": "تسجيل الألم",
    },
    "history": {
        "English": "History", "Yoruba": "Ìtàn", "Igbo": "Akụkọ",
        "Hausa": "Tarihi", "Nigerian Pidgin": "History",
        "Spanish": "Historial", "French": "Historique",
        "Portuguese": "Histórico", "Arabic": "السجل",
    },
    "recommendations": {
        "English": "Recommendations", "Yoruba": "Àbá", "Igbo": "Ndụmọdụ",
        "Hausa": "Shawarwari", "Nigerian Pidgin": "Wetin to do",
        "Spanish": "Recomendaciones", "French": "Recommandations",
        "Portuguese": "Recomendações", "Arabic": "توصيات",
    },
    "local_resources": {
        "English": "Local resources", "Yoruba": "Àwọn orísun agbègbè",
        "Igbo": "Akụrụngwa mpaghara", "Hausa": "Albarkatu na yanki",
        "Nigerian Pidgin": "People wey fit help", "Spanish": "Recursos locales",
        "French": "Ressources locales", "Portuguese": "Recursos locais",
        "Arabic": "موارد محلية",
    },
    "reminders": {
        "English": "Reminders", "Yoruba": "Ìránnilétí", "Igbo": "Ncheta",
        "Hausa": "Tunatarwa", "Nigerian Pidgin": "Reminder",
        "Spanish": "Recordatorios", "French": "Rappels",
        "Portuguese": "Lembretes", "Arabic": "التذكيرات",
    },
    "export": {
        "English": "Export report", "Yoruba": "Gbé ìròyìn jáde",
        "Igbo": "Wepụta akụkọ", "Hausa": "Fitar da rahoto",
        "Nigerian Pidgin": "Print report", "Spanish": "Exportar informe",
        "French": "Exporter le rapport", "Portuguese": "Exportar relatório",
        "Arabic": "تصدير التقرير",
    },
    "profile": {
        "English": "Profile", "Yoruba": "Profáìlì", "Igbo": "Profaịlụ",
        "Hausa": "Bayani", "Nigerian Pidgin": "My info",
        "Spanish": "Perfil", "French": "Profil",
        "Portuguese": "Perfil", "Arabic": "الملف الشخصي",
    },
    "sign_in": {
        "English": "Sign in", "Yoruba": "Wọlé", "Igbo": "Banye",
        "Hausa": "Shiga", "Nigerian Pidgin": "Login",
        "Spanish": "Iniciar sesión", "French": "Se connecter",
        "Portuguese": "Entrar", "Arabic": "تسجيل الدخول",
    },
    "sign_up": {
        "English": "Create account", "Yoruba": "Ṣẹda àkọọlẹ̀",
        "Igbo": "Mepụta akaụntụ", "Hausa": "Bude asusu",
        "Nigerian Pidgin": "New account", "Spanish": "Crear cuenta",
        "French": "Créer un compte", "Portuguese": "Criar conta",
        "Arabic": "إنشاء حساب",
    },
    "sign_out": {
        "English": "Sign out", "Yoruba": "Jáde", "Igbo": "Pụọ",
        "Hausa": "Fita", "Nigerian Pidgin": "Logout",
        "Spanish": "Cerrar sesión", "French": "Se déconnecter",
        "Portuguese": "Sair", "Arabic": "تسجيل الخروج",
    },
    "sign_in_prompt": {
        "English": "Sign in or create an account to begin.",
        "Yoruba": "Wọlé tàbí ṣẹda àkọọlẹ̀ láti bẹ̀rẹ̀.",
        "Nigerian Pidgin": "Login abi create new account to start.",
        "Spanish": "Inicia sesión o crea una cuenta para comenzar.",
        "French": "Connectez-vous ou créez un compte pour commencer.",
        "Portuguese": "Entre ou crie uma conta para começar.",
        "Arabic": "سجّل الدخول أو أنشئ حسابًا لتبدأ.",
    },
    "tagline": {
        "English": "Cross-condition neurological pain self-management.",
        "Yoruba": "Ìṣakoso ìrora nípa iṣan ara fún ọpọlọpọ àìsàn.",
        "Nigerian Pidgin": "Manage your nerve pain by yourself.",
        "Spanish": "Autogestión del dolor neurológico multicondicional.",
        "French": "Auto-gestion de la douleur neurologique multi-conditions.",
        "Portuguese": "Autogestão da dor neurológica multi-condições.",
        "Arabic": "الإدارة الذاتية للألم العصبي عبر حالات متعددة.",
    },

    # Auth
    "username": {"English": "Username", "Spanish": "Usuario",
                  "French": "Nom d'utilisateur", "Portuguese": "Nome de utilizador",
                  "Arabic": "اسم المستخدم"},
    "username_or_email": {"English": "Username or email",
                            "Spanish": "Usuario o correo",
                            "French": "Nom d'utilisateur ou email"},
    "email": {"English": "Email", "Spanish": "Correo", "French": "Email",
                "Portuguese": "Email", "Arabic": "البريد الإلكتروني"},
    "password": {"English": "Password", "Spanish": "Contraseña",
                   "French": "Mot de passe", "Portuguese": "Palavra-passe",
                   "Arabic": "كلمة المرور"},
    "primary_condition": {"English": "Primary neurological condition"},
    "gender": {"English": "Gender"},
    "age": {"English": "Age"},
    "city": {"English": "City"},
    "agree_research_use": {
        "English": "I understand this is a research prototype, not a medical "
                     "device, and I consent to my anonymised data being used "
                     "for research."
    },
    "must_agree": {"English": "You must agree to the research consent to continue."},
    "password_too_short": {"English": "Password must be at least 8 characters."},
    "create_account": {"English": "Create account"},
    "account_created": {"English": "Account created. Please sign in."},
    "invalid_credentials": {"English": "Wrong username or password."},

    # Body map / log
    "body_view": {"English": "View"},
    "front": {"English": "Front", "Yoruba": "Iwájú", "Igbo": "Ihu",
                "Hausa": "Gaba", "Spanish": "Frente", "French": "Avant"},
    "back": {"English": "Back", "Yoruba": "Ẹ̀yìn", "Igbo": "Azụ",
              "Hausa": "Baya", "Spanish": "Espalda", "French": "Arrière"},
    "log_pain_caption": {
        "English": "Tap a body part to begin. The list of pain types "
                     "narrows to your condition.",
    },
    "tap_region_prompt": {
        "English": "Tap a body part on the figure to log pain there.",
    },
    "no_specific_types": {
        "English": "No condition-specific pain types listed for this region. "
                     "Showing general types.",
    },
    "pain_type": {"English": "Pain type"},
    "intensity": {"English": "Intensity (0–10)"},
    "pain_quality": {"English": "Quality (pick all that apply)"},
    "trigger_optional": {"English": "Trigger (optional)"},
    "trigger_placeholder": {
        "English": "e.g., long walk, sitting, cold weather, stress",
    },
    "duration_minutes": {"English": "How long has it lasted? (minutes)"},
    "notes_optional": {"English": "Notes (optional)"},
    "save_log": {"English": "Save & get advice"},
    "log_saved": {"English": "Logged."},
    "what_to_do_now": {"English": "What to do now"},
    "red_flag_header": {
        "English": "Red flags — when to stop self-managing and see a doctor:",
    },

    # History
    "no_logs_yet": {"English": "No logs yet. Add your first one to get started."},
    "total_logs": {"English": "Total logs"},
    "avg_intensity": {"English": "Avg intensity"},
    "days_tracked": {"English": "Days tracked"},
    "top_region": {"English": "Top region"},
    "intensity_over_time": {"English": "Intensity over time"},
    "pain_by_region": {"English": "Pain by region"},
    "recent_entries": {"English": "Recent entries"},

    # Recommendations
    "recommendations_caption": {
        "English": "Pattern detection and a personalised plan from your logs."
    },
    "log_first_for_recs": {
        "English": "Log a few entries first — recommendations need data.",
    },
    "patterns_detected": {"English": "Patterns detected"},
    "personalised_plan": {"English": "Personalised weekly plan"},

    # Resources
    "resources_caption": {
        "English": "Physiotherapists, orthotists, and rehab services in your "
                     "city. Crowdsourced — contribute to grow the directory.",
    },
    "category": {"English": "Category"},
    "no_resources_found": {
        "English": "No matches in this city for this category yet.",
    },
    "contribute_resources": {
        "English": "Know a good provider? Open an issue on GitHub to contribute it.",
    },
    "results_found": {"English": "results found"},
    "rating": {"English": "Rating"},

    # Reminders
    "active_reminders": {"English": "Active reminders"},
    "no_reminders": {"English": "No reminders yet. Add one below."},
    "add_reminder": {"English": "Add a reminder"},
    "reminder_label": {"English": "Reminder label"},
    "reminder_placeholder": {"English": "e.g., Morning pain check-in"},
    "time": {"English": "Time of day"},
    "frequency": {"English": "Frequency"},
    "also_email_me": {"English": "Also send me an email"},
    "save_reminder": {"English": "Save reminder"},
    "reminder_saved": {"English": "Reminder saved."},
    "delete": {"English": "Delete"},
    "test_notification": {"English": "Test notification"},
    "send_test_email": {"English": "Send test email"},
    "email_sent": {"English": "Email sent. Check your inbox."},
    "email_not_configured": {
        "English": "Email is not configured on this deployment. "
                     "In-app reminders still work.",
    },

    # Export
    "export_caption": {
        "English": "Generate a clinical PDF for your physio, or export raw CSV.",
    },
    "date_range": {"English": "Date range (days)"},
    "nothing_to_export": {"English": "No logs in this range to export."},
    "logs_in_range": {"English": "logs in range"},
    "generate_pdf": {"English": "Generate clinical PDF"},
    "download_pdf": {"English": "Download PDF"},
    "download_csv": {"English": "Download CSV"},

    # Profile
    "save_changes": {"English": "Save changes"},
    "profile_updated": {"English": "Profile updated."},
    "change_password": {"English": "Change password"},
    "current_password": {"English": "Current password"},
    "new_password": {"English": "New password"},
    "update_password": {"English": "Update password"},
    "password_updated": {"English": "Password updated."},
    "wrong_current_password": {"English": "Current password is wrong."},
    "danger_zone": {"English": "Danger zone"},
    "delete_account": {"English": "Delete my account"},
    "confirm_delete_account": {
        "English": "This permanently deletes your account and all logs. "
                     "Click again to confirm.",
    },
    "yes_delete": {"English": "Yes, delete everything"},
    "watch_demo": {
        "English": "Watch demonstration",
        "Yoruba": "Wo ìfihàn",
        "Igbo": "Lee ngosipụta",
        "Hausa": "Kalli zanga-zangar",
        "Nigerian Pidgin": "Watch how to do am",
        "Spanish": "Ver demostración",
        "French": "Voir la démonstration",
        "Portuguese": "Ver demonstração",
        "Arabic": "شاهد العرض",
    },
    "how_to": {
        "English": "How to do it",
        "Yoruba": "Báwo ni a ṣe ń ṣe é",
        "Igbo": "Otu esi eme ya",
        "Hausa": "Yadda ake yi",
        "Nigerian Pidgin": "How to do am",
        "Spanish": "Cómo hacerlo",
        "French": "Comment le faire",
        "Portuguese": "Como fazer",
        "Arabic": "كيف تفعل ذلك",
    },
}


def t(key: str, language: str = "English") -> str:
    """Translate a key to the target language. Falls back to English, then key."""
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key.replace("_", " ").capitalize()
    return entry.get(language) or entry.get("English") or key
