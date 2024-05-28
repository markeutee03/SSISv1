from tkinter import *
from tkinter import ttk
import tkinter.ttk as ttk
from tkinter import messagebox
import csv
from tkinter import Tk, Toplevel, Button  # Import destroy



class SecondPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Information System")
        self.root.geometry("1600x900")
        self.create_course_widgets()
        self.current_frame = None  # To keep track of the current frame



        
        self.create_second_page()
    def create_course_widgets(self):
        self.csv_filename = "course.csv"
        self.fields = ["courseCode", "courseName"]

    def create_second_page(self):
        self.second_page_frame = Frame(self.root, bd=5, relief=RIDGE, bg="#408181")
        self.second_page_frame.pack(fill=BOTH, expand=True)

        title = Label(self.second_page_frame, text="COURSE PAGE", bd=4, relief=RIDGE, font=("Source code", 40, "bold"),
                      bg="#142b39", fg="White")
        title.pack(side=TOP)

        self.detail_frame = Frame(self.second_page_frame, bd=4, relief=RIDGE, bg="Sky Blue")
        self.detail_frame.place(x=20, y=150, width=780, height=420)

        # Add widgets for the second page
        lblInfo = Button(self.second_page_frame, text="LIST OF COURSES", font=("Source code", 20, "bold"), bg="#142b39", fg="White")
        lblInfo.place(x=275, y=90)

        # Frame for course entry and search
        CourseFrame = Frame(self.second_page_frame, bd=4, bg="Sky Blue", relief=RIDGE)
        CourseFrame.place(x=870, y=150, width=630, height=250)

        self.coursecode_label = Label(CourseFrame, text="Course Code:", font=("Arial", 14, "bold"), bg="#142b39", fg="White")
        self.coursecode_label.place(x=20, y=20)
        self.coursecode_entries = Entry(CourseFrame, font=("Arial", 14), bg="white", fg="black")
        self.coursecode_entries.place(x=170, y=20, width=180)

        self.coursetitle_label = Label(CourseFrame, text="Course Title:", font=("Arial", 14, "bold"), bg="#142b39", fg="White")
        self.coursetitle_label.place(x=20, y=70)
        self.coursetitle_entries = Entry(CourseFrame, font=("Arial", 14), bg="white", fg="black")
        self.coursetitle_entries.place(x=170, y=70, width=400)

        # Search frame within the CourseFrame
        SearchFrame = Frame(CourseFrame, bd=4, bg="Sky Blue", relief=RIDGE)
        SearchFrame.place(x=20, y=120, width=590, height=100)

        self.search_entry = Entry(SearchFrame, font=("Arial", 14), bg="white", fg="black")
        self.search_entry.place(x=150, y=20, width=300)

        self.btnSearchData = Button(SearchFrame, text="SEARCH", font=("Source code", 13, "bold"), bg="#142b39", fg="white", height=1, width=12, bd=5, command=self.search_course)
        self.btnSearchData.place(x=20, y=15, width=100)
        '''
        # Add a button to switch back to the main page
        self.btnSwitchToMainPage = Button(self.second_page_frame, text="GO BACK", font=("Source code", 10, "bold"), bg="#142b39", fg="White", height=2, width=12, bd=5, command=self.return_to_main_page)
        self.btnSwitchToMainPage.pack(pady=20)
        '''
        #BUTTONS FOR CRUDL
        ButtonFrame = Frame(self.second_page_frame, bd=4, bg="Sky Blue", relief=RIDGE)
        ButtonFrame.place(x=870, y=420, width=630, height=140)  # Adjusted position and dimensions

        
        # Add buttons to ButtonFrame
        self.add_button = Button(ButtonFrame, text="ADD", font=("Source code", 10, "bold"), bg="#142b39", fg="White", command=self.add_course)
        self.add_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        btn2 = Button(ButtonFrame, text="UPDATE", font=("Source code", 10, "bold"), bg="#142b39", fg="White", command=self.edit_course)
        btn2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        btn3 = Button(ButtonFrame, text="DELETE", font=("Source code", 10, "bold"), bg="#142b39", fg="White", command=self.delete_course)
        btn3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        btn4 = Button(ButtonFrame, text="SEARCH", font=("Source code", 10, "bold"), bg="#142b39", fg="White", command=self.search_course)
        btn4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Add SAVE and GO BACK buttons
        btn5 = Button(ButtonFrame, text="SAVE", font=("Source code", 10, "bold"), bg="#142b39", fg="White", command=self.save_changes)
        btn5.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        btn6 = Button(ButtonFrame, text="GO BACK", font=("Source code", 10, "bold"), bg="#142b39", fg="White", command=self.return_to_main_page)
        btn6.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Configure grid options to make buttons fill the frame
        ButtonFrame.grid_columnconfigure(0, weight=1)
        ButtonFrame.grid_columnconfigure(1, weight=1)
        ButtonFrame.grid_columnconfigure(2, weight=1)
        ButtonFrame.grid_rowconfigure(0, weight=1)
        ButtonFrame.grid_rowconfigure(1, weight=1)

        # def create_tree_view(self):
        self.tree = ttk.Treeview(self.detail_frame, columns=("Course Code", "Course Name"), show="headings")
        self.tree.heading("Course Code", text="Course Code")
        self.tree.heading("Course Name", text="Course Name")
        self.tree.column("Course Name", width=200)
        self.tree.column("Course Name", width=400)
        #self.tree.place(x=200, y=400, width=700, height=250)

        # Add vertical scrollbar
        vsb = ttk.Scrollbar(self.detail_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        self.tree.pack(fill="both", expand=True)

        # Load courses into the Treev
        self.load_courses()
        self.selected_item = None

        
        
    def return_to_main_page(self):
        # Destroy the current frame (second page)
        self.second_page_frame.pack_forget()
        self.root

    def edit_course(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a course to edit.")
            return

        # Store the selected item for later use
        self.selected_item = selected_item

        # Extract course information from the selected item
        course_values = self.tree.item(selected_item, "values")
        if not course_values:
            messagebox.showwarning("Warning", "Selected item does not contain course information.")
            return

        # Display course information in entry fields for editing
        self.coursetitle_entries.delete(0, END)  # Clear the entry field before inserting new text

        self.coursecode_entries.insert(0, course_values[0])

        self.coursetitle_entries.delete(0, END)
        self.coursetitle_entries.insert(0, course_values[1])

    def clear_entry_fields(self):
        self.coursecode_entries.delete(0, "end")
        self.coursetitle_entries.delete(0, "end")

    def cancel_edit(self):
        self.selected_item = None
        self.clear_entry_fields()
        self.coursecode_entries.delete(0, "end")
        self.coursetitle_entries.delete(0, "end")

    def save_changes(self):
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select a course to edit.")
            return

        # Retrieve edited values from entry fields
        edited_course_code = self.coursecode_entries.get()
        edited_course_title = self.coursetitle_entries.get()

        # Check if any field is empty
        if edited_course_code == '' or edited_course_title == '':
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        selected_course_code = self.tree.item(self.selected_item, "values")[0]

        # Update Treeview with the edited values
        self.tree.item(self.selected_item, values=(edited_course_code, edited_course_title))

        # Update CSV file with the edited values
        self.update_csv(selected_course_code, edited_course_code, edited_course_title)

        self.selected_item = None

        # Clear entry fields
        self.clear_entry_fields()

        messagebox.showinfo("Success", "Changes saved successfully!")

    def update_csv(self, selected_course_code, edited_course_code, edited_course_title):
        data = []
        with open(self.csv_filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)

        for row in data:
            if row[0] == selected_course_code:
                row[0] = edited_course_code
                row[1] = edited_course_title
                break

        # Write the updated data back to the CSV file
        with open(self.csv_filename, "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(data)

    def load_courses(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load courses from CSV file
        with open(self.csv_filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                self.tree.insert("", "end", values=(row[0], row[1]))

    def add_course(self):
        values = [self.coursecode_entries.get(), self.coursetitle_entries.get()]

        # Check if any field is empty
        if any(value == '' for value in values):
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        # Check if course code already exists
        course_code = values[0]
        if self.check_course(course_code):
            messagebox.showerror("Error", f"Course {course_code} already exists.")
            return

        # Write to CSV file
        with open(self.csv_filename, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(values)

        # Update Treeview
        self.tree.insert("", "end", values=values)

        # Clear entry fields
        self.coursecode_entries.delete(0, "end")
        self.coursetitle_entries.delete(0, "end")

        messagebox.showinfo("Success", "Course added successfully!")

    def delete_course(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a course to delete.")
            return

        course_values = self.tree.item(selected_item, "values")
        if not course_values:
            messagebox.showwarning("Warning", "Selected item does not contain course information.")
            return

        course_code = course_values[0]
        self.tree.delete(selected_item)

        self.delete_course_from_csv(course_code)

        messagebox.showinfo("Success", f"Course {course_code} deleted successfully!")

    def check_course(self, course_code):
        with open(self.csv_filename, "r") as csvfile:
            csvreader = csv.DictReader(csvfile, fieldnames=self.fields)
            for row in csvreader:
                if course_code.lower() == str(row["courseCode"]).lower():
                    return True
        return False

    def delete_course_from_csv(self, course_code):
        data = []
        with open(self.csv_filename, "r") as csvfile:
            csvreader = csv.DictReader(csvfile, fieldnames=self.fields)
            for row in csvreader:
                if row["courseCode"].lower() != course_code.lower():
                    data.append(row)

        # Write the data back to the CSV file
        with open(self.csv_filename, "w", newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=self.fields)
            csvwriter.writerows(data)

        # Update corresponding course code to "N/A" in the student CSV file
        student_data = []
        with open("students.csv", "r") as student_file:
            student_reader = csv.reader(student_file)
            for student_row in student_reader:
                if student_row[3] == course_code:  # If the student's course code matches the deleted course code
                    student_row[3] = "N/A"  # Set course code to "N/A"
                student_data.append(student_row)

        # Write the updated student data back to the CSV file
        with open("students.csv", "w", newline='') as student_file:
            student_writer = csv.writer(student_file)
            student_writer.writerows(student_data)

    def search_course(self, event=None):
        keyword = self.search_entry.get().lower()

        if not keyword.strip():
            messagebox.showwarning("Warning", "Please enter a keyword to search.")
            return

        # Clear previous selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)

        # Highlight rows matching the search keyword
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values and any(keyword in value.lower() for value in values):
                self.tree.selection_add(item)
    

if __name__ == "__main__":
    root = Tk()
    app = SecondPage(root)
    root.mainloop()
