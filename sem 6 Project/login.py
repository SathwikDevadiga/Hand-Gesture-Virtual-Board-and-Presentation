import tkinter as tk
from tkinter import messagebox
import psycopg2
window = tk.Tk()
import re
import  cv2 
import mediapipe as mp
import time
import ht as htm
import  cv2 
import mediapipe as mp
import time
import numpy as np
import os



def create_users_table():
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='HGR_project',
            user='postgres',
            password='satu',
            port='5432'
        )
        cursor = connection.cursor()

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS test (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        );
        '''
        cursor.execute(create_table_query)
        connection.commit()

    except Exception as e:
        print("Error creating users table:", e)

    finally:
        if connection:
            cursor.close()
            connection.close()

# Actions on Pressing Login Button
def login():
    def login_database():
        try:
            connection = psycopg2.connect(
                host='localhost',
            database='HGR_project',
            user='postgres',
            password='satu',
            port='5432'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM test WHERE email=%s AND password=%s", (e1.get(), e2.get()))
            row = cursor.fetchall()

            if row:
                user_name = row[0][1]
                l3.config(text="User found with name: " + user_name)
                
                brushThickness =15
                eraserThickness = 50
                xp,yp = 0,0
                imgCanva = np.zeros((720,1280,3),np.uint8)


                folderPath = "header"
                myList = os.listdir(folderPath)
                print(myList)
                overlayList = []
                for imPath in myList:
                    image = cv2.imread(f'{folderPath}/{imPath}')
                    overlayList.append(image)
                print(len(overlayList))
                header = overlayList[0]
                drawColor = (255, 0, 255)

                cap = cv2.VideoCapture(0)
                cap.set(3, 1280)
                cap.set(4, 720)
                detector = htm.handDetector(MaxHands=1)

                tipIds = [4,8,12,16,20]

                while True:
                    success, frame = cap.read() 

                    frame = detector.findHands(frame)
                    lmList = detector.findPosition(frame, draw=False)

                    if len(lmList) != 0:

                        # print(lmList)

                        # tip of index and middle fingers
                        x1, y1 = lmList[8][1:]
                        x2, y2 = lmList[12][1:]

                        fingers = detector.fingersUp()
                        print(fingers)

                        if fingers[1] and fingers[2]:
                            # xp, yp = 0, 0
                            
                            print("Selection Mode")
                            if y1 < 125:
                                if 250 < x1 < 450:
                                    header = overlayList[0]
                                    drawColor = (255, 0, 255)
                                elif 550 < x1 < 750:
                                    header = overlayList[1]
                                    drawColor = (255, 0, 0)
                                elif 800 < x1 < 950:
                                    header = overlayList[2]
                                    drawColor = (0, 255, 0)
                                elif 1050 < x1 < 1200:
                                    header = overlayList[3]
                                    drawColor = (0, 0, 0)
                            cv2.rectangle(frame,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

                        if fingers[1] and fingers[2] == False:
                            cv2.circle(frame, (x1, y1), 15, drawColor, cv2.FILLED)
                            print("Drawing Mode")
                            if xp == 0 and yp == 0:
                                xp, yp = x1, y1
                            
                            if drawColor==(0,0,0):
                                cv2.line(frame, (xp, yp), (x1, y1), drawColor, eraserThickness) 
                                cv2.line(imgCanva, (xp, yp), (x1, y1), drawColor, brushThickness)
                            else:
                                cv2.line(frame, (xp, yp), (x1, y1), drawColor, brushThickness)
                                cv2.line(imgCanva, (xp, yp), (x1, y1), drawColor, brushThickness)
                            xp,yp=x1,y1

                    frame[0:125,0:1280] = header
                    frame = cv2.addWeighted(frame,0.5,imgCanva,0.5,0) 
                    cv2.imshow("Image", frame) 
                    cv2.imshow("CANVAS", imgCanva) 
                    cv2.waitKey(1) 



            else:
                l3.config(text="User not found")

        except Exception as e:
            print("Error during login:", e)
            l3.config(text="An error occurred during login.")

        finally:
            if connection:
                cursor.close()
                connection.close()

    window.destroy()  # closes the previous window
    login_window = tk.Tk()  
    login_window.title("LogIn")  
    login_window.geometry("400x250") 
   
    l1 = tk.Label(login_window, text="email: ", font="times 20")
    l1.grid(row=1, column=0)

    l2 = tk.Label(login_window, text="Password: ", font="times 20")
    l2.grid(row=2, column=0)

    l3 = tk.Label(login_window, font="times 20")
    l3.grid(row=5, column=1)

   
    email_text = tk.StringVar()
    e1 = tk.Entry(login_window, textvariable=email_text)
    e1.grid(row=1, column=1)

    password_text = tk.StringVar()
    e2 = tk.Entry(login_window, textvariable=password_text, show='*')
    e2.grid(row=2, column=1)

    # create 1 button to login
    b = tk.Button(login_window, text="login", width=20, command=login_database)
    b.grid(row=4, column=1)

    login_window.mainloop()

# Actions on Pressing Signup button
def signup():
    connection = psycopg2.connect(
                host='localhost',
            database='HGR_project',
            user='postgres',
            password='satu',
            port='5432'
            )
    cur = connection.cursor()
    
    def signup_database():
        def validate_username(user_name):           
            return len(user_name) > 0 and user_name.isalpha()
        
        
        def validate_email(email):
            pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            return pattern.match(email)


        def validate_password(password):
            
            return len(password) >= 6
        
        if not validate_username(e1.get()):
            validation_label.config(text="Invalid username", fg="red")
            return
           
        if not validate_email(e2.get()):
            validation_label.config(text="Invalid email format", fg="red")
            return
      
        if not validate_password(e3.get()):
            validation_label.config(text="Password must be at least 6 characters long", fg="red")
            return
  
        cur.execute("CREATE TABLE IF NOT EXISTS test(id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, "
                    "email VARCHAR(100) UNIQUE NOT NULL, password VARCHAR(100) NOT NULL)")
        cur.execute("INSERT INTO test (name, email, password) VALUES (%s, %s, %s)",
                    (e1.get(), e2.get(), e3.get()))

        
        l4 = tk.Label(signup_window, text="Account created", font="times 15")
        l4.grid(row=6, column=2)

        connection.commit()  # save the changes
    
        

    window.destroy()  # closes the previous window
    signup_window = tk.Tk()  # creates a new window for signup process
    signup_window.geometry("400x250")  # dimensions for new window
    signup_window.title("Sign Up")  # title for the window
    # create 3 Labels
    l1 = tk.Label(signup_window, text="User Name: ", font="times 20")
    l1.grid(row=1, column=1)

    l2 = tk.Label(signup_window, text="User email: ", font="times 20")
    l2.grid(row=2, column=1)

    l3 = tk.Label(signup_window, text="Password: ", font="times 20")
    l3.grid(row=3, column=1)

    # create 3 adjacent text entries
    name_text = tk.StringVar()  # declaring string variable for storing name and password
    e1 = tk.Entry(signup_window, textvariable=name_text)
    e1.grid(row=1, column=2)

    email_text = tk.StringVar()
    e2 = tk.Entry(signup_window, textvariable=email_text)
    e2.grid(row=2, column=2)

    password_text = tk.StringVar()
    e3 = tk.Entry(signup_window, textvariable=password_text, show='*')
    e3.grid(row=3, column=2)
    
    
    validation_label = tk.Label(signup_window, text="", fg="black")
    validation_label.grid(row=5,column=2)
    # create 1 button to signup
    b1 = tk.Button(signup_window, text="signup", width=20, command=signup_database)
    b1.grid(row=4, column=2)   
    signup_window.mainloop()

window.geometry("300x150")
window.title("Login and Signup system")

label1 = tk.Label(window, text="Welcome to VBoard", font="times 20")
label1.grid(row=1, column=2, columnspan=2)

button1 = tk.Button(window, text="Login", width=20, command=login)
button1.grid(row=2, column=2)

button2 = tk.Button(window, text="Signup", width=20, command=signup)
button2.grid(row=2, column=3)

window.mainloop()
