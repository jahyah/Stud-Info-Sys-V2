import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.messagebox
import csv
import os
import sqlite3


LARGE_FONT= ("Verdana", 20)

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)
        
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Student, Course):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Student)

    def show_frame(self, page_number):

        frame = self.frames[page_number]
        frame.tkraise()


class Course(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Student Information System")
                        
        leftcolor = tk.Label(self,height = 5,width=250, bg= "#1B4965")
        leftcolor.place(x=0,y=0)
        
        label2 = tk.Label(self, text="Student Information System", font=LARGE_FONT, bg= "#1B4965", fg= "snow")
        label2.place(x=15,y=10)
               
        Course_Code = StringVar()
        Course_Name = StringVar()
        SearchBar_Var = StringVar()
        
        def connectCourse():
            conn = sqlite3.connect("StudentDatabase.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses (Course_Code TEXT PRIMARY KEY, Course_Name TEXT)") 
            conn.commit() 
            conn.close()
            
        def addCourse():
            conn = sqlite3.connect("StudentDatabase.db")
            c = conn.cursor()         
            #Insert Table
            c.execute("INSERT INTO courses(Course_Code,Course_Name) VALUES (?,?)",\
                      (Course_Code.get(),Course_Name.get()))        
            conn.commit()           
            conn.close()
            Course_Code.set('')
            Course_Name.set('') 
            tkinter.messagebox.showinfo("Student Information System", "Course Recorded Successfully")
            displayCourse()
              
        def displayCourse():
            self.courselist.delete(*self.courselist.get_children())
            conn = sqlite3.connect("StudentDatabase.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                self.courselist.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
        
        def updateCourse():
            for selected in self.courselist.selection():
                conn = sqlite3.connect("StudentDatabase.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET Course_Code=?, Course_Name=? WHERE Course_Code=?", \
                            (Course_Code.get(),Course_Name.get(), self.courselist.set(selected, '#1')))                       
                conn.commit()
                tkinter.messagebox.showinfo("Student Information System", "Course Updated Successfully")
                displayCourse()
                conn.close()
                
        def editCourse():
            x = self.courselist.focus()
            if x == "":
                tkinter.messagebox.showerror("Student Information System", "Please select a record from the table.")
                return
            values = self.courselist.item(x, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
                    
        def deleteCourse(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("SSIS", "Do you want to permanently delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("StudentDatabase.db")
                    cur = con.cursor()
                    x = self.courselist.selection()[0]
                    id_no = self.courselist.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM courses WHERE Course_Code = ?",(id_no,))                   
                    con.commit()
                    self.courselist.delete(x)
                    tkinter.messagebox.askyesno("Student Information System", "Course Deleted Successfully")
                    displayCourse()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("Student Information System", "Students are still enrolled in this course")
                
        def searchCourse():
            Course_Code = SearchBar_Var.get()                
            con = sqlite3.connect("StudentDatabase.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM courses WHERE Course_Code = ?",(Course_Code,))
            con.commit()
            self.courselist.delete(*self.courselist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.courselist.insert("", tk.END, text=row[0], values=row[0:])
            con.close()
 
        def Refresh():
            pass
            displayCourse()
        
        def clear():
            Course_Code.set('')
            Course_Name.set('') 
        

        button2 = tk.Button(self, text="Course",font=("Verdana",10,"bold"),bd=0,
                            width = 10,
                            bg= "#1B4965",
                            fg="snow",
                            command=lambda: controller.show_frame(Course))
        button2.place(x=200,y=50)
        button2.config(cursor= "hand2")
        
        button3 = tk.Button(self, text="Students",font=("Verdana",10,"bold"),bd=0,
                            width = 10,
                            bg="#1B4965",
                            fg="snow",
                            command=lambda: controller.show_frame(Student))
        button3.place(x=100,y=50)
        button3.config(cursor= "hand2")

        ## Label and Entry
        
        self.lblCourseCode = Label(self, font=("Poppins", 12, "bold"), text="COURSE CODE:*", padx=5, pady=5)
        self.lblCourseCode.place(x=25,y=144)
        self.txtCourseCode = Entry(self, font=("Poppins", 13), textvariable=Course_Code, width=35)
        self.txtCourseCode.place(x=170,y=150)
        #self.txtStudentID.insert(0,"     -")

        self.lblCourseName = Label(self, font=("Poppins", 12,"bold"), text="COURSE NAME:*", padx=5, pady=5)
        self.lblCourseName.place(x=25,y=205)
        self.txtCourseName = Entry(self, font=("Poppins", 13), textvariable=Course_Name, width=35)
        self.txtCourseName.place(x=170,y=210)
        
        self.SearchBar = Entry(self, font=("Poppins", 11), textvariable=SearchBar_Var, width=29)
        self.SearchBar.place(x=810,y=110)
        self.SearchBar.insert(0,'Search course code here')
        

        ##==================================================Treeview========================================##
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1160,y=140,height=430)

        self.courselist = ttk.Treeview(self,
                                        columns=("Course Code","Course Name"),
                                        height = 20,
                                        yscrollcommand=scrollbar.set)

        self.courselist.heading("Course Code", text="Course Code", anchor=W)
        self.courselist.heading("Course Name", text="Course Name",anchor=W)
        self.courselist['show'] = 'headings'

        self.courselist.column("Course Code", width=200, anchor=W, stretch=False)
        self.courselist.column("Course Name", width=430, stretch=False)


        self.courselist.place(x=520,y=140)
        scrollbar.config(command=self.courselist.yview)
            
        ##===================================================Buttons=======================================##

        self.btnAddID = Button(self, text="ADD", font=('Poppins', 11), height=1, width=10, bd=1,
                               bg="#1B4965", fg="snow", command=addCourse)
        self.btnAddID.place(x=200,y=260)
        
        self.btnUpdate = Button(self, text="UPDATE", font=('Poppins', 11), height=1, width=10, bd=1,
                                bg="#1B4965", fg="snow", command=updateCourse) 
        self.btnUpdate.place(x=350,y=260)
        
        self.btnClear = Button(self, text="CLEAR", font=('Poppins', 11), height=1, width=10, bd=1,
                               bg="#1B4965", fg="snow", command=clear)
        self.btnClear.place(x=200,y=310)
        
        self.btnDelete = Button(self, text="DELETE", font=('Poppins', 11), height=1, width=10, bd=1,
                                bg="#1B4965", fg="snow", command=deleteCourse)
        self.btnDelete.place(x=350,y=310)
        
        self.btnSelect = Button(self, text="Select", font=('Poppins', 10), height=1, width=11,
                              bg="#1B4965", fg="snow", command=editCourse)
        self.btnSelect.place(x=520,y=103)
        
        self.btnSearch = Button(self, text="Search", font=('Poppins', 10), height=1, width=10,
                                bg="#1B4965", fg="snow", command=searchCourse)
        self.btnSearch.place(x=1062,y=103)
        
        self.btnRefresh = Button(self, text="Show All", font=('Poppins', 10), height=1, width=11,
                              bg="#1B4965", fg="snow", command=Refresh)
        self.btnRefresh.place(x=630,y=103)
        
        connectCourse()
        displayCourse()

class Student(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("Student Information System")        
        
        leftcolor = tk.Label(self,height = 5,width=250, bg= "#1B4965")
        leftcolor.place(x=0,y=0)
        
        label2 = tk.Label(self, text="Student Information System", font=LARGE_FONT, bg= "#1B4965", fg= "snow")
        label2.place(x=15,y=10)
        
        
        

        ##=============================================WindowBtn=====================================##
        button2 = tk.Button(self, text="Course",font=("Verdana",10,"bold"),bd=0,
                            width = 10,
                            bg= "#1B4965",
                            fg="snow",
                            command=lambda: controller.show_frame(Course))
        button2.place(x=200,y=50)
        button2.config(cursor= "hand2")
        
        button3 = tk.Button(self, text="Students",font=("Verdana",10,"bold"),bd=0,
                            width = 10,
                            bg="#1B4965",
                            fg="snow",
                            command=lambda: controller.show_frame(Student))
        button3.place(x=100,y=50)
        button3.config(cursor= "hand2")
        
        
        ##=====================================================Functions================================##
        Student_ID = StringVar()
        Student_Name = StringVar()       
        Student_YearLevel = StringVar()
        Student_Gender = StringVar()
        Course_Code = StringVar()
        SearchBar_Var = StringVar()
        
       
        def connect():
            conn = sqlite3.connect("StudentDatabase.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS studentdatabase (Student_ID TEXT PRIMARY KEY, Student_Name TEXT, Course_Code TEXT, \
                      Student_YearLevel TEXT, Student_Gender TEXT, \
                      FOREIGN KEY(Course_Code) REFERENCES courses(Course_Code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def addData():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("Student Information System", "Please fill in the box with *")
            else:  
                ID = Student_ID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("Student Information System", "Invalid ID\nID Number Format:YYYY-NNNN")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("Student Information System", "Invalid ID\nIID Number Format:YYYY-NNNN")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("Student Information System", "Invalid ID\nIID Number Format:YYYY-NNNN")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("Student Information System", "Invalid ID")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("Student Information System", "Invalid ID")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("StudentDatabase.db")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                    c.execute("INSERT INTO studentdatabase(Student_ID,Student_Name,Course_Code,Student_YearLevel,Student_Gender) VALUES (?,?,?,?,?)",\
                                                          (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get()))                                       
                                                                       
                                    tkinter.messagebox.showinfo("Student Information System", "Student Recorded Successfully")
                                    conn.commit() 
                                    clear()
                                    displayData()
                                    conn.close()
                                except:
                                    tkinter.messagebox.showerror("Student Information System", "Course Unavailable")
                    else:
                        tkinter.messagebox.showerror("Student Information System", "Invalid ID")
                else:
                    tkinter.messagebox.showerror("Student Information System", "Invalid ID")
                 
        def updateData():
            for selected in self.studentlist.selection():
                conn = sqlite3.connect("StudentDatabase.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE studentdatabase SET Student_ID=?, Student_Name=?, Course_Code=?, Student_YearLevel=?,Student_Gender=?\
                      WHERE Student_ID=?", (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get(),\
                          self.studentlist.set(selected, '#1')))
                conn.commit()
                tkinter.messagebox.showinfo("Student Information System", "Student Updated Successfully")
                displayData()
                conn.close()
        
        def deleteData():   
            try:
                messageDelete = tkinter.messagebox.askyesno("Student Information System", "Do you want to permanently delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("StudentDatabase.db")
                    cur = con.cursor()
                    x = self.studentlist.selection()[0]
                    id_no = self.studentlist.item(x)["values"][0]
                    cur.execute("DELETE FROM studentdatabase WHERE Student_ID = ?",(id_no,))                   
                    con.commit()
                    self.studentlist.delete(x)
                    tkinter.messagebox.showinfo("Student Information System", "Student Deleted Successfully")
                    displayData()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def searchData():
            Student_ID = SearchBar_Var.get()
            try:  
                con = sqlite3.connect("StudentDatabase.db")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM studentdatabase WHERE Student_ID = ?",(Student_ID,))
                con.commit()
                self.studentlist.delete(*self.studentlist.get_children())
                rows = cur.fetchall()
                for row in rows:
                    self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("Student Information System", "Invalid ID")
            
                
        def displayData():
            self.studentlist.delete(*self.studentlist.get_children())
            conn = sqlite3.connect("StudentDatabase.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM studentdatabase")
            rows = cur.fetchall()
            for row in rows:
                self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
                            
        def editData():
            x = self.studentlist.focus()
            if x == "":
                tkinter.messagebox.showerror("Student Information System", "Please select a record from the table.")
                return
            values = self.studentlist.item(x, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])
        
        def Refresh():
            displayData()
        
        def clear():
            Student_ID.set('')
            Student_Name.set('') 
            Student_YearLevel.set('')
            Student_Gender.set('')
            Course_Code.set('')
            
        ##=====================================Label and Entry=====================================##
        
        self.lblStudentID = Label(self, font=("Poppins", 12,"bold"), text="STUDENT ID:*", padx=5, pady=5)
        self.lblStudentID.place(x=25,y=144)
        self.lblStudentIDFormat = Label(self, font=("Poppins", 12,"bold"), text="(YYYY - NNNN)")
        self.lblStudentIDFormat.place(x=150,y=178)
        self.txtStudentID = Entry(self, font=("Poppins", 13), textvariable=Student_ID, width=35)
        self.txtStudentID.place(x=150,y=150)
        

        self.lblStudentName = Label(self, font=("Poppins", 12,"bold"), text="FULL NAME:*", padx=5, pady=5)
        self.lblStudentName.place(x=25,y=205)
        self.txtStudentName = Entry(self, font=("Poppins", 13), textvariable=Student_Name, width=35)
        self.txtStudentName.place(x=150,y=210)
        self.lblStudentNameFormat = Label(self, font=("Poppins", 12,"bold"),
                                          text="(SURNAME, NAME, MIDDLE INITIAL)")
        self.lblStudentNameFormat.place(x=150,y=238)
        
        self.lblStudentCourse = Label(self, font=("Poppins", 12,"bold"), text="COURSE:*", padx=5, pady=5)
        self.lblStudentCourse.place(x=25,y=269)
        self.txtStudentCourse = Entry(self, font=("Poppins", 13), textvariable=Course_Code, width=35)
        self.txtStudentCourse.place(x=150,y=274)

        self.lblStudentYearLevel = Label(self, font=("Poppins", 12,"bold"), text="YEAR LEVEL:*", padx=5, pady=5)
        self.lblStudentYearLevel.place(x=25,y=315)
        self.txtStudentYearLevel = ttk.Combobox(self,
                                                value=["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"],
                                                state="readonly", font=("Poppins", 13), textvariable=Student_YearLevel,
                                                width=33)
        self.txtStudentYearLevel.place(x=150,y=320)
        

        self.lblStudentGender = Label(self, font=("Poppins", 12,"bold"), text="GENDER:*", padx=5, pady=5)
        self.lblStudentGender.place(x=25,y=361)
        self.txtStudentGender = ttk.Combobox(self, value=["Male", "Female"], font=("Poppins", 13),
                                             state="readonly", textvariable=Student_Gender, width=33)
        self.txtStudentGender.place(x=150,y=366)

        
        self.SearchBar = Entry(self, font=("Poppins", 11), textvariable=SearchBar_Var, width=29)
        self.SearchBar.place(x=800,y=110)
        self.SearchBar.insert(0,'Search ID here')
        
        

        ##=========================Treeview==============================##
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1150,y=140,height=420)

        self.studentlist = ttk.Treeview(self,
                                        columns=("ID Number", "Name", "Course", "Year Level", "Gender"),
                                        height = 20,
                                        yscrollcommand=scrollbar.set)

        self.studentlist.heading("ID Number", text="ID Number", anchor=W)
        self.studentlist.heading("Name", text="Name",anchor=W)
        self.studentlist.heading("Course", text="Course",anchor=W)
        self.studentlist.heading("Year Level", text="Year Level",anchor=W)
        self.studentlist.heading("Gender", text="Gender",anchor=W)
        self.studentlist['show'] = 'headings'

        self.studentlist.column("ID Number", width=100, anchor=W, stretch=False)
        self.studentlist.column("Name", width=200, stretch=False)
        self.studentlist.column("Course", width=130, anchor=W, stretch=False)
        self.studentlist.column("Year Level", width=100, anchor=W, stretch=False)
        self.studentlist.column("Gender", width=100, anchor=W, stretch=False)

        self.studentlist.place(x=510,y=140)
        scrollbar.config(command=self.studentlist.yview)
        
        ##========================Buttons=================================##
        
        self.btnAddID = Button(self, text="ADD", font=('Poppins', 11), height=1, width=10, bd=0, 
                               bg="#1B4965", fg="white", command=addData)
        self.btnAddID.place(x=180,y=420)
        self.btnAddID.config(cursor= "hand2")
        
        self.btnUpdate = Button(self, text="UPDATE", font=('Poppins', 11), height=1, width=10, bd=1,
                                bg="#1B4965", fg="snow", command=updateData)
        self.btnUpdate.place(x=315,y=420)
        self.btnUpdate.config(cursor= "hand2")
        
        self.btnClear = Button(self, text="CLEAR", font=('Poppins', 11), height=1, width=10, bd=1,
                               bg="#1B4965", fg="snow", command=clear)
        self.btnClear.place(x=180,y=465)
        self.btnClear.config(cursor= "hand2")
        
        self.btnDelete = Button(self, text="DELETE", font=('Poppins', 11), height=1, width=10, bd=1,
                                bg="#1B4965", fg="snow", command=deleteData)
        self.btnDelete.place(x=315,y=465)
        self.btnDelete.config(cursor= "hand2")
        
        self.btnSelect = Button(self, text="Select", font=('Poppins', 10), height=1, width=11,
                              bg="#1B4965", fg="snow", command=editData)
        self.btnSelect.place(x=512,y=103)
        self.btnSelect.config(cursor= "hand2")
        
        self.btnSearch = Button(self, text="Search", font=('Poppins', 10), height=1, width=10,
                                bg="#1B4965", fg="snow", command=searchData)
        self.btnSearch.place(x=1050,y=103)
        self.btnSearch.config(cursor= "hand2")
        
        self.btnRefresh = Button(self, text="Show All", font=('Poppins', 10), height=1, width=11,
                              bg="#1B4965", fg="snow",command = Refresh)
        self.btnRefresh.place(x=625,y=103)
        self.btnRefresh.config(cursor= "hand2")
        
        connect()
        displayData()
        

app = App()
app.geometry("1260x600")
app.mainloop()
