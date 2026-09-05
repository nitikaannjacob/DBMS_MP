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
# CITIZEN APPLICATION
# =========================================================

class CitizenApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Municipal Complaint Management System — Citizen Portal")
        self.geometry("1180x740")
        self.minsize(1050, 680)
        self.configure(fg_color=BG_MAIN)

        self.conn = connect_db()

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        configure_treeview_styles()

        self.create_sidebar()
        self.create_main_container()
        self.show_register_view()


    # =====================================================
    # SIDEBAR
    # =====================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self, width=255, corner_radius=0, fg_color=BG_SIDEBAR
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        brand_frame = ctk.CTkFrame(
            self.sidebar, fg_color="transparent"
        )
        brand_frame.pack(padx=25, pady=(30, 28), fill="x")

        ctk.CTkLabel(
            brand_frame,
            text="◆",
            font=(FONT, 22, "bold"),
            text_color=GOLD
        ).pack(side="left", padx=(0, 10))

        brand_text_frame = ctk.CTkFrame(
            brand_frame, fg_color="transparent"
        )
        brand_text_frame.pack(side="left")

        ctk.CTkLabel(
            brand_text_frame,
            text="MUNICIPAL",
            font=(FONT, 10, "bold"),
            text_color=GOLD
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand_text_frame,
            text="CITIZEN PORTAL",
            font=(FONT, 13, "bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.sidebar,
            text="MAIN MENU",
            font=(FONT, 11, "bold"),
            text_color=TEXT_MUTED
        ).pack(padx=25, pady=(0, 10), anchor="w")

        self.nav_buttons = {}

        nav_buttons = [
            ("♙", "Register", self.show_register_view),
            ("▣", "Submit Complaint", self.show_submit_complaint_view),
            ("▤", "Track My Complaints", self.show_track_view),
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

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        spacer.pack(
            fill="both",
            expand=True
        )

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
    # REGISTER PAGE
    # =====================================================

    def show_register_view(self):

        self.clear_main_frame()

        self.set_active_nav("Register")

        self.create_page_header(
            "Register as a Citizen",
            "Create your profile so you can start filing complaints.",
            "Citizen Registration"
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

        ctk.CTkLabel(
            form_card,
            text="YOUR INFORMATION",
            font=(FONT, FONT_SECTION, "bold"),
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
            text="Enter your personal and contact details.",
            font=(FONT, 11),
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
            ),
        ]

        for label_text, var_name, placeholder, row, column in fields:

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
                font=(FONT, FONT_LABEL, "bold"),
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
                font=(FONT, FONT_BODY)
            )

            entry.grid(
                row=1,
                column=0,
                sticky="ew"
            )

            self.citizen_inputs[var_name] = entry

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

        btn_submit = ctk.CTkButton(
            form_card,
            text="Register   →",
            height=43,
            width=195,
            fg_color=GOLD_DARK,
            hover_color="#8F783F",
            text_color="#090A0C",
            font=(FONT, FONT_BUTTON, "bold"),
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


    def insert_citizen(self):

        name = self.citizen_inputs["entry_name"].get().strip()
        email = self.citizen_inputs["entry_email"].get().strip()
        phone = self.citizen_inputs["entry_phone"].get().strip()
        address = self.citizen_inputs["entry_address"].get().strip()

        if not name or not email or not phone or not address:

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
                (CITIZEN_ID, NAME, PHONE_NUMBER, EMAIL, ADDRESS)
                VALUES
                (Citizen_Seq.NEXTVAL, :name, :phone, :email, :address)
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
                f"Welcome, {name}!\n\n"
                f"Your Citizen ID is: {new_id}\n"
                f"Keep this ID — you'll need it to submit and track complaints."
            )

            for entry in self.citizen_inputs.values():
                entry.delete(0, tk.END)

        except Exception as e:

            self.conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Failed to register:\n{e}"
            )

        finally:

            cursor.close()


    # =====================================================
    # SUBMIT COMPLAINT PAGE
    # =====================================================

    def show_submit_complaint_view(self):

        self.clear_main_frame()

        self.set_active_nav("Submit Complaint")

        self.create_page_header(
            "Submit a Complaint",
            "Tell us about the issue and which department it concerns.",
            "Complaint Filing"
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

        ctk.CTkLabel(
            form_card,
            text="COMPLAINT DETAILS",
            font=(FONT, FONT_SECTION, "bold"),
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
            text="Provide the issue details and your Citizen ID below.",
            font=(FONT, 10),
            text_color=TEXT_MUTED
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(0, 10)
        )

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
            font=(FONT, FONT_LABEL, "bold"),
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
            font=(FONT, FONT_BODY)
        )

        self.entry_comp_title.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.entry_citizen_id = self.create_compact_form_field(
            form_card,
            "Your Citizen ID",
            "e.g. 10",
            3,
            0
        )

        self.entry_dept_id = self.create_compact_form_field(
            form_card,
            "Department ID",
            "e.g. 2",
            3,
            1
        )

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
            font=(FONT, FONT_LABEL, "bold"),
            text_color=TEXT_SECONDARY
        ).pack(
            anchor="w",
            pady=(0, 4)
        )

        self.combo_priority = ctk.CTkComboBox(
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

        self.combo_priority.set("Medium")

        self.combo_priority.pack(
            fill="x"
        )

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
            font=(FONT, 9, "bold"),
            text_color=GOLD
        ).pack(
            padx=14,
            pady=(7, 2),
            anchor="w"
        )

        department_text = ""

        if self.conn:

            cursor = self.conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT DEPARTMENTID, DEPT_NAME
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

        ctk.CTkLabel(
            dept_box,
            text=department_text.strip(),
            font=(FONT, 9),
            text_color=TEXT_SECONDARY,
            justify="left",
            anchor="w"
        ).pack(
            padx=14,
            pady=(0, 7),
            fill="x"
        )

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

        btn_submit = ctk.CTkButton(
            form_card,
            text="Submit Complaint   →",
            height=41,
            width=205,
            fg_color=GOLD_DARK,
            hover_color="#8F783F",
            text_color="#090A0C",
            font=(FONT, FONT_BUTTON, "bold"),
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
            font=(FONT, FONT_LABEL, "bold"),
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
            font=(FONT, FONT_BODY)
        )

        entry.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        return entry


    def insert_complaint(self):

        title = self.entry_comp_title.get().strip()
        citizen_id = self.entry_citizen_id.get().strip()
        dept_id = self.entry_dept_id.get().strip()
        priority = self.combo_priority.get()

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
                (COMPLAINT_ID, COMPLAINT_TITLE, COMPLAINT_DATE, STATUS,
                 PRIORITY, CITIZEN_ID, DEPARTMENTID)
                VALUES
                (Complaint_Seq.NEXTVAL, :title, SYSDATE, 'Open',
                 :priority, :citizen_id, :dept_id)
            """

            cursor.execute(
                query,
                {
                    "title": title,
                    "priority": priority,
                    "citizen_id": int(citizen_id),
                    "dept_id": int(dept_id)
                }
            )

            self.conn.commit()

            messagebox.showinfo(
                "Complaint Submitted",
                "Your complaint has been logged successfully!\n"
                "You can check its status anytime under "
                "'Track My Complaints'."
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
                f"Failed to submit complaint:\n{e}"
            )

        finally:

            cursor.close()


    # =====================================================
    # TRACK MY COMPLAINTS PAGE
    # =====================================================

    def show_track_view(self):

        self.clear_main_frame()

        self.set_active_nav(
            "Track My Complaints"
        )

        self.create_page_header(
            "Track My Complaints",
            "Enter your Citizen ID to see the status of everything you've filed.",
            "Status Lookup"
        )

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
            pady=(0, 12)
        )

        ctk.CTkLabel(
            lookup_card,
            text="YOUR CITIZEN ID",
            font=(FONT, 9, "bold"),
            text_color=TEXT_MUTED
        ).pack(
            side="left",
            padx=(18, 10),
            pady=10
        )

        self.track_citizen_id_entry = ctk.CTkEntry(
            lookup_card,
            placeholder_text="e.g. 101",
            width=155,
            height=40,
            fg_color=BG_CARD,
            border_color=BORDER,
            text_color=TEXT_PRIMARY,
            placeholder_text_color="#5E5B53",
            corner_radius=8,
            font=(FONT, FONT_BODY)
        )

        self.track_citizen_id_entry.pack(
            side="left",
            padx=5,
            pady=10
        )

        lookup_btn = ctk.CTkButton(
            lookup_card,
            text="View My Complaints   →",
            height=40,
            width=200,
            fg_color=GOLD_DARK,
            hover_color="#8F783F",
            text_color="#090A0C",
            font=(FONT, FONT_BUTTON, "bold"),
            corner_radius=8,
            command=self.load_my_complaints
        )

        lookup_btn.pack(
            side="left",
            padx=(8, 15),
            pady=10
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

        # =================================================
        # UPDATED TABLE
        # =================================================
        #
        # Now displays BOTH:
        # 1. Complaint ID
        # 2. Citizen ID
        #
        # =================================================

        columns = (
            "ID",
            "Citizen ID",
            "Title",
            "Department",
            "Status",
            "Priority",
            "Date"
        )

        self.track_tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings"
        )

        col_widths = {
            "ID": 65,
            "Citizen ID": 90,
            "Title": 225,
            "Department": 130,
            "Status": 90,
            "Priority": 90,
            "Date": 145
        }

        for col in columns:

            self.track_tree.heading(
                col,
                text=col.upper()
            )

            if col in (
                "ID",
                "Citizen ID",
                "Status",
                "Priority",
                "Date"
            ):

                align = "center"

            else:

                align = "w"

            self.track_tree.column(
                col,
                anchor=align,
                width=col_widths.get(col, 120),
                minwidth=60
            )

        scrollbar = ttk.Scrollbar(
            table_card,
            orient="vertical",
            command=self.track_tree.yview,
            style="Vertical.TScrollbar"
        )

        self.track_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.track_tree.pack(
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


    # =====================================================
    # LOAD CITIZEN COMPLAINTS
    # =====================================================

    def load_my_complaints(self):

        citizen_id = (
            self.track_citizen_id_entry
            .get()
            .strip()
        )

        if not citizen_id.isdigit():

            messagebox.showwarning(
                "Input Error",
                "Please enter a valid numeric Citizen ID."
            )

            return

        if not self.conn:

            messagebox.showerror(
                "Database Error",
                "No active database connection."
            )

            return

        # Clear old results first
        for row in self.track_tree.get_children():

            self.track_tree.delete(row)

        cursor = self.conn.cursor()

        try:

            # =================================================
            # UPDATED QUERY
            # =================================================
            #
            # c.CITIZEN_ID has been added to the SELECT.
            #
            # The WHERE condition still makes sure that ONLY
            # complaints belonging to the searched Citizen ID
            # are displayed.
            #
            # =================================================

            query = """
                SELECT
                    c.COMPLAINT_ID,
                    c.CITIZEN_ID,
                    c.COMPLAINT_TITLE,
                    d.DEPT_NAME,
                    c.STATUS,
                    c.PRIORITY,
                    c.COMPLAINT_DATE
                FROM Complaint c
                JOIN Department d
                    ON c.DEPARTMENTID = d.DEPARTMENTID
                WHERE c.CITIZEN_ID = :citizen_id
                ORDER BY c.COMPLAINT_DATE DESC
            """

            cursor.execute(
                query,
                {
                    "citizen_id": int(citizen_id)
                }
            )

            rows = cursor.fetchall()

            if not rows:

                messagebox.showinfo(
                    "No Complaints Found",
                    "No complaints were found for this Citizen ID."
                )

                return

            # Insert the matching complaints
            for row in rows:

                self.track_tree.insert(
                    "",
                    "end",
                    values=row
                )

        except Exception as e:

            messagebox.showerror(
                "Query Error",
                f"Error retrieving your complaints:\n{e}"
            )

        finally:

            cursor.close()


# =========================================================
# APPLICATION START
# =========================================================

if __name__ == "__main__":

    app = CitizenApp()

    app.mainloop()