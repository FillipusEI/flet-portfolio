import flet as ft
import threading
import time
import base64
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_b64(filename):
    path = os.path.join(BASE_DIR, "assets", filename)
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return None

TIMELINE_ENTRIES = [
    {
        "week": "Week 1",
        "title": "Firebase Project Setup & Configuration",
        "contributions": [
            "Created the Firebase project on the Firebase Console for ENGITRIAD.",
            "Configured Firestore collections: users, corrosionRecords, concreteMixes, blastingEvents.",
            "Set up .env file for Firebase API keys and added it to .gitignore to protect credentials.",
            "Initialised Firebase in the Expo project using the JavaScript SDK.",
        ],
        "module": "Firebase Lead",
    },
    {
        "week": "Week 2",
        "title": "Firestore Security Rules & Database Design",
        "contributions": [
            "Wrote Firestore security rules: request.auth != null on all four collections.",
            "Designed Firestore document schemas for corrosionRecords and concreteMixes collections.",
            "Tested security rules using Firebase Emulator to ensure no unauthorized access.",
            "Collaborated with Login & Sign-up team to link Auth UIDs to Firestore user documents.",
        ],
        "module": "Firebase Lead",
    },
    {
        "week": "Week 3",
        "title": "Firestore Integration — Corrosion Records",
        "contributions": [
            "Integrated Firestore write operations to save corrosion results under authenticated UID.",
            "Implemented real-time Firestore listener so history updates without manual refresh.",
            "Ensured each corrosionRecord is scoped to the user's UID — no cross-user data access.",
            "Reviewed and approved PR from Metallurgical module team on corrosion input form.",
        ],
        "module": "Firebase Lead",
    },
    {
        "week": "Week 4",
        "title": "Firestore Integration — Concrete Mixes & Blasting Events",
        "contributions": [
            "Integrated Firestore save and retrieve for concreteMixes collection.",
            "Set up real-time Firestore listeners for blastingEvents — live sync for all authorised users.",
            "Added Firebase Storage configuration for blasting event photo/document attachments.",
            "Fixed a Firestore timestamp ordering bug causing history to display in wrong order.",
        ],
        "module": "Firebase Lead",
    },
    {
        "week": "Week 5",
        "title": "Firebase Environment Variables & Testing",
        "contributions": [
            "Wrote Firebase setup and .env configuration guide in the group README.",
            "Tested all Firebase operations end-to-end: create, read, update, delete across all collections.",
            "Verified Firebase Storage file URL is correctly saved to the blastingEvents Firestore document.",
            "Completed 7 MathWorks MATLAB courses — certificates saved for portfolio.",
        ],
        "module": "Firebase Lead",
    },
    {
        "week": "Week 6",
        "title": "Portfolio Development & Final Submission",
        "contributions": [
            "Built all four Flet portfolio pages: Timeline, MATLAB Hub, Technical Blog, GitHub Evidence.",
            "Uploaded all 7 MathWorks completion certificates to the MATLAB Achievement Hub.",
            "Final portfolio running live and all sections verified before submission.",
            "Submitted portfolio link and GitHub evidence to lecturer.",
        ],
        "module": "Portfolio / Assessment",
    },
]

MODULE_COLORS = {
    "Firebase Lead":          "#58a6ff",
    "Portfolio / Assessment": "#58a6ff",
}

def timeline_page(page: ft.Page = None):
    profile_b64 = load_b64("profile_nobg.png")

    # ── Photo circle ──────────────────────────────────────────────────────────
    photo_circle = ft.Container(
        content=ft.Image(
            src_base64=profile_b64,
            width=150, height=150,
            fit="cover",
        ) if profile_b64 else ft.Text("EF", size=40, color="#fff", weight="bold"),
        width=150, height=150,
        border_radius=75,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        bgcolor="#0d1117",
    )

    # ── Hero banner ──────────────────────────────────────────────────────────
    hero = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Container(
                    content=ft.Image(src_base64=profile_b64, fit="cover", width=2000, height=280) if profile_b64 else ft.Container(bgcolor="#161b22"),
                    width=2000, height=280, clip_behavior=ft.ClipBehavior.ANTI_ALIAS, opacity=0.35,
                ),
                ft.Container(bgcolor="#0d1117cc", width=2000, height=280),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(content=photo_circle, alignment=ft.alignment.center, width=190, height=190),
                            ft.Column(
                                controls=[
                                    ft.Text("Eamon Fillipus", size=28, color="#e6edf3", weight="bold"),
                                    ft.Text("EI_225057425", size=14, color="#8b949e"),
                                    ft.Row(
                                        controls=[
                                            ft.Container(content=ft.Text("Firebase Lead", size=12, color="#58a6ff", weight="bold"), bgcolor="#0d1f38", border=ft.border.all(1, "#58a6ff"), border_radius=4, padding=ft.padding.symmetric(horizontal=10, vertical=4)),
                                            ft.Container(content=ft.Text("Group 8 — ENGITRIAD", size=12, color="#58a6ff"), bgcolor="#0d1f38", border=ft.border.all(1, "#58a6ff"), border_radius=4, padding=ft.padding.symmetric(horizontal=10, vertical=4)),
                                            ft.Container(content=ft.Text("UNAM", size=12, color="#e03131", weight="bold"), bgcolor="#2d0000", border=ft.border.all(1, "#e03131"), border_radius=4, padding=ft.padding.symmetric(horizontal=10, vertical=4)),
                                        ],
                                        spacing=8, wrap=True,
                                    ),
                                ],
                                spacing=10, expand=True,
                            ),
                        ],
                        spacing=24, vertical_alignment="center",
                    ),
                    padding=ft.padding.symmetric(horizontal=32, vertical=24), height=280, alignment=ft.alignment.center_left,
                ),
            ],
        ),
        border_radius=12, clip_behavior=ft.ClipBehavior.ANTI_ALIAS, border=ft.border.all(1, "#30363d"),
    )

    def entry_card(entry):
        color = MODULE_COLORS.get(entry["module"], "#30363d")
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(entry["module"], size=11, color=color, weight="bold"),
                                bgcolor="#161b22",
                                border=ft.border.all(1, color),
                                border_radius=4,
                                padding=ft.padding.symmetric(horizontal=8, vertical=3),
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Text(entry["title"], size=16, color="#e6edf3", weight="bold"),
                    ft.Text(entry["week"], size=11, color="#484f58", weight="bold"),
                    ft.Divider(color="#21262d"),
                    ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Text(f"  {c}", size=13, color="#c9d1d9"),
                                border=ft.border.only(left=ft.BorderSide(3, color)),
                                padding=ft.padding.only(left=12, top=4, bottom=4),
                            )
                            for c in entry["contributions"]
                        ],
                        spacing=6,
                    ),
                ],
                spacing=8,
            ),
            padding=20, bgcolor="#161b22", border=ft.border.all(1, "#30363d"), border_radius=10,
        )

    timeline_cards = [entry_card(e) for e in TIMELINE_ENTRIES]

    return ft.Column(
        controls=[
            hero,
            ft.Divider(color="#21262d"),
            ft.Text("Weekly Contributions", size=18, color="#e6edf3", weight="bold"),
            *timeline_cards,
        ],
        spacing=20,
        scroll="auto",
    )