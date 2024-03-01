from tkinter import *
from tkinter import ttk
import tkinter.ttk as ttk
import tkinter.messagebox
import os 
import csv

class Student:
    
    def __init__ (self,root):
        self.root = root
        self.root.title("MSU-IIT STUDENT INFORMATION SYSTEM")
        self.root.geometry("1350x750+0+0")
        self.root.config(bg="#001F3F")
        self.data = dict()
        self.temp = dict()
        self.filename = "students.csv"
        
        
        Name = StringVar()
        StudID = StringVar()
        YearLevel = StringVar()
        Gender = StringVar()
        Course_Code = StringVar()
        Searchbar = StringVar()
        Course_Code = StringVar()

        
        if not os.path.exists('students.csv'):
            with open('students.csv', mode='w') as csv_file:
                fieldnames = ["Student ID", "Name","Gender", "Year Level", "Course Code"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
        
        else:
            with open('students.csv', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    self.data[row["Student ID"]] = {'Name': row["Name"], 'Gender': row["Gender"],'Year Level': row["Year Level"], 'Course Code': row["Course Code"]}
            self.temp = self.data.copy()

    # To open data for course    
        self.course_data = dict()
        if os.path.exists('course.csv'):
            with open('course.csv', newline='') as course_file:
                course_reader = csv.DictReader(course_file)
                for course_row in course_reader:
                    self.course_data[course_row["course code"]] = course_row["course name"]
         
        #=============================================================FUNCTIONS================================================================#
        
        def Quit():
            Quit = tkinter.messagebox.askyesno("MSU-IIT SIS","Are you sure you want to QUIT?")
            if Quit > 0:
                root.destroy()
                return
            
        def addStd():
            with open('students.csv', "a", newline="") as file:
                csvfile = csv.writer(file)
                if StudID.get()=="" or Name.get()=="" or YearLevel.get()=="" or Gender.get()=="" or Course_Code.get()=="":
                    tkinter.messagebox.showinfo("MSU-IIT SIS","Fill in the box.")
                else:
                    self.data[StudID.get()] = {'Name': Name.get(),  'Gender': Gender.get(),'Year Level': YearLevel.get(), 'Course Code': Course_Code.get()}
                    self.saveData()
                    tkinter.messagebox.showinfo("MSU-IIT SIS", "Successfully added!")
                    DisplayStd()
                ClearStd()

                    
        def ClearStd():
            StudID.set("")
            Name.set("")
            YearLevel.set("")
            Gender.set("")
            Course_Code.set("")
        
        def DisplayStd():
            tree.delete(*tree.get_children())
            with open('students.csv') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    IDNumber=row['Student ID']
                    Name=row['Name']
                    YearLevel=row['Year Level']
                    CourseCode=row['Course Code']
                    Gender=row['Gender']
                    # Get course name from the loaded course data
                    CourseName = self.course_data.get(CourseCode, "N/A")
                    tree.insert("",END, values=(IDNumber,Name , Gender, YearLevel, CourseCode, CourseName))
                    
        def deleteStd():
            if tree.focus()=="":
                tkinter.messagebox.showerror("MSU-IIT SIS","Select a student")
                return
            id_no = tree.item(tree.focus(),"values")[0]
            self.data.pop(id_no, None)
            self.saveData()
            tree.delete(tree.focus())
            tkinter.messagebox.showinfo("MSU-IIT SIS","Oops! Record Deleted!")
            
        def searchStd():
            if self.Search.get() in self.data:
                vals = list(self.data[self.Search.get()].values())
                tree.delete(*tree.get_children())
                tree.insert("",END, values =(self.Search.get(), vals[0],vals[1],vals[2],vals[3],vals[4],vals[5]))
            elif self.Search.get() =="":
                DisplayStd()
            else:
                tkinter.messagebox.showerror("MSU-IIT SIS", "Oops! Student not found")
                return
        
        def editStd():
            if tree.focus() == "":
                tkinter.messagebox.showerror("MSU-IIT SIS", "Select a student")
                return
            values = tree.item(tree.focus(), "values")
            StudID.set(values[0])
            Name.set(values[1])
            Gender.set(values[2])
            YearLevel.set(values[3])
            Course_Code.set(values[4])
       
        def updateStd():
            with open('students.csv', "a", newline="") as file:
                csvfile = csv.writer(file)
                if StudID.get()=="" or Name.get()==""  or YearLevel.get()=="" or Gender.get()=="" or Course_Code.get()=="":
                    tkinter.messagebox.showinfo("MSU-IIT SIS","Select a student")
                else:
                    self.data[StudID.get()] = {'Name': Name.get(), 'Gender': Gender.get(),'Year Level': YearLevel.get(), 'Course Code': Course_Code.get()}
                    self.saveData()
                    tkinter.messagebox.showinfo("MSU-IIT SIS", "Successfully Updated")
                DisplayStd()
                ClearStd()     

        #============================================================FRAMES=====================================================================#


        ManageFrame = Frame(self.root, bd=5, relief=RIDGE, bg="Sky Blue")
        ManageFrame.place(x=1080, y=260, width=660, height=400)

        title = Label(self.root, text="STUDENT INFORMATION SYSTEM", bd=4, relief=RIDGE, font=("Source code", 40, "bold"),
              bg="Sky Blue", fg="#2B8180")
        title.pack(side=TOP)

        DetailFrame = Frame(self.root, bd=4, relief=RIDGE, bg="Sky Blue")
        DetailFrame.place(x=20, y=100, width=1030, height=560)

        ButtonFrame = Frame(self.root, bd=4, bg="Sky Blue", relief=RIDGE)
        ButtonFrame.place(x=1080, y=100, width=450, height=140)  # Adjusted the x position and width

        TableFrame = Frame(DetailFrame, bd=4, relief=RIDGE, bg='Sky Blue')
        TableFrame.place(x=10, y=10, width=1030, height=450)  # Adjusted the width of TableFrame        
        #============================================================LABELS AND ENTRY WIDGETS====================================================#

        title=Label(ManageFrame, text="STUDENT INFORMATION",bg="#2B8180", fg="White", font=("Source code",20,"bold"))
        title.grid(row=0, columnspan=2, pady=20)
        
        self.lblStdID = Label(ManageFrame, font=("Source code",15,"bold"),text="ID Number:", padx=2, pady=2, bg="#2B8180", fg="black",  height=1, width=11)
        self.lblStdID.grid(row=1, column=0,padx=5,pady=5)
        self.txtStdID = Entry(ManageFrame, font=("Source code",15,"bold"),textvariable=StudID, relief=GROOVE, width=27, fg="#2B8180")
        self.txtStdID.grid(row=1, column=1)
        

        self.lblname = Label(ManageFrame,font=("Source code",15,"bold"),text="Name:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblname.grid(row=2, column=0,padx=5,pady=5, sticky="w")        
        self.txtname = Entry(ManageFrame, font=("Source code",15,"bold"),textvariable=Name, relief=GROOVE,width=27, fg="#2B8180")
        self.txtname.grid(row=2, column=1)
        
        


        self.lblYearlevel = Label(ManageFrame, font=("Source code",15,"bold"),text="Year Level:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblYearlevel.grid(row=3, column=0,padx=5,pady=5, sticky="w")
        ttk.Style().layout('combostyleO.TCombobox')
        ttk.Style().configure('combostyleO.TCombobox', selectforeground='#2B8180', selectbackground='grey',  foreground='#2B8180')
        self.comboYearlevel=ttk.Combobox(ManageFrame,font=("Source code",15,"bold"), state="readonly",width=26, textvariable=YearLevel, style="combostyleO.TCombobox")
        self.comboYearlevel['values']=("First Year","Second Year", "Third Year", "Fourth Year")
        self.comboYearlevel.grid(row=3,column=1)


        self.lblGender = Label(ManageFrame, font=("Source code", 15, "bold"), text="Gender:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblGender.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        ttk.Style().layout('combostyleO.TCombobox')
        ttk.Style().configure('combostyleO.TCombobox', selectforeground='#2B8180', selectbackground='grey', foreground='#2B8180')

        self.comboGender = ttk.Combobox(ManageFrame, font=("Source code", 15, "bold"), state="readonly", width=26, textvariable=Gender, style="combostyleO.TCombobox")
        self.comboGender['values'] = ("Male", "Female")
        self.comboGender.grid(row=4, column=1, padx=5, pady=5, sticky="w")  # Adjusted the column to 1 and added padx, pady, and sticky


        self.lblCourse_Code = Label(ManageFrame, font=("Source code",15,"bold"),text="Course Code:", padx=2, pady=2, bg="#2B8180", fg="black", height=1, width=11)
        self.lblCourse_Code.grid(row=5, column=0,padx=5,pady=5, sticky="w")
        self.txtCourse_Code = Entry(ManageFrame, font=("Source code",15,"bold"),textvariable=Course_Code, relief=GROOVE,width=27, fg="#2B8180")
        self.txtCourse_Code.grid(row=5, column=1)

        #============================================================BUTTON WIDGET====================================================#

        self.btnAddData = Button(ButtonFrame,text="Add", font=("Source code",10,"bold"),bg="#2B8180", fg="black", height=2, width=12, bd=5,command=addStd)
        self.btnAddData.grid(row=0, column=0, padx=15, pady=15)
        self.btnAddData.place(x=20,y=10)

        self.btnUpdateData = Button(ButtonFrame, text="Update", font=("Source code",10,"bold"),bg="#2B8180", fg="black", height=2, width=12, bd=5, command=updateStd)
        self.btnUpdateData.grid(row=0, column=2, padx=15, pady=15)
        self.btnUpdateData.place(x=20,y=70)

        self.btnClearData = Button(ButtonFrame, text="Clear", font=("Source code",10,"bold"),bg="#2B8180", fg="black", height=2, width=12, bd=5,command=ClearStd)
        self.btnClearData.grid(row=1, column=0,padx=15, pady=15)
        self.btnClearData.place(x=180,y=10)

        self.btnDeleteData = Button(ButtonFrame, text="Delete", font=("Source code",10,"bold"),bg="#2B8180", fg="black", height=2, width=12, bd=5, command=deleteStd)
        self.btnDeleteData.grid(row=1, column=1,padx=15, pady=15)
        self.btnDeleteData.place(x=180,y=70)

        self.btnExit = Button(ButtonFrame, text="Exit", font=("Source code",10,"bold"),bg="#2B8180", fg="black", height=2, width=12, bd=5, command=Quit)
        self.btnExit.grid(row=1, column=2,padx=15, pady=15)
        self.btnExit.place(x=330,y=70)

        self.btnDisplay = Button(ButtonFrame, text="Display", font=("Source code",10,"bold"),bg="#2B8180", fg="black", height=2, width=12, bd=5, command=DisplayStd)
        self.btnDisplay.grid(row=1, column=2,padx=15, pady=15)
        self.btnDisplay.place(x=330,y=10)

        #============================================================DETAIL FRAME====================================================#
        
        self.lblSearch = Button(DetailFrame, font=('Source code',15,'bold'),text="Search by ID:", padx=2, pady=2, bg="#008080", fg="white", height=1, width=12)
        self.lblSearch.grid(row=1, column=0,padx=2,pady=2, sticky="w")
        self.lblSearch.place(x=50,y=480)
        
        self.Search = Entry(DetailFrame, font=('Source code',15,'normal'),textvariable=Searchbar, relief=GROOVE, width=25, fg = "#008080")
        self.Search.grid(row=1, column=1)
        self.Search.place(x=220,y=488)

        self.btnSearch = Button(DetailFrame, text="Search",font=("Source code",12,"bold"),bg="#008080", fg="white", height=1, width=12, bd=4, command=searchStd)
        self.btnSearch.grid(row=1, column=2,padx=15, pady=15)
        self.btnSearch.place(x=520,y=480)
        
        self.btnDisplayData = Button(DetailFrame, text="Select", font=("Source code",12,"bold"),bg="#008080", fg="white", height=1, width=12, bd=4,command=editStd)
        self.btnDisplayData.grid(row=1, column=3, padx=15, pady=15)
        self.btnDisplayData.place(x=670,y=480)
        


        scroll_y=Scrollbar(TableFrame, orient=VERTICAL)

        tree = ttk.Treeview(TableFrame, height=10, columns=("StudID","Name","Gender","YearLevel","Course Code", "Course Name"), yscrollcommand=scroll_y.set)
        
        scroll_y.pack(side=LEFT, fill=Y)

        tree.heading("StudID", text="Student ID")
        tree.heading("Name", text="Name")
        tree.heading("Gender", text="Gender")
        tree.heading("YearLevel", text="Year Level")
        tree.heading("Course Code", text="Course Code")  # New column
        tree.heading("Course Name", text="Course Name")  # New column
        tree['show'] = 'headings'
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Source code",14,"bold"),foreground="#001F3F")
        style.configure("Treeview",font=("Source code",12,"normal"))
        style.map('Treeview', background=[('selected', 'grey')], foreground=[('selected', '#001F3F')])
        
        tree.column("StudID", width=110,anchor='center')
        tree.column("Name", width=110,anchor='center')
        tree.column("Gender", width=90,anchor='center')
        tree.column("YearLevel", width=120,anchor='center')
        tree.column("Course Code", width=100,anchor='center')
        tree.column("Course Name", width=100,anchor='center')
        tree.pack(fill=BOTH,expand=1,anchor='center')
        
        #===========================================================================================================================================================#
    def saveData(self):
        temps = []
        with open('students.csv', "w", newline ='') as update:
            fieldnames = ["Student ID","Name","Gender","Year Level","Course Code"]
            writer = csv.DictWriter(update, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            for id, val in self.data.items():
                temp ={"Student ID": id}
                for key, value in val.items():
                    temp[key] = value
                temps.append(temp)
            writer.writerows(temps)
            

if __name__ =='__main__':
    root = Tk()
    application = Student(root)
    root.mainloop()