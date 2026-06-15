import flet as ft
import asyncio
import base64
import os

# ── Import Your Actual Pages ─────────────────────────────────────────────
from pages.timeline import timeline_page
from pages.matlab import matlab_page
from pages.blog import blog_page
from pages.github import github_page


def main(page: ft.Page):
    page.title = "Web Portfolio 2026"
    page.bgcolor = "#0d1117"
    page.padding = 0
    page.scroll = None  # Prevents full-window jitter during animations

    NAV_ITEMS = [
        {"label": "Timeline", "icon": "🗓", "color": "#58a6ff"},
        {"label": "MATLAB",   "icon": "🔢", "color": "#58a6ff"},
        {"label": "Blog",     "icon": "📝", "color": "#58a6ff"},
        {"label": "GitHub",   "icon": "🐙", "color": "#58a6ff"},
    ]


    # Routing: Calls page builders with correct signatures based on their definitions
    def get_page(index):
        if index == 0: return timeline_page(page)
        if index == 1: return matlab_page(page)
        if index == 2: return blog_page()      # No arguments as per blog.py
        if index == 3: return github_page()    # No arguments as per github.py
        return ft.Container()

    # ── Main App Structure ──────────────────────────────────────────────────
    def build_main_app():
        page.controls.clear()
        btn_refs = []

        content_area = ft.Column(
            controls=[get_page(0)],
            scroll="auto",
            expand=True,
        )

        def switch_page(index):
            for i, b in enumerate(btn_refs):
                is_now = i == index
                b.data["label"].color = b.data["color"] if is_now else "#8b949e"
                b.data["label"].weight = "bold" if is_now else "normal"
                b.data["glow"].opacity = 1.0 if is_now else 0.0
                b.update()
            
            content_area.controls.clear()
            content_area.controls.append(get_page(index))
            content_area.update()

        def make_btn(item, index):
            is_active = index == 0
            icon_widget = ft.Text(item["icon"], size=16)
            label = ft.Text(
                item["label"], size=13,
                color=item["color"] if is_active else "#8b949e",
                weight="bold" if is_active else "normal",
            )
            glow_dot = ft.Container(
                width=5, height=5,
                bgcolor=item["color"],
                border_radius=3,
                opacity=1.0 if is_active else 0.0,
                animate_opacity=ft.animation.Animation(300, "easeOut"),
                shadow=ft.BoxShadow(blur_radius=6, color=item["color"], spread_radius=1),
            )
            btn = ft.Container(
                content=ft.Row(
                    controls=[icon_widget, label, glow_dot],
                    spacing=6,
                    vertical_alignment="center",
                ),
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                border_radius=8,
                on_click=lambda e, idx=index: switch_page(idx),
                ink=True,
                data={"label": label, "glow": glow_dot, "color": item["color"]},
            )
            btn_refs.append(btn)
            return btn

        nav_btns = [make_btn(item, i) for i, item in enumerate(NAV_ITEMS)]

        navbar = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text("FE", size=14, color="#ffffff", weight="bold"),
                                width=36, height=36,
                                bgcolor="#58a6ff",
                                border_radius=18,
                                alignment=ft.alignment.center,
                                shadow=ft.BoxShadow(blur_radius=12, color="#58a6ff44", spread_radius=1),
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Fillipus Eamon", size=13, color="#e6edf3", weight="bold"),
                                    ft.Text("Lead Developer · ENGITRIAD", size=10, color="#8b949e"),
                                ],
                                spacing=1,
                            ),
                        ],
                        spacing=10,
                        vertical_alignment="center",
                    ),
                    ft.Row(controls=nav_btns, spacing=0),
                    ft.Row(
                        controls=[
                            ft.Container(
                                width=8, height=8,
                                bgcolor="#58a6ff",
                                border_radius=4,
                                shadow=ft.BoxShadow(blur_radius=8, color="#58a6ff44", spread_radius=1),
                            ),
                            ft.Text("Live", size=11, color="#58a6ff"),
                            ft.Text("2026", size=11, color="#484f58"),
                        ],
                        spacing=6,
                        vertical_alignment="center",
                    ),
                ],
                alignment="spaceBetween",
                vertical_alignment="center",
            ),
            bgcolor="#0d1117",
            border=ft.border.only(bottom=ft.BorderSide(1, "#21262d")),
            padding=ft.padding.symmetric(horizontal=28, vertical=10),
            shadow=ft.BoxShadow(blur_radius=20, color="#000000aa", spread_radius=0),
        )

        page.add(
            ft.Column(
                controls=[
                    navbar,
                    ft.Container(
                        content=content_area,
                        padding=ft.padding.symmetric(horizontal=32, vertical=24),
                        expand=True,
                    )
                ],
                expand=True,
                spacing=0
            )
        )
        page.update()

    # ── Thread-Safe Splash Screen ───────────────────────────────────────────
    def build_splash():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        def load_b64(filename):
            try:
                with open(os.path.join(BASE_DIR, "assets", filename), "rb") as f:
                    return base64.b64encode(f.read()).decode()
            except Exception:
                return None

        profile_b64 = load_b64("profile_nobg.png")

        ring = ft.Container(
            width=180, height=180, border_radius=90,
            border=ft.border.all(2, "#58a6ff"),
            opacity=0.0, 
            animate_opacity=ft.animation.Animation(800, "easeOut"),
            shadow=ft.BoxShadow(blur_radius=20, color="#58a6ff44", spread_radius=2),
        )
        ring2 = ft.Container(
            width=200, height=200, border_radius=100,
            border=ft.border.all(1, "#58a6ff66"),
            opacity=0.0, 
            animate_opacity=ft.animation.Animation(1000, "easeOut"),
        )
        
        if profile_b64:
            photo_content = ft.Image(src_base64=profile_b64, width=160, height=160, fit="cover")
        else:
            photo_content = ft.Text("FE", size=48, color="#fff", weight="bold")

        photo = ft.Container(
            content=photo_content,
            width=160, height=160, border_radius=80,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor="#0d1117", opacity=0.0, 
            animate_opacity=ft.animation.Animation(800, "easeOut")
        )
        
        name_text = ft.Text(
            "Fillipus Eamon", size=36, color="#e6edf3", weight="bold", opacity=0.0,
            animate_opacity=ft.animation.Animation(600, "easeOut")
        )
        role_text = ft.Text(
            "Lead Developer  ·  ENGITRIAD", size=14, color="#8b949e", opacity=0.0,
            animate_opacity=ft.animation.Animation(600, "easeOut")
        )
        unam_text = ft.Text(
            "UNIVERSITY OF NAMIBIA", size=13, color="#3fb950", weight="bold", opacity=0.0,
            animate_opacity=ft.animation.Animation(600, "easeOut")
        )
        tagline = ft.Text(
            "Triad of Terror App Development  ·  Web Portfolio 2026", size=12, color="#484f58", opacity=0.0,
            animate_opacity=ft.animation.Animation(600, "easeOut")
        )
        
        progress = ft.ProgressBar(
            width=300, bgcolor="#21262d", color="#3fb950", value=0, opacity=0.0,
            animate_opacity=ft.animation.Animation(400, "easeOut")
        )
        loading_txt = ft.Text(
            "Loading...", size=11, color="#484f58", opacity=0.0,
            animate_opacity=ft.animation.Animation(400, "easeOut")
        )
        
        enter_btn = ft.Container(
            content=ft.Text("Enter Portfolio →", size=14, color="#0d1117", weight="bold"),
            bgcolor="#3fb950", border_radius=8,
            padding=ft.padding.symmetric(horizontal=32, vertical=14),
            opacity=0.0, 
            animate_opacity=ft.animation.Animation(600, "easeOut"),
            on_click=lambda e: launch_app(), ink=True,
            shadow=ft.BoxShadow(blur_radius=20, color="#3fb95044", spread_radius=2),
        )

        photo_stack = ft.Stack(
            width=210, height=210,
            controls=[
                ft.Container(content=ring2, alignment=ft.alignment.center, width=210, height=210),
                ft.Container(content=ring,  alignment=ft.alignment.center, width=210, height=210),
                ft.Container(content=photo, alignment=ft.alignment.center, width=210, height=210),
            ],
        )

        splash = ft.Container(
            content=ft.Column(
                controls=[
                    photo_stack, name_text, role_text, unam_text, tagline,
                    ft.Container(height=10), progress, loading_txt,
                    ft.Container(height=10), enter_btn
                ],
                horizontal_alignment="center",
                alignment="center",
                spacing=12,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )

        page.add(splash)
        page.update()

        async def animate_in_async():
            await asyncio.sleep(0.2)
            ring.opacity = 1.0; ring.update()
            ring2.opacity = 1.0; ring2.update()
            await asyncio.sleep(0.2)
            photo.opacity = 1.0; photo.update()
            await asyncio.sleep(0.3)
            name_text.opacity = 1.0; name_text.update()
            await asyncio.sleep(0.15)
            role_text.opacity = 1.0; role_text.update()
            await asyncio.sleep(0.1)
            unam_text.opacity = 1.0; unam_text.update()
            await asyncio.sleep(0.1)
            tagline.opacity = 1.0; tagline.update()
            await asyncio.sleep(0.2)
            progress.opacity = 1.0; loading_txt.opacity = 1.0
            progress.update(); loading_txt.update()
            
            for v in [0.2, 0.4, 0.6, 0.8, 1.0]:
                progress.value = v
                progress.update()
                await asyncio.sleep(0.2)
                
            loading_txt.value = "System Ready!"; loading_txt.color = "#3fb950"
            loading_txt.update()
            await asyncio.sleep(0.2)
            enter_btn.opacity = 1.0; enter_btn.update()

        page.run_task(animate_in_async)

    def launch_app():
        page.controls.clear()
        page.update()
        build_main_app()
        
    build_splash()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, port=int(os.environ.get("PORT", 8080)))