from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
from main import Face_Recognisiton_System


def main():
    win = Tk()
    app = Login_window(win)
    win = mainloop()
    

class Login_window:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Login system")
    
        img_top = Image.open(r"college_images\LNCT.jpg")
        img_top = img_top.resize((1530,780), Image.ANTIALIAS)
        
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        f_lbl = Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0, y=0, width = 1530, height=780)
        
        main_frame = Frame(self.root, bg= "black")
        main_frame.place(x= 610, y = 170, width = 340, height=450)
        
        img1 = Image.open(r"college_images\LoginIconAppl.png")
        img1 = img1.resize((100,100), Image.ANTIALIAS)
        
        self.photoimg1 = ImageTk.PhotoImage(img1)
        f_lbl = Label(image=self.photoimg1,bg="black", borderwidth=0)
        f_lbl.place(x=730, y=175, width = 100, height=100)
        
        lbl = Label(main_frame,text="Get Started",font=("times new roman" ,20, "bold"), fg= "white", bg= "black")
        lbl.place(x=95, y=100)
        
        #UserName
        username_lbl = Label(main_frame,text="Username:",font=("times new roman" ,15, "bold"), fg= "white", bg= "black")
        username_lbl.place(x=70, y=155)
        
        self.textuser = ttk.Entry(main_frame,font=("times new roman" ,15, "bold"))
        self.textuser.place(x=40, y=190,width=270)
        
        # password
        
        password = Label(main_frame,text="Password:",font=("times new roman" ,15, "bold"), fg= "white", bg= "black")
        password.place(x=70, y=225)
        
        self.textpass = ttk.Entry(main_frame,font=("times new roman" ,15, "bold"))
        self.textpass.place(x=40, y=260,width=270)
        
        #icons
        img3 = Image.open(r"college_images\LoginIconAppl.png")
        img3 = img3.resize((25,25), Image.ANTIALIAS)
        
        self.photoimg3 = ImageTk.PhotoImage(img3)
        f_lbl3 = Label(image=self.photoimg3,bg="black", borderwidth=0)
        f_lbl3.place(x=650, y=323, width = 25, height=25)
        
        img4 = Image.open(r"college_images\lock-512.png")
        img4 = img4.resize((25,25), Image.ANTIALIAS)
        
        self.photoimg4 = ImageTk.PhotoImage(img4)
        f_lbl4 = Label(image=self.photoimg4,bg="black", borderwidth=0)
        f_lbl4.place(x=650, y=395, width = 25, height=25)
        
        #Login button
        
        loginbutton = Button(main_frame,command=self.login, text = "Login",font=("times new roman" ,15, "bold"), bg="blue", fg="white",bd=3,relief=RIDGE)
        loginbutton.place(x= 110, y=300,width=120, height=35)
        
        #RegisterButton
        regbutton = Button(main_frame,command=self.register_window,text = "New User Register",font=("times new roman" ,10, "bold"), bg="black", fg="white",borderwidth=0,relief=RIDGE)
        regbutton.place(x= 15, y=350,width=160)
        
        #forgetbutton
        passbutton = Button(main_frame, text = "Forgot Password",command=self.forgot_password_window,font=("times new roman" ,10, "bold"), bg="black", fg="white",borderwidth=0,relief=RIDGE)
        passbutton.place(x= 10, y=390,width=160)
        
    def register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = Register(self.new_window)
        
    def login(self):
        if self.textuser.get() =="" or self.textpass.get() =="":
            messagebox.showerror("Error","All Fields are required")
        elif self.textuser.get()  == "Hanuman" and self.textpass.get() == "0604":
            messagebox.showinfo("Success","Welcome")
        else:
            conn = mysql.connector.connect(host = "localhost",user ="root", passwd = "Akshat123", database = "mydata")
            my_cursor = conn.cursor()
            my_cursor.execute("select * from register where email=%s and password=%s",(
                                                                                    self.textuser.get(),
                                                                                    self.textpass.get()
                                                                                    ))
            row =  my_cursor.fetchone()
            if row == None:
                messagebox.showerror("Error","Invalid Username and Password")
            else:
                open_main =  messagebox.askyesno("Yes No","Access only admin")
                if open_main > 0:
                    self.new_window = Toplevel(self.root)
                    self.app = Face_Recognisiton_System(self.new_window)
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()
            
    #================resetpassword================
    def reset_pass(self):
        if self.combo_security_Q.get() == "Select":
            messagebox.showerror("Error","Select security question", parent = self.root2)
        elif self.txt_security.get() == "":
            messagebox.showerror("Error","Please enter the answer", parent = self.root2)
        elif self.txt_newpass.get() == "":
            messagebox.showerror("Error","Please enter the new password", parent = self.root2)
        else:
            conn = mysql.connector.connect(host = "localhost",user ="root", passwd = "Akshat123", database = "mydata")
            my_cursor = conn.cursor()    
            qury = ("select * from register where email= %s and securityQ = %s and securityA = %s")
            vlaue = (self.textuser.get(),self.combo_security_Q.get(),self.txt_security.get())
            my_cursor.execute(qury,vlaue)
            row = my_cursor.fetchone()
            if row == None:
                messagebox.showerror("Error","Please enter correct answer", parent = self.root2)
            else:
                query =("update register set password=%s where email=%s")
                value = (self.txt_newpass.get(), self.textuser.get())
                my_cursor.execute(query,value)
                
                conn.commit()
                conn.close()
                messagebox.showinfo("Info","Your password has been reset , please login new password", parent = self.root2)
                self.root2.destroy()
                
                
            
    #======================Forget Password =================
    
    def forgot_password_window(self):
        if self.textuser.get() =="":
            messagebox.showerror("Error","Please enter the email address to reset the password")
        else:
            conn = mysql.connector.connect(host = "localhost",user ="root", passwd = "Akshat123", database = "mydata")
            my_cursor = conn.cursor()
            query = ("select * from register where email=%s")
            value = (self.textuser.get(),)
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            #print(row)
            
            if row == None:
                messagebox.showerror("My Error","Please enter valid username")
            else:
                conn.close()
                self.root2 = Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("340x450+610+170")
                
                l = Label(self.root2,text="Forget Password",font=("times new roman" ,15, "bold"),fg= "red", bg= "white")
                l.place(x= 0,y= 0,relwidth=1)
                
                security_Q = Label(self.root2,text="Select Security Question",font=("times new roman" ,15, "bold"), fg="green")
                security_Q.place(x=50, y=80)
        
                self.combo_security_Q = ttk.Combobox(self.root2, font=("times new roman" ,12, "bold"),state="readonly",width=20)
                self.combo_security_Q["values"] = ("Select ","Your Birth Place","Your Name", "Your Pet Name")
                self.combo_security_Q.current(0)
                self.combo_security_Q.place(x= 50, y= 110, width = 250)
        
                security_A = Label(self.root2,text="Security Answer :",font=("times new roman" ,15, "bold"), fg="green")
                security_A.place(x=50, y=150)
        
                self.txt_security = ttk.Entry(self.root2,font=("times new roman" ,15, "bold"))
                self.txt_security.place(x=50, y=180,width=250)
                
                new_password = Label(self.root2,text="New Password :",font=("times new roman" ,15, "bold"), fg="green")
                new_password.place(x=50, y=220)
        
                self.txt_newpass = ttk.Entry(self.root2,font=("times new roman" ,15, "bold"))
                self.txt_newpass.place(x=50, y=250,width=250)
                
                btn = Button(self.root2, text = "Reset",command=self.reset_pass,font=("times new roman" ,15, "bold"), bg="blue", fg="white",bd=3,relief=RIDGE)
                btn.place(x= 100, y=300)
            
            
class Register:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Register")
        
        #===============variables=============
        self.var_fname= StringVar()
        self.var_lname= StringVar()
        self.var_contact= StringVar()
        self.var_email= StringVar()
        self.var_securityQ= StringVar()
        self.var_securityA= StringVar()
        self.var_pass= StringVar()
        self.var_confpass =  StringVar()
        
        #background image
        img_top = Image.open(r"college_images\LNCT.jpg")
        img_top = img_top.resize((1530,780), Image.ANTIALIAS)
        
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        bg_img = Label(self.root,image=self.photoimg_top)
        bg_img.place(x=0, y=0, width = 1530, height=780)
        
        #leftImage
        left_img = Image.open(r"college_images\thought-good-morning-messages-LoveSove.jpg")
        left_img = left_img.resize((470,550), Image.ANTIALIAS)
        
        self.photoleft_img = ImageTk.PhotoImage(left_img)
        bg_img1 = Label(self.root,image=self.photoleft_img)
        bg_img1.place(x=60, y=100, width = 470, height=550)
        #=============mainFrame=========
        frame = Frame(self.root, bd= 2)
        frame.place(x= 520, y = 100, width = 800, height=550)
        
        #=======register label=========
        register_lbl = Label(frame,text="REGISTER HERE",font=("times new roman" ,20, "bold"), fg="green")
        register_lbl.place(x=20, y=20)
        
        #=========label and entry ========
        fname = Label(frame,text="First Name",font=("times new roman" ,15, "bold"), fg="green")
        fname.place(x=50, y=100)
        
        fname_entry = ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman" ,15, "bold"))
        fname_entry.place(x=50, y=130,width=250)
        
        lname = Label(frame,text="Last Name",font=("times new roman" ,15, "bold"), fg="green")
        lname.place(x=370, y=100)
        
        self.txt_lname = ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman" ,15, "bold"))
        self.txt_lname.place(x=370, y=130,width=250)
        
        #==========row2
        contact = Label(frame,text="Contact No.",font=("times new roman" ,15, "bold"), fg="green")
        contact.place(x=50, y=170)
        
        self.txt_contact = ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman" ,15, "bold"))
        self.txt_contact.place(x=50, y=200,width=250)
        
        email = Label(frame,text="Eamil :",font=("times new roman" ,15, "bold"), fg="green")
        email.place(x=370, y=170)
        
        self.txt_email = ttk.Entry(frame,textvariable=self.var_email,font=("times new roman" ,15, "bold"))
        self.txt_email.place(x=370, y=200,width=250)
        
        #==========row3
        security_Q = Label(frame,text="Select Security Question",font=("times new roman" ,15, "bold"), fg="green")
        security_Q.place(x=50, y=240)
        
        self.combo_security_Q = ttk.Combobox(frame,textvariable=self.var_securityQ,  font=("times new roman" ,12, "bold"),state="readonly",width=20)
        self.combo_security_Q["values"] = ("Select ","Your Birth Place","Your Name", "Your Pet Name")
        self.combo_security_Q.current(0)
        self.combo_security_Q.place(x= 50, y= 270, width = 250)
        
        security_A = Label(frame,text="Security Answer :",font=("times new roman" ,15, "bold"), fg="green")
        security_A.place(x=370, y=240)
        
        self.txt_security = ttk.Entry(frame,textvariable=self.var_securityA,font=("times new roman" ,15, "bold"))
        self.txt_security.place(x=370, y=270,width=250)
        
        #==========row4
        pswd = Label(frame,text="Password",font=("times new roman" ,15, "bold"), fg="green")
        pswd.place(x=50, y=310)
        
        self.txt_pswd = ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman" ,15, "bold"))
        self.txt_pswd.place(x=50, y=340,width=250)
        
        confirm_pswd = Label(frame,text="Confirm Password :",font=("times new roman" ,15, "bold"), fg="green")
        confirm_pswd.place(x=370, y=310)
        
        self.txt_confirm_pswd = ttk.Entry(frame,textvariable=self.var_confpass,font=("times new roman" ,15, "bold"))
        self.txt_confirm_pswd.place(x=370, y=340,width=250)
        
        #==========checkbutton =====
        self.var_check = IntVar()
        check_btn = Checkbutton(frame,variable=self.var_check,text="I agree to the terms and conditions",font=("times new roman",12, "bold"), fg="green", onvalue=1, offvalue=0)
        check_btn.place(x=50, y=380)
        
        #==========button=========
        img = Image.open(r"college_images\register-now-button1.jpg")
        img = img.resize((200,50), Image.ANTIALIAS)
        
        self.photo_img = ImageTk.PhotoImage(img)
        b1 = Button(frame, image = self.photo_img,borderwidth=0,command=self.register_data,cursor="hand2")
        b1.place(x=50, y=430, width=300)
        
        img1 = Image.open(r"college_images\loginpng.png")
        img1 = img1.resize((200,50), Image.ANTIALIAS)
        
        self.photo_img1 = ImageTk.PhotoImage(img1)
        b1 = Button(frame, image = self.photo_img1,command=self.return_login,borderwidth=0,cursor="hand2")
        b1.place(x=330, y=430, width=300)
        
    #================Function Declaration================
    def register_data(self):
        if self.var_fname.get() =="" or self.var_email.get() =="" or self.var_securityQ.get() =="Select":
            messagebox.showerror("Error","All Fields are required")
        elif self.var_pass.get() != self.var_confpass.get():
            messagebox.showerror("Error","Password does not match")
        elif self.var_check.get() == 0:
            messagebox.showerror("Error","Please agree terms and conditions")
        else:
            conn = mysql.connector.connect(host = "localhost",user ="root", passwd = "Akshat123", database = "mydata")
            my_cursor = conn.cursor()
            query  = ("select * from register where email = %s")
            value = (self.var_email.get(),)
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            if row != None:
                messagebox.showinfo("Error","User already exist, please try another email")
            else:
                my_cursor.execute("INSERT INTO register values (%s,%s,%s,%s,%s,%s,%s)",( 
                                                                                    self.var_fname.get(),
                                                                                    self.var_lname.get(),
                                                                                    self.var_contact.get(),
                                                                                    self.var_email.get(),
                                                                                    self.var_securityQ.get(),
                                                                                    self.var_securityA.get(),
                                                                                    self.var_pass.get()
                                                                                     ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registered successfully")
    
    def return_login(self):
        self.root.destroy()
        
if __name__ == "__main__":
    main()