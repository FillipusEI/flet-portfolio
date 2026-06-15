import flet as ft
import threading
import math
import time

GITHUB_REPO = "ENGITRIAD"

COMMIT_LOG = [
    {"hash": "368b6cd", "message": "chore: fix expo dependency compatibility mismatches", "date": "9 Jun 2026"},
    {"hash": "e40dc41", "message": "docs: add inline comment for npm install",             "date": "9 Jun 2026"},
    {"hash": "f639970", "message": "docs: minor README update",                            "date": "3 Jun 2026"},
]

IMPACT_TEXT = (
    "Delivered full-stack contributions to establish and refine the portfolio application. "
    "Architected the initial project foundation and systematically enhanced the codebase by implementing "
    "robust authentication error handling, streamlining the WorkerDashboard, and enforcing strict naming conventions. "
    "Additionally, maintained project health through proactive dependency hygiene and comprehensive README documentation updates."
)


def github_page():

    def make_glow_card(inner_content, offset=0):
        """Returns a (glow_container, start_thread_fn) pair."""
        glow = ft.Container(
            content=inner_content,
            border_radius=12,
            padding=2,
            bgcolor="#640000",
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=14,
                color="#aa000055",
                offset=ft.Offset(0, 0),
            ),
        )

        def _animate():
            step = offset
            while True:
                step += 1
                t = (step % 100) / 100.0
                pulse = abs(math.sin(t * math.pi))
                intensity = int(100 + 120 * pulse)
                glow.bgcolor = f"#{intensity:02x}0000"
                glow.shadow = ft.BoxShadow(
                    spread_radius=2 + 4 * pulse,
                    blur_radius=14 + 16 * pulse,
                    color=f"#{intensity:02x}000055",
                    offset=ft.Offset(0, 0),
                )
                try:
                    glow.update()
                except Exception:
                    break
                time.sleep(0.05)

        threading.Thread(target=_animate, daemon=True).start()
        return glow

    def commit_row(commit):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(commit["hash"], size=11, color="#58a6ff"),
                        bgcolor="#0d1f38",
                        border_radius=4,
                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                    ),
                    ft.Text(commit["message"], size=13, color="#c9d1d9", expand=True),
                    ft.Text(commit["date"], size=11, color="#484f58"),
                ],
                spacing=12,
                vertical_alignment="center",
            ),
            border=ft.border.only(bottom=ft.BorderSide(1, "#21262d")),
            padding=ft.padding.symmetric(vertical=10),
        )

    def section(title, controls_list):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(title, size=16, color="#e6edf3", weight="bold"),
                    ft.Divider(color="#21262d"),
                    ft.Column(controls=controls_list, spacing=0),
                ],
                spacing=12,
            ),
            bgcolor="#161b22",
            border=ft.border.all(1, "#30363d"),
            border_radius=10,
            padding=20,
        )

    # Screenshot card with glow (offset=0 so it starts in phase)
    screenshot_glow = make_glow_card(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("GitHub Commit History (Screenshot)", size=16, color="#e6edf3", weight="bold"),
                    ft.Divider(color="#21262d"),
                    ft.Image(
                        src="github_screenshot.png",
                        fit=ft.ImageFit.CONTAIN,
                        border_radius=8,
                    ),
                ],
                spacing=12,
            ),
            bgcolor="#0d1117",
            border_radius=10,
            padding=20,
        ),
        offset=0,
    )

    # Impact Summary card with glow (offset=50 so it pulses out of phase — nice effect)
    impact_glow = make_glow_card(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("💡", size=18),
                            ft.Text("Impact Summary", size=16, color="#FFD700", weight="bold"),
                        ],
                        spacing=8,
                        vertical_alignment="center",
                    ),
                    ft.Text(IMPACT_TEXT, size=13, color="#c9d1d9"),
                ],
                spacing=12,
            ),
            bgcolor="#0d1117",
            border_radius=10,
            padding=20,
        ),
        offset=50,
    )

    return ft.Column(
        controls=[
            ft.Text("GitHub Evidence & Documentation", size=28, color="#e6edf3", weight="bold"),
            ft.Text(
                f"Individual contribution evidence for {GITHUB_REPO} — University of Namibia.",
                size=14,
                color="#8b949e",
            ),
            ft.Divider(color="#21262d"),
            screenshot_glow,
            section("Commits", [commit_row(c) for c in COMMIT_LOG]),
            impact_glow,
        ],
        spacing=20,
        scroll="auto",
    )