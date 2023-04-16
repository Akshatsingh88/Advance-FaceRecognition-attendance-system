from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np
from time import strftime
from datetime import datetime
class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("face recognition system")
        
        title_lbl = Label(self.root, text = "FACE RECOGNISTION", font=("times new roman" ,35, "bold"), bg = "blue", fg = "white")
        title_lbl.place(x = 0, y = 0, width=1530, height=45)
        
        #IMAGE 1
        img_top = Image.open(r"college_images\face_detector1.jpg")
        img_top = img_top.resize((650,700), Image.ANTIALIAS)
        
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        f_lbl = Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width = 650, height=700)
        
        #IMAGE 2
        img_bottom = Image.open(r"college_images\tyu.jpg")
        img_bottom = img_bottom.resize((950,700), Image.ANTIALIAS)
        
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
        f_lbl = Label(self.root,image=self.photoimg_bottom)
        f_lbl.place(x=650, y=55, width = 950, height=700)
        
        #button
        train_btn = Button(f_lbl, text ="Face Recognition",command=self.face_recog,cursor="hand2",font=("times new roman" ,18, "bold"), bg="darkgreen", fg="white")
        train_btn.place(x= 365, y= 620,width = 200,height =40)
        
    #========attendance===========
    def mark_attendance(self,i,r,n,d):
        with open("akshat.csv","r+",newline="\n") as f:
            myDataList = f.readlines()
            name_List = []
            for line in myDataList:
                entry = line.split((","))
                name_List.append(entry[0])
            if ((i not in name_List) and (r not in name_List) and (n not in name_List) and (d not in name_List)):
                now = datetime.now()
                d1 = now.strftime("%d/%m/%y")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n {i},{r},{n},{d},{dtString},{d1},Present")
                
        
    #=========face recognition==================
    def face_recog(self):
        def draw_boundary(img,classifier,scalefactor,minNeighbors,color,text,clf):
            gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image,scalefactor,minNeighbors)
            
            coord = []
            
            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id, predict = clf.predict(gray_image[y:y+h,x:x+w])
                confidence = int((100*(1-predict/300)))
                
                conn = mysql.connector.connect(host = "localhost",user ="root", passwd = "Akshat123", database = "facerecog")
                mycursor = conn.cursor()
                
                mycursor.execute("select Name from student where Student_id ="+str(id))
                n = mycursor.fetchone()
                n="+".join(n)
                
                mycursor.execute("select Roll from student where Student_id ="+str(id))
                r = mycursor.fetchone()
                r="+".join(r)
                
                mycursor.execute("select Dep from student where Student_id ="+str(id))
                d = mycursor.fetchone()
                d="+".join(d)
                
                mycursor.execute("select Student_id from student where Student_id ="+str(id))
                i = mycursor.fetchone()
                i="+".join(i)
                
                if confidence>77:
                    cv2.putText(img, f"ID:{i}",(x,y-75),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img, f"Roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img, f"Name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img, f"Department:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    self.mark_attendance(i,r,n,d)
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Unknown Face",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    
                coord = [x, y, w, h]
            return coord
        
        def recognize(img,clf,faceCascade):
            coord = draw_boundary(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
            return img 
        
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")
        
        video_cap = cv2.VideoCapture(0)
        
        while True:
            ret, img = video_cap.read()
            img =recognize(img,clf,faceCascade)
            cv2.imshow("Welcome to face Recognition!",img)
            
            if cv2.waitKey(1) == 13:
                break
        video_cap.release()
        cv2.destroyAllWindows()
            
                    

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()