"""
Shared configuration for the Municipal Complaint Management System.

Both admin_app.py and citizen_app.py import from this file so that
colors, fonts, and the database connection logic stay identical and
only need to be changed in one place.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import oracledb


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DB_USER = "system"
DB_PASSWORD = "u2403217"
DB_DSN = "localhost:1521/XEPDB1"


# =========================================================
# APPEARANCE
# =========================================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


# =========================================================
# COLORS
# =========================================================

BG_MAIN = "#08090B"
BG_SIDEBAR = "#0D0E11"

BG_CARD = "#141519"
BG_CARD_LIGHT = "#191A1F"
BG_INPUT = "#101115"

GOLD = "#D8C08A"
GOLD_LIGHT = "#E8D6A7"
GOLD_DARK = "#A58C55"

TEXT_PRIMARY = "#F5F1E7"
TEXT_SECONDARY = "#C2BCA9"
TEXT_MUTED = "#77746B"

BORDER = "#292A2D"
BORDER_GOLD = "#403822"

SUCCESS = "#8FAF83"
DANGER = "#B98278"


# =========================================================
# FONT
# =========================================================

FONT = "Montserrat"

FONT_TITLE = 26
FONT_SUBTITLE = 12
FONT_SECTION = 11
FONT_LABEL = 12
FONT_BODY = 11
FONT_BUTTON = 11
FONT_SMALL = 10

FONT_TABLE = 10
FONT_TABLE_HEADER = 10


# =========================================================
# DATABASE CONNECTION
# =========================================================

def connect_db():
    """
    Attempts to connect to the Oracle DB.
    Returns a connection object on success, or None on failure
    (and shows a messagebox explaining why).
    """

    try:

        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )

        return conn

    except Exception as e:

        messagebox.showerror(
            "Database Connection Error",
            f"Could not connect to Oracle DB:\n{e}"
        )

        return None


# =========================================================
# TREEVIEW STYLE
# =========================================================

def configure_treeview_styles():
    """
    Applies the dark/gold Treeview theme used by both the admin
    and citizen apps. Call this once after the root window exists.
    """

    style = ttk.Style()

    style.theme_use("clam")

    # Table contents
    style.configure(
        "Treeview",
        background=BG_INPUT,
        foreground=TEXT_PRIMARY,
        fieldbackground=BG_INPUT,
        rowheight=43,
        borderwidth=0,
        relief="flat",
        font=(FONT, FONT_TABLE)
    )

    # Table headings
    style.configure(
        "Treeview.Heading",
        background="#1B1C20",
        foreground=GOLD_LIGHT,
        font=(FONT, FONT_TABLE_HEADER, "bold"),
        borderwidth=0,
        relief="flat",
        padding=(10, 12)
    )

    style.map(
        "Treeview",
        background=[("selected", "#403823")],
        foreground=[("selected", GOLD_LIGHT)]
    )

    style.map(
        "Treeview.Heading",
        background=[("active", "#24231F")]
    )

    style.configure(
        "Vertical.TScrollbar",
        background="#18191D",
        troughcolor=BG_INPUT,
        bordercolor=BG_INPUT,
        arrowcolor=GOLD,
        width=10
    )
