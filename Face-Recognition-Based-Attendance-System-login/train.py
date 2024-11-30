import tkinter as tk
from tkinter import Message ,Text
import tkinter.messagebox as tkMessageBox

from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from sendEmail import sendEmail
import sqlite3

window = tk.Tk()
#helv36 = tk.Font(family='Italic', size=36, weight='bold')
window.title("Face_Recognizer")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)
 
window.geometry('1000x720')
#window.configure(background='black')






#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

#path = "profile.jpg"

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
#img = ImageTk.PhotoImage(Image.open(path))

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
#panel = tk.Label(window, image = img)


#panel.pack(side = "left", fill = "y", expand = "no")

#cv_img = cv2.imread("img541.jpg")
#x, y, no_channels = cv_img.shape
#canvas = tk.Canvas(window, width = x, height =y)
#canvas.pack(side="left")
#photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img)) 
# Add a PhotoImage to the Canvas
#canvas.create_image(0, 0, image=photo, anchor=tk.NW)

#msg = Message(window, text='Hello, world!')

# Font is a tuple of (font_family, size_in_points, style_modifier_string)




bg=PhotoImage(file="D:/Face-Recognition-Based-Attendance-System-login/static/wallpaperflare.com_wallpaper.png")
bglabel=Label(window,image=bg)
bglabel.place(x=0,y=0)




message = tk.Label(window, text="Student Attendance-Face Recognition" ,bg="black" , fg="cyan3"  ,font=('times', 30, 'bold'))

message.place(x=20, y=20)

#=======================================VARIABLES=====================================
USERNAME = StringVar()
PASSWORD = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()

#=======================================METHODS=======================================
def Database():
    global conn, cursor
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, firstname TEXT, lastname TEXT)")


def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        window.destroy()
        exit()


def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(window,bg="black")
    LoginFrame.place(x=250,y=230)
    #LoginFrame.pack(side=TOP, pady=100)
    lbl_username = Label(LoginFrame, text="Username:", font=('arial', 23), bd=18,bg="black",fg="cyan3")
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="Password:", font=('arial', 23), bd=18,bg="black",fg="cyan3")
    lbl_password.grid(row=2)
    lbl_result1 = Label(LoginFrame, text="", font=('arial', 18),bg="black",fg="cyan3")
    lbl_result1.grid(row=3, columnspan=2)
    username = Entry(LoginFrame, font=('arial', 20), textvariable=USERNAME, width=17)
    username.grid(row=1, column=1)
    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=17, show="*")
    password.grid(row=2, column=1)
    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=26, command=Login,bg="cyan3",fg="black")
    btn_login.grid(row=4, columnspan=2, pady=20)
    lbl_register = Label(LoginFrame, text="Register", font=('arial', 17),bg="cyan3",fg="black")
    lbl_register.grid(row=0, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)

def RegisterForm():
    global RegisterFrame, lbl_result2
    RegisterFrame = Frame(window,bg="black")
    RegisterFrame.place(x=250,y=230)
    #RegisterFrame.pack(side=TOP, pady=40)
    lbl_username = Label(RegisterFrame, text="Username:", font=('arial', 18), bd=18,bg="black",fg="cyan3")
    lbl_username.grid(row=1)
    lbl_password = Label(RegisterFrame, text="Password:", font=('arial', 18), bd=18,bg="black",fg="cyan3")
    lbl_password.grid(row=2)
    lbl_firstname = Label(RegisterFrame, text="Firstname:", font=('arial', 18), bd=18,bg="black",fg="cyan3")
    lbl_firstname.grid(row=3)
    lbl_lastname = Label(RegisterFrame, text="Lastname:", font=('arial', 18), bd=18,bg="black",fg="cyan3")
    lbl_lastname.grid(row=4)
    lbl_result2 = Label(RegisterFrame, text="", font=('arial', 18))
    lbl_result2.grid(row=5, columnspan=2)
    username = Entry(RegisterFrame, font=('arial', 20), textvariable=USERNAME, width=20)
    username.grid(row=1, column=1)
    password = Entry(RegisterFrame, font=('arial', 20), textvariable=PASSWORD, width=20, show="*")
    password.grid(row=2, column=1)
    firstname = Entry(RegisterFrame, font=('arial', 20), textvariable=FIRSTNAME, width=20)
    firstname.grid(row=3, column=1)
    lastname = Entry(RegisterFrame, font=('arial', 20), textvariable=LASTNAME, width=20)
    lastname.grid(row=4, column=1)
    btn_login = Button(RegisterFrame, text="Register", font=('arial', 18), width=25, command=Register,bg="cyan3",fg="black")
    btn_login.grid(row=6, columnspan=2, pady=20)
    lbl_login = Label(RegisterFrame, text="Login",  font=('arial', 17),bg="cyan3",fg="black")
    lbl_login.grid(row=0, sticky=W)
    lbl_login.bind('<Button-1>', ToggleToLogin)

def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()

def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()

def Register():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get == "":
        lbl_result2.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (USERNAME.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Username is already taken", fg="red")
        else:
            cursor.execute("INSERT INTO `member` (username, password, firstname, lastname) VALUES(?, ?, ?, ?)", (str(USERNAME.get()), str(PASSWORD.get()), str(FIRSTNAME.get()), str(LASTNAME.get())))
            conn.commit()
            USERNAME.set("")
            PASSWORD.set("")
            FIRSTNAME.set("")
            LASTNAME.set("")
            lbl_result2.config(text="Successfully Created!", fg="black")
        cursor.close()
        conn.close()
def Login():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            lbl_result1.config(text="You Successfully Login", fg="blue")
            LoginFrame.destroy()
            attendance()
        else:
            lbl_result1.config(text="Invalid Username or password", fg="red")
LoginForm()

#========================================MENUBAR WIDGETS==================================
menubar = Menu(window)
#filemenu = Menu(menubar, tearoff=0)
#filemenu.add_command(label="Exit", command=Exit)
#menubar.add_cascade(label="File", menu=filemenu)
#window.config(menu=menubar)



def attendance():
    lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="black"  ,bg="cyan3" ,font=('times', 15, ' bold ') )
    lbl.place(x=50, y=200)

    txt = tk.Entry(window,width=20, bg="black" ,fg="cyan3",font=('times', 15, ' bold '))
    txt.place(x=350, y=215)


    lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="black"  ,bg="cyan3"    ,height=2 ,font=('times', 15, ' bold '))
    lbl2.place(x=50, y=275)

    txt2 = tk.Entry(window,width=20  ,bg="black"  ,fg="cyan3",font=('times', 15, ' bold ')  )
    txt2.place(x=350, y=290)

    lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="black"  ,bg="cyan3"  ,height=2 ,font=('times', 15, ' bold'))
    lbl3.place(x=50, y=375)

    message = tk.Label(window, text="" ,bg="black"  ,fg="cyan3"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold '))
    message.place(x=350, y=375)

    lbl3 = tk.Label(window, text="Attendance : ",width=20  ,fg="black"  ,bg="cyan3"  ,height=2 ,font=('times', 15, ' bold'))
    lbl3.place(x=50, y=450)

    exitbutton = tk.Button(window, text="Exit", command=Exit,fg="black"  ,bg="cyan3"  ,height=1 ,activebackground = "red" ,font=('times', 18, ' bold '))
    exitbutton.place(x=900, y=23)


    message2 = tk.Label(window, text="" ,fg="cyan3"   ,bg="black",activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold '))
    message2.place(x=350, y=450)
     
    def clear():
        txt.delete(0, 'end')    
        res = ""
        message.configure(text= res)

    def clear2():
        txt2.delete(0, 'end')    
        res = ""
        message.configure(text= res)    
        
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
     
        try:
              import unicodedata
              unicodedata.numeric(s)
              return True
        except (TypeError, ValueError):
            pass
     
        return False
     
    def TakeImages():        
        Id=(txt.get())
        name=(txt2.get())
        if(is_number(Id) and name.isalpha()):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                    #incrementing sample number 
                    sampleNum=sampleNum+1
                    #saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImages\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    #display the frame
                    cv2.imshow('frame',img)
                #wait for 100 miliseconds 
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum>60:
                    break
            cam.release()
            cv2.destroyAllWindows() 
            res = "Images Saved for ID : " + Id +" Name : "+ name
            row = [Id , name]
            with open('StudentDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message.configure(text= res)
        else:
            if(is_number(Id)):
                res = "Enter Alphabetical Name"
                message.configure(text= res)
            if(name.isalpha()):
                res = "Enter Numeric Id"
                message.configure(text= res)
        
    def TrainImages():
        recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector =cv2.CascadeClassifier(harcascadePath)
        faces,Id = getImagesAndLabels("TrainingImages")
        recognizer.train(faces, np.array(Id))
        recognizer.save("Trainner.yml")
        res = "Image Trained"#+",".join(str(f) for f in Id)
        message.configure(text= res)

    def getImagesAndLabels(path):
        #get the path of all the files in the folder
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        #print(imagePaths)
        
        #create empth face list
        faces=[]
        #create empty ID list
        Ids=[]
        #now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            #loading the image and converting it to gray scale
            pilImage=Image.open(imagePath).convert('L')
            #Now we are converting the PIL image into numpy array
            imageNp=np.array(pilImage,'uint8')
            #getting the Id from the image
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces.append(imageNp)
            Ids.append(Id)        
        return faces,Ids

    def sendmail():
        sendEmail()
        return 0




    def TrackImages():
        recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
        recognizer.read("Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        df=pd.read_csv("StudentDetails.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        col_names =  ['Id','Name','Date','Time']
        attendance = pd.DataFrame(columns = col_names)
        while True:
            ret,im =cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.3,5)
            for(x, y, w, h) in faces:
                cv2.rectangle(im,(x, y), (x + w, y + h), (255,0,0), 2)
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                #print (" Id:",Id)
                #print("Confidence:",conf)
                if conf < 50:
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    #print(date)
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['ID'] == Id]['NAME'].values
                    tt=str(Id)+"-"+aa
                    attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                else:
                    Id='Unknown'
                    #print ("ID:",Id)
                    tt=str(Id)  
                if(conf > 75):
                    noOfFile=len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)
            attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
            cv2.imshow('im',im) 
            if (cv2.waitKey(1)==ord('q')):
                break
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        Hour,Minute,Second=timeStamp.split(":")
        fileName="Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        attendance.to_csv(fileName,index=False)
        cam.release()
        cv2.destroyAllWindows()
        res=attendance
        message2.configure(text= res)

      
    clearButton = tk.Button(window, text="Clear", command=clear,fg="white"  ,bg="cyan3"  ,width=15  ,height=1 ,activebackground = "red" ,font=('times', 15, ' bold '))
    clearButton.place(x=580, y=200)
    clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="white"  ,bg="cyan3"  ,width=15  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
    clearButton2.place(x=580, y=280)
    takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="cyan3"  ,bg="black"  ,width=15  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
    takeImg.place(x=50, y=550)
    trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="black"  ,bg="cyan3"  ,width=15  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
    trainImg.place(x=350, y=550)
    trackImg = tk.Button(window, text="Track Images", command=TrackImages  ,fg="cyan3"  ,bg="black"  ,width=15  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
    trackImg.place(x=550, y=550)
    sendmailBtn = tk.Button(window, text="SEND MAIL", command=sendmail  ,fg="black"  ,bg="cyan3"  ,width=15  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
    sendmailBtn.place(x=750, y=550)



window.mainloop()
time.sleep(10)
