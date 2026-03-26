import flet as ft
import requests
from typing import List, Dict, Optional

API_BASE_URL = "http://192.168.100.40:3500"

# ── STYLE COLOR MAP ───────────────────────────────────────────────────────────
STYLE_COLOR_MAP = {
    "nature":    "#2d6a4f",
    "beach":     "#0077b6",
    "temple":    "#c77dff",
    "cafe&food": "#e07a5f",
    "culture":   "#e9c46a",
    "city":      "#4361ee",
}
DEFAULT_EMOJI = "📍"
DEFAULT_COLOR = "#9e9e9e"


def style_color(style_name: Optional[str]) -> str:
    return STYLE_COLOR_MAP.get((style_name or "").lower(), DEFAULT_COLOR)


# ── LOGIN PAGE ────────────────────────────────────────────────────────────────
class LoginPage:
    def __init__(self, page: ft.Page, on_login_success):
        self.page = page
        self.on_login_success = on_login_success
        self.username_field = ft.TextField(
            label="Username",
            border_radius=12,
            bgcolor="#ffffff",
            border_color="#e0e0e0",
            focused_border_color="#FF5F3D",
            label_style=ft.TextStyle(color="#888888", size=12),
            text_style=ft.TextStyle(color="#1a1a1a", size=14),
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            filled=True,
        )
        self.password_field = ft.TextField(
            label="Password",
            password=True,
            border_radius=12,
            bgcolor="#ffffff",
            border_color="#e0e0e0",
            focused_border_color="#FF5F3D",
            label_style=ft.TextStyle(color="#888888", size=12),
            text_style=ft.TextStyle(color="#1a1a1a", size=14),
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            filled=True,
        )
        self.error_message = ft.Text(
            "",
            color="#d32f2f",
            size=12,
            text_align=ft.TextAlign.CENTER,
        )

    def _on_login_click(self, e):
        """Handle login button click"""
        username = self.username_field.value.strip()
        password = self.password_field.value.strip()

        if not username or not password:
            self.error_message.value = "Please enter username and password"
            self.error_message.update()
            return

        try:
            # Send login request to API
            response = requests.post(
                f"{API_BASE_URL}/login",
                json={"username": username, "password": password},
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    # Login successful - call callback
                    self.on_login_success()
                else:
                    # Login failed
                    self.error_message.value = "Invalid username or password"
                    self.error_message.update()
            else:
                self.error_message.value = "Invalid username or password"
                self.error_message.update()
        except Exception as ex:
            self.error_message.value = f"Connection error: {str(ex)}"
            self.error_message.update()

    def build_login_page(self):
        """Build the login page UI"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(expand=True),
                    ft.Column(
                        [
                            # Logo/Header
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Container(
                                            content=ft.Text("T", size=32, weight=ft.FontWeight.BOLD, color="#ffffff"),
                                            width=64, height=64,
                                            border_radius=32,
                                            bgcolor="#FF5F3D",
                                            alignment=ft.Alignment(0, 0),
                                            shadow=ft.BoxShadow(blur_radius=16, color="#FF5F3D44", offset=ft.Offset(0, 4)),
                                        ),
                                        ft.Text("Travel App", size=24, weight=ft.FontWeight.BOLD, color="#1a1a1a", text_align=ft.TextAlign.CENTER),
                                        ft.Text("Discover amazing places", size=13, color="#888888", text_align=ft.TextAlign.CENTER),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=12,
                                ),
                                padding=ft.padding.symmetric(vertical=24),
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Container(height=24),
                            # Form
                            ft.Column(
                                [
                                    # Username field
                                    self.username_field,
                                    ft.Container(height=12),
                                    # Password field
                                    self.password_field,
                                    ft.Container(height=16),
                                    # Login button
                                    ft.ElevatedButton(
                                        content=ft.Row(
                                            [
                                                ft.Text("Login", color="#ffffff", size=16, weight=ft.FontWeight.BOLD),
                                                ft.Text("→", color="#ffffff", size=18),
                                            ],
                                            spacing=8,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        bgcolor="#FF5F3D",
                                        width=9999,
                                        height=52,
                                        on_click=self._on_login_click,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=12),
                                        ),
                                    ),
                                    ft.Container(height=12),
                                    # Error message
                                    self.error_message,
                                ],
                                spacing=0,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(expand=True),
                ],
                spacing=0,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=24, vertical=20),
            bgcolor="#f5f5f5",
            expand=True,
        )


# ── MAIN APP ──────────────────────────────────────────────────────────────────
class TravelApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.all_places: List[Dict]      = []
        self.all_categories: List[Dict]  = []
        self.filtered_places: List[Dict] = []
        self.selected_style_id: Optional[int] = None
        self.search_query: str = ""
        self.nav_index: int    = 0

        self.places_column   = ft.Column(scroll="auto", spacing=0, expand=True)
        self.category_row: Optional[ft.Row]         = None
        self.search_field: Optional[ft.TextField]   = None

    # ── PAGE SETUP ────────────────────────────────────────────────────────────
    def setup_page(self):
        self.page.title         = "Travel App"
        self.page.bgcolor       = "#f5f5f5"
        self.page.padding       = 0
        self.page.window_width  = 390
        self.page.window_height = 844

    # ── DATA LAYER ────────────────────────────────────────────────────────────
    def load_data(self):
        """
        Fetch data from MariaDB via FastAPI:
        GET /styles       →  style_travel table
        GET /places       →  rec_travel table
        """
        try:
            r = requests.get(f"{API_BASE_URL}/styles", timeout=3)
            r.raise_for_status()
            self.all_categories = r.json()
        except Exception as e:
            print(f"Error loading categories: {e}")
            self.all_categories = []

        try:
            r = requests.get(f"{API_BASE_URL}/places", timeout=3)
            r.raise_for_status()
            self.all_places = r.json()
        except Exception as e:
            print(f"Error loading places: {e}")
            self.all_places = []

        self.apply_filters()

    def load_places_by_style(self, style_id: int):
        """
        Fetch places filtered by style_id from API
        """
        try:
            r = requests.get(f"{API_BASE_URL}/places?style_id={style_id}", timeout=3)
            r.raise_for_status()
            self.filtered_places = r.json()
        except Exception as e:
            print(f"Error loading places by style: {e}")
            # Fallback to client-side filter
            self.filtered_places = [
                p for p in self.all_places if p.get("style_id") == style_id
            ]

    def apply_filters(self):
        """Category + search-text filter (client-side)."""
        if self.selected_style_id is None:
            base = list(self.all_places)
        else:
            base = [p for p in self.all_places if p.get("style_id") == self.selected_style_id]

        if self.search_query.strip():
            q = self.search_query.lower()
            base = [
                p for p in base
                if q in p.get("place_name", "").lower()
                or q in p.get("place_descript", "").lower()
            ]
        self.filtered_places = base

    def get_category(self, style_id: Optional[int]) -> Dict:
        """Get category by style_id, with auto-generated emoji if missing"""
        emoji_map = {
            "nature": "🌿", "beach": "🏖️", "temple": "🛕",
            "cafe&food": "☕", "cafe": "☕", "food": "🍽️",
            "culture": "🏛️", "city": "🏙️", "urban": "🏙️"
        }
        
        for c in self.all_categories:
            if c["style_id"] == style_id:
                # Add emoji if missing
                if "style_icon" not in c:
                    style_name = c.get("style_name", "").lower()
                    c["style_icon"] = emoji_map.get(style_name, DEFAULT_EMOJI)
                return c
        return {"style_id": None, "style_name": "other", "style_icon": DEFAULT_EMOJI}

    # ── HEADER ────────────────────────────────────────────────────────────────
    def build_header(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("T", size=18, weight=ft.FontWeight.BOLD, color="#ffffff"),
                                width=46, height=46,
                                border_radius=23,
                                bgcolor="#FF5F3D",
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Column(
                                [
                                    ft.Text("Hi, Traveler! 👋", size=12, color="#aaaaaa"),
                                    ft.Text(
                                        "Where do you want to go?",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color="#1a1a1a",
                                    ),
                                ],
                                spacing=1, tight=True,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Stack(
                        [
                            ft.Container(
                                content=ft.Text("🔔", size=24),
                                width=44, height=44,
                                border_radius=22,
                                bgcolor="#ffffff",
                                alignment=ft.Alignment(0, 0),
                                shadow=ft.BoxShadow(blur_radius=10, color="#00000015", offset=ft.Offset(0, 3)),
                            ),
                            ft.Container(width=9, height=9, border_radius=5, bgcolor="#FF5F3D", right=8, top=8),
                        ],
                        width=44, height=44,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=18),
            bgcolor="#f5f5f5",
        )

    # ── SEARCH ────────────────────────────────────────────────────────────────
    def build_search(self):
        self.search_field = ft.TextField(
            hint_text="🔍 Search for places...",
            border_radius=16,
            bgcolor="#ffffff",
            border_color="transparent",
            focused_border_color="#FF5F3D",
            hint_style=ft.TextStyle(color="#c0c0c0"),
            text_style=ft.TextStyle(color="#1a1a1a", size=14),
            on_change=self._on_search,
            content_padding=ft.padding.symmetric(horizontal=8, vertical=14),
            filled=True,
            fill_color="#ffffff",
        )
        return ft.Container(
            content=self.search_field,
            padding=ft.padding.symmetric(horizontal=20, vertical=4),
            shadow=ft.BoxShadow(blur_radius=14, color="#0000000d", offset=ft.Offset(0, 4)),
        )

    # ── CATEGORIES ────────────────────────────────────────────────────────────
    def _build_chip(self, style_id: Optional[int], style_name: str, emoji: str) -> ft.Container:
        is_selected = self.selected_style_id == style_id

        display_map = {
            "All":       "ทั้งหมด",
            "nature":    "ธรรมชาติ",
            "beach":     "ทะเล",
            "temple":    "วัด",
            "cafe&food": "คาเฟ่",
            "culture":   "วัฒนธรรม",
            "city":      "เมือง",
        }
        display_name = display_map.get(style_name, style_name.capitalize())

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(emoji, size=22),
                        width=52, height=52,
                        border_radius=16,
                        bgcolor="#FF5F3D" if is_selected else "#f0f0f0",
                        alignment=ft.Alignment(0, 0),
                        shadow=ft.BoxShadow(
                            blur_radius=8 if is_selected else 0,
                            color="#FF5F3D44" if is_selected else "#00000000",
                            offset=ft.Offset(0, 3),
                        ),
                    ),
                    ft.Text(
                        display_name, size=11,
                        color="#FF5F3D" if is_selected else "#888888",
                        weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6, tight=True,
            ),
            on_click=lambda e, sid=style_id: self._on_category(sid),
            padding=ft.padding.only(right=10),
        )

    def build_categories(self):
        """Build category chips with auto-generated emojis"""
        emoji_map = {
            "nature": "🌿", "beach": "🏖️", "temple": "🛕",
            "cafe&food": "☕", "cafe": "☕", "food": "🍽️",
            "culture": "🏛️", "city": "🏙️", "urban": "🏙️"
        }
        
        chips = [self._build_chip(None, "All", "🗺️")]
        for cat in self.all_categories:
            style_name = cat.get("style_name", "").lower()
            emoji = emoji_map.get(style_name, DEFAULT_EMOJI)
            chips.append(self._build_chip(cat["style_id"], cat["style_name"], emoji))

        self.category_row = ft.Row(chips, scroll="auto", spacing=0)
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text("Categories", size=17, weight=ft.FontWeight.BOLD, color="#1a1a1a"),
                        padding=ft.padding.only(left=20, right=20, top=18, bottom=12),
                    ),
                    ft.Container(content=self.category_row, padding=ft.padding.only(left=20)),
                ],
                spacing=0,
            )
        )

    def _refresh_categories(self):
        """Refresh category chips"""
        emoji_map = {
            "nature": "🌿", "beach": "🏖️", "temple": "🛕",
            "cafe&food": "☕", "cafe": "☕", "food": "🍽️",
            "culture": "🏛️", "city": "🏙️", "urban": "🏙️"
        }
        
        self.category_row.controls.clear()
        self.category_row.controls.append(self._build_chip(None, "All", "🗺️"))
        for cat in self.all_categories:
            style_name = cat.get("style_name", "").lower()
            emoji = emoji_map.get(style_name, DEFAULT_EMOJI)
            self.category_row.controls.append(
                self._build_chip(cat["style_id"], cat["style_name"], emoji)
            )

    # ── PLACE CARD ────────────────────────────────────────────────────────────
    def build_place_card(self, place: Dict) -> ft.Container:
        cat      = self.get_category(place.get("style_id"))
        style_nm = cat.get("style_name", "")
        emoji    = cat.get("style_icon") or DEFAULT_EMOJI
        color    = style_color(style_nm)
        rating   = place.get("rating", 0)
        img_src  = place.get("place_image", "")

        img_widget = (
            ft.Image(
                src=img_src,
                width=9999, height=150,
                fit="cover",
                border_radius=ft.border_radius.only(top_left=18, top_right=18),
                error_content=ft.Container(
                    height=150, bgcolor="#e0e0e0",
                    border_radius=ft.border_radius.only(top_left=18, top_right=18),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("🖼️", size=36),
                ),
            )
            if img_src
            else ft.Container(
                height=150, bgcolor="#e0e0e0",
                border_radius=ft.border_radius.only(top_left=18, top_right=18),
                alignment=ft.Alignment(0, 0),
                content=ft.Text("🖼️", size=36),
            )
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Stack(
                        [
                            img_widget,
                            ft.Container(
                                content=ft.Text("🤍", size=16),
                                width=32, height=32,
                                border_radius=16,
                                bgcolor="#00000040",
                                alignment=ft.Alignment(0, 0),
                                top=10, right=10,
                            ),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text("★", size=13, color="#f9c74f"),
                                        ft.Text(f"{rating:.1f}", size=11, color="#ffffff", weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=2, tight=True,
                                ),
                                padding=ft.padding.symmetric(horizontal=7, vertical=3),
                                border_radius=10,
                                bgcolor="#00000055",
                                bottom=8, right=8,
                            ),
                        ],
                        height=150,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    place.get("place_name", ""),
                                    size=13, weight=ft.FontWeight.BOLD, color="#1a1a1a",
                                    max_lines=1,
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        f"{emoji}  {style_nm}",
                                        size=10, color=color, weight=ft.FontWeight.W_600,
                                    ),
                                    padding=ft.padding.symmetric(horizontal=7, vertical=3),
                                    border_radius=8,
                                    bgcolor=color + "18",
                                ),
                                ft.Row(
                                    [
                                        ft.Text("🕐", size=11),
                                        ft.Text(place.get("openning_hr", ""), size=10, color="#aaaaaa"),
                                    ],
                                    spacing=3,
                                ),
                            ],
                            spacing=5, tight=True,
                        ),
                        padding=ft.padding.all(10),
                    ),
                ],
                spacing=0, tight=True,
            ),
            border_radius=18,
            bgcolor="#ffffff",
            shadow=ft.BoxShadow(blur_radius=14, color="#0000001a", offset=ft.Offset(0, 4)),
            on_click=lambda e, p=place: self._on_place_tap(p),
        )

    # ── PLACE GRID ────────────────────────────────────────────────────────────
    def build_place_grid(self):
        self.places_column.controls.clear()

        if not self.filtered_places:
            self.places_column.controls.append(
                ft.Container(
                    content=ft.Column(
                        [ft.Text("🔍", size=48), ft.Text("ไม่พบสถานที่", size=16, color="#9e9e9e")],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    alignment=ft.Alignment(0, 0),
                    height=200,
                )
            )
            return

        self.places_column.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            f"Top trips  ({len(self.filtered_places)})",
                            size=17, weight=ft.FontWeight.BOLD, color="#1a1a1a",
                        ),
                        ft.TextButton("Explore →"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=ft.padding.only(left=20, right=8, top=18, bottom=6),
            )
        )

        for i in range(0, len(self.filtered_places), 2):
            left  = self.filtered_places[i]
            right = self.filtered_places[i + 1] if i + 1 < len(self.filtered_places) else None

            left_card = ft.Container(self.build_place_card(left), expand=True)
            if right:
                right_card = ft.Container(self.build_place_card(right), expand=True)
                row = ft.Row([left_card, right_card], spacing=14, expand=True)
            else:
                row = ft.Row([left_card, ft.Container(expand=True)], spacing=14, expand=True)

            self.places_column.controls.append(
                ft.Container(content=row, padding=ft.padding.symmetric(horizontal=20, vertical=5))
            )

        self.places_column.controls.append(ft.Container(height=24))

    # ── EXPLORE PAGE ──────────────────────────────────────────────────────────
    def build_explore_page(self):
        return ft.Column(
            [
                self.build_header(),
                self.build_search(),
                self.build_categories(),
                ft.Container(height=4),
                self.places_column,
            ],
            spacing=0, expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # ── BOTTOM NAV ────────────────────────────────────────────────────────────
    def build_bottom_nav(self):
        nav_data = [
            ("🏠",     "🏠",  "Home"),
            ("🧭", "🧭",       "Explore"),
            ("🤍",  "❤️",      "Saved"),
            ("👤",   "👤",        "Profile"),
        ]
        items = []
        for i, (off_icon, on_icon, label) in enumerate(nav_data):
            active = i == self.nav_index
            items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Text(
                                    on_icon if active else off_icon,
                                    size=22,
                                    color="#ffffff" if active else "#aaaaaa",
                                ),
                                width=42 if active else 32,
                                height=32,
                                border_radius=12,
                                bgcolor="#FF5F3D" if active else "transparent",
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Text(
                                label, size=10,
                                color="#FF5F3D" if active else "#aaaaaa",
                                weight=ft.FontWeight.W_600 if active else ft.FontWeight.NORMAL,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2, tight=True,
                    ),
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                    on_click=lambda e, idx=i: self._on_nav(idx),
                    padding=ft.padding.symmetric(vertical=10),
                )
            )
        return ft.Container(
            content=ft.Row(items, spacing=0),
            bgcolor="#1a1a1a",
            border_radius=ft.border_radius.only(top_left=24, top_right=24),
            shadow=ft.BoxShadow(blur_radius=20, color="#0000002a", offset=ft.Offset(0, -4)),
            padding=ft.padding.only(bottom=6),
        )

    # ── DETAIL PAGE ───────────────────────────────────────────────────────────
    def build_detail_page(self, place: Dict):
        cat      = self.get_category(place.get("style_id"))
        style_nm = cat.get("style_name", "")
        emoji    = cat.get("style_icon") or DEFAULT_EMOJI
        color    = style_color(style_nm)
        img_src  = place.get("place_image", "")
        rating   = place.get("rating", 0)
        place_id = place.get("place_id")
        
        # Fetch travel cost data
        cost_data = {"budget_info": None, "transportation_info": None, "total_cost": None}
        try:
            response = requests.get(f"{API_BASE_URL}/travel-cost/{place_id}", timeout=3)
            if response.status_code == 200:
                cost_data = response.json()
        except Exception as e:
            print(f"Error loading travel cost: {e}")
        
        # Fetch transportation recommendations
        transport_options = []
        try:
            response = requests.get(f"{API_BASE_URL}/transportation-options/{place_id}", timeout=3)
            if response.status_code == 200:
                transport_options = response.json()
                print(f"✓ Loaded {len(transport_options)} transportation option(s) for place {place_id}")
            else:
                print(f"✗ API returned status {response.status_code}")
        except Exception as e:
            print(f"✗ Error loading transportation options: {e}")
        
        # Extract cost information
        budget_info = cost_data.get("budget_info")
        transport_info = cost_data.get("transportation_info")
        total_cost = cost_data.get("total_cost")

        # Build transportation recommendations section
        transport_section = []
        
        # Prioritize transport_options over transport_info
        options_to_display = transport_options if (transport_options and len(transport_options) > 0) else []
        
        # If no options list but have single transport_info, use that
        if not options_to_display and transport_info:
            options_to_display = [transport_info]
        
        if options_to_display:
            transport_section.append(ft.Divider(height=20, color="#f0f0f0"))
            
            # Header with option count
            header_text = "🚌 Transportation Options"
            if len(options_to_display) > 1:
                header_text = f"🚌 Transportation Options ({len(options_to_display)} available)"
            
            transport_section.append(ft.Text(header_text, size=15, weight=ft.FontWeight.BOLD, color="#FF5F3D"))
            transport_section.append(ft.Container(height=6))  # Spacer
            
            # Display each option
            for idx, option in enumerate(options_to_display):
                tran_cost = option.get("tran_cost", 0)
                tran_name = option.get("tran_name", "Transportation")
                tran_time = option.get("tran_time", "N/A")
                is_recommended = idx == 0  # First option is recommended
                
                if is_recommended:
                    # ⭐ RECOMMENDED OPTION - Orange background
                    transport_section.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(f"🚌 {tran_name.capitalize()}", size=12, color="#ffffff", weight=ft.FontWeight.W_600, expand=True),
                                    ft.Container(
                                        content=ft.Text("⭐ Recommended", size=10, color="#ffffff", weight=ft.FontWeight.W_600),
                                        padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                        border_radius=4,
                                        bgcolor="#CC3D20",
                                    ),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=8),
                                ft.Row([
                                    ft.Text("Best rated option", size=10, color="#e8e8e8"),
                                ]),
                                ft.Container(height=4),
                                ft.Row([
                                    ft.Text("Price:", size=11, color="#e8e8e8"),
                                    ft.Text(f"฿{tran_cost:,.0f}", size=13, color="#ffffff", weight=ft.FontWeight.BOLD),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Row([
                                    ft.Text("⏱️ Duration:", size=11, color="#e8e8e8"),
                                    ft.Text(f"{tran_time} minutes", size=13, color="#ffffff"),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ], spacing=3, tight=True),
                            padding=ft.padding.symmetric(horizontal=14, vertical=12),
                            border_radius=10,
                            bgcolor="#FF5F3D",
                            shadow=ft.BoxShadow(blur_radius=8, color="#FF5F3D44", offset=ft.Offset(0, 2)),
                            margin=ft.margin.only(bottom=10),
                        )
                    )
                else:
                    # 🔄 ALTERNATIVE OPTIONS - Light gray background (same layout as recommended)
                    transport_section.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(f"🚌 {tran_name.capitalize()}", size=12, color="#333333", weight=ft.FontWeight.W_600, expand=True),
                                    ft.Container(
                                        content=ft.Text("↔️ Alternative", size=10, color="#666666", weight=ft.FontWeight.W_600),
                                        padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                        border_radius=4,
                                        bgcolor="#d0d0d0",
                                    ),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=8),
                                ft.Row([
                                    ft.Text("Other available option", size=10, color="#666666"),
                                ]),
                                ft.Container(height=4),
                                ft.Row([
                                    ft.Text("Price:", size=11, color="#666666"),
                                    ft.Text(f"฿{tran_cost:,.0f}", size=13, color="#1a1a1a", weight=ft.FontWeight.BOLD),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Row([
                                    ft.Text("⏱️ Duration:", size=11, color="#666666"),
                                    ft.Text(f"{tran_time} minutes", size=13, color="#1a1a1a"),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ], spacing=3, tight=True),
                            padding=ft.padding.symmetric(horizontal=14, vertical=12),
                            border_radius=10,
                            bgcolor="#f0f0f0",
                            shadow=ft.BoxShadow(blur_radius=4, color="#00000010", offset=ft.Offset(0, 1)),
                            margin=ft.margin.only(bottom=10),
                        )
                    )

        # Build cost display section
        cost_section = []
        if budget_info or transport_info or total_cost:
            cost_section.append(ft.Divider(height=20, color="#f0f0f0"))
            cost_section.append(ft.Text("💰 Travel Cost Details", size=15, weight=ft.FontWeight.BOLD, color="#FF5F3D"))
            
            # Budget info
            if budget_info:
                min_budget = budget_info.get("min_budget", 0)
                max_budget = budget_info.get("max_budget", 0)
                avg_budget = (min_budget + max_budget) / 2
                cost_section.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Budget Range", size=12, color="#888888", weight=ft.FontWeight.W_600),
                            ft.Row([
                                ft.Text(f"฿{min_budget:,.0f}", size=11, color="#1a1a1a"),
                                ft.Text("—", size=11, color="#1a1a1a"),
                                ft.Text(f"฿{max_budget:,.0f}", size=11, color="#1a1a1a"),
                            ], spacing=8),
                            ft.Text(f"Average: ฿{avg_budget:,.0f}", size=11, color="#FF5F3D", weight=ft.FontWeight.W_600),
                        ], spacing=3, tight=True),
                        padding=ft.padding.symmetric(horizontal=12, vertical=8),
                        border_radius=8,
                        bgcolor="#f5f5f5",
                    )
                )
            
            
            # Total cost
            if total_cost is not None:
                cost_section.append(ft.Container(height=6))
                cost_section.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text("Total Cost", size=14, color="#ffffff", weight=ft.FontWeight.BOLD),
                            ft.Text(f"฿{total_cost:,.0f}", size=16, color="#ffffff", weight=ft.FontWeight.BOLD),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=ft.padding.symmetric(horizontal=16, vertical=12),
                        border_radius=10,
                        bgcolor="#FF5F3D",
                    )
                )

        return ft.Column(
            [
                ft.Stack(
                    [
                        ft.Image(
                            src=img_src,
                            width=9999, height=320,
                            fit="cover",
                            error_content=ft.Container(
                                height=320, bgcolor="#e0e0e0",
                                alignment=ft.Alignment(0, 0),
                                content=ft.Text("🏞️", size=60),
                            ),
                        ),
                        ft.Container(
                            content=ft.Text("←", size=16, color="#1a1a1a"),
                            width=40, height=40,
                            border_radius=20,
                            bgcolor="#ffffffdd",
                            alignment=ft.Alignment(0, 0),
                            top=52, left=18,
                            on_click=lambda e: self._go_home(),
                            shadow=ft.BoxShadow(blur_radius=8, color="#00000020", offset=ft.Offset(0, 2)),
                        ),
                        ft.Container(
                            content=ft.Text("🤍", size=18),
                            width=40, height=40,
                            border_radius=20,
                            bgcolor="#ffffffdd",
                            alignment=ft.Alignment(0, 0),
                            top=52, right=18,
                            shadow=ft.BoxShadow(blur_radius=8, color="#00000020", offset=ft.Offset(0, 2)),
                        ),
                    ],
                    height=320,
                ),
                ft.Container(
                    content=ft.ListView(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        place.get("place_name", ""),
                                        size=22, weight=ft.FontWeight.BOLD, color="#1a1a1a",
                                        expand=True,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text("★", size=16, color="#f9c74f"),
                                            ft.Text(
                                                f"{rating:.1f} out of 5",
                                                size=13, color="#1a1a1a", weight=ft.FontWeight.W_600,
                                            ),
                                        ],
                                        spacing=3, tight=True,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(
                                            f"{emoji}  {style_nm}",
                                            size=12, color=color, weight=ft.FontWeight.W_600,
                                        ),
                                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                        border_radius=10,
                                        bgcolor=color + "20",
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text("🕐", size=14),
                                            ft.Text(place.get("openning_hr", ""), size=13, color="#666666"),
                                        ],
                                        spacing=5,
                                    ),
                                ],
                                spacing=12,
                            ),
                            ft.Divider(height=20, color="#f0f0f0"),
                        ] + transport_section + [
                            ft.Text("Overview", size=15, weight=ft.FontWeight.BOLD, color="#FF5F3D"),
                            ft.Text(place.get("place_descript", ""), size=14, color="#666666"),
                            ft.Container(height=12),
                        ] + cost_section + [
                            ft.Container(height=16),
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Text("Book now", color="#ffffff", size=16, weight=ft.FontWeight.BOLD),
                                        ft.Text("→", color="#ffffff", size=18),
                                    ],
                                    spacing=8, tight=True,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                bgcolor="#1a1a1a",
                                width=9999,
                            ),
                        ],
                        spacing=12,
                        expand=True,
                    ),
                    padding=ft.padding.all(22),
                    expand=True,
                    bgcolor="#ffffff",
                    border_radius=ft.border_radius.only(top_left=28, top_right=28),
                    margin=ft.margin.only(top=-24),
                ),
            ],
            spacing=0,
            expand=True,
        )

    # ── EVENTS ────────────────────────────────────────────────────────────────
    def _on_search(self, e):
        self.search_query = e.control.value
        self.apply_filters()
        self.build_place_grid()
        self.places_column.update()

    def _on_category(self, style_id: Optional[int]):
        self.selected_style_id = style_id
        self._refresh_categories()

        if style_id is None:
            # All categories — use full list with text filter
            self.apply_filters()
        else:
            # Specific category → call GET /places/style/{style_id}
            self.load_places_by_style(style_id)
            # Then apply search text on top
            if self.search_query.strip():
                q = self.search_query.lower()
                self.filtered_places = [
                    p for p in self.filtered_places
                    if q in p.get("place_name", "").lower()
                    or q in p.get("place_descript", "").lower()
                ]

        self.build_place_grid()
        self.page.update()

    def _on_place_tap(self, place: Dict):
        self.page.controls.clear()
        detail_col = self.build_detail_page(place)
        self.page.add(detail_col)
        self.page.update()

    def _go_home(self):
        self.page.controls.clear()
        self._build_main_layout()
        self.page.update()

    def _on_nav(self, index: int):
        self.nav_index = index
        if index == 0:
            self._go_home()
        else:
            labels = ["Home", "Explore", "Saved", "Profile"]
            self.page.controls.clear()
            self.page.add(
                ft.Column(
                    [
                        ft.Container(expand=True),
                        ft.Column(
                            [
                                ft.Text("🚧", size=54),
                                ft.Text(labels[index], size=18, weight=ft.FontWeight.BOLD, color="#1a1a1a"),
                                ft.Text("Coming soon...", size=14, color="#aaaaaa"),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        ft.Container(expand=True),
                        self.build_bottom_nav(),
                    ],
                    spacing=0, expand=True,
                )
            )
            self.page.update()

    # ── MAIN LAYOUT ───────────────────────────────────────────────────────────
    def _build_main_layout(self):
        explore = self.build_explore_page()
        self.build_place_grid()
        self.page.add(
            ft.Column(
                [explore, self.build_bottom_nav()],
                spacing=0, expand=True,
            )
        )

    def run(self):
        self.setup_page()
        self.load_data()
        self._build_main_layout()


# ── APP MANAGER (handling login flow) ──────────────────────────────────────────
class AppManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.is_logged_in = False

    def _on_login_success(self):
        """Called when login is successful"""
        self.is_logged_in = True
        self.show_main_app()

    def show_login_page(self):
        """Display the login page"""
        self.page.controls.clear()
        login_page = LoginPage(self.page, self._on_login_success)
        self.page.add(login_page.build_login_page())
        self.page.update()

    def show_main_app(self):
        """Display the main travel app"""
        self.page.controls.clear()
        app = TravelApp(self.page)
        app.run()

    def start(self):
        """Start the application"""
        self.page.title = "Travel App"
        self.page.bgcolor = "#f5f5f5"
        self.page.padding = 0
        self.page.window_width = 390
        self.page.window_height = 844
        self.page.window_resizable = False
        self.page.window_max_width = 390
        self.page.window_max_height = 844
        self.page.window_min_width = 390
        self.page.window_min_height = 844
        self.show_login_page()


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
def main(page: ft.Page):
    app_manager = AppManager(page)
    app_manager.start()


if __name__ == "__main__":
    ft.app(target=main)
