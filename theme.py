import customtkinter as ctk


THEMES = {
    "blue": {
        "accent": "#3B82F6",
        "accent_hover": "#2563EB",
    },
    "purple": {
        "accent": "#8B5CF6",
        "accent_hover": "#7C3AED",
    },
    "green": {
        "accent": "#10B981",
        "accent_hover": "#059669",
    },
    "orange": {
        "accent": "#F59E0B",
        "accent_hover": "#D97706",
    },
    "red": {
        "accent": "#EF4444",
        "accent_hover": "#DC2626",
    },
}


class ThemeManager:

    def __init__(self):
        self.mode = "dark"
        self.accent = "blue"

    def set_mode(self, mode):
        self.mode = mode
        ctk.set_appearance_mode(mode)

    def set_accent(self, accent):
        if accent in THEMES:
            self.accent = accent

    def get(self):
        return THEMES[self.accent]