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
# MAIN APPLICATION
# =========================================================

class ComplaintManagementApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # -------------------------------------------------
        # WINDOW
        # -------------------------------------------------

        self.title(
            "Municipal Complaint Management System"
        )

        self.geometry(
            "1180x740"
        )

        self.minsize(
            1050,
            680
        )

        self.configure(
            fg_color=BG_MAIN
        )

        # -------------------------------------------------
        # DATABASE
        # -------------------------------------------------

        self.conn = None

        self.connect_db()

        # -------------------------------------------------
        # MAIN GRID
        # -------------------------------------------------

        self.grid_columnconfigure(
            0,
            weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        # -------------------------------------------------
        # UI
        # -------------------------------------------------

        self.configure_treeview_styles()

        self.create_sidebar()

        self.create_main_container()

        self.show_overview_view()


    # =====================================================
    # DATABASE CONNECTION
    # =====================================================

    def connect_db(self):

        try:

            self.conn = oracledb.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                dsn=DB_DSN
            )

        except Exception as e:

            self.conn = None

            messagebox.showerror(
                "Database Connection Error",
                f"Could not connect to Oracle DB:\n{e}"
            )


    # =====================================================
    # TREEVIEW STYLE
    # =====================================================

    def configure_treeview_styles(self):

        style = ttk.Style()

        style.theme_use(
            "clam"
        )

        # Table contents
        style.configure(
            "Treeview",
            background=BG_INPUT,
            foreground=TEXT_PRIMARY,
            fieldbackground=BG_INPUT,
            rowheight=43,
            borderwidth=0,
            relief="flat",
            font=(
                FONT,
                FONT_TABLE
            )
        )

        # Table headings
        style.configure(
            "Treeview.Heading",
            background="#1B1C20",
            foreground=GOLD_LIGHT,
            font=(
                FONT,
                FONT_TABLE_HEADER,
                "bold"
            ),
            borderwidth=0,
            relief="flat",
            padding=(10, 12)
        )

        style.map(
            "Treeview",
            background=[
                (
                    "selected",
                    "#403823"
                )
            ],
            foreground=[
                (
                    "selected",
                    GOLD_LIGHT
                )
            ]
        )

        style.map(
            "Treeview.Heading",
            background=[
                (
                    "active",
                    "#24231F"
                )
            ]
        )

        style.configure(
            "Vertical.TScrollbar",
            background="#18191D",
            troughcolor=BG_INPUT,
            bordercolor=BG_INPUT,
            arrowcolor=GOLD,
            width=10
        )


    # =====================================================
    # SIDEBAR
    # =====================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=255,
            corner_radius=0,
            fg_color=BG_SIDEBAR
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # -------------------------------------------------
        # BRAND
        # -------------------------------------------------

        brand_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        brand_frame.pack(
            padx=25,
            pady=(30, 28),
            fill="x"
        )

        ctk.CTkLabel(
            brand_frame,
            text="◆",
            font=(
                FONT,
                22,
                "bold"
            ),
            text_color=GOLD
        ).pack(
            side="left",
            padx=(0, 10)
        )

        brand_text_frame = ctk.CTkFrame(
            brand_frame,
            fg_color="transparent"
        )

        brand_text_frame.pack(
            side="left"
        )

        ctk.CTkLabel(
            brand_text_frame,
            text="MUNICIPAL",
            font=(
                FONT,
                10,
                "bold"
            ),
            text_color=GOLD
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            brand_text_frame,
            text="COMPLAINT SYSTEM",
            font=(
                FONT,
                13,
                "bold"
            ),
            text_color=TEXT_PRIMARY
        ).pack(
            anchor="w"
        )

        # -------------------------------------------------
        # MENU LABEL
        # -------------------------------------------------

        ctk.CTkLabel(
            self.sidebar,
            text="MAIN MENU",
            font=(
                FONT,
                FONT_SECTION,
                "bold"
            ),
            text_color=TEXT_MUTED
        ).pack(
            padx=25,
            pady=(0, 10),
            anchor="w"
        )

        # -------------------------------------------------
        # NAVIGATION
        # -------------------------------------------------

        self.nav_buttons = {}

        nav_buttons = [

            (
                "⌂",
                "Overview",
                self.show_overview_view
            ),

            (
                "♙",
                "Add Citizen",
                self.show_add_citizen_view
            ),

            (
                "▣",
                "Log Complaint",
                self.show_add_complaint_view
            ),

            (
                "▤",
                "Department Report",
                self.show_report_view
            )
        ]

        for icon, text, command in nav_buttons:

            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {icon}     {text}",
                height=48,
                corner_radius=10,
                fg_color="transparent",
                hover_color="#1C1B18",
                text_color=TEXT_SECONDARY,
                anchor="w",
                font=(
                    FONT,
                    11,
                    "bold"
                ),
                command=command
            )

            btn.pack(
                padx=16,
                pady=3,
                fill="x"
            )

            self.nav_buttons[text] = btn

        # -------------------------------------------------
        # SPACER
        # -------------------------------------------------

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        spacer.pack(
            fill="both",
            expand=True
        )

        # -------------------------------------------------
        # BOTTOM SECTION
        # -------------------------------------------------

        bottom_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        bottom_frame.pack(
            side="bottom",
            fill="x",
            padx=16,
            pady=18
        )

        # -------------------------------------------------
        # DATABASE STATUS
        # -------------------------------------------------

        status_card = ctk.CTkFrame(
            bottom_frame,
            fg_color=BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )

        status_card.pack(
            fill="x",
            pady=(0, 10)
        )

        status_dot = (
            "●"
            if self.conn
            else "○"
        )

        ctk.CTkLabel(
            status_card,
            text=status_dot,
            text_color=(
                SUCCESS
                if self.conn
                else DANGER
            ),
            font=(
                FONT,
                12
            )
        ).pack(
            side="left",
            padx=(12, 7),
            pady=10
        )

        ctk.CTkLabel(
            status_card,
            text=(
                "Database Connected"
                if self.conn
                else "Database Offline"
            ),
            text_color=TEXT_SECONDARY,
            font=(
                FONT,
                9,
                "bold"
            )
        ).pack(
            side="left",
            pady=10
        )

        # -------------------------------------------------
        # RECONNECT
        # -------------------------------------------------

        reconnect_btn = ctk.CTkButton(
            bottom_frame,
            text="↻   Reconnect Database",
            height=40,
            corner_radius=9,
            fg_color="transparent",
            border_color=BORDER_GOLD,
            border_width=1,
            text_color=GOLD,
            hover_color="#1C1B18",
            font=(
                FONT,
                9,
                "bold"
            ),
            command=self.connect_db
        )

        reconnect_btn.pack(
            fill="x"
        )


    # =====================================================
    # MAIN CONTAINER
    # =====================================================

    def create_main_container(self):

        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color=BG_CARD,
            border_color=BORDER,
            border_width=1
        )

        self.main_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(18, 25),
            pady=20
        )

        self.main_frame.grid_columnconfigure(
            0,
            weight=1
        )


    # =====================================================
    # CLEAR MAIN FRAME
    # =====================================================

    def clear_main_frame(self):

        for widget in self.main_frame.winfo_children():

            widget.destroy()


    # =====================================================
    # PAGE HEADER
    # =====================================================

    def create_page_header(
        self,
        title,
        subtitle,
        page_name
    ):

        header = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=32,
            pady=(24, 15)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left.grid(
            row=0,
            column=0,
            sticky="w"
        )

        # Page category
        ctk.CTkLabel(
            left,
            text=page_name.upper(),
            font=(
                FONT,
                9,
                "bold"
            ),
            text_color=GOLD
        ).pack(
            anchor="w",
            pady=(0, 4)
        )

        # Page title
        ctk.CTkLabel(
            left,
            text=title,
            font=(
                FONT,
                FONT_TITLE,
                "bold"
            ),
            text_color=TEXT_PRIMARY
        ).pack(
            anchor="w"
        )

        # Page subtitle
        ctk.CTkLabel(
            left,
            text=subtitle,
            font=(
                FONT,
                FONT_SUBTITLE
            ),
            text_color=TEXT_MUTED
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        ctk.CTkLabel(
            header,
            text="◆",
            font=(
                FONT,
                16
            ),
            text_color=GOLD
        ).grid(
            row=0,
            column=1,
            padx=5
        )


    # =====================================================
    # ACTIVE NAVIGATION
    # =====================================================

    def set_active_nav(
        self,
        active
    ):

        for name, button in self.nav_buttons.items():

            if name == active:

                button.configure(
                    fg_color="#211F1A",
                    text_color=GOLD_LIGHT
                )

            else:

                button.configure(
                    fg_color="transparent",
                    text_color=TEXT_SECONDARY
                )


    # =====================================================
    # OVERVIEW PAGE
    # =====================================================

    def show_overview_view(self):

        self.clear_main_frame()

        self.set_active_nav(
            "Overview"
        )

        self.create_page_header(
            "Complaint Overview",
            "Monitor and review all registered municipal complaints.",
            "Dashboard"
        )

        # -------------------------------------------------
        # FILTER CARD
        # -------------------------------------------------

        filter_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=BG_INPUT,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        filter_card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=32,
            pady=(0, 12)
        )

        ctk.CTkLabel(
            filter_card,
            text="FILTER BY PRIORITY",
            font=(
                FONT,
                9,
                "bold"
            ),
            text_color=TEXT_MUTED
        ).pack(
            side="left",
            padx=(18, 10),
            pady=10
        )

        self.priority_filter = ctk.CTkComboBox(
            filter_card,
            values=[
                "All",
                "High",
                "Medium",
                "Low"
            ],
            width=145,
            height=36,
            fg_color=BG_CARD,
            border_color=BORDER,
            button_color="#25231D",
            button_hover_color="#353025",
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color="#332E21",
            text_color=TEXT_PRIMARY,
            font=(
                FONT,
                10
            ),
            command=self.load_complaints_data
        )

        self.priority_filter.set(
            "All"
        )

        self.priority_filter.pack(
            side="left",
            padx=(0, 15),
            pady=9
        )

        # -------------------------------------------------
        # TABLE CARD
        # -------------------------------------------------

        table_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=BG_INPUT,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        table_card.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=32,
            pady=(0, 25)
        )

        self.main_frame.grid_rowconfigure(
            2,
            weight=1
        )

        columns = (
            "ID",
            "Title",
            "Citizen",
            "Department",
            "Status",
            "Priority"
        )

        self.tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings"
        )

        col_widths = {

            "ID": 65,

            "Title": 280,

            "Citizen": 165,

            "Department": 165,

            "Status": 110,

            "Priority": 100
        }

        for col in columns:

            self.tree.heading(
                col,
                text=col.upper()
            )

            align = (

                "center"

                if col in (
                    "ID",
                    "Status",
                    "Priority"
                )

                else "w"
            )

            self.tree.column(
                col,
                anchor=align,
                width=col_widths.get(
                    col,
                    120
                )
            )

        scrollbar = ttk.Scrollbar(
            table_card,
            orient="vertical",
            command=self.tree.yview,
            style="Vertical.TScrollbar"
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0),
            pady=10
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 8),
            pady=10
        )

        self.load_complaints_data()


    # =====================================================
    # LOAD COMPLAINT DATA
    # =====================================================

    def load_complaints_data(
        self,
        *args
    ):

        if not self.conn:

            return

        for row in self.tree.get_children():

            self.tree.delete(
                row
            )

        selected_priority = (
            self.priority_filter.get()
        )

        cursor = self.conn.cursor()

        try:

            if selected_priority == "All":

                query = """
                    SELECT Complaint_ID,
                           Complaint_Title,
                           Citizen_Name,
                           Dept_Name,
                           Status,
                           Priority
                    FROM vw_complaint_overview
                """

                cursor.execute(
                    query
                )

            else:

                query = """
                    SELECT Complaint_ID,
                           Complaint_Title,
                           Citizen_Name,
                           Dept_Name,
                           Status,
                           Priority
                    FROM vw_complaint_overview
                    WHERE Priority = :p
                """

                cursor.execute(
                    query,
                    [selected_priority]
                )

            for row in cursor.fetchall():

                self.tree.insert(
                    "",
                    "end",
                    values=row
                )

        except Exception as e:

            messagebox.showerror(
                "Query Error",
                f"Error querying database view:\n{e}"
            )

        finally:

            cursor.close()


    # =====================================================
    # ADD CITIZEN PAGE
    # =====================================================

    def show_add_citizen_view(self):

        self.clear_main_frame()

        self.set_active_nav(
            "Add Citizen"
        )

        self.create_page_header(
            "Register New Citizen",
            "Create a new citizen profile in the municipal system.",
            "Citizen Management"
        )

        form_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=BG_INPUT,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        form_card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=32,
            pady=(0, 25)
        )

        form_card.grid_columnconfigure(
            0,
            weight=1
        )

        form_card.grid_columnconfigure(
            1,
            weight=1
        )

        # -------------------------------------------------
        # FORM HEADER
        # -------------------------------------------------

        ctk.CTkLabel(
            form_card,
            text="CITIZEN INFORMATION",
            font=(
                FONT,
                FONT_SECTION,
                "bold"
            ),
            text_color=GOLD
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=28,
            pady=(20, 3)
        )

        ctk.CTkLabel(
            form_card,
            text="Enter the citizen's personal and contact details.",
            font=(
                FONT,
                11
            ),
            text_color=TEXT_MUTED
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            padx=28,
            pady=(0, 15)
        )

        self.citizen_inputs = {}

        fields = [

            (
                "Full Name",
                "entry_name",
                "e.g. Nitika Jacob",
                2,
                0
            ),

            (
                "Email Address",
                "entry_email",
                "e.g. user@example.com",
                2,
                1
            ),

            (
                "Phone Number",
                "entry_phone",
                "e.g. 9876543210",
                4,
                0
            ),

            (
                "Address",
                "entry_address",
                "e.g. Kochi, Kerala",
                4,
                1
            )
        ]

        for (
            label_text,
            var_name,
            placeholder,
            row,
            column
        ) in fields:

            field_frame = ctk.CTkFrame(
                form_card,
                fg_color="transparent"
            )

            field_frame.grid(
                row=row,
                column=column,
                sticky="ew",
                padx=28,
                pady=7
            )

            field_frame.grid_columnconfigure(
                0,
                weight=1
            )

            ctk.CTkLabel(
                field_frame,
                text=label_text,
                font=(
                    FONT,
                    FONT_LABEL,
                    "bold"
                ),
                text_color=TEXT_SECONDARY
            ).grid(
                row=0,
                column=0,
                sticky="w",
                pady=(0, 5)
            )

            entry = ctk.CTkEntry(
                field_frame,
                height=43,
                placeholder_text=placeholder,
                fg_color=BG_CARD,
                border_color=BORDER,
                text_color=TEXT_PRIMARY,
                placeholder_text_color="#5E5B53",
                corner_radius=9,
                font=(
                    FONT,
                    FONT_BODY
                )
            )

            entry.grid(
                row=1,
                column=0,
                sticky="ew"
            )

            self.citizen_inputs[
                var_name
            ] = entry

        # -------------------------------------------------
        # DIVIDER
        # -------------------------------------------------

        divider = ctk.CTkFrame(
            form_card,
            height=1,
            fg_color=BORDER
        )

        divider.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=28,
            pady=(10, 10)
        )

        # -------------------------------------------------
        # SAVE BUTTON
        # -------------------------------------------------

        btn_submit = ctk.CTkButton(
            form_card,
            text="Save Citizen   →",
            height=43,
            width=195,
            fg_color=GOLD_DARK,
            hover_color="#8F783F",
            text_color="#090A0C",
            font=(
                FONT,
                FONT_BUTTON,
                "bold"
            ),
            corner_radius=9,
            command=self.insert_citizen
        )

        btn_submit.grid(
            row=7,
            column=1,
            sticky="e",
            padx=28,
            pady=(0, 20)
        )


    # =====================================================
    # INSERT CITIZEN
    # =====================================================

    def insert_citizen(self):

        name = self.citizen_inputs[
            "entry_name"
        ].get().strip()

        email = self.citizen_inputs[
            "entry_email"
        ].get().strip()

        phone = self.citizen_inputs[
            "entry_phone"
        ].get().strip()

        address = self.citizen_inputs[
            "entry_address"
        ].get().strip()

        if (
            not name
            or not email
            or not phone
            or not address
        ):

            messagebox.showwarning(
                "Validation Error",
                "All fields (Name, Email, Phone, Address) are required!"
            )

            return

        if not self.conn:

            messagebox.showerror(
                "Database Error",
                "No active database connection."
            )

            return

        cursor = self.conn.cursor()

        try:

            generated_id = cursor.var(
                oracledb.NUMBER
            )

            query = """
                INSERT INTO Citizen
                (
                    CITIZEN_ID,
                    NAME,
                    PHONE_NUMBER,
                    EMAIL,
                    ADDRESS
                )
                VALUES
                (
                    Citizen_Seq.NEXTVAL,
                    :name,
                    :phone,
                    :email,
                    :address
                )
                RETURNING CITIZEN_ID INTO :generated_id
            """

            cursor.execute(
                query,
                {
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "address": address,
                    "generated_id": generated_id
                }
            )

            self.conn.commit()

            new_id = int(
                generated_id.getvalue()[0]
            )

            messagebox.showinfo(
                "Registration Successful",
                f"Citizen '{name}' registered successfully!\n\n"
                f"Assigned Citizen ID: {new_id}"
            )

            for entry in self.citizen_inputs.values():

                entry.delete(
                    0,
                    tk.END
                )

        except Exception as e:

            self.conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Failed to insert citizen:\n{e}"
            )

        finally:

            cursor.close()


    # =====================================================
    # LOG NEW COMPLAINT PAGE
    # =====================================================

    def show_add_complaint_view(self):

        self.clear_main_frame()

        self.set_active_nav(
            "Log Complaint"
        )

        self.create_page_header(
            "Log New Complaint",
            "Register a municipal issue and assign it to the appropriate department.",
            "Complaint Management"
        )

        # =================================================
        # FORM CARD
        # =================================================

        form_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=BG_INPUT,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        form_card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=32,
            pady=(0, 20)
        )

        form_card.grid_columnconfigure(
            0,
            weight=1
        )

        form_card.grid_columnconfigure(
            1,
            weight=1
        )

        # =================================================
        # HEADER
        # =================================================

        ctk.CTkLabel(
            form_card,
            text="COMPLAINT DETAILS",
            font=(
                FONT,
                FONT_SECTION,
                "bold"
            ),
            text_color=GOLD
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(17, 2)
        )

        ctk.CTkLabel(
            form_card,
            text="Provide the issue details and routing information below.",
            font=(
                FONT,
                10
            ),
            text_color=TEXT_MUTED
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(0, 10)
        )

        # =================================================
        # COMPLAINT TITLE
        # =================================================

        title_frame = ctk.CTkFrame(
            form_card,
            fg_color="transparent"
        )

        title_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=4
        )

        title_frame.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            title_frame,
            text="Complaint Title",
            font=(
                FONT,
                FONT_LABEL,
                "bold"
            ),
            text_color=TEXT_SECONDARY
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 4)
        )

        self.entry_comp_title = ctk.CTkEntry(
            title_frame,
            height=40,
            placeholder_text="e.g. Water Pipe Leakage",
            fg_color=BG_CARD,
            border_color=BORDER,
            text_color=TEXT_PRIMARY,
            placeholder_text_color="#5E5B53",
            corner_radius=9,
            font=(
                FONT,
                FONT_BODY
            )
        )

        self.entry_comp_title.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # =================================================
        # CITIZEN ID
        # =================================================

        self.entry_citizen_id = self.create_compact_form_field(
            form_card,
            "Citizen ID",
            "e.g. 10",
            3,
            0
        )

        # =================================================
        # DEPARTMENT ID
        # =================================================

        self.entry_dept_id = self.create_compact_form_field(
            form_card,
            "Department ID",
            "e.g. 2",
            3,
            1
        )

        # =================================================
        # PRIORITY
        # =================================================

        priority_frame = ctk.CTkFrame(
            form_card,
            fg_color="transparent"
        )

        priority_frame.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=25,
            pady=4
        )

        ctk.CTkLabel(
            priority_frame,
            text="Priority",
            font=(
                FONT,
                FONT_LABEL,
                "bold"
            ),
            text_color=TEXT_SECONDARY
        ).pack(
            anchor="w",
            pady=(0, 4)
        )

        self.combo_priority = ctk.CTkComboBox(
            priority_frame,
            values=[
                "Low",
                "Medium",
                "High"
            ],
            height=40,
            fg_color=BG_CARD,
            border_color=BORDER,
            button_color="#25231D",
            button_hover_color="#353025",
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color="#332E21",
            text_color=TEXT_PRIMARY,
            corner_radius=9,
            font=(
                FONT,
                FONT_BODY
            )
        )

        self.combo_priority.set(
            "Medium"
        )

        self.combo_priority.pack(
            fill="x"
        )

        # =================================================
        # AVAILABLE DEPARTMENTS
        # =================================================

        dept_box = ctk.CTkFrame(
            form_card,
            fg_color=BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )

        dept_box.grid(
            row=4,
            column=1,
            sticky="ew",
            padx=25,
            pady=4
        )

        ctk.CTkLabel(
            dept_box,
            text="AVAILABLE DEPARTMENTS",
            font=(
                FONT,
                9,
                "bold"
            ),
            text_color=GOLD
        ).pack(
            padx=14,
            pady=(7, 2),
            anchor="w"
        )

        # =================================================
        # LOAD DEPARTMENTS
        # =================================================

        department_text = ""

        if self.conn:

            cursor = self.conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT DEPARTMENTID,
                           DEPT_NAME
                    FROM Department
                    ORDER BY DEPARTMENTID
                    """
                )

                rows = cursor.fetchall()

                for dept_id, dept_name in rows:

                    department_text += (
                        f"{dept_id}   •   {dept_name}\n"
                    )

            except Exception as e:

                department_text = (
                    f"Error loading departments:\n{e}"
                )

            finally:

                cursor.close()

        else:

            department_text = (
                "Database connection unavailable."
            )

        # =================================================
        # DEPARTMENT LIST
        # =================================================

        ctk.CTkLabel(
            dept_box,
            text=department_text.strip(),
            font=(
                FONT,
                9
            ),
            text_color=TEXT_SECONDARY,
            justify="left",
            anchor="w"
        ).pack(
            padx=14,
            pady=(0, 7),
            fill="x"
        )

        # =================================================
        # DIVIDER
        # =================================================

        divider = ctk.CTkFrame(
            form_card,
            height=1,
            fg_color=BORDER
        )

        divider.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(6, 7)
        )

        # =================================================
        # SUBMIT BUTTON
        # =================================================

        btn_submit = ctk.CTkButton(
            form_card,
            text="Submit Complaint   →",
            height=41,
            width=205,
            fg_color=GOLD_DARK,
            hover_color="#8F783F",
            text_color="#090A0C",
            font=(
                FONT,
                FONT_BUTTON,
                "bold"
            ),
            corner_radius=9,
            command=self.insert_complaint
        )

        btn_submit.grid(
            row=6,
            column=1,
            sticky="e",
            padx=25,
            pady=(0, 15)
        )


    # =====================================================
    # COMPACT FORM FIELD
    # =====================================================

    def create_compact_form_field(
        self,
        parent,
        label,
        placeholder,
        row,
        column
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=25,
            pady=4
        )

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            frame,
            text=label,
            font=(
                FONT,
                FONT_LABEL,
                "bold"
            ),
            text_color=TEXT_SECONDARY
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 4)
        )

        entry = ctk.CTkEntry(
            frame,
            height=40,
            placeholder_text=placeholder,
            fg_color=BG_CARD,
            border_color=BORDER,
            text_color=TEXT_PRIMARY,
            placeholder_text_color="#5E5B53",
            corner_radius=9,
            font=(
                FONT,
                FONT_BODY
            )
        )

        entry.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        return entry


    # =====================================================
    # INSERT COMPLAINT
    # =====================================================

    def insert_complaint(self):

        title = (
            self.entry_comp_title
            .get()
            .strip()
        )

        citizen_id = (
            self.entry_citizen_id
            .get()
            .strip()
        )

        dept_id = (
            self.entry_dept_id
            .get()
            .strip()
        )

        priority = (
            self.combo_priority
            .get()
        )

        if (
            not title
            or not citizen_id.isdigit()
            or not dept_id.isdigit()
        ):

            messagebox.showwarning(
                "Validation Error",
                "Please fill in all fields with valid values."
            )

            return

        if not self.conn:

            messagebox.showerror(
                "Database Error",
                "No active database connection."
            )

            return

        cursor = self.conn.cursor()

        try:

            query = """
                INSERT INTO Complaint
                (
                    COMPLAINT_ID,
                    COMPLAINT_TITLE,
                    COMPLAINT_DATE,
                    STATUS,
                    PRIORITY,
                    CITIZEN_ID,
                    DEPARTMENTID
                )
                VALUES
                (
                    Complaint_Seq.NEXTVAL,
                    :title,
                    SYSDATE,
                    'Open',
                    :priority,
                    :citizen_id,
                    :dept_id
                )
            """

            cursor.execute(
                query,
                {
                    "title": title,
                    "priority": priority,
                    "citizen_id": int(
                        citizen_id
                    ),
                    "dept_id": int(
                        dept_id
                    )
                }
            )

            self.conn.commit()

            messagebox.showinfo(
                "Complaint Submitted",
                "Complaint logged successfully!"
            )

            self.entry_comp_title.delete(
                0,
                tk.END
            )

            self.entry_citizen_id.delete(
                0,
                tk.END
            )

            self.entry_dept_id.delete(
                0,
                tk.END
            )

        except Exception as e:

            self.conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Failed to log complaint:\n{e}"
            )

        finally:

            cursor.close()


    # =====================================================
    # DEPARTMENT REPORT PAGE
    # =====================================================

    def show_report_view(self):

        self.clear_main_frame()

        self.set_active_nav(
            "Department Report"
        )

        self.create_page_header(
            "Department Report",
            "Generate departmental analytics using the PL/SQL reporting procedure.",
            "Analytics"
        )

        report_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=BG_INPUT,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        report_card.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=32,
            pady=(0, 25)
        )

        report_card.grid_columnconfigure(
            0,
            weight=1
        )

        report_card.grid_rowconfigure(
            2,
            weight=1
        )

        self.main_frame.grid_rowconfigure(
            1,
            weight=1
        )

        # =================================================
        # CONTROLS
        # =================================================

        controls = ctk.CTkFrame(
            report_card,
            fg_color=BG_CARD,
            corner_radius=11,
            border_width=1,
            border_color=BORDER
        )

        controls.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=18
        )

        ctk.CTkLabel(
            controls,
            text="REPORT PARAMETERS",
            font=(
                FONT,
                9,
                "bold"
            ),
            text_color=GOLD
        ).pack(
            side="left",
            padx=(18, 12),
            pady=12
        )

        self.dept_id_entry = ctk.CTkEntry(
            controls,
            placeholder_text="Department ID",
            width=155,
            height=40,
            fg_color=BG_INPUT,
            border_color=BORDER,
            text_color=TEXT_PRIMARY,
            placeholder_text_color="#5E5B53",
            corner_radius=8,
            font=(
                FONT,
                FONT_BODY
            )
        )

        self.dept_id_entry.pack(
            side="left",
            padx=5,
            pady=10
        )

        run_btn = ctk.CTkButton(
            controls,
            text="Generate Report   →",
            height=40,
            width=180,
            fg_color=GOLD_DARK,
            hover_color="#8F783F",
            text_color="#090A0C",
            font=(
                FONT,
                FONT_BUTTON,
                "bold"
            ),
            corner_radius=8,
            command=self.execute_dept_report
        )

        run_btn.pack(
            side="left",
            padx=(8, 15),
            pady=10
        )

        # =================================================
        # OUTPUT HEADER
        # =================================================

        output_header = ctk.CTkFrame(
            report_card,
            fg_color="transparent"
        )

        output_header.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 7)
        )

        ctk.CTkLabel(
            output_header,
            text="GENERATED REPORT",
            font=(
                FONT,
                9,
                "bold"
            ),
            text_color=GOLD
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            output_header,
            text="PL/SQL OUTPUT",
            font=(
                FONT,
                9,
                "bold"
            ),
            text_color=TEXT_MUTED
        ).pack(
            side="right"
        )

        # =================================================
        # OUTPUT BOX
        # =================================================

        self.output_box = ctk.CTkTextbox(
            report_card,
            fg_color=BG_MAIN,
            font=(
                FONT,
                11
            ),
            text_color=TEXT_SECONDARY,
            corner_radius=10,
            border_color=BORDER,
            border_width=1
        )

        self.output_box.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 25)
        )

        self.output_box.insert(
            "1.0",
            "No report generated yet.\n\n"
            "Enter a Department ID above and select "
            "'Generate Report' to view the results."
        )


    # =====================================================
    # EXECUTE DEPARTMENT REPORT
    # =====================================================

    def execute_dept_report(self):

        dept_id = (
            self.dept_id_entry
            .get()
            .strip()
        )

        if not dept_id.isdigit():

            messagebox.showwarning(
                "Input Error",
                "Please enter a valid numeric Department ID."
            )

            return

        if not self.conn:

            messagebox.showerror(
                "Database Error",
                "No active database connection."
            )

            return

        cursor = self.conn.cursor()

        try:

            cursor.callproc(
                "dbms_output.enable"
            )

            cursor.callproc(
                "prc_department_report",
                [
                    int(dept_id)
                ]
            )

            status = cursor.var(
                oracledb.NUMBER
            )

            line = cursor.var(
                oracledb.STRING
            )

            output_text = ""

            while True:

                cursor.callproc(
                    "dbms_output.get_line",
                    [
                        line,
                        status
                    ]
                )

                if status.getvalue() != 0:

                    break

                output_text += (
                    line.getvalue()
                    + "\n"
                )

            self.output_box.delete(
                "1.0",
                tk.END
            )

            self.output_box.insert(
                tk.END,
                (
                    output_text
                    if output_text.strip()
                    else "No output returned."
                )
            )

        except Exception as e:

            messagebox.showerror(
                "Execution Error",
                f"Error executing PL/SQL procedure:\n{e}"
            )

        finally:

            cursor.close()


# =========================================================
# APPLICATION START
# =========================================================

if __name__ == "__main__":

    app = ComplaintManagementApp()

    app.mainloop()