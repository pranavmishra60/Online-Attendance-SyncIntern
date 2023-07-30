import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date
from PIL import Image, ImageTk

class AttendanceSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Attendance Monitoring System")
        self.geometry("400x600")

         # Set the background image
        self.background_image = Image.open("attendance.png") 
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0,relwidth=1,relheight=1)

        self.students = ["Akash", "Arohi", "Sakshi", "Sejal"]  
        self.attendance_data = {}  # To store attendance data

        # Create or connect to the database
        self.conn = sqlite3.connect("attendance.db")
        self.create_table()

        self.create_widgets()

    def create_table(self):
        # Create a table to store attendance data if it doesn't exist
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS Attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            ''')

    def create_widgets(self):
        self.label = tk.Label(self, text="Select Student:")
        self.label.pack(pady=10)

        # Dropdown to select students
        self.student_var = tk.StringVar(self)
        self.student_var.set(self.students[0])  # Set the default value
        self.student_dropdown = tk.OptionMenu(self, self.student_var, *self.students)
        self.student_dropdown.pack()

        # Mark attendance button
        self.mark_button = tk.Button(self, text="Mark Attendance", command=self.mark_attendance)
        self.mark_button.pack(pady=20)

    def mark_attendance(self):
        selected_student = self.student_var.get()
        today = date.today().strftime("%d/%m/%Y")
        self.attendance_data[selected_student] = today

        # Update attendance in the database
        self.update_attendance_db(selected_student, today)

        messagebox.showinfo("Attendance Marked", f"Attendance marked for {selected_student} on {today}")

    def update_attendance_db(self, student, date):
        with self.conn:
            self.conn.execute("INSERT INTO Attendance (student_name, date) VALUES (?, ?)", (student, date))

if __name__ == "__main__":
    app = AttendanceSystem()
    app.mainloop()
