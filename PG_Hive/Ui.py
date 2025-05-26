import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk
from PIL import Image, ImageTk
import bridge
from bridge import search_pg_bridge
import time


class PGFinderApp:

    def __init__(self, root):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = root
        self.root.geometry("358x537")
        self.root.title("PG Hive")
        self.bg_image = None

        self.create_menubar()
        self.create_main_buttons()

        global servers
        servers = bridge.check_database_status()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.geometry("358x537")

    def create_menubar(self):
        menubar = tk.Menu(self.root,
                          bg="#051424",
                          fg="white",
                          activebackground="#102030",
                          activeforeground="white")
        menubar.add_command(label="Home", command=self.create_main_buttons)
        menubar.add_command(label="Login", command=self.show_login_screen)
        menubar.add_command(label="Signup", command=self.show_signup_screen)
        menubar.add_command(label="Seeker", command=self.show_seeker_screen)
        self.root.config(menu=menubar)

    def login_menubar(self):
        menubar = tk.Menu(self.root,
                          bg="#051424",
                          fg="white",
                          activebackground="#102030",
                          activeforeground="white")
        menubar.add_command(label="Logout", command=self.create_main_buttons)
        menubar.add_command(label="Add", command=self.structure)
        menubar.add_command(label="Update", command=self.update)
        self.root.config(menu=menubar)

    def loggedin_screen(self):
        self.clear_window()
        self.login_menubar()
        self.set_background_image("PG_background.png")

        self.fore_img = tk.PhotoImage(file='PG_foreground.png')
        fore_lbl = tk.Label(self.root,
                            image=self.fore_img,
                            bd=0,
                            highlightthickness=0,
                            bg="#000D27")
        fore_lbl.pack(pady=(30, 10))

        tk.Label(self.root,
                 text=f"Welcome, {self.logged_in_user}",
                 font=("Arial", 14),
                 bg="#000F2C",
                 fg="white").pack()

        self.host_img = tk.PhotoImage(file='add.png')
        host_lbl = tk.Label(self.root,
                            image=self.host_img,
                            bd=0,
                            highlightthickness=0,
                            bg="#001A3E")
        host_lbl.place(x=50, y=300)
        host_lbl.bind("<Button-1>", lambda e: self.structure())

        self.seeker_img = tk.PhotoImage(file='update.png')
        seeker_lbl = tk.Label(self.root,
                              image=self.seeker_img,
                              bd=0,
                              highlightthickness=0,
                              bg="#001435")
        seeker_lbl.place(x=50, y=180)
        seeker_lbl.bind("<Button-1>", lambda e: self.update())

    def add_screen(self):
        self.structure()

    def structure(self, data=None):
        self.clear_window()
        self.login_menubar()
        self.set_background_image("PG_background.png")

        # Set the heading based on whether data is provided
        heading_text = "Update PG Details" if data else "Add PG Details"
        tk.Label(self.root,
                 text=heading_text,
                 font=("Arial", 20),
                 bg="#000D27",
                 fg="white").pack(pady=20)

        container = tk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        canvas = tk.Canvas(container, bg="#000D27", highlightthickness=0)
        v_scrollbar = tk.Scrollbar(container,
                                   orient="vertical",
                                   command=canvas.yview)

        canvas.configure(yscrollcommand=v_scrollbar.set)

        v_scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scrollable_frame = tk.Frame(canvas, bg="#000D27")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.pg_form_entries = {}

        def create_dark_entry(parent):
            return tk.Entry(parent,
                            width=18,
                            bg="#001F4D",
                            fg="white",
                            insertbackground="white",
                            relief=tk.FLAT)

        def create_dark_combobox(parent, values):
            style = ttk.Style()
            style.theme_use('default')
            style.configure("Dark.TCombobox",
                            fieldbackground="#001F4D",
                            background="#001F4D",
                            foreground="white")
            combo = ttk.Combobox(parent,
                                 values=values,
                                 width=16,
                                 style="Dark.TCombobox")
            return combo

        entries = {
            "Name":
            create_dark_entry(scrollable_frame),
            "City":
            create_dark_entry(scrollable_frame),
            "State":
            create_dark_combobox(scrollable_frame,
                                 ["Haryana", "Delhi", "Punjab"]),
            "Duration":
            create_dark_entry(scrollable_frame),
            "Timing":
            create_dark_entry(scrollable_frame),
            "Floor":
            create_dark_entry(scrollable_frame),
            "Category":
            create_dark_combobox(scrollable_frame,
                                 ["family", "student", "both"]),
            "Furniture":
            create_dark_combobox(
                scrollable_frame,
                ["fully furnished", "semi furnished", "unfurnished"]),
            "Ac/cooler":
            create_dark_combobox(scrollable_frame,
                                 ["ac", "cooler", "both", "none"]),
            "Rent":
            create_dark_entry(scrollable_frame),
            "Rooms":
            create_dark_entry(scrollable_frame),
            "Address":
            create_dark_entry(scrollable_frame),
            "Contact No":
            create_dark_entry(scrollable_frame),
        }

        toggles = {
            "Nearby Market": tk.BooleanVar(),
            "Locality": tk.StringVar(),
            "Availability": tk.BooleanVar()
        }

        row_num = 0
        for label, widget in entries.items():
            tk.Label(scrollable_frame,
                     text=label,
                     width=16,
                     anchor='w',
                     bg="#000D27",
                     fg="white",
                     font=("Arial", 10)).grid(row=row_num,
                                              column=0,
                                              sticky="w",
                                              pady=5,
                                              padx=5)
            widget.grid(row=row_num, column=1, sticky="w", pady=5, padx=5)
            self.pg_form_entries[label] = widget
            row_num += 1

        for label, var in toggles.items():
            tk.Label(scrollable_frame,
                     text=label,
                     width=16,
                     anchor='w',
                     bg="#000D27",
                     fg="white",
                     font=("Arial", 10)).grid(row=row_num,
                                              column=0,
                                              sticky="w",
                                              pady=5,
                                              padx=5)
            if label == "Locality":
                frame = tk.Frame(scrollable_frame, bg="#000D27")
                tk.Radiobutton(frame,
                               text="Urban",
                               variable=var,
                               value="urban",
                               bg="#000D27",
                               fg="white",
                               selectcolor="#001537").pack(side=tk.LEFT,
                                                           padx=5)
                tk.Radiobutton(frame,
                               text="Rural",
                               variable=var,
                               value="rural",
                               bg="#000D27",
                               fg="white",
                               selectcolor="#001537").pack(side=tk.LEFT,
                                                           padx=5)
                frame.grid(row=row_num, column=1, sticky="w", pady=5, padx=5)
            else:
                tk.Checkbutton(scrollable_frame,
                               text="Yes",
                               variable=var,
                               bg="#000D27",
                               fg="white",
                               selectcolor="#001537").grid(row=row_num,
                                                           column=1,
                                                           sticky="w",
                                                           pady=5,
                                                           padx=5)
            self.pg_form_entries[label] = var
            row_num += 1

        if data:
            for key in entries:
                entries[key].insert(0, data.get(key, ""))
            for key in toggles:
                if key == "Locality":
                    toggles[key].set(data.get(key, "urban"))
                else:
                    toggles[key].set(data.get(key, "yes") == "yes")

        def submit_form():
            self.submit_status_lbl.configure(text="✅ Submitted Successfully!",
                                             fg="lightgreen")

        if data:  # Update mode
            action_btn = ctk.CTkButton(self.root,
                                       text="Update",
                                       command=self.update_pg)
        else:  # Add mode
            action_btn = ctk.CTkButton(self.root,
                                       text="Add",
                                       command=self.add_new)

        action_btn.pack(pady=10)

        self.submit_status_lbl = tk.Label(self.root,
                                          text="",
                                          font=("Arial", 12),
                                          bg="#000D27")
        self.submit_status_lbl.pack(pady=5)


    def update(self):

        self.clear_window()
        self.login_menubar()
        self.set_background_image("PG_background.png")
        tk.Label(self.root,
                 text="Update PG Details",
                 font=("Arial", 20),
                 bg="#000E2A",
                 fg="white").pack(pady=40)

        tk.Label(self.root,
                 text="Here's your PG(s)",
                 font=("Arial", 12),
                 bg="#00102E",
                 fg="white").pack(pady=10)

        tree_frame = tk.Frame(self.root)
        tree_frame.pack(padx=10, pady=5)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(tree_frame,
                                 columns=("Name", "Address", "Availability"),
                                 show='headings',
                                 yscrollcommand=tree_scroll.set,
                                 height=8)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Availability", text="Availability")

        self.tree.column("Name", width=90, anchor=tk.CENTER)
        self.tree.column("Address", width=170, anchor=tk.CENTER)
        self.tree.column("Availability", width=65, anchor=tk.CENTER)

        self.tree.pack()
        tree_scroll.config(command=self.tree.yview)

        self.avail_btn = ctk.CTkButton(self.root,
                                       text="Change Availability",
                                       state=tk.DISABLED,
                                       command=self.toggle_availability)
        self.avail_btn.place(x=110, y=370)

        self.update_btn = ctk.CTkButton(self.root,
                                        text="Update",
                                        state=tk.DISABLED,
                                        command=self.open_update_form)
        self.update_btn.place(x=20, y=410)

        self.delete_btn = ctk.CTkButton(self.root,
                                        text="Delete",
                                        state=tk.DISABLED,
                                        command=self.delete_pg)
        self.delete_btn.place(x=200, y=410)

        self.feedback_label = ctk.CTkLabel(self.root,
                                           text="",
                                           fg_color="#000D27",
                                           text_color="white",
                                           corner_radius=0)
        self.feedback_label.place(x=123, y=450)

        self.tree.bind("<<TreeviewSelect>>", self.enable_buttons)

        user_id = self.logged_in_user_id  # Make sure you store user_id during login!
        results = bridge.get_pgs_by_owner_bridge(user_id)

        self.pg_data = results  # Store for later use

        for row in results:
            self.selected_id = row[0]
            name = row[13]
            address = f"{row[2]}, {row[16]}, {row[15]}"
            availability = row[17]
            self.tree.insert('', tk.END, values=(name, address, availability))

    def enable_buttons(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]
            row_values = self.tree.item(item_id, 'values')

            selected_name = row_values[0]
            selected_address = row_values[1]

            for row in self.pg_data:
                name = row[13]
                address = f"{row[2]}, {row[16]}, {row[15]}"
                if name == selected_name and address == selected_address:
                    self.selected_p_g_id = row[0] 
                    break

            self.update_btn.configure(state=tk.NORMAL)
            self.delete_btn.configure(state=tk.NORMAL)
            self.avail_btn.configure(state=tk.NORMAL)

    def add_new(self):
        data = {
            "user_id": self.logged_in_user_id,
            "name": self.pg_form_entries["Name"].get(),
            "address": self.pg_form_entries["Address"].get(),
            "availability": "Yes" if self.pg_form_entries["Availability"].get() else "No",
            "city": self.pg_form_entries["City"].get(),
            "state": self.pg_form_entries["State"].get(),
            "duration": self.pg_form_entries["Duration"].get(),
            "timing": self.pg_form_entries["Timing"].get(),
            "floor": self.pg_form_entries["Floor"].get(),
            "category": self.pg_form_entries["Category"].get(),
            "furniture": self.pg_form_entries["Furniture"].get(),
            "ac_cooler": self.pg_form_entries["Ac/cooler"].get(),
            "rent": self.pg_form_entries["Rent"].get(),
            "market": "yes" if self.pg_form_entries["Nearby Market"].get() else "no",
            "locality": self.pg_form_entries["Locality"].get(),
            "rooms": self.pg_form_entries["Rooms"].get(),
            "contact": self.pg_form_entries["Contact No"].get()
        }

        bridge.add_new_bridge(data)

        self.submit_status_lbl.configure(text="✅ PG added successfully!", fg="lightgreen")

    def delete_pg(self):
        selected_item = self.tree.selection()
        if selected_item:  
            pg_id = self.selected_id  

            success = bridge.delete_pg_bridge(pg_id)

            if success:
                self.tree.delete(selected_item[0])  
                self.feedback_label.configure(text="PG deleted from database", text_color="#32D74B")
            else:
                self.feedback_label.configure(text="Failed to delete from database", text_color="#FF3B30")

    def update_pg(self):
        update_dict = {
            "name": self.pg_form_entries["Name"].get(),
            "address": self.pg_form_entries["Address"].get(),
            "availability": "yes" if self.pg_form_entries["Availability"].get() else "no",
            "city": self.pg_form_entries["City"].get(),
            "state": self.pg_form_entries["State"].get(),
            "duration": self.pg_form_entries["Duration"].get(),
            "timing": self.pg_form_entries["Timing"].get(),
            "floor": self.pg_form_entries["Floor"].get(),
            "category": self.pg_form_entries["Category"].get(),
            "furniture": self.pg_form_entries["Furniture"].get(),
            "ac_cooler": self.pg_form_entries["Ac/cooler"].get(),
            "rent": self.pg_form_entries["Rent"].get(),
            "market": "yes" if self.pg_form_entries["Nearby Market"].get() else "no",
            "locality": self.pg_form_entries["Locality"].get(),
            "rooms": self.pg_form_entries["Rooms"].get(),
            "contact": self.pg_form_entries["Contact No"].get(),
        }
      
        bridge.edit_data(update_dict, self.selected_id)
        self.submit_status_lbl.configure(text="✅ PG details updated!", fg="lightgreen")

    def toggle_availability(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]
            values = self.tree.item(item_id, 'values')

            current_availability = values[2]
            new_availability = "No" if current_availability == "Yes" else "Yes"
            pg_id = self.selected_id
            success = bridge.edit_data({"availability": new_availability}, pg_id)

            if success:
                self.tree.item(item_id, values=(values[0], values[1], new_availability))
                self.feedback_label.configure(text="Availability updated", text_color="#32D74B")
            else:
                self.feedback_label.configure(text="Failed to update availability", text_color="#FF3B30")


    def open_update_form(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_pg_id = self.selected_p_g_id

            for row in self.pg_data:
                if row[0] == selected_pg_id: 
                    data = {
                        "Name": row[13],
                        "Address": row[2],
                        "Availability": row[17],
                        "City": row[16],
                        "State": row[15],
                        "Duration": row[12],
                        "Timing": row[11],
                        "Floor": row[10],
                        "Category": row[9],
                        "Furniture": row[8],
                        "Ac/cooler": row[7],
                        "Rent": row[6],
                        "Nearby Market": row[5],
                        "Locality": row[4],
                        "Rooms": row[3],
                        "Contact No": row[14]
                    }
                    self.structure(data)
                    break  

    def set_background_image(self, image_file):
        image = Image.open(image_file)
        self.bg_image = ImageTk.PhotoImage(image)
        bg_label = tk.Label(self.root, image=self.bg_image, borderwidth=0)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()

    def create_main_buttons(self):
        self.clear_window()
        self.create_menubar()
        self.set_background_image("PG_background.png")

        self.fore_img = tk.PhotoImage(file='PG_foreground.png')
        fore_lbl = tk.Label(self.root,
                            image=self.fore_img,
                            bd=0,
                            highlightthickness=0,
                            bg="#000D27")
        fore_lbl.pack(pady=60)

        self.host_img = tk.PhotoImage(file='host.png')
        host_lbl = tk.Label(self.root,
                            image=self.host_img,
                            bd=0,
                            highlightthickness=0,
                            bg="#00183C")
        host_lbl.place(x=50, y=290)
        host_lbl.bind("<Button-1>", lambda e: self.show_login_screen())

        self.seeker_img = tk.PhotoImage(file='seeker.png')
        seeker_lbl = tk.Label(self.root,
                              image=self.seeker_img,
                              bd=0,
                              highlightthickness=0,
                              bg="#001435")
        seeker_lbl.place(x=50, y=177)
        seeker_lbl.bind("<Button-1>", lambda e: self.show_seeker_screen())

    def show_login_screen(self):
        self.clear_window()
        self.create_menubar()
        self.set_background_image("PG_background.png")
        dot_color = "green" if servers == "online" else "red"
        tk.Label(self.root,
                 text="●",
                 fg=dot_color,
                 bg="#000D27",
                 font=("Arial", 15)).place(relx=0.99, rely=0, anchor="ne")

        tk.Label(self.root,
                 text="Login",
                 font=("Arial", 20),
                 bg="#000D27",
                 fg="white").pack(pady=15)
        tk.Label(self.root,
                 text="User name",
                 font=("Arial", 12),
                 bg="#00102D",
                 fg="white").pack()
        self.username_entry = ctk.CTkEntry(self.root)
        self.username_entry.pack(padx=20, pady=5)
        tk.Label(self.root,
                 text="Password",
                 font=("Arial", 12),
                 bg="#001130",
                 fg="white").pack()
        self.password_entry = ctk.CTkEntry(self.root, show="*")
        self.password_entry.pack(padx=15, pady=5)

        self.feedback_label = ctk.CTkLabel(self.root,
                                           text="",
                                           fg_color="#000D27",
                                           text_color="white",
                                           corner_radius=0)
        self.feedback_label.pack(pady=5)


        ctk.CTkButton(self.root, text="Submit",
                      command=self.check_login).pack(pady=5)

        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=(15,1))
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=(1,15))
        tk.Label(self.root,
                 text="Don't have an account!?",
                 font=("Arial", 12),
                 bg="#00193D",
                 fg="white").pack()
        tk.Label(self.root,
                 text="Create a new one",
                 font=("Arial", 12),
                 bg="#00193D",
                 fg="white").pack()
        ctk.CTkButton(self.root,
                      text="Signup",
                      command=self.show_signup_screen).pack(pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        user_row = bridge.login_bridge(username, password)

        if user_row: 
            self.logged_in_user_id = user_row[0]  
            self.logged_in_user = user_row[1]  
            self.feedback_label.configure(text="Logged in",
                                          text_color="#32D74B")
            self.root.after(1500, self.loggedin_screen)
        else:
            self.feedback_label.configure(text="Wrong username or password",
                                          text_color="#FF3B30")
    def show_signup_screen(self):
        self.clear_window()
        self.create_menubar()
        self.set_background_image("PG_background.png")

        dot_color = "green" if servers == "online" else "red"
        tk.Label(self.root,
                 text="●",
                 fg=dot_color,
                 bg="#000D27",
                 font=("Arial", 15)).place(relx=0.99, rely=0, anchor="ne")

        tk.Label(self.root,
                 text="Signup",
                 font=("Arial", 20),
                 bg="#000D27",
                 fg="white").pack(pady=10)
        tk.Label(self.root,
                 text="User name",
                 font=("Arial", 12),
                 bg="#000F2B",
                 fg="white").pack()
        self.signup_username = ctk.CTkEntry(self.root)
        self.signup_username.pack(padx=20, pady=5)

        tk.Label(self.root,
                 text="Email",
                 font=("Arial", 12),
                 bg="#001130",
                 fg="white").pack()
        self.signup_email = ctk.CTkEntry(self.root)
        self.signup_email.pack(padx=20, pady=5)

        tk.Label(self.root,
                 text="Password",
                 font=("Arial", 12),
                 bg="#001433",
                 fg="white").pack()
        self.signup_password = ctk.CTkEntry(self.root, show="*")
        self.signup_password.pack(padx=20, pady=5)

        tk.Label(self.root,
                 text="Confirm Password",
                 font=("Arial", 12),
                 bg="#001738",
                 fg="white").pack()
        self.signup_confirm = ctk.CTkEntry(self.root, show="*")
        self.signup_confirm.pack(padx=20, pady=5)

        self.signup_feedback = ctk.CTkLabel(self.root,
                                            text="",
                                            fg_color="#000D27",
                                            text_color="#FF3B30",
                                            corner_radius=0)
        self.signup_feedback.pack(pady=5)

        self.send_otp_btn = ctk.CTkButton(self.root,
                                          text="Send OTP",
                                          command=self.send_otp,
                                          fg_color="#FF9F0A",
                                          state="disabled")
        self.send_otp_btn.pack(pady=5)

        tk.Label(self.root,
                 text="OTP",
                 font=("Arial", 12),
                 bg="#001C41",
                 fg="white").pack()
        self.otp_entry = ctk.CTkEntry(self.root, state="disabled")
        self.otp_entry.pack(padx=20, pady=5)

        self.register_btn = ctk.CTkButton(self.root,
                                          text="Register",
                                          command=self.register_button,
                                          fg_color="#32D74B",
                                          state="disabled")
        self.register_btn.pack(pady=10)

        self.signup_password.bind("<KeyRelease>", self.check_password_match)
        self.signup_confirm.bind("<KeyRelease>", self.check_password_match)

        self.generated_otp = None  

    def send_otp(self):
        user_email = self.signup_email.get()
        otp_code = bridge.send_otp_bridge(user_email)  

        if otp_code:
            self.signup_feedback.configure(text="OTP sent to your email",
                                           text_color="#32D74B")
            self.otp_entry.configure(state="normal")
            self.register_btn.configure(state="normal")
            self.generated_otp = otp_code  
        else:
            self.signup_feedback.configure(text="Failed to send OTP",
                                           text_color="#FF3B30")

    def register_button(self):
        eotp = self.otp_entry.get()
        username = self.signup_username.get()
        email = self.signup_email.get()
        password = self.signup_password.get()

        if not username.strip() or not email.strip() or not password.strip():
            self.signup_feedback.configure(text="Fill all fields",
                                           text_color="#FF3B30")
            return

        if bridge.verify_otp_bridge(eotp, self.generated_otp):
            success = bridge.register_user_bridge(username, email, password)
            if success:
                self.signup_feedback.configure(
                    text="Registration Successful ✅", text_color="#32D74B")
                self.root.after(3000, self.show_login_screen)
            else:
                self.signup_feedback.configure(text="Error: User not saved",
                                               text_color="#FF3B30")
        else:
            self.signup_feedback.configure(text="Wrong OTP ❌",
                                           text_color="#FF3B30")

    def check_password_match(self, _event=None):
        username = self.signup_username.get()
        pwd = self.signup_password.get()
        conf = self.signup_confirm.get()

        if not username.strip():
            self.send_otp_btn.configure(state="disabled")
            self.signup_feedback.configure(text="Username can't be null",
                                           text_color="#FF3B30")
            return

        if pwd and conf:
            if pwd == conf:
                self.send_otp_btn.configure(state="normal")
                self.signup_feedback.configure(text="", text_color="#32D74B")
            else:
                self.send_otp_btn.configure(state="disabled")
                self.signup_feedback.configure(
                    text="Password and confirm password must be same",
                    text_color="#FF3B30")
        else:
            self.send_otp_btn.configure(state="disabled")
            self.signup_feedback.configure(text="", text_color="white")

    def _enable_otp(self):
        self.otp_entry.configure(state="normal")
        self.register_btn.configure(state="normal")
        self.signup_feedback.configure(text="OTP sent", text_color="#32D74B")

    def search_pgs(self, state, city):
        import bridge  
        results = bridge.search_pg_bridge(state, city)
        self.pg_results = results  
        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, row in enumerate(results):
            name = row[13] 
            address = f"{row[2]}, {row[16]}, {row[15]}"  
            availability = row[17] 
            self.tree.insert('',
                             'end',
                             iid=str(idx),
                             values=(name, address, availability))
          
        self.tree.bind("<<TreeviewSelect>>", self.show_pg_description)

    def show_pg_description(self, event):
        selected = self.tree.focus()
        if selected:
            idx = int(selected)
            row = self.pg_results[idx]

            description = (
                f"Rent: {row[6]}, Locality: {row[4]}, Market: {row[5]}, "
                f"Rooms: {row[3]}, AC/Cooler: {row[7]}, Furniture: {row[8]}, "
                f"Category: {row[9]}, Floor: {row[10]}, Timing: {row[11]}, "
                f"Duration: {row[12]}, Contact: {row[14]}"
            )
            self.desc_label.config(text=f"➤ {description}")

    def show_seeker_screen(self):
        self.clear_window()
        self.create_menubar()
        self.set_background_image("PG_background.png")

        dot_color = "green" if servers == "online" else "red"
        tk.Label(self.root,
                 text="●",
                 fg=dot_color,
                 bg="#000D27",
                 font=("Arial", 15)).place(relx=0.99, rely=0, anchor="ne")

        tk.Label(self.root,
                 text="State",
                 font=("Arial", 12),
                 bg="#000F2B",
                 fg="white").pack(anchor="w", padx=10, pady=10)
        self.state_cb = ctk.CTkComboBox(self.root,
                                        values=["Haryana", "Delhi", "Punjab"])
        self.state_cb.pack(fill="x", padx=10, pady=5)

        tk.Label(self.root,
                 text="City",
                 font=("Arial", 12),
                 bg="#001130",
                 fg="white").pack(anchor="w", padx=10, pady=10)
        self.city_entry = ctk.CTkEntry(self.root)
        self.city_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(self.root,
                      text="Search",
                      command=self.on_search_button_click).pack(pady=10)

        # Table frame
        table_frame = tk.Frame(self.root, bg="#000D27")
        table_frame.pack(expand=False, fill="x", padx=5, pady=5)

        columns = ("Name", "Address", "Availability")
        self.tree = ttk.Treeview(table_frame,
                                 columns=columns,
                                 show="headings",
                                 selectmode="browse")
        vsb = tk.Scrollbar(table_frame,
                           orient="vertical",
                           command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)

        self.tree.pack(fill="x")

        desc_frame = tk.Frame(self.root, bg="#000D27", height=70)
        desc_frame.pack(fill="x", padx=5, pady=5)

        self.desc_label = tk.Label(desc_frame,
                                   text="Select a PG to see details.",
                                   bg="#000D27",
                                   fg="white",
                                   anchor="nw",
                                   justify="left",
                                   wraplength=330,
                                   font=("Arial", 10))
        self.desc_label.pack(fill="both", expand=True, padx=8, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.show_pg_description)

        self.pg_results = []

    def on_search_button_click(self):
        state = self.state_cb.get()
        city = self.city_entry.get()

        self.search_pgs(state, city)


if __name__ == "__main__":
    root = ctk.CTk()
    app = PGFinderApp(root)
    root.resizable(0, 0)
    root.mainloop()

