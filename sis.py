from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import os
import csv
from second_page import SecondPage
from tkinter import messagebox
from tkinter import Tk, Button, Frame

class Student:
    
    def __init__(self, root):
        self.root = root
        self.root.title("MSU-IIT STUDENT INFORMATION SYSTEM")
        self.root.geometry("1350x750+0+0")
        self.root.config(bg="#001F3F")
        self.data = dict()
        self.temp = dict()
        self.filename = "students.csv"
        
        self.Name = StringVar()
        self.StudID = StringVar()
        self.YearLevel = StringVar()
        self.Gender = StringVar()
        self.Course_Code = StringVar()
        self.Searchbar = StringVar()

        if not os.path.exists('students.csv'):
            with open('students.csv', mode='w') as csv_file:
                fieldnames = ["Student ID", "Name", "Gender", "Year Level", "Course Code"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
        else:
            with open('students.csv', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    self.data[row["Student ID"]] = {
                        'Name': row["Name"],
                        'Gender': row["Gender"],
                        'Year Level': row["Year Level"],
                        'Course Code': row["Course Code"]
                    }
            self.temp = self.data.copy()

        self.course_data = dict()
        if os.path.exists('course.csv'):
            with open('course.csv', newline='') as course_file:
                course_reader = csv.DictReader(course_file)
                headers = course_reader.fieldnames
                print(f"Headers in 'course.csv': {headers}")  # Debugging statement
                for course_row in course_reader:
                    self.course_data[course_row["course code"]] = course_row["course name"]

        self.create_widgets()
        self.DisplayStd()

    def Quit(self):
        Quit = tkinter.messagebox.askyesno("MSU-IIT SIS", "Are you sure you want to QUIT?")
        if Quit > 0:
            self.root.destroy()
            return
    def check_IDNo(self, idNo):
        with open(self.filename, "r") as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                if idNo == row["Student ID"]:
                    return True
        return False        
    def add_student(self):
        with open('students.csv', "a", newline="") as file:
            csvfile = csv.writer(file)
            if self.StudID.get() == "" or self.Name.get() == "" or self.YearLevel.get() == "" or self.Gender.get() == "" or self.Course_Code.get() == "":
                tkinter.messagebox.showinfo("MSU-IIT SIS", "Fill in the box.")
            if self.check_IDNo(self.StudID.get()):
                messagebox.showerror("Error", f"Student {self.StudID.get()} already exists.")
                return
            else:
                self.data[self.StudID.get()] = {'Name': self.Name.get(), 'Gender': self.Gender.get(), 'Year Level': self.YearLevel.get(), 'Course Code': self.Course_Code.get()}
                self.saveData()
                tkinter.messagebox.showinfo("MSU-IIT SIS", "Successfully added!")
                self.DisplayStd()
            self.ClearStd()

    def ClearStd(self):
        self.StudID.set("")
        self.Name.set("")
        self.YearLevel.set("")
        self.Gender.set("")
        self.Course_Code.set("")

    def DisplayStd(self):
        self.tree.delete(*self.tree.get_children())
        with open('students.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                IDNumber = row['Student ID']
                Name = row['Name']
                YearLevel = row['Year Level']
                CourseCode = row['Course Code']
                Gender = row['Gender']
                CourseName = self.course_data.get(CourseCode, "N/A")
                self.tree.insert("", END, values=(IDNumber, Name, Gender, YearLevel, CourseCode, CourseName))

    def delete_student(self):
        if self.tree.focus() == "":
            tkinter.messagebox.showerror("MSU-IIT SIS", "Select a student")
            return
        id_no = self.tree.item(self.tree.focus(), "values")[0]
        self.data.pop(id_no, None)
        self.saveData()
        self.tree.delete(self.tree.focus())
        tkinter.messagebox.showinfo("MSU-IIT SIS", "Oops! Record Deleted!")
            


        
    def edit_student(self):
        if self.tree.focus() == "":
            tkinter.messagebox.showerror("MSU-IIT SIS", "Select a student")
            return
        values = self.tree.item(self.tree.focus(), "values")
        self.StudID.set(values[0])
        self.Name.set(values[1])
        self.Gender.set(values[2])
        self.YearLevel.set(values[3])
        self.Course_Code.set(values[4])
       
    def update_student(self):
        with open('students.csv', "a", newline="") as file:
            csvfile = csv.writer(file)
            if self.StudID.get() == "" or self.Name.get() == "" or self.YearLevel.get() == "" or self.Gender.get() == "" or self.Course_Code.get() == "":
                tkinter.messagebox.showinfo("MSU-IIT SIS", "Select a student")
            else:
                self.data[self.StudID.get()] = {'Name': self.Name.get(), 'Gender': self.Gender.get(), 'Year Level': self.YearLevel.get(), 'Course Code': self.Course_Code.get()}
                self.saveData()
                tkinter.messagebox.showinfo("MSU-IIT SIS", "Successfully Updated")
            self.DisplayStd()
            self.ClearStd()

    def create_widgets(self):
        ManageFrame = Frame(self.root, bd=5, relief=RIDGE, bg="Sky Blue")
        ManageFrame.place(x=1080, y=260, width=660, height=400)

        title = Label(self.root, text="STUDENT INFORMATION SYSTEM", bd=4, relief=RIDGE, font=("Source code", 40, "bold"),
                      bg="Sky Blue", fg="#2B8180")
        title.pack(side=TOP)

        DetailFrame = Frame(self.root, bd=4, relief=RIDGE, bg="Sky Blue")
        DetailFrame.place(x=20, y=100, width=1030, height=560)

        ButtonFrame = Frame(self.root, bd=4, bg="Sky Blue", relief=RIDGE)
        ButtonFrame.place(x=1080, y=100, width=430, height=140)

        TableFrame = Frame(DetailFrame, bd=4, relief=RIDGE, bg='Sky Blue')
        TableFrame.place(x=10, y=10, width=1030, height=450)

        title = Label(ManageFrame, text="STUDENT INFORMATION", bg="#2B8180", fg="White", font=("Source code", 20, "bold"))
        title.grid(row=0, columnspan=2, pady=20)
        
        self.lblStdID = Label(ManageFrame, font=("Source code", 15, "bold"), text="ID Number:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblStdID.grid(row=1, column=0, padx=5, pady=5)
        self.txtStdID = Entry(ManageFrame, font=("Source code", 15, "bold"), textvariable=self.StudID, relief=GROOVE, width=27, fg="#2B8180")
        self.txtStdID.grid(row=1, column=1)

        self.lblname = Label(ManageFrame, font=("Source code", 15, "bold"), text="Name:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblname.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.txtname = Entry(ManageFrame, font=("Source code", 15, "bold"), textvariable=self.Name, relief=GROOVE, width=27, fg="#2B8180")
        self.txtname.grid(row=2, column=1)

        self.lblYearlevel = Label(ManageFrame, font=("Source code", 15, "bold"), text="Year Level:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblYearlevel.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.comboYearlevel = ttk.Combobox(ManageFrame, font=("Source code", 15, "bold"), state="readonly", width=27, textvariable=self.YearLevel, style="combostyleO.TCombobox")
        self.comboYearlevel['values'] = ("First Year", "Second Year", "Third Year", "Fourth Year")
        self.comboYearlevel.grid(row=3, column=1, padx=5, pady=5)

        self.lblgender = Label(ManageFrame, font=("Source code", 15, "bold"), text="Gender:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblgender.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.combogender = ttk.Combobox(ManageFrame, font=("Source code", 15, "bold"), state="readonly", width=27, textvariable=self.Gender, style="combostyleO.TCombobox")
        self.combogender['values'] = ("Male", "Female", "Others")
        self.combogender.grid(row=4, column=1, padx=5, pady=5)

        self.lblCourseCode = Label(ManageFrame, font=("Source code", 15, "bold"), text="Course Code:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblCourseCode.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.comboCourseCode = ttk.Combobox(ManageFrame, font=("Source code", 15, "bold"), state="readonly", width=27, textvariable=self.Course_Code, style="combostyleO.TCombobox")
        self.comboCourseCode['values'] = list(self.course_data.keys())
        self.comboCourseCode.grid(row=5, column=1, padx=5, pady=5)

        self.btnAddData = Button(ButtonFrame, text="Add", font=("Source code", 10, "bold"), bg="#2B8180", fg="black", height=2, width=12, bd=5, command=self.add_student)
        self.btnAddData.grid(row=0, column=0, padx=10, pady=10)
        
        self.btnDeleteData = Button(ButtonFrame, text="Delete", font=("Source code", 10, "bold"), bg="#2B8180", fg="black", height=2, width=12, bd=5, command=self.delete_student)
        self.btnDeleteData.grid(row=0, column=1, padx=10, pady=10)
        

# Create Entry widget for search input
        self.search_entry = Entry(self.root, font=("Arial", 14), bg="white", fg="black")
        self.search_entry.place(x=200, y=600, width=400)

# Create Button widget for search button
        self.btnSearchData = Button(self.root, text="Search", font=("Source code", 10, "bold"), bg="#2B8180", fg="black", height=2, width=12, bd=5, command=self.search_student)
        self.btnSearchData.place(x=90, y=590, width=100)


        
        self.save_button = Button(ButtonFrame, text="SAVE", font=("Source code", 10, "bold"), bg="#2B8180", fg="black", height=2, width=12, bd=5, command=self.save_changes)
        self.save_button.grid(row=0, column=2, padx=10, pady=10)
        


        self.btnEditData = Button(ButtonFrame, text="Edit", font=("Source code", 10, "bold"), bg="#2B8180", fg="black", height=2, width=12, bd=5, command=self.edit_student)
        self.btnEditData.grid(row=1, column=0, padx=10, pady=10)


        self.btnResetData = Button(ButtonFrame, text="Reset", font=("Source code", 10, "bold"), bg="#2B8180", fg="black", height=2, width=12, bd=5, command=self.ClearStd)
        self.btnResetData.grid(row=1, column=1, padx=10, pady=10)

        self.btnExit = Button(ButtonFrame, text="Exit", font=("Source code", 10, "bold"), bg="#2B8180", fg="black", height=2, width=12, bd=5, command=self.Quit)
        self.btnExit.grid(row=1, column=2, padx=10, pady=10)

        self.tree = ttk.Treeview(TableFrame, columns=("Student ID", "Name", "Gender", "Year Level", "Course Code", "Course Name"), show="headings")
        self.tree.heading("Student ID", text="Student ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Year Level", text="Year Level")
        self.tree.heading("Course Code", text="Course Code")
        self.tree.heading("Course Name", text="Course Name")
        self.tree['show'] = 'headings'
        self.tree.column("Student ID", width=70)
        self.tree.column("Name", width=100)
        self.tree.column("Gender", width=70)
        self.tree.column("Year Level", width=100)
        self.tree.column("Course Code", width=70)
        self.tree.column("Course Name", width=100)
        self.tree.pack(fill=BOTH, expand=1)
        
        self.refresh_button = Button(self.root, text="Refresh", font=("Source code", 8, "bold"), bg="#2B8180", fg="black", height=1, width=6, bd=5, command=self.refresh_data)
        self.refresh_button.place(x=20, y=20)
    
 # Add button to open second page
        self.btnOpenSecondPage = Button(self.root, text="Open Course Page", font=("Source code", 10, "bold"), bg="#2B8180", fg="black", height=2, width=18, bd=5, command=self.open_second_page)
        self.btnOpenSecondPage.place(x=1300, y=20)  # Adjust the position as needed
    
    def open_second_page(self):
        self.second_page = SecondPage(self.root)  # Create SecondPage instance within the root window

        
    def saveData(self):
        with open(self.filename, "w", newline="") as csvfile:
            fieldnames = ["Student ID", "Name", "Gender", "Year Level", "Course Code"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key, value in self.data.items():
                writer.writerow({
                    "Student ID": key,
                    "Name": value['Name'],
                    "Gender": value['Gender'],
                    "Year Level": value['Year Level'],
                    "Course Code": value['Course Code']
                })
    def refresh_data(self):
        # Update course data from the CSV file
        self.course_data.clear()
        if os.path.exists('course.csv'):
            with open('course.csv', newline='') as course_file:
                course_reader = csv.DictReader(course_file)
                for course_row in course_reader:
                    self.course_data[course_row["course code"]] = course_row["course name"]

        # Update Course Code combo box with refreshed data
        self.comboCourseCode['values'] = list(self.course_data.keys())
                
    def save_changes(self):
        if not self.tree.focus():
            messagebox.showwarning("Warning", "Please select a student to edit.")
            return

        edited_values = [
            self.StudID.get(),
            self.Name.get(),
            self.Gender.get(),
            self.YearLevel.get(),
            self.Course_Code.get()
        ]

        original_id = self.tree.item(self.tree.focus(), "values")[0]

        if edited_values[0] != original_id and self.check_IDNo(edited_values[0]):
            messagebox.showerror("Error", f"Student {edited_values[0]} already exists.")
            return

        # Update data dictionary with edited values
        self.data[original_id] = {
            'Name': edited_values[1],
            'Gender': edited_values[2],
            'Year Level': edited_values[3],
            'Course Code': edited_values[4]
        }

        # Save changes to CSV
        self.saveData()

        # Display updated student records
        self.DisplayStd()

        # Clear input fields
        self.ClearStd()
    def search_student(self):
        search_key = self.search_entry.get().strip().lower()


        if not search_key:
            messagebox.showwarning("Warning", "Please enter a keyword to search.")
            return

        for item in self.tree.selection():
            self.tree.selection_remove(item)

        first_match_item = None

        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values and any(search_key in value.lower() for value in values):
                self.tree.selection_add(item)
                if not first_match_item:
                    first_match_item = item
            else:
                self.tree.selection_remove(item)

        if first_match_item:
            self.tree.see(first_match_item)



if __name__ == "__main__":
    root = Tk()
    application = Student(root)
    root.mainloop()
