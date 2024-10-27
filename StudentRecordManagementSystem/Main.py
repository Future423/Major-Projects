import tkinter as tk
from tkinter import ttk, font, messagebox, Menu
import pandas as pd
from datetime import datetime  
import csv 

class StudentDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Management System")
        self.root.geometry('1250x600')
        self.bg_color = "#C2FFD7"  # Background color
        self.root.configure(bg=self.bg_color)

        self.label_font = font.Font(family="Helvetica", size=10, weight="bold")
        self.entry_font = font.Font(family="Helvetica", size=10)

        # Upper Frame
        self.upper_frame = tk.Frame(self.root, bg=self.bg_color)
        self.upper_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        options = [
            ("Date:", "date_entry", 0, 5, 30),
            ("Roll No:", "roll_no_entry", 0, 1, 30),
            ("Name:", "name_entry", 0, 3, 30),
            ("Course:", "course_entry", 1, 5, 30),
            ("DOB:", ["d_entry", "m_entry", "y_entry"], 1, 1),
            ("Contact:", "contact_entry", 5, 1, 25),
            ("Gender:", "gender_combobox", 6, 1),
            ("Address:", "address_entry", 5, 3, 25)
        ]

        self.entries = {}

        for option in options:
            label_text, entry_name, row, col = option[:4]
            width = option[4] if len(option) == 5 else 20

            tk.Label(self.upper_frame, text=label_text, bg=self.bg_color, font=self.label_font).grid(row=row, column=col, pady=2, sticky='e')

            if isinstance(entry_name, list):  
                day_options = list(range(1, 32))
                self.d_var = tk.StringVar(self.upper_frame)
                self.d_combobox = ttk.Combobox(self.upper_frame, textvariable=self.d_var, values=day_options, font=self.entry_font, width=5, state="readonly")
                self.d_combobox.set(day_options[0])  
                self.d_combobox.grid(row=row, column=col + 1, padx=5, pady=5, sticky='we')

                month_options = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                self.m_var = tk.StringVar(self.upper_frame)
                self.m_combobox = ttk.Combobox(self.upper_frame, textvariable=self.m_var, values=month_options, font=self.entry_font, width=5, state="readonly")
                self.m_combobox.set(month_options[0])  
                self.m_combobox.grid(row=row, column=col + 2, padx=5, pady=5, sticky='we')

                year_options = list(range(2024, 1943, -1))
                self.y_var = tk.StringVar(self.upper_frame)
                self.y_combobox = ttk.Combobox(self.upper_frame, textvariable=self.y_var, values=year_options, font=self.entry_font, width=5, state="readonly")
                self.y_combobox.set(year_options[-1])  
                self.y_combobox.grid(row=row, column=col + 3, padx=5, pady=5, sticky='we')

            elif label_text == "Gender:":
                self.gender_var = tk.StringVar(self.upper_frame)
                self.gender_combobox = ttk.Combobox(self.upper_frame, textvariable=self.gender_var, values=["Male", "Female"], font=self.entry_font, width=24, state="readonly")
                self.gender_combobox.grid(row=row, column=col + 1, padx=5, pady=5, sticky='we')

            else:
                self.entries[entry_name] = tk.Entry(self.upper_frame, font=self.entry_font, width=width)
                self.entries[entry_name].grid(row=row, column=col + 1, padx=5, pady=5, sticky='we')

            # Bind mouse click event to enable roll_no_entry
            if entry_name == "roll_no_entry":
                self.entries[entry_name].bind("<Button-1>", self.enable_new)

        # Separator
        ttk.Separator(self.upper_frame, orient='horizontal').grid(row=7, column=0, columnspan=13, sticky='ew', pady=10)

        self.search_label = tk.Label(self.upper_frame, text="Search", bg=self.bg_color, font=self.label_font)
        self.search_label.grid(row=8, column=1, padx=5, pady=10, sticky='w')

        # Search By Dropdown
        self.search_by_var = tk.StringVar(self.upper_frame)
        self.search_by_combobox = ttk.Combobox(self.upper_frame, textvariable=self.search_by_var, values=["Roll No", "Name", "DOB", "Contact"], state="readonly", font=self.entry_font, width=15)
        self.search_by_combobox.grid(row=8, column=2, padx=10, pady=5, sticky='ew')
        self.search_by_combobox.set("Search By")  
        self.search_by_combobox.bind("<<ComboboxSelected>>", self.on_select_by_change)

        self.text_entry = tk.Entry(self.upper_frame, state='disabled', font=self.entry_font, width=30)
        self.text_entry.grid(row=8, column=3, padx=10, pady=10)
        self.text_entry.bind("<FocusIn>", self.on_text_entry_focus_in)
        self.text_entry.bind("<KeyRelease>", self.on_text_entry_key_release)

        # Buttons
        self.search_button = tk.Button(self.upper_frame, text="Search", command=self.search_data,state='disabled', font=self.label_font, bg="#68F793")
        self.search_button.grid(row=8, column=4, padx=10, sticky='w')

        self.save_button = tk.Button(self.upper_frame, text="Save", command=self.save_data, state='disabled', font=self.label_font, bg="#68F793", width=10)
        self.save_button.grid(row=6, column=4, padx=15, pady=5)

        self.update_button = tk.Button(self.upper_frame, text="Update", command=self.update_data, state='disabled', font=self.label_font, bg="#68F793", width=10)
        self.update_button.grid(row=6, column=5, padx=15, pady=1, sticky='w')

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_text, font=self.label_font, bg="#68F793")
        self.clear_button.pack(side=tk.TOP, fill=tk.X, padx=10)

        # Lower Frame
        self.lower_frame = tk.Frame(self.root, bg=self.bg_color)
        self.lower_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))

        self.tree = ttk.Treeview(self.lower_frame)
        self.tree.pack(expand=True, fill='both', side=tk.LEFT)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbar = tk.Scrollbar(self.lower_frame, command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Message Label
        self.message_label = tk.Label(self.root, text="", bg=self.bg_color, font=self.label_font)
        self.message_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self.delete_record)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.load_data()
 
    def on_select_by_change(self, event):
        selected_option = self.search_by_combobox.get() 
        if selected_option:
            self.text_entry.config(state='normal')  
            self.text_entry.insert(0, f"enter {selected_option}") 

    def load_data(self):
        self.df = pd.read_csv("SData.csv")
        self.update_treeview(self.df)

    def on_text_entry_focus_in(self, event):
        current_value = self.text_entry.get()
        if current_value.startswith("enter"):
            self.text_entry.delete(0, tk.END)

    def on_text_entry_key_release(self, event):
        if self.text_entry.get():  
            self.search_button.config(state='normal')  
        else:
            self.search_button.config(state='disabled')  

    def clear_text(self):
        for entry_name, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.config()

        self.gender_var.set("Select Gender")
        self.save_button.config()
        self.gender_combobox.config()
        self.update_button.config()
        self.update_button.config(state='disabled')
        self.update_treeview(self.df)  
        
    def update_treeview(self, df):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.tree["column"] = list(df.columns)
        self.tree["show"] = "headings"
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        for col in self.tree["columns"]:
            max_width = max(df[col].astype(str).map(len).max(), len(col)) * 10  
            self.tree.column(col, width=max_width)

        colors = ["#FFFFFF", "#C2FFD7"]  

        for idx, (_, row) in enumerate(df.iterrows(), start=1):
            if idx % 2 == 0:
                bg_color = colors[1]  
            else:
                bg_color = colors[0]  

            self.tree.insert("", "end", values=list(row), tags=('evenrow' if idx % 2 == 0 else 'oddrow'))

        self.tree.tag_configure('evenrow', background='#FFFFFF')  
        self.tree.tag_configure('oddrow', background='#C2FFD7')  

    def editable(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        record_values = self.tree.item(selected_item)["values"]
        self.current_record_index = self.tree.index(selected_item)

        for entry_name, entry in self.entries.items():
            entry.config(state='normal')

        self.gender_combobox.config(state='normal')
        self.update_button.config(state='normal')

        col_mapping = {
            "Date": "date_entry",
            "Roll No": "roll_no_entry",
            "Name": "name_entry",
            "Course": "course_entry",
            "Address": "address_entry",
            "Gender": "gender_combobox",
            "Contact": "contact_entry"
        }

        for col_name, value in zip(self.df.columns, record_values):
            if col_name in col_mapping:
                entry_name = col_mapping[col_name]
                if entry_name == "gender_combobox":
                    self.gender_var.set(value)
                elif entry_name in self.entries:
                    self.entries[entry_name].delete(0, tk.END)
                    self.entries[entry_name].insert(0, value)

        # Handling the DOB
        dob = record_values[self.df.columns.get_loc("DOB")].split('-')
        
        self.d_combobox.set(dob[0])  
        self.m_combobox.set(dob[1])  
        self.y_combobox.set(dob[2])  

    def update_data(self):
        updated_data = {}
        col_mapping = {
            "Date": "date_entry",
            "Roll No": "roll_no_entry",
            "Name": "name_entry",
            "Course": "course_entry",
            "Address": "address_entry",
            "Gender": "gender_combobox",
            "Contact": "contact_entry"
        }

        for col_name, entry_name in col_mapping.items():
            if entry_name in self.entries:
                updated_data[col_name] = self.entries[entry_name].get()
            elif entry_name == "gender_combobox":
                updated_data[col_name] = self.gender_var.get()

        dob = f"{self.d_combobox.get()}-{self.m_combobox.get()}-{self.y_combobox.get()}"
        updated_data["DOB"] = dob

        for col_name, value in updated_data.items():
            self.df.at[self.current_record_index, col_name] = value

        self.df.to_csv("SData.csv", index=False)

        self.clear_text()
        self.update_treeview(self.df)

        self.message_label.config(text="Record updated successfully.", fg="green")
        self.update_button.config(state='disabled')
        
        self.message_label.after(3000, lambda: self.message_label.config(text=""))

    def delete_record(self):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, "values")

        confirm = messagebox.askyesno("Delete Record", "Do you want to delete the selected record?")
        if confirm:
            selected_tuple = tuple(values)
            
            with open("SData.csv", "r", newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)
            
            rows = [row for row in rows if tuple(row) != selected_tuple]
            
            with open("SData.csv", "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            self.df = pd.DataFrame(rows[1:], columns=rows[0]) 
            self.update_treeview(self.df)
            messagebox.showinfo("Success", "Record deleted successfully")

    def on_tree_select(self, event):
        if self.tree.selection():
            self.editable()

    def enable_new(self,event):
        for entry in self.entries.values():
            if isinstance(entry, list):
                for sub_entry in entry:
                    sub_entry.config(state='normal')
            else:
                entry.config(state='normal')

        current_date = datetime.now().strftime("%d/%m/%y")
        self.entries["date_entry"].config(state='normal')
        self.entries["date_entry"].delete(0, tk.END)
        self.entries["date_entry"].insert(0, current_date)
        self.entries["date_entry"].config()

        self.gender_combobox.config(state='normal')

        self.save_button.config(state='normal')

    def show_context_menu(self, event):
        if self.tree.selection():
            self.context_menu.post(event.x_root, event.y_root)   

    def search_data(self):
        search_by = self.search_by_var.get()
        search_term = self.text_entry.get()
        
        column_map = {
            "Roll No": "Roll No",
            "Name": "Name",
            "DOB": "DOB",
            "Contact": "Contact"
        }
        search_column = column_map.get(search_by)
        
        if not search_column or not search_term:
            self.message_label.config(text="Please select a valid search option and enter a search term.")
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            with open("SData.csv", mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                matches = [row for row in reader if search_term.lower() in row.get(search_column, "").lower()]
                
                if not matches:
                    self.message_label.config(text="No matching records found.")
                    return
                
                self.tree["column"] = list(matches[0].keys())
                self.tree["show"] = "headings"
                for col in self.tree["columns"]:
                    self.tree.heading(col, text=col, anchor=tk.CENTER)
                    
                    max_width = max(len(str(row[col])) for row in matches) * 10  
                    self.tree.column(col, width=max_width)
                                
                colors = ["#FFFFFF", "#C2FFD7"]  
                
                for idx, row in enumerate(matches, start=1):
                    bg_color = colors[idx % 2]  # Alternate colors
                    tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                    self.tree.insert("", "end", values=list(row.values()), tags=(tag,))
                
                self.tree.tag_configure('evenrow', background='#FFFFFF')
                self.tree.tag_configure('oddrow', background='#C2FFD7')
                
                self.message_label.config(text=f"Found {len(matches)} matching record(s).")
                
        except FileNotFoundError:
            self.message_label.config(text="SData.csv file not found.")
        except Exception as e:
            self.message_label.config(text=f"An error occurred: {e}")

    def save_data(self):
        new_data = {
            "Date": self.entries["date_entry"].get(),
            "Name": self.entries["name_entry"].get(),
            "Course": self.entries["course_entry"].get(),
            "Contact": self.entries["contact_entry"].get(),
            "Roll No": self.entries["roll_no_entry"].get(),
            "DOB": f"{self.d_combobox.get()}-{self.m_combobox.get()}-{self.y_combobox.get()}",
            "Gender": self.gender_var.get(), 
            "Address": self.entries["address_entry"].get()
        }

        self.df = pd.concat([self.df, pd.DataFrame([new_data])], ignore_index=True)
        self.df.to_csv("SData.csv", index=False)
        self.update_treeview(self.df)

        for entry in self.entries.values():
            if isinstance(entry, list):
                for sub_entry in entry:
                    sub_entry.delete(0, tk.END)
                    sub_entry.config()
            else:
                entry.delete(0, tk.END)
                entry.config()
        
        self.gender_combobox.config()
        self.gender_var.set("Select Gender")

        self.save_button.config(state='disabled')

        self.message_label.config(text="SAVED", fg="green")
        self.root.after(2000, self.clear_message)

    def clear_message(self):
        self.message_label.config(text="")

def main():
    root = tk.Tk()
    app = StudentDataApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
