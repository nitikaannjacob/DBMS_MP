import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import oracledb

from styles import (
    BG_MAIN, BG_SIDEBAR, BG_CARD, BG_CARD_LIGHT, BG_INPUT,
    GOLD, GOLD_LIGHT, GOLD_DARK,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    BORDER, BORDER_GOLD,
    SUCCESS, DANGER,
    FONT, FONT_TITLE, FONT_SUBTITLE, FONT_SECTION, FONT_LABEL,
    FONT_BODY, FONT_BUTTON, FONT_SMALL,
    connect_db, configure_treeview_styles
)


# =========================================================
# ADMIN APPLICATION
# =========================================================

class AdminApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # -------------------------------------------------
        # WINDOW
        # -------------------------------------------------

        self.title("Municipal Complaint Management System — Admin Panel")
        self.geometry("1180x740")
        self.minsize(1050, 680)
        self.configure(fg_color=BG_MAIN)

        # -------------------------------------------------
        # DATABASE
        # -------------------------------------------------

        self.conn = connect_db()

        # -------------------------------------------------
        # MAIN GRID
        # -------------------------------------------------

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # -------------------------------------------------
        # UI
        # -------------------------------------------------

        configure_treeview_styles()

        self.create_sidebar()
        self.create_main_container()
        self.show_overview_view()


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
            font=(FONT, 22, "bold"),
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
            font=(FONT, 10, "bold"),
            text_color=GOLD
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            brand_text_frame,
            text="ADMIN PANEL",
            font=(FONT, 13, "bold"),
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
            font=(FONT, 11, "bold"),
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
            ("⌂", "Overview", self.show_overview_view),
            ("⚑", "Manage Complaints", self.show_manage_view),
            ("▤", "Department Report", self.show_report_view),
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
                font=(FONT, 11, "bold"),
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

        status_dot = "●" if self.conn else "○"

        ctk.CTkLabel(
            status_card,
            text=status_dot,
            text_color=(SUCCESS if self.conn else DANGER),
            font=(FONT, 12)
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
            font=(FONT, 9, "bold")
        ).pack(
            side="left",
            pady=10
        )

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
            font=(FONT, 9, "bold"),
            command=self.reconnect
        )

        reconnect_btn.pack(
            fill="x"
        )


    def reconnect(self):

        self.conn = connect_db()

        # Refresh the sidebar so the status dot/text updates.
        self.sidebar.destroy()
        self.create_sidebar()


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

        ctk.CTkLabel(
            left,
            text=page_name.upper(),
            font=(FONT, 9, "bold"),
            text_color=GOLD
        ).pack(
            anchor="w",
            pady=(0, 4)
        )

        ctk.CTkLabel(
            left,
            text=title,
            font=(FONT, FONT_TITLE, "bold"),
            text_color=TEXT_PRIMARY
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            left,
            text=subtitle,
            font=(FONT, FONT_SUBTITLE),
            text_color=TEXT_MUTED
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        ctk.CTkLabel(
            header,
            text="◆",
            font=(FONT, 16),
            text_color=GOLD
        ).grid(
            row=0,
            column=1,
            padx=5
        )


    def set_active_nav(self, active):

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

        self.set_active_nav("Overview")

        self.create_page_header(
            "Complaint Overview",
            "Monitor and review all registered municipal complaints.",
            "Dashboard"
        )

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
            font=(FONT, 9, "bold"),
            text_color=TEXT_MUTED
        ).pack(
            side="left",
            padx=(18, 10),
            pady=10
        )

        self.priority_filter = ctk.CTkComboBox(
            filter_card,
            values=["All", "High", "Medium", "Low"],
            width=145,
            height=36,
            fg_color=BG_CARD,
            border_color=BORDER,
            button_color="#25231D",
            button_hover_color="#353025",
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color="#332E21",
            text_color=TEXT_PRIMARY,
            font=(FONT, 10),
            command=self.load_complaints_data
        )

        self.priority_filter.set("All")

        self.priority_filter.pack(
            side="left",
            padx=(0, 15),
            pady=9
        )

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
                if col in ("ID", "Status", "Priority")
                else "w"
            )

            self.tree.column(
                col,
                anchor=align,
                width=col_widths.get(col, 120)
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


    def load_complaints_data(self, *args):

        if not self.conn:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        selected_priority = self.priority_filter.get()

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

                cursor.execute(query)

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
                    {"p": selected_priority}
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
    # MANAGE COMPLAINTS PAGE
    # =====================================================

    def show_manage_view(self):

        self.clear_main_frame()

        self.set_active_nav("Manage Complaints")

        self.create_page_header(
            "Manage Complaints",
            "Look up a complaint, then open, close, or escalate it.",
            "Complaint Actions"
        )

        # -------------------------------------------------
        # LOOKUP CARD
        # -------------------------------------------------

        lookup_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=BG_INPUT,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        lookup_card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=32,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            lookup_card,
            text="COMPLAINT ID",
            font=(FONT, 9, "bold"),
            text_color=TEXT_MUTED
        ).pack(
            side="left",
            padx=(18, 10),
            pady=10
        )

        self.manage_id_entry = ctk.CTkEntry(
            lookup_card,
            placeholder_text="e.g. 5",
            width=140,
            height=40,
            fg_color=BG_CARD,
            border_color=BORDER,
            text_color=TEXT_PRIMARY,
            placeholder_text_color="#5E5B53",
            corner_radius=8,
            font=(FONT, FONT_BODY)
        )

        self.manage_id_entry.pack(
            side="left",
            padx=5,
            pady=10
        )

        lookup_btn = ctk.CTkButton(
            lookup_card,
            text="Load Complaint   →",
            height=40,
            width=170,
            fg_color=GOLD_DARK,
            hover_color="#8F783F",
            text_color="#090A0C",
            font=(FONT, FONT_BUTTON, "bold"),
            corner_radius=8,
            command=self.load_complaint_for_management
        )

        lookup_btn.pack(
            side="left",
            padx=(8, 15),
            pady=10
        )

        # -------------------------------------------------
        # DETAILS CARD
        # -------------------------------------------------

        details_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=BG_INPUT,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        details_card.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=32,
            pady=(0, 15)
        )

        details_card.grid_columnconfigure(
            0,
            weight=1
        )

        details_card.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            details_card,
            text="COMPLAINT DETAILS",
            font=(FONT, FONT_SECTION, "bold"),
            text_color=GOLD
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(17, 8)
        )

        self.manage_info_label = ctk.CTkLabel(
            details_card,
            text=(
                "Enter a Complaint ID above and select "
                "'Load Complaint' to begin."
            ),
            font=(FONT, 11),
            text_color=TEXT_SECONDARY,
            justify="left",
            anchor="w"
        )

        self.manage_info_label.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(0, 15)
        )

        # -------------------------------------------------
        # COMPLAINT DESCRIPTION
        # -------------------------------------------------

        ctk.CTkLabel(
            details_card,
            text="Complaint Description",
            font=(FONT, FONT_LABEL, "bold"),
            text_color=TEXT_SECONDARY
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(0, 5)
        )

        self.manage_description_box = ctk.CTkTextbox(
            details_card,
            height=90,
            fg_color=BG_CARD,
            border_color=BORDER,
            border_width=1,
            text_color=TEXT_PRIMARY,
            corner_radius=9,
            font=(FONT, FONT_BODY),
            wrap="word"
        )

        self.manage_description_box.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(0, 12)
        )

        self.manage_description_box.insert(
            "1.0",
            "Complaint description will appear here."
        )

        self.manage_description_box.configure(
            state="disabled"
        )

        # -------------------------------------------------
        # STATUS CONTROL
        # -------------------------------------------------

        status_frame = ctk.CTkFrame(
            details_card,
            fg_color="transparent"
        )

        status_frame.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=25,
            pady=6
        )

        ctk.CTkLabel(
            status_frame,
            text="Status",
            font=(FONT, FONT_LABEL, "bold"),
            text_color=TEXT_SECONDARY
        ).pack(
            anchor="w",
            pady=(0, 4)
        )

        self.manage_status_combo = ctk.CTkComboBox(
            status_frame,
            values=["Open", "In Progress", "Closed"],
            height=40,
            fg_color=BG_CARD,
            border_color=BORDER,
            button_color="#25231D",
            button_hover_color="#353025",
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color="#332E21",
            text_color=TEXT_PRIMARY,
            corner_radius=9,
            font=(FONT, FONT_BODY)
        )

        self.manage_status_combo.set("Open")

        self.manage_status_combo.pack(
            fill="x"
        )

        # -------------------------------------------------
        # PRIORITY CONTROL
        # -------------------------------------------------

        priority_frame = ctk.CTkFrame(
            details_card,
            fg_color="transparent"
        )

        priority_frame.grid(
            row=4,
            column=1,
            sticky="ew",
            padx=25,
            pady=6
        )

        ctk.CTkLabel(
            priority_frame,
            text="Priority",
            font=(FONT, FONT_LABEL, "bold"),
            text_color=TEXT_SECONDARY
        ).pack(
            anchor="w",
            pady=(0, 4)
        )

        self.manage_priority_combo = ctk.CTkComboBox(
            priority_frame,
            values=["Low", "Medium", "High"],
            height=40,
            fg_color=BG_CARD,
            border_color=BORDER,
            button_color="#25231D",
            button_hover_color="#353025",
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color="#332E21",
            text_color=TEXT_PRIMARY,
            corner_radius=9,
            font=(FONT, FONT_BODY)
        )

        self.manage_priority_combo.set("Medium")

        self.manage_priority_combo.pack(
            fill="x"
        )

        # -------------------------------------------------
        # DIVIDER
        # -------------------------------------------------

        divider = ctk.CTkFrame(
            details_card,
            height=1,
            fg_color=BORDER
        )

        divider.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(12, 12)
        )

        # -------------------------------------------------
        # ACTION BUTTONS
        # -------------------------------------------------

        actions_frame = ctk.CTkFrame(
            details_card,
            fg_color="transparent"
        )

        actions_frame.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=(0, 18)
        )

        ctk.CTkButton(
            actions_frame,
            text="Open Complaint",
            height=40,
            width=155,
            fg_color="transparent",
            border_width=1,
            border_color=SUCCESS,
            text_color=SUCCESS,
            hover_color="#1C1F1A",
            font=(FONT, FONT_BUTTON, "bold"),
            corner_radius=9,
            command=lambda: self.set_complaint_status("Open")
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ctk.CTkButton(
            actions_frame,
            text="Close Complaint",
            height=40,
            width=155,
            fg_color="transparent",
            border_width=1,
            border_color=DANGER,
            text_color=DANGER,
            hover_color="#1F1A1A",
            font=(FONT, FONT_BUTTON, "bold"),
            corner_radius=9,
            command=lambda: self.set_complaint_status("Closed")
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            actions_frame,
            text="Escalate Priority   ↑",
            height=40,
            width=175,
            fg_color="transparent",
            border_width=1,
            border_color=GOLD,
            text_color=GOLD,
            hover_color="#211F1A",
            font=(FONT, FONT_BUTTON, "bold"),
            corner_radius=9,
            command=self.escalate_complaint
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            actions_frame,
            text="Save Changes   →",
            height=40,
            width=170,
            fg_color=GOLD_DARK,
            hover_color="#8F783F",
            text_color="#090A0C",
            font=(FONT, FONT_BUTTON, "bold"),
            corner_radius=9,
            command=self.save_complaint_changes
        ).pack(
            side="right"
        )

        # Keep track of the currently loaded complaint id
        self.manage_loaded_id = None


    def _get_manage_complaint_id(self):

        raw_id = self.manage_id_entry.get().strip()

        if not raw_id.isdigit():

            messagebox.showwarning(
                "Input Error",
                "Please enter a valid numeric Complaint ID."
            )

            return None

        return int(raw_id)


    def load_complaint_for_management(self):

        complaint_id = self._get_manage_complaint_id()

        if complaint_id is None:
            return

        if not self.conn:

            messagebox.showerror(
                "Database Error",
                "No active database connection."
            )

            return

        cursor = self.conn.cursor()

        try:

            # -------------------------------------------------
            # LOAD COMPLAINT
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT c.COMPLAINT_TITLE,
                       c.DESCRIPTION,
                       ci.FIRST_NAME || ' ' || ci.LAST_NAME AS CITIZEN_NAME,
                       d.DEPT_NAME,
                       c.STATUS,
                       c.PRIORITY,
                       c.COMPLAINT_DATE
                FROM Complaint c
                JOIN Citizen ci
                    ON c.CITIZEN_ID = ci.CITIZEN_ID
                JOIN Department d
                    ON c.DEPARTMENTID = d.DEPARTMENTID
                WHERE c.COMPLAINT_ID = :id
                """,
                {"id": complaint_id}
            )

            row = cursor.fetchone()

            if not row:

                messagebox.showinfo(
                    "Not Found",
                    f"No complaint found with ID {complaint_id}."
                )

                self.manage_loaded_id = None

                return

            (
                title,
                description,
                citizen_name,
                dept_name,
                status,
                priority,
                comp_date
            ) = row

            # -------------------------------------------------
            # DISPLAY BASIC INFORMATION
            # -------------------------------------------------

            self.manage_info_label.configure(
                text=(
                    f"Title:        {title}\n"
                    f"Citizen:      {citizen_name}\n"
                    f"Department:   {dept_name}\n"
                    f"Filed on:     {comp_date}"
                )
            )

            # -------------------------------------------------
            # DISPLAY DESCRIPTION
            # -------------------------------------------------

            self.manage_description_box.configure(
                state="normal"
            )

            self.manage_description_box.delete(
                "1.0",
                tk.END
            )

            self.manage_description_box.insert(
                "1.0",
                description
                if description
                else "No description provided."
            )

            self.manage_description_box.configure(
                state="disabled"
            )

            # -------------------------------------------------
            # SET STATUS
            # -------------------------------------------------

            self.manage_status_combo.set(
                status if status else "Open"
            )

            # -------------------------------------------------
            # SET PRIORITY
            # -------------------------------------------------

            self.manage_priority_combo.set(
                priority if priority else "Medium"
            )

            self.manage_loaded_id = complaint_id

        except Exception as e:

            messagebox.showerror(
                "Query Error",
                f"Error loading complaint:\n{e}"
            )

        finally:

            cursor.close()


    # =====================================================
    # UPDATE COMPLAINT
    # =====================================================

    def _update_complaint(
        self,
        complaint_id,
        status,
        priority
    ):

        if not self.conn:

            messagebox.showerror(
                "Database Error",
                "No active database connection."
            )

            return False

        cursor = self.conn.cursor()

        try:

            cursor.execute(
                """
                UPDATE Complaint
                SET STATUS = :status,
                    PRIORITY = :priority
                WHERE COMPLAINT_ID = :id
                """,
                {
                    "status": status,
                    "priority": priority,
                    "id": complaint_id
                }
            )

            self.conn.commit()

            return True

        except Exception as e:

            self.conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Failed to update complaint:\n{e}"
            )

            return False

        finally:

            cursor.close()


    # =====================================================
    # SET STATUS
    # =====================================================

    def set_complaint_status(self, new_status):

        if self.manage_loaded_id is None:

            messagebox.showwarning(
                "No Complaint Loaded",
                "Load a complaint first before changing its status."
            )

            return

        priority = self.manage_priority_combo.get()

        if self._update_complaint(
            self.manage_loaded_id,
            new_status,
            priority
        ):

            self.manage_status_combo.set(
                new_status
            )

            messagebox.showinfo(
                "Status Updated",
                f"Complaint #{self.manage_loaded_id} "
                f"marked as '{new_status}'."
            )


    # =====================================================
    # ESCALATE COMPLAINT
    # =====================================================

    def escalate_complaint(self):

        if self.manage_loaded_id is None:

            messagebox.showwarning(
                "No Complaint Loaded",
                "Load a complaint first before escalating it."
            )

            return

        priority_order = [
            "Low",
            "Medium",
            "High"
        ]

        current = self.manage_priority_combo.get()

        if current not in priority_order:
            current = "Medium"

        current_index = priority_order.index(
            current
        )

        if current_index == len(priority_order) - 1:

            messagebox.showinfo(
                "Already at Highest Priority",
                f"Complaint #{self.manage_loaded_id} "
                "is already marked High priority."
            )

            return

        new_priority = priority_order[
            current_index + 1
        ]

        status = self.manage_status_combo.get()

        if self._update_complaint(
            self.manage_loaded_id,
            status,
            new_priority
        ):

            self.manage_priority_combo.set(
                new_priority
            )

            messagebox.showinfo(
                "Complaint Escalated",
                f"Complaint #{self.manage_loaded_id} "
                f"escalated to '{new_priority}' priority."
            )


    # =====================================================
    # SAVE CHANGES
    # =====================================================

    def save_complaint_changes(self):

        if self.manage_loaded_id is None:

            messagebox.showwarning(
                "No Complaint Loaded",
                "Load a complaint first before saving changes."
            )

            return

        status = self.manage_status_combo.get()
        priority = self.manage_priority_combo.get()

        if self._update_complaint(
            self.manage_loaded_id,
            status,
            priority
        ):

            messagebox.showinfo(
                "Changes Saved",
                f"Complaint #{self.manage_loaded_id} updated "
                f"(Status: {status}, Priority: {priority})."
            )


    # =====================================================
    # DEPARTMENT REPORT PAGE
    # =====================================================

    def show_report_view(self):

        self.clear_main_frame()

        self.set_active_nav("Department Report")

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
            font=(FONT, 9, "bold"),
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
            font=(FONT, FONT_BODY)
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
            font=(FONT, FONT_BUTTON, "bold"),
            corner_radius=8,
            command=self.execute_dept_report
        )

        run_btn.pack(
            side="left",
            padx=(8, 15),
            pady=10
        )

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
            font=(FONT, 9, "bold"),
            text_color=GOLD
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            output_header,
            text="PL/SQL OUTPUT",
            font=(FONT, 9, "bold"),
            text_color=TEXT_MUTED
        ).pack(
            side="right"
        )

        self.output_box = ctk.CTkTextbox(
            report_card,
            fg_color=BG_MAIN,
            font=(FONT, 11),
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


    def execute_dept_report(self):

        dept_id = self.dept_id_entry.get().strip()

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
                [int(dept_id)]
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
                    [line, status]
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
                output_text
                if output_text.strip()
                else "No output returned."
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

    app = AdminApp()
    app.mainloop()