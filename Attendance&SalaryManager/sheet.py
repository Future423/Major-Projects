import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime, timedelta 
import calendar 

def calculate_hours_worked(start_time, end_time):
    start_dt = datetime.strptime(start_time, '%H:%M')
    end_dt = datetime.strptime(end_time, '%H:%M')
    if start_dt >= end_dt:
        end_dt += timedelta(hours=24)
    worked_hours = (end_dt - start_dt).seconds / 3600
    return worked_hours

def calculate_overtime(hours_worked, date):
    """Calculate overtime based on hours worked and date."""
    standard_hours = 8.5
    overtime = hours_worked - standard_hours
    
    if "(R)" in date:
        return hours_worked

    if hours_worked <= 6:
        overtime_minutes = hours_worked * 60
        rounded_overtime_minutes = overtime_minutes - (overtime_minutes % 30)
        return rounded_overtime_minutes / 60
    elif overtime > 0:
        overtime_minutes = (overtime * 60)
        rounded_overtime_minutes = overtime_minutes - (overtime_minutes % 30)
        return rounded_overtime_minutes / 60
    else:
        return 0

def create_csv_file():
    selected_file = file_combobox.get()
    file_name = file_name_entry.get()

    if not selected_file or not file_name:
        messagebox.showwarning("Warning", "Please select a file and enter a file name.")
        return

    input_file_path = os.path.join("C:\\Users\\hello\\Documents\\Attandence", selected_file)
    output_file_path = os.path.join(os.path.expanduser("~\\Desktop"), file_name + ".csv")

    try:
        data = pd.read_csv(input_file_path)
        salary_data = pd.read_csv("C:\\Users\\hello\\Documents\\Attandence\\Salary.csv")

        employees = data.columns[1:]
        dates = data.iloc[:, 0]
        
        output_data = {
            "Names": employees,
            "P": [],
            "R": [],
            "H": [],
            "A": [],
            "Attendance": [],
            "Overtime": [],
            "Salary": [],
            "Amount": [],
            "Overtime Salary": [],
            "Total Amount": []
        }

        month_str = selected_file.split('.')[0]
        month_number = datetime.strptime(month_str, "%b").month
        year = datetime.now().year  
        month_days = calendar.monthrange(year, month_number)[1]

        for employee in employees:
            p_count = 0
            r_count = 0
            h_count = 0
            a_count = 0
            overtime_total = 0.0
            salary = salary_data.loc[salary_data['Name'] == employee, 'Salary'].values[0]

            for index, entry in enumerate(data[employee]):
                date = dates[index]
                if isinstance(entry, str) and '-' in entry:
                    times = entry.split('-')
                    if len(times) == 2:
                        start_time, end_time = times
                        hours_worked = calculate_hours_worked(start_time, end_time)
                        if hours_worked > 6:
                            p_count += 1
                            overtime_total += calculate_overtime(hours_worked, date)
                        else:
                            a_count += 1
                            overtime_total += calculate_overtime(hours_worked, date)  
                elif entry == "R":
                    r_count += 1
                elif entry == "H":
                    h_count += 1
                elif entry == "A":
                    a_count += 1

            attendance_count = p_count + r_count + (h_count / 2)
            ote = (salary / 8.5) / month_days
            amount = attendance_count * ote * 8.5
            overtime_salary = overtime_total * ote
            total_amount = amount + overtime_salary

            output_data["P"].append(p_count)
            output_data["R"].append(r_count)
            output_data["H"].append(h_count)
            output_data["A"].append(a_count)
            output_data["Attendance"].append(attendance_count)
            output_data["Overtime"].append(overtime_total)
            output_data["Salary"].append(salary)
            output_data["Amount"].append(amount)
            output_data["Overtime Salary"].append(overtime_salary)
            output_data["Total Amount"].append(total_amount)

        output_df = pd.DataFrame(output_data)
        output_df.loc["Total"] = output_df.sum(numeric_only=True)
        output_df.to_csv(output_file_path, index=False)

        messagebox.showinfo("Success", f"CSV file '{file_name}.csv' created successfully on the Desktop.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def get_files():
    files = [f for f in os.listdir("C:\\Users\\hello\\Documents\\Attandence") if f.endswith(".csv") and f != "Salary.csv"]
    return files

root = tk.Tk()
root.title("Salary Sheet")
root.geometry("260x130")
root.resizable(False, False)
root.attributes('-fullscreen', False)
root.config(bg="#ddffee")

tk.Label(root, text="Select File:", bg="#ddffee").grid(row=0, column=0, padx=10, pady=10)
file_combobox = ttk.Combobox(root, values=get_files())
file_combobox.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="File Name:", bg="#ddffee").grid(row=1, column=0, padx=10, pady=10)
file_name_entry = tk.Entry(root)
file_name_entry.grid(row=1, column=1, padx=10, pady=10)

create_button = tk.Button(root, text="Create", command=create_csv_file, padx=6, bg="#b9ffdc")#, fg="white")
create_button.grid(row=2, columnspan=2, pady=10)

root.mainloop()
