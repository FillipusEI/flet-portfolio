import flet as ft
import base64
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MATLAB_COURSES = [
    {"number": 1, "title": "MATLAB Onramp",                                      "date": "9 April 2026",  "img": "assets/certificates/cert1.jpg"},
    {"number": 2, "title": "Machine Learning Onramp",                            "date": "10 May 2026",   "img": "assets/certificates/cert2.jpg"},
    {"number": 3, "title": "Signal Processing Techniques for Streaming Signals",  "date": "10 May 2026",   "img": "assets/certificates/cert3.jpg"},
    {"number": 4, "title": "Make and Manipulate Matrices",                        "date": "13 April 2026", "img": "assets/certificates/cert4.jpg"},
    {"number": 5, "title": "Explore Data with MATLAB Plots",                      "date": "13 April 2026", "img": "assets/certificates/cert5.jpg"},
    {"number": 6, "title": "Calculations with Vectors and Matrices",              "date": "13 April 2026", "img": "assets/certificates/cert6.jpg"},
    {"number": 7, "title": "Simulink Onramp",                                     "date": "19 April 2026", "img": "assets/certificates/cert7.jpg"},
]


def load_image_base64(relative_path):
    full_path = os.path.join(BASE_DIR, relative_path)
    try:
        with open(full_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return None


def matlab_page(page: ft.Page = None):

    def open_fullscreen(e, img_b64, title):
        def close(e):
            page.overlay.clear()
            page.update()

        modal = ft.Container(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(title, size=15, color="#e6edf3", weight="bold", expand=True),
                                ft.ElevatedButton("✕ Close", on_click=close, bgcolor="#e6edf3", color="#ffffff"),
                            ],
                        ),
                        ft.Container(
                            content=ft.Image(
                                src_base64=img_b64,
                                fit="fill",
                                width=880,
                                height=600,
                            ),
                            bgcolor="#ffffff",
                            border_radius=8,
                            padding=0,
                        ),
                    ],
                    spacing=16,
                    horizontal_alignment="center",
                ),
                bgcolor="#0d1117",
                border=ft.border.all(1, "#30363d"),
                border_radius=12,
                padding=24,
                width=940,
                animate=ft.animation.Animation(300, "easeOut"),
            ),
            bgcolor="#000000bb",
            alignment=ft.alignment.center,
            expand=True,
        )

        page.overlay.clear()
        page.overlay.append(modal)
        page.update()

    def course_card(course, index):
        img_b64 = load_image_base64(course["img"])

        card_ref = ft.Ref()

        def on_hover(e):
            e.control.scale = 1.02 if e.data == "true" else 1.0
            e.control.shadow = ft.BoxShadow(
                blur_radius=20, color="#238636aa", spread_radius=2
            ) if e.data == "true" else ft.BoxShadow(blur_radius=0, color="#00000000")
            e.control.update()

        if img_b64:
            cert_img = ft.Container(
                content=ft.Image(
                    src_base64=img_b64,
                    fit="fill",
                    width=700,
                    height=490,
                ),
                bgcolor="#ffffff",
                border=ft.border.all(2, "#58a6ff"),
                border_radius=8,
                padding=0,
                margin=ft.margin.only(top=10),
                width=700,
                height=490,
                on_click=lambda e, b=img_b64, t=course["title"]: open_fullscreen(e, b, t),
                ink=True,
                tooltip="Click to view fullscreen",
                animate_scale=ft.animation.Animation(200, "easeOut"),
                scale=1.0,
            )
        else:
            cert_img = ft.Container(
                content=ft.Text(f"Image not found: {course['img']}", color="#484f58", italic=True, size=12),
                bgcolor="#0d1117",
                border=ft.border.all(1, "#484f58"),
                border_radius=8,
                padding=12,
                margin=ft.margin.only(top=10),
            )

        return ft.Container(
            ref=card_ref,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(str(course["number"]), size=16, color="#58a6ff", weight="bold"),
                                bgcolor="#0d1f38",
                                border_radius=20,
                                width=36,
                                height=36,
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(course["title"], size=15, color="#e6edf3", weight="bold"),
                                    ft.Text(f"Completed: {course['date']}", size=11, color="#484f58"),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Text("✅", size=20),
                        ],
                        spacing=12,
                        vertical_alignment="center",
                    ),
                    ft.Row(controls=[cert_img]),
                ],
                spacing=0,
            ),
            bgcolor="#161b22",
            border=ft.border.all(1, "#30363d"),
            border_radius=10,
            padding=16,
            animate=ft.animation.Animation(400 + index * 80, "easeOut"),
            animate_scale=ft.animation.Animation(300, "easeOut"),
            scale=1.0,
            on_hover=on_hover,
            shadow=ft.BoxShadow(blur_radius=0, color="#00000000"),
        )

    completed = len(MATLAB_COURSES)
    required = 7

    cards = [course_card(c, i) for i, c in enumerate(MATLAB_COURSES)]

    return ft.Column(
        controls=[
            ft.Text("MATLAB Achievement Hub", size=28, color="#e6edf3", weight="bold"),
            ft.Text("Eamon Fillipus — MathWorks Learning Center Course Completions", size=14, color="#8b949e"),
            ft.Divider(color="#21262d"),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Overall Progress", size=14, color="#8b949e", expand=True),
                                ft.Text(f"{completed} / {required} courses", size=14, color="#58a6ff", weight="bold"),
                            ],
                        ),
                        ft.ProgressBar(value=completed / required, bgcolor="#21262d", color="#58a6ff", height=10),
                        ft.Text("✅ All 7 courses completed!", size=12, color="#58a6ff"),
                    ],
                    spacing=10,
                ),
                bgcolor="#161b22",
                border=ft.border.all(1, "#30363d"),
                border_radius=10,
                padding=20,
                animate=ft.animation.Animation(300, "easeOut"),
            ),
            ft.Divider(color="#21262d"),
            ft.Column(controls=cards, spacing=16),
        ],
        spacing=20,
        scroll="auto",
    )
