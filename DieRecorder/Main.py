import tkinter as tk
from tkinter import ttk, font, messagebox, Menu
import pandas as pd
import itertools
from datetime import datetime 
import csv 

class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TPS Meraki Die Recorder")
        self.root.geometry('1250x600')
        self.bg_color = "#E3DEF3"  
        self.root.configure(bg=self.bg_color)
        
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        def bind_enter_key(button, window=None):
            if window is None:
                window = self.root
            window.bind('<Return>', lambda event: button.invoke())

        self.new_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="New", command=self.enable_new)
        self.menu_bar.add_command(label="Delete", command=self.delete_record)
        self.menu_bar.add_command(label="Help", command=self.show_help)
        self.upper_frame = tk.Frame(root, bg=self.bg_color)
        self.upper_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.label_font = font.Font(family="Helvetica", size=10, weight="bold")
        self.entry_font = font.Font(family="Helvetica", size=10)

        tk.Label(self.upper_frame, text="             ", bg=self.bg_color, font=self.label_font).grid(row=0, column=0, pady=2, sticky='e')
        tk.Label(self.upper_frame, text="   ", bg=self.bg_color, font=self.label_font).grid(row=0, column=5, pady=2, sticky='e')
        tk.Label(self.upper_frame, text="                          ", bg=self.bg_color, font=self.label_font).grid(row=0, column=8, pady=2, sticky='e')


        options = [
            ("Date:", "date_entry"),
            ("Die Code:", "die_code_entry"),
            ("Party:", "party_entry"),
            ("Job Name:", "job_name_entry"),
            ("Box Size:", ["l_entry", "w_entry", "h_entry"]), 
            ("Sheet Size:", "sheet_size_entry"),
            ("UPS:", "ups_entry"),
            ("Pasting:", "pasting_dropdown"), 
            ("Packing:", "packing_entry")
        ]

        self.entries = {}
        for idx, (label_text, entry_name) in enumerate(options):
            if label_text in ["Date:", "Die Code:"]:
                column = 1 if label_text == "Date:" else 3
                self.entries[entry_name] = tk.Entry(self.upper_frame, font=self.entry_font, state='disabled')
                tk.Label(self.upper_frame, text=label_text, bg=self.bg_color, font=self.label_font).grid(row=0, column=column, pady=2, sticky='e')
                self.entries[entry_name].grid(row=0, column=column + 1, padx=5, pady=5, sticky='we')
            elif label_text == "Box Size:":
                tk.Label(self.upper_frame, text=label_text, bg=self.bg_color, font=self.label_font).grid(row=1, column=1, pady=2, sticky='e')  
                self.entries[entry_name[0]] = tk.Entry(self.upper_frame, font=self.entry_font, state='disabled')
                self.entries[entry_name[1]] = tk.Entry(self.upper_frame, font=self.entry_font, state='disabled')
                self.entries[entry_name[2]] = tk.Entry(self.upper_frame, font=self.entry_font, state='disabled')
                self.entries[entry_name[0]].grid(row=1, column=2, padx=5, pady=5, sticky='we')
                self.entries[entry_name[1]].grid(row=1, column=3, padx=5, pady=5, sticky='we')
                self.entries[entry_name[2]].grid(row=1, column=4, padx=5, pady=5, sticky='we')
            elif label_text in ["Sheet Size:", "UPS:"]:
                column = 1 if label_text == "Sheet Size:" else 3
                self.entries[entry_name] = tk.Entry(self.upper_frame, font=self.entry_font, state='disabled', width=25)
                tk.Label(self.upper_frame, text=label_text, bg=self.bg_color, font=self.label_font).grid(row=5, column=column, pady=2, sticky='e') 
                self.entries[entry_name].grid(row=5, column=column + 1, padx=5, pady=5, sticky='we')
            elif label_text in ["Packing:", "Pasting:"]:
                if label_text == "Pasting:":
                    self.pasting_var = tk.StringVar(self.upper_frame)
                    self.pasting_var.set("Select ID")  # Default value
                    self.pasting_dropdown = tk.OptionMenu(self.upper_frame, self.pasting_var, "Top Opening Lock Pasting", "Top Opening Inter Lock", "2 Side Opening Reverse Track")
                    self.pasting_dropdown.config(font=self.entry_font, state='disabled',width=24)
                    tk.Label(self.upper_frame, text=label_text, bg=self.bg_color, font=self.label_font).grid(row=6, column=1, pady=2, sticky='e')  
                    self.pasting_dropdown.grid(row=6, column=2, padx=5, pady=5, sticky='we')
                else:
                    column = 3  
                    self.entries[entry_name] = tk.Entry(self.upper_frame, font=self.entry_font, state='disabled', width=25)
                    tk.Label(self.upper_frame, text=label_text, bg=self.bg_color, font=self.label_font).grid(row=6, column=column, pady=2, sticky='e')  
                    self.entries[entry_name].grid(row=6, column=column + 1, padx=5, pady=5, sticky='we')
            elif label_text == "Party:":
                column = 6
                self.entries[entry_name] = tk.Entry(self.upper_frame, font=self.entry_font, state='disabled', width=45)  # Twice as wide
                tk.Label(self.upper_frame, text=label_text, bg=self.bg_color, font=self.label_font).grid(row=0, column=column, pady=2, sticky='e')
                self.entries[entry_name].grid(row=0, column=column + 1, padx=5, pady=5, sticky='we')
            elif label_text == "Job Name:":
                column = 6
                self.entries[entry_name] = tk.Entry(self.upper_frame, font=self.entry_font, state='disabled', width=45)  
                tk.Label(self.upper_frame, text=label_text, bg=self.bg_color, font=self.label_font).grid(row=1, column=column, pady=2, sticky='e')
                self.entries[entry_name].grid(row=1, column=column + 1, padx=5, pady=5, sticky='we')
            else:
                self.entries[entry_name] = tk.Entry(self.upper_frame, font=self.entry_font, state='disabled')
                tk.Label(self.upper_frame, text=label_text, bg=self.bg_color, font=self.label_font).grid(row=idx, column=0, pady=2, sticky='e')
                self.entries[entry_name].grid(row=idx, column=1, padx=5, pady=3, columnspan=3, sticky='we')
                
        self.separator = ttk.Separator(self.upper_frame, orient='horizontal')
        self.separator.grid(row=len(options)+1, column=0, columnspan=13, sticky='ew', pady=10)

        self.save_button = tk.Button(self.upper_frame, text="Save", command=self.save_data, state='disabled', padx=5, font=self.label_font, bg="#C4BAE4")
        self.save_button.grid(row=6, column=6, padx=15, pady=1, sticky='e')  # Adjust row as per your layout

        tk.Label(self.upper_frame, text="Search", bg=self.bg_color, font=self.label_font).grid(row=len(options)+2, column=1)
        self.l_entry = tk.Entry(self.upper_frame, font=self.entry_font)
        self.w_entry = tk.Entry(self.upper_frame, font=self.entry_font)
        self.h_entry = tk.Entry(self.upper_frame, font=self.entry_font)

        self.l_entry.grid(row=len(options)+2, column=2, padx=5)
        self.w_entry.grid(row=len(options)+2, column=3, padx=5)
        self.h_entry.grid(row=len(options)+2, column=4, padx=5)

        tk.Label(self.upper_frame, text="L", bg=self.bg_color, font=self.label_font).grid(row=len(options)+3, column=2)
        tk.Label(self.upper_frame, text="W", bg=self.bg_color, font=self.label_font).grid(row=len(options)+3, column=3)
        tk.Label(self.upper_frame, text="H", bg=self.bg_color, font=self.label_font).grid(row=len(options)+3, column=4)

        self.search_button = tk.Button(self.upper_frame, text="Search", command=self.search_data, padx=7, font=self.label_font, bg="#C4BAE4")
        self.search_button.grid(row=len(options)+2, column=6, padx=10)

        self.update_button = tk.Button(self.upper_frame, text="Update", command=self.update_data,padx=5, state='disabled', font=self.label_font, bg="#C4BAE4")
        self.update_button.grid(row=6, column=7, padx=15, pady=1, sticky='w')

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_text, font=self.label_font, bg="#C4BAE4")
        self.clear_button.pack(side=tk.TOP, fill=tk.X, padx=10, ipady=0)

        self.lower_frame = tk.Frame(root, bg=self.bg_color)
        self.lower_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))  # Adjust pady as needed

        self.tree = ttk.Treeview(self.lower_frame)
        self.tree.pack(expand=True, fill='both', side=tk.LEFT)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.context_menu = Menu(root, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self.delete_record)

        self.tree.bind("<Button-3>", self.show_context_menu)

        self.scrollbar = tk.Scrollbar(self.lower_frame, command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')

        self.message_label = tk.Label(root, text="", bg=self.bg_color, font=self.label_font)
        self.message_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))
        
        bind_enter_key(self.search_button)

        self.load_data()

    def load_data(self):
        self.df = pd.read_csv("SampleData.csv")
        self.update_treeview(self.df)

    def clear_text(self):
        for entry_name, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.config(state='disabled')

        self.pasting_var.set("Select ID")
        self.save_button.config(state='disabled')
        self.pasting_dropdown.config(state='disabled')
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

        colors = ["#FFFFFF", "#E3DEF3"]  

        for idx, (_, row) in enumerate(df.iterrows(), start=1):
            if idx % 2 == 0:
                bg_color = colors[1]  
            else:
                bg_color = colors[0]  

            self.tree.insert("", "end", values=list(row), tags=('evenrow' if idx % 2 == 0 else 'oddrow'))

        self.tree.tag_configure('evenrow', background='#FFFFFF')  
        self.tree.tag_configure('oddrow', background='#E3DEF3')  

    def editable(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        record_values = self.tree.item(selected_item)["values"]
        self.current_record_index = self.tree.index(selected_item)

        for entry_name, entry in self.entries.items():
            entry.config(state='normal')

        self.pasting_dropdown.config(state='normal')
        self.update_button.config(state='normal')

        col_mapping = {
            "Date": "date_entry",
            "Die Code": "die_code_entry",
            "Party": "party_entry",
            "Job Name": "job_name_entry",
            "Packing": "packing_entry",
            "Pasting": "pasting_dropdown",
            "Sheet Size": "sheet_size_entry",
            "UPS": "ups_entry"
        }

        for col_name, value in zip(self.df.columns, record_values):
            if col_name in col_mapping:
                entry_name = col_mapping[col_name]
                if entry_name == "pasting_dropdown":
                    self.pasting_var.set(value)
                elif entry_name in self.entries:
                    self.entries[entry_name].delete(0, tk.END)
                    self.entries[entry_name].insert(0, value)
        
        box_size = record_values[self.df.columns.get_loc("Box Size")].split('X')
        self.entries["l_entry"].delete(0, tk.END)
        self.entries["l_entry"].insert(0, box_size[0])
        self.entries["w_entry"].delete(0, tk.END)
        self.entries["w_entry"].insert(0, box_size[1])
        self.entries["h_entry"].delete(0, tk.END)
        self.entries["h_entry"].insert(0, box_size[2])

    def update_data(self):
        updated_data = {}
        col_mapping = {
            "Date": "date_entry",
            "Die Code": "die_code_entry",
            "Party": "party_entry",
            "Job Name": "job_name_entry",
            "Packing": "packing_entry",
            "Pasting": "pasting_dropdown",
            "Sheet Size": "sheet_size_entry",
            "UPS": "ups_entry"
        }

        for col_name, entry_name in col_mapping.items():
            if entry_name in self.entries:
                updated_data[col_name] = self.entries[entry_name].get()
            elif entry_name == "pasting_dropdown":
                updated_data[col_name] = self.pasting_var.get()

        box_size = f"{self.entries['l_entry'].get()}X{self.entries['w_entry'].get()}X{self.entries['h_entry'].get()}"
        updated_data["Box Size"] = box_size

        for col_name, value in updated_data.items():
            self.df.at[self.current_record_index, col_name] = value

        self.df.to_csv("Die_Record.csv", index=False)
        self.clear_text()
        self.update_treeview(self.df)


    def delete_record(self):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, "values")

        confirm = messagebox.askyesno("Delete Record", "Do you want to delete the selected record?")
        if confirm:
            selected_tuple = tuple(values)
            
            with open("Die_Record.csv", "r", newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)
            
            rows = [row for row in rows if tuple(row) != selected_tuple]
            
            with open("Die_Record.csv", "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            self.df = pd.DataFrame(rows[1:], columns=rows[0]) 
            self.update_treeview(self.df)
            messagebox.showinfo("Success", "Record deleted successfully")

    def on_tree_select(self, event):
        if self.tree.selection():
            self.editable()

    def enable_new(self):
        for entry in self.entries.values():
            if isinstance(entry, list):
                for sub_entry in entry:
                    sub_entry.config(state='normal')
            else:
                entry.config(state='normal')

        self.entries["die_code_entry"].config(state='normal')
        next_die_code = self.generate_next_die_code()
        self.entries["die_code_entry"].delete(0, tk.END)
        self.entries["die_code_entry"].insert(0, next_die_code)
        self.entries["die_code_entry"].config(state='disabled')

        current_date = datetime.now().strftime("%d/%m/%y")
        self.entries["date_entry"].config(state='normal')
        self.entries["date_entry"].delete(0, tk.END)
        self.entries["date_entry"].insert(0, current_date)
        self.entries["date_entry"].config(state='disabled')

        self.pasting_dropdown.config(state='normal')

        self.save_button.config(state='normal')

    def show_context_menu(self, event):
        if self.tree.selection():
            self.context_menu.post(event.x_root, event.y_root)
    def show_help(self):
        help_text = (
            "For assistance, please contact:\n\n"
            "Phone: +XY-ABCDEFGH\n"
            "Email: yourgmail@gmail.com\n\n"
            "Thank you!"
        )
        messagebox.showinfo("Help", help_text)
    
    def generate_next_die_code(self):
        if self.df.empty:
            return "1"
        max_die_code = self.df["Die Code"].dropna().apply(lambda x: int(x) if str(x).isdigit() else 0).max()
        return str(max_die_code + 1)

    def search_data(self):
        l_value = self.l_entry.get()
        w_value = self.w_entry.get()
        h_value = self.h_entry.get()

        if l_value and w_value and h_value:
            dimensions = [l_value, w_value, h_value]
            perm = list(itertools.permutations(dimensions))

            search_values = [f"{perm[i][0]}X{perm[i][1]}X{perm[i][2]}" for i in range(len(perm))]

            result_df = pd.DataFrame()
            for value in search_values:
                result_df = pd.concat([result_df, self.df[self.df["Box Size"].apply(self.approx_match, search_value=value)]])
            if not result_df.empty:
                self.update_treeview(result_df)
            else:
                self.message_label.config(text="No Match Found", fg="green")
                self.root.after(2000, self.clear_message)
        else:
            self.message_label.config(text="Enter valid data", fg="green")
            self.root.after(2000, self.clear_message)
        
        self.l_entry.delete(0, tk.END)
        self.w_entry.delete(0, tk.END)
        self.h_entry.delete(0, tk.END)

    def approx_match(self, box_size, search_value):
        if pd.isna(box_size):
            return False

        box_size = str(box_size)
        box_dims = box_size.split("X")
        search_dims = search_value.split("X")
        tolerance = 5 

        for s_dim, b_dim in zip(search_dims, box_dims):
            try:
                b_dim_int = int(b_dim)
                s_dim_int = int(s_dim)
                if not (b_dim_int - tolerance <= s_dim_int <= b_dim_int + tolerance):
                    return False
            except ValueError:
                return False 
        return True

    def save_data(self):
        new_data = {
            "Date": self.entries["date_entry"].get(),
            "Party": self.entries["party_entry"].get(),
            "Job Name": self.entries["job_name_entry"].get(),
            "Sheet Size": self.entries["sheet_size_entry"].get(),
            "UPS": self.entries["ups_entry"].get(),
            "Die Code": self.entries["die_code_entry"].get(),
            "Box Size": f"{self.entries['l_entry'].get()}X{self.entries['w_entry'].get()}X{self.entries['h_entry'].get()}",
            "Pasting": self.pasting_var.get(), 
            "Packing": self.entries["packing_entry"].get()
        }

        self.df = pd.concat([self.df, pd.DataFrame([new_data])], ignore_index=True)
        self.df.to_csv("Die_Record.csv", index=False)
        self.update_treeview(self.df)

        for entry in self.entries.values():
            if isinstance(entry, list):
                for sub_entry in entry:
                    sub_entry.delete(0, tk.END)
                    sub_entry.config(state='disabled')
            else:
                entry.delete(0, tk.END)
                entry.config(state='disabled')

        self.pasting_dropdown.config(state='disabled')

        self.save_button.config(state='disabled')

        self.message_label.config(text="SAVED", fg="green")
        self.root.after(2000, self.clear_message)

    def clear_message(self):
        self.message_label.config(text="")

def main():
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
