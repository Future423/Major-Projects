from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import os
import pandas as pd
import calendar
from sheet import SalarySheetGenerator

def fetch_employee_names(file_path):
    try:
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
            names = data.iloc[:, 0].tolist()[0:] 
            return names
        else:
            return []
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching employee names: {e}")
        return []

def update_employee_name_combobox():
    file_path = "Salary.csv"
    employee_names = fetch_employee_names(file_path)
    if employee_names:
        employee_name_combobox['values'] = employee_names
        employee_name_combobox.set('')  
    else:
        employee_name_combobox['values'] = []

def fetch_month_files():
    directory_path = "Attandence" #replace it with your path
    try:
        files = os.listdir(directory_path)
        month_files = [file for file in files if file.endswith('.csv') and file != 'Salary.csv']
        months = [os.path.splitext(file)[0] for file in month_files]
        return months
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching month files: {e}")
        return []

def update_month_combobox():
    months = fetch_month_files()
    month_combobox['values'] = months
    month_combobox.set('') 
def fetch_names_from_month_file(file_path):
    try:
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
            names = data.columns.tolist()[1:]  
            return names
        else:
            return []
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching names from the month file: {e}")
        return []

def update_employee_combobox_for_month():
    selected_month = month_combobox.get()
    if selected_month:
        file_path = f"Attandence\\{selected_month}.csv"
        employee_names = fetch_names_from_month_file(file_path)
        if employee_names:
            employee_combobox['values'] = employee_names
            employee_combobox.set('')  
        else:
            employee_combobox['values'] = []

def on_month_selection(event):
    update_employee_combobox_for_month()

def add_attendance(directory, salary_file_path, employee_name, attendance_entry):
    """Add attendance data for the previous day."""
    employee_names = fetch_employee_names(salary_file_path)
    
    if not employee_names:
        status_label.config(text="No employees found.")
        return
    
    if employee_name not in employee_names:
        status_label.config(text="Selected employee not found.")
        return
    
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    month_name = yesterday.strftime('%b')  
    yesterday_date = yesterday.strftime('%d')  
    
    if yesterday.weekday() == 6: 
        yesterday_date = f"(R){yesterday_date}"
    
    file_name = f"{month_name}.csv"
    file_path = os.path.join(directory, file_name)
    
    if os.path.exists(file_path):
        data = pd.read_csv(file_path, index_col=0)
    else:
        data = pd.DataFrame(columns=['Date/Name'] + employee_names)
        data.set_index('Date/Name', inplace=True)
        data.to_csv(file_path)
    
    if employee_name not in data.columns:
        data[employee_name] = [''] * len(data)
    
    attendance = attendance_entry.get().strip()
    if attendance:
        if yesterday_date in data.index:
            data.at[yesterday_date, employee_name] = attendance
        else:
            new_row = pd.Series([''] * len(data.columns), index=data.columns)
            data.loc[yesterday_date] = new_row
            data.at[yesterday_date, employee_name] = attendance

        data.to_csv(file_path)
        status_label.config(text=f"Attendance for {employee_name} on {yesterday_date} has been added.")
        
        employee_name_combobox.set('')
        attendance_entry.delete(0, tk.END)
    else:
        status_label.config(text="Attendance cannot be empty.")


def handle_button_click():
    employee_name = employee_name_combobox.get()
    attendance_entry_text = attendance_entry.get()
    directory = r"Attandence"
    salary_file_path = os.path.join(directory, "Salary.csv")
    add_attendance(directory, salary_file_path, employee_name, attendance_entry)
    root.after(2000, clear_status)

def clear_status():
    status_label.config(text="")

def open_file_explorer():
    directory_path = r"Attandence"
    if os.path.isdir(directory_path):
        os.startfile(directory_path)
    else:
        messagebox.showerror("Error", "Directory does not exist.")

def calculate_ote(salary, month):
    year = datetime.now().year
    month_number = datetime.strptime(month, "%b").month
    days_in_month = calendar.monthrange(year, month_number)[1]
    return (salary / 8.5) / days_in_month

def show_salary_info():
    selected_employee = employee_combobox.get()
    selected_month = month_combobox.get()
    
    if not selected_employee or not selected_month:
        messagebox.showwarning("Warning", "Please select both employee and month.")
        return
    
    file_path = f"Attandence\\{selected_month}.csv"
    salary_file_path = r"Attandence\Salary.csv"
    
    try:
        data = pd.read_csv(file_path)
        salary_data = pd.read_csv(salary_file_path)
        
        if selected_employee not in data.columns:
            messagebox.showwarning("Warning", f"No data found for {selected_employee}.")
            return
        
        employee_salary_row = salary_data[salary_data['Name'] == selected_employee]
        if employee_salary_row.empty:
            messagebox.showwarning("Warning", f"Salary information for {selected_employee} not found.")
            return
        
        salary = employee_salary_row.iloc[0]['Salary']
        days_in_month = (datetime(datetime.now().year, datetime.strptime(selected_month, "%b").month + 1, 1) - timedelta(days=1)).day
        OTE = (salary / 8.5) / days_in_month

        total_absent = 0
        total_halftime = 0
        total_overtime = 0
        total_attendance_records = 0
        
        for index, row in data.iterrows():
            date = row['Date/Name']
            attendance = row[selected_employee]
            if pd.isna(attendance):
                continue
            hours_worked = None
            
            if attendance not in ["A", "H", "R"]:
                times = attendance.split('-')
                if len(times) == 2:
                    start_time, end_time = times
                    hours_worked = calculate_hours_worked(start_time, end_time)
                    if hours_worked is not None and hours_worked > 6:
                        total_attendance_records += 1
                    if hours_worked is not None:
                        total_overtime += calculate_overtime(hours_worked, date)
            elif attendance == "R":
                total_attendance_records += 1
                
            if attendance == "A":
                total_absent += 1
            elif attendance == "H":
                total_halftime += 1
            
        total_overtime = round(total_overtime, 2)

        salary_total = OTE * 8.5 * total_attendance_records
        halftime_salary = OTE * 4.25 * total_halftime
        overtime_salary = OTE * total_overtime
        total_salary = salary_total + halftime_salary + overtime_salary

        result = (
            f"Total Attendance Records: {total_attendance_records}\n"
            f"Total Halftime: {total_halftime}\n"
            f"Total Overtime: {total_overtime:.2f}\n"
            f"OTE: {OTE:.2f}\n"
            f"Salary: {salary_total:.2f}\n"
            f"Halftime Salary: {halftime_salary:.2f}\n"
            f"Overtime Salary: {overtime_salary:.2f}\n"
            f"Total Salary: {total_salary:.2f}"
        )
        
        messagebox.showinfo("Salary Information", result)
        
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred while showing salary information: {e}")

def calculate_hours_worked(arrival_time, departure_time):
    try:
        arrival = datetime.strptime(arrival_time, '%H:%M')
        departure = datetime.strptime(departure_time, '%H:%M')
        if arrival >= departure:
            departure += timedelta(hours=24)
        delta = departure - arrival
        total_hours = delta.seconds / 3600
        return total_hours
    except ValueError:
        return None

def round_off_minutes(hours):
    total_minutes = int(hours * 60)
    rounded_minutes = (total_minutes // 30) * 30
    rounded_hours = rounded_minutes / 60
    return rounded_hours

def calculate_overtime(hours_worked, date):
    standard_hours = 8.5
    if "(R)" in date:
        hours_worked = round_off_minutes(hours_worked)
        return hours_worked
    else:
        overtime = hours_worked - standard_hours
        if overtime <= 0 and hours_worked <= 6:
            overtime_minutes = hours_worked * 60
            rounded_overtime_minutes = round_off_minutes(overtime_minutes / 60)
            return rounded_overtime_minutes
        elif overtime <= 0:
            return 0
        else:
            overtime_minutes = (overtime * 60)
            rounded_overtime_minutes = round_off_minutes(overtime_minutes / 60)
            return rounded_overtime_minutes

def show_help():
    help_text = (
        "For assistance, please contact:\n\n"
        "Phone: +XY-ABCDEFGH\n"
        "Email: yourgmail@gmail.com\n\n"
        "Thank you!"
    )
    messagebox.showinfo("Help", help_text)

def show_attendance_info():
    selected_employee = employee_combobox.get()
    selected_month = month_combobox.get()
    
    if not selected_employee or not selected_month:
        messagebox.showwarning("Warning", "Please select both employee and month.")
        return
    
    file_path = f"Attandence\\{selected_month}.csv"
    
    try:
        data = pd.read_csv(file_path)
        
        if selected_employee not in data.columns:
            messagebox.showwarning("Warning", f"No data found for {selected_employee}.")
            return
        
        header_format = "{:<12} {:<15} {:<15} {:<10}"
        row_format = "{:<15} {:<25} {:<20} {:<0}"
        
        output_lines = []
        output_lines.append(header_format.format('Date', 'Attendance', 'Hours Worked', 'Overtime'))
        
        total_absent = 0
        total_halftime = 0
        total_attendance_records = 0
        total_overtime = 0
        
        hours_worked_list = []
        
        for index, row in data.iterrows():
            date = row['Date/Name']
            attendance = row[selected_employee]
            if pd.isna(attendance):
                continue
            hours_worked = None
            overtime = 0
            
            if attendance not in ["A", "H", "R"]:
                times = attendance.split('-')
                if len(times) == 2:
                    start_time, end_time = times
                    hours_worked = calculate_hours_worked(start_time, end_time)
                    if hours_worked is not None:
                        hours_worked_formatted = f"{int(hours_worked)}:{int((hours_worked % 1) * 60):02}"
                        overtime = calculate_overtime(hours_worked, date)
                        if hours_worked > 6:
                            hours_worked_list.append(hours_worked)
                        total_overtime += overtime
                    else:
                        hours_worked_formatted = "N/A"
                else:
                    hours_worked_formatted = "N/A"
            else:
                hours_worked_formatted = "N/A"
            
            if attendance == "A":
                total_absent += 1
            elif attendance == "H":
                total_halftime += 1
            elif attendance == "R":
                total_attendance_records += 1
            
            output_lines.append(row_format.format(date, attendance, hours_worked_formatted, f"{overtime:.2f}"))
        
        total_attendance_records += len(hours_worked_list)
        total_overtime = round(total_overtime, 2)

        output_lines.append(f"\nTotal Attendance Records: {total_attendance_records}")
        output_lines.append(f"Total Halftime: {total_halftime}")
        output_lines.append(f"Total Overtime: {total_overtime:.2f}")
        output_lines.append(f"Total Absent: {total_absent}")
        
        result = "\n".join(output_lines)
        messagebox.showinfo("Attendance Information", result)
        
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred while showing attendance information: {e}")

def open_add_employee_popup():
    add_employee_popup = tk.Toplevel(root)
    add_employee_popup.title("Add Employee")
    add_employee_popup.geometry("300x200")
    add_employee_popup.configure(bg="#ddffee")

    add_employee_popup.resizable(False, False)
    add_employee_popup.attributes('-toolwindow', True)
    
    style = ttk.Style()
    style.configure("TEntry", background="#b9ffdc", font=("Helvetica", 11))
    style.configure("TButton", background="#b9ffdc", foreground="#000000", font=("Helvetica", 11))

    ttk.Label(add_employee_popup, text="Enter Name:", background="#ddffee").pack(padx=10, pady=5, anchor="w")
    name_entry = ttk.Entry(add_employee_popup, width=25)
    name_entry.pack(padx=10, pady=5)

    ttk.Label(add_employee_popup, text="Enter Salary:", background="#ddffee").pack(padx=10, pady=5, anchor="w")
    salary_entry = ttk.Entry(add_employee_popup, width=25)
    salary_entry.pack(padx=10, pady=5)

    def add_employee():
        name = name_entry.get()
        salary = salary_entry.get()
        if name and salary:
            file_path = r"Attandence\Salary.csv"
            try:
                if os.path.exists(file_path):
                    salary_data = pd.read_csv(file_path)
                else:
                    salary_data = pd.DataFrame(columns=['Name', 'Salary'])
                
                new_data = pd.DataFrame([[name, salary]], columns=['Name', 'Salary'])
                salary_data = pd.concat([salary_data, new_data], ignore_index=True)
                
                salary_data.to_csv(file_path, index=False)
                messagebox.showinfo("Add Employee", f"Employee {name} with salary {salary} added.")
                update_employee_name_combobox()
                update_employee_combobox_for_month()
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred while adding a new employee: {e}")
            add_employee_popup.destroy()
        else:
            messagebox.showwarning("Input Error", "Both name and salary must be provided.")

    add_button = ttk.Button(add_employee_popup, text="Add", command=add_employee)
    add_button.pack(pady=10)
    bind_enter_key(add_button, add_employee_popup)

def bind_enter_key(button, window=None):
    if window is None:
        window = root
    window.bind('<Return>', lambda event: button.invoke())

def view_sheet():
    if __name__ == "__main__":
        root = tk.Tk()
        app = SalarySheetGenerator(root)
        root.mainloop()

root = tk.Tk()
root.title("TPS Attendance & Salary")
root.geometry("410x380")
root.resizable(False, False)
root.attributes('-fullscreen', False)

style = ttk.Style()
style.configure("TFrame", background="#ddffee")
style.configure("TLabel", background="#ddffee", font=("Helvetica", 11))
style.configure("TCombobox", background="#b9ffdc", font=("Helvetica", 11))
style.configure("TLabelframe", background="#ddffee", font=("Helvetica", 10))
style.configure("TLabelframe.Label", background="#ddffee", font=("Helvetica", 10))

style.configure("Custom.TButton", background="#b9ffdc", foreground="#000000", font=("Helvetica", 11), 
                relief="flat", padding=5)
style.map("Custom.TButton",
          background=[('active', '#b9ffdc')],
          foreground=[('active', '#000000')])

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
root.configure(bg="#ddffee")

menu_bar.add_command(label="Files", command=open_file_explorer)
menu_bar.add_command(label="View Sheet", command=view_sheet)
menu_bar.add_command(label="Add Employee", command=open_add_employee_popup)
menu_bar.add_command(label="Help", command=show_help)

main_frame = ttk.Frame(root)
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

attendance_frame = ttk.LabelFrame(main_frame, text="Attendance Management", padding=(10, 5), style="TLabelframe")
attendance_frame.pack(fill="both", expand=True, pady=5)

salary_frame = ttk.LabelFrame(main_frame, text="Salary Management", padding=(10, 5), style="TLabelframe")
salary_frame.pack(fill="both", expand=True, pady=5)

ttk.Label(attendance_frame, text="Employee Name:", background="#ddffee").grid(row=0, column=0, padx=10, pady=5, sticky="w")
employee_name_combobox = ttk.Combobox(attendance_frame, state="readonly", style="TCombobox")
employee_name_combobox.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(attendance_frame, text="Yesterday's Attendance:", background="#ddffee").grid(row=1, column=0, padx=10, pady=5, sticky="w")
attendance_entry = ttk.Entry(attendance_frame, width=25)
attendance_entry.grid(row=1, column=1, padx=10, pady=5)

add_attendance_button = ttk.Button(attendance_frame, text="Add Attendance", command=handle_button_click, style="Custom.TButton")
add_attendance_button.grid(row=2, column=0, columnspan=2, pady=5)

status_label = ttk.Label(attendance_frame, text="", background="#ddffee", font=("Helvetica", 11))
status_label.grid(row=3, column=0, columnspan=2, pady=5)

ttk.Label(salary_frame, text="Select Month:", background="#ddffee").grid(row=0, column=0, padx=10, pady=5, sticky="w")
month_combobox = ttk.Combobox(salary_frame, state="readonly", style="TCombobox")
month_combobox.grid(row=0, column=1, padx=10, pady=5)
month_combobox.bind("<<ComboboxSelected>>", on_month_selection)

ttk.Label(salary_frame, text="Select Employee:", background="#ddffee").grid(row=1, column=0, padx=10, pady=5, sticky="w")
employee_combobox = ttk.Combobox(salary_frame, state="readonly", style="TCombobox")
employee_combobox.grid(row=1, column=1, padx=10, pady=5)

salary_button = ttk.Button(salary_frame, text="Salary", command=show_salary_info, style="Custom.TButton")
salary_button.grid(row=2, column=0, pady=5, padx=5, sticky="e")

attendance_button = ttk.Button(salary_frame, text="Attendance", command=show_attendance_info, style="Custom.TButton")
attendance_button.grid(row=2, column=1, pady=5, padx=5, sticky="w")

bind_enter_key(add_attendance_button)

update_month_combobox()
update_employee_name_combobox()

root.mainloop()
