import flet as ft
import threading
import math
import time
import os

BLOG_TITLE = "Technical Blog"
BLOG_SUBTITLE = "Confidence in Concepts — watch the video explanation below."

# Path to your video asset
VIDEO_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "assets", "Blog.mp4"
)


def blog_page():

    # Custom continuous glowing background animation
    def make_glow_card(inner_content, offset=0):
        glow = ft.Container(
            content=inner_content,
            border_radius=12,
            padding=2,
            bgcolor="#640000",
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
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

    # --- NATIVE INLINE VIDEO PLAYER CONFIGURATION ---
    video_player = ft.Video(
        expand=True,
        playlist=[
            ft.VideoMedia(VIDEO_PATH)
        ],
        show_controls=True,
        autoplay=False,
        muted=False,
    )

    # Video container adjusted to match a vertical phone display layout
    video_container = ft.Container(
        content=video_player,
        bgcolor="#000000",
        border_radius=10,
        width=340,         # Narrowed down to wrap tightly around a 9:16 frame
        height=580,        # Tall vertical canvas height
        alignment=ft.alignment.center,
    )

    # Wrap the embedded player with your custom pulsing glow animation
    video_card = make_glow_card(video_container, offset=0)

    # --- HOVER ANIMATION EFFECT FOR THE VIDEO CONTAINER ---
    def on_video_hover(e):
        video_card.scale = 1.03 if e.data == "true" else 1.0
        video_card.update()

    # Wrap inside a transparent container to handle mouse hover interactions cleanly
    video_hover_wrapper = ft.Container(
        content=video_card,
        on_hover=on_video_hover,
        border_radius=12,
        alignment=ft.alignment.center, # Keeps the phone card centered on the page layout
    )

    # --- ENHANCED HEADER ANIMATIONS ---
    title_text = ft.Text(BLOG_TITLE, size=32, color="#e6edf3", weight="bold")
    
    underline = ft.Container(
        width=0, 
        height=3, 
        bgcolor="#00c853", 
        border_radius=2,
        animate=ft.animation.Animation(800, ft.AnimationCurve.DECELERATE)
    )
    
    subtitle_text = ft.Text(BLOG_SUBTITLE, size=14, color="#8b949e")

    # Group headers into an animated opacity block
    header_container = ft.Container(
        content=ft.Column(
            controls=[title_text, underline, subtitle_text],
            horizontal_alignment="center",
            spacing=8,
        ),
        opacity=0,
        animate_opacity=ft.animation.Animation(1000, ft.AnimationCurve.EASE_OUT),
    )

    # Handle component arrival entrance updates
    def trigger_entrance_animations():
        time.sleep(0.1)
        header_container.opacity = 1
        underline.width = 80
        try:
            header_container.update()
            underline.update()
        except Exception:
            pass

    threading.Thread(target=trigger_entrance_animations, daemon=True).start()

    return ft.Column(
        controls=[
            header_container,
            ft.Divider(color="#21262d", height=20),
            video_hover_wrapper,
        ],
        spacing=20,
        scroll="auto",
        horizontal_alignment="center",
    )