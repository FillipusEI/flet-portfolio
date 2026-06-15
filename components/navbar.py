import flet as ft
from pages.timeline import timeline_page
from pages.matlab import matlab_page
from pages.blog import blog_page
from pages.github import github_page


def main(page: ft.Page):
    page.title = "Portfolio 2026"
    page.bgcolor = "#0d1117"  # Deep dark background
    page.padding = 0
    # Let the containers inside handle their own scrolling for a fixed navbar look
    page.scroll = None  

    # Colors mapping (GitHub dark-mode palette)
    text_active = "#ffffff"
    text_inactive = "#8b949e"
    accent_color = "#58a6ff"  # Clean neon blue

    nav_buttons = []

    # --- Page Switcher ---
    def switch_page(index):
        # Update text styles and active indicators
        for i, btn in enumerate(nav_buttons):
            # The structure of our button container is: Column -> [Text, Container(indicator)]
            btn.content.controls[0].color = text_active if i == index else text_inactive
            btn.content.controls[1].visible = True if i == index else False
            btn.update()

        # Page components factory
        builders = [
            lambda: timeline_page(page),
            lambda: matlab_page(page),
            lambda: blog_page(),
            lambda: github_page(),
        ]
        
        content_area.controls.clear()
        content_area.controls.append(builders[index]())
        content_area.update()

    # --- Navigation Items Builder ---
    labels = ["🗓 Timeline", "🔢 MATLAB", "📝 Blog", "🐙 GitHub"]
    
    for i, label in enumerate(labels):
        is_active = (i == 0)
        
        # Inner layout for a custom text button with a bottom active line indicator
        btn_layout = ft.Column(
            controls=[
                ft.Text(
                    label, 
                    color=text_active if is_active else text_inactive, 
                    weight="w500", 
                    size=14
                ),
                # The underline active indicator
                ft.Container(
                    height=2, 
                    width=30, 
                    bgcolor=accent_color, 
                    border_radius=1, 
                    visible=is_active
                )
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=4
        )

        # Container wrapper to handle hover styling and click events
        nav_item = ft.Container(
            content=btn_layout,
            on_click=lambda e, idx=i: switch_page(idx),
            on_hover=lambda e: on_nav_hover(e),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            cursor="pointer",
            animate_opacity=150,
        )
        
        nav_buttons.append(nav_item)

    # Hover effect callback
    def on_nav_hover(e):
        # Only change opacity if it's not the active button
        # (Checking visibility of its underline indicator to know if it's active)
        if not e.control.content.controls[1].visible:
            e.control.content.controls[0].color = text_active if e.data == "true" else text_inactive
            e.control.update()

    # --- Custom Modern Navbar ---
    navbar = ft.Container(
        content=ft.Row(
            controls=[
                # Brand Logo / Name
                ft.Row(
                    controls=[
                        ft.Container(
                            width=10,
                            height=10,
                            bgcolor=accent_color,
                            shape=ft.BoxShape.CIRCLE,
                        ),
                        ft.Text(
                            "Portfolio '26", 
                            size=18, 
                            color="#e6edf3", 
                            weight="bold",
                            font_family="Segoe UI"
                        ),
                    ],
                    spacing=10
                ),
                # Nav Links Array
                ft.Row(
                    controls=nav_buttons, 
                    spacing=4,
                    alignment="center"
                ),
            ],
            alignment="spaceBetween",
        ),
        bgcolor="#161b22",  # Sleek dark gray header background
        border=ft.border.only(bottom=ft.BorderSide(1, "#30363d")),
        padding=ft.padding.symmetric(horizontal=40, vertical=12),
    )

    # --- Dynamic Content Area ---
    content_area = ft.Column(
        controls=[timeline_page(page)],
        scroll="auto",
        expand=True,
    )

    # Base Layout Structure
    page.add(
        ft.Column(
            controls=[
                navbar,
                ft.Container(
                    content=content_area,
                    padding=ft.padding.symmetric(horizontal=40, vertical=28),
                    expand=True,
                )
            ],
            expand=True,
            spacing=0
        )
    )


if __name__ == "__main__":
    ft.app(target=main, port=3000, view="web_browser", assets_dir="assets")