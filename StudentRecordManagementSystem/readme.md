# Admission Management System

A Tkinter-based GUI application for managing student admission records. This application uses a CSV file to store and retrieve data, allowing users to add, search, update, and display records. The interface is intuitive, with search and filter functionalities, making it easy to maintain and view student information.

---

## Features

- **Add New Records**: Enter details such as Date, Roll No, Name, Course, DOB, Contact, Gender, and Address.
- **Search Records**: Filter records by attributes like Roll No, Name, DOB, and Contact.
- **Update Records**: Edit selected records and update them in the CSV file.
- **Treeview Display**: Display all records in a Treeview with alternating row colors for readability.
- **Error Messaging**: Informative messages for successful updates and any issues encountered.
- **CSV Storage**: All records are saved to a `SData.csv` file for easy access and manipulation.

---

## Screenshots
<p align="center">
  <img src="https://github.com/user-attachments/assets/0b25e26f-9cce-46b6-b39f-df3590fe1cfa" alt="Home Page" width="80%">
</p>

---

## Usage

1. **Adding Records**: Enter all required fields in the input area and click "Save" to add a new record to the CSV file.
2. **Searching Records**:
   - Choose a search attribute from the "Search By" dropdown.
   - Enter a search term in the search field, and click "Search" to view matching records.
3. **Updating Records**:
   - Select a record from the displayed list, edit the fields, and click "Update" to save changes. 
   - After updating, the "Update" button disables automatically.
4. **Clear**: Clears all input fields, resetting the form.

---

## Dependencies

- **Tkinter**: Built-in Python library for GUI development.
- **pandas**: For reading, writing, and manipulating the CSV data.
- **datetime**: For managing date formats in records.
- **ttk**: For themed Tkinter widgets.

---

## File Storage

- **`SData.csv`**: The CSV file where all records are stored. Make sure this file is present in the root directory or created on the first run.

---

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your improvements.

---
