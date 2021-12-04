import tkinter
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog
from skimage.draw import line
import ntpath
import tkinter.messagebox
import time
from timeit import default_timer as timer
import math

counter = 0
maincount = 0
points = np.zeros((2, 2), np.int)

def Detect_bags():
	global counter, cap, maincount, points, reflectCount, count
	
	status = 0
	timeStart = timer()

	#Reading Video Stream
	while(1):

		ret, frame = cap.read()

		if ret == False:
			cap.release()
			cv2.destroyAllWindows() 
			tkinter.messagebox.showinfo("Indicator",  "Video Stream Ended")
			break
		
		rr = cv2.line(frame, (points[0][0], points[0][1]), (points[1][0], points[1][1]), (0, 255, 0), 9)

		rr, cc = line(points[0][0], points[0][1], points[1][0], points[1][1])
		cods = list(zip(rr, cc))

		pixels = np.array([frame[x, y] for (x, y) in cods])
		B_mean = np.mean(pixels[:,0])
		G_mean = np.mean(pixels[:,1])
		R_mean = np.mean(pixels[:,2])
		strVal = 'B' + str(B_mean) + ' R' + str(R_mean) + ' G' + str(G_mean)

		if(B_mean<80):
			counter = counter + 1
			cv2.circle(frame, (points[0][0]+10, points[0][1]-10), 5, (255, 255, 0), cv2.FILLED)
		else:
			if counter > 0:
				maincount = maincount + 1
			counter = 0

		window.update_idletasks()

		cv2.putText(frame, str(counter), (points[0][0]+20, points[0][1]-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0),1)
		cv2.putText(frame, str(maincount), (points[0][0]+50, points[0][1]-10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0),1)

		if reflectCount != 0:
			if maincount%reflectCount == 0:
				iteration = math.floor(maincount/reflectCount)
				status += 1
				time = timer() - timeStart
				timeStart = timer()
				
		if status != 0:
			Bags = ' Iteration : '+ str(iteration) +" , " + str(maincount) + ' Bags are Counted'
			cv2.putText(frame, Bags,(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),2, cv2.LINE_AA)
			
		cv2.imshow('frame', frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()

	cv2.destroyAllWindows()  

	totalBagsCount = "Total Bags Count : " + str(maincount)
	
	lblCounts = tkinter.Label(window, text=totalBagsCount).place(x = 50, y=200)


def mousePoints(event, x, y, flags, params):
	global cap

	if event == cv2.EVENT_LBUTTONDOWN:
		global counter
		global points
		points[counter] = x, y
		counter = counter + 1  


def DrawLine():
	global cap, tail, Camera, reflectCount, head
	pathh = head+"/"+tail
	print(pathh)

	if txtbagslimit.get("1.0",'end-1c') != '':
		reflectCount = int(txtbagslimit.get("1.0",'end-1c'))
	else:
		reflectCount = 0

	if Camera == True:
		cap = cv2.VideoCapture(0)
	else:
		cap = cv2.VideoCapture(pathh)

	cv2.namedWindow('image')
	cv2.setMouseCallback('image',mousePoints)

	time.sleep(2)
	ret, img = cap.read()
	while(1):
		cv2.imshow('image', img)
		for x in range(2):
			cv2.circle(img, (points[x][0], points[x][1]), 5, (0, 255, 0), cv2.FILLED)

		if cv2.waitKey(20) & 0xFF == 27:
			break
	cv2.destroyWindow('image') 

	Detect_bags()	


def openFile():
	global video_path, tail, filename, head
	
	filename =  filedialog.askopenfilename(title="Select A File", filetypes=(("mp4", "*.mp4"),("all files", "*.*")))

	head, tail = ntpath.split(filename)
	filenameLabel = tkinter.Label(window,text=tail).place(x=150, y = 134)
	

def videoSelect():
	global video_path
	btnStart = tkinter.Button(window, text= "Open Video File", command=openFile).place(x = 50,y = 134)  
	print(video_path)


def CameraSelect():
	global Camera, chooseFile, filename
	Camera = True


window = tkinter.Tk()
window.title("Object Detection & Tracking From Real-Time Video") 
window.geometry("500x350")
window.configure()

video_path = ""
cap = ""
tail = ""
reflectCount = 0
Camera = False
filename = ""
head = ""
count = 1
# timeStart = 0

select_one = tkinter.Label(window, text = "Select One").place(x = 50,y = 60)

R1 = tkinter.Radiobutton(window, text="Camera", value=1, command = CameraSelect).place(x = 50,y = 90)  

R2 = tkinter.Radiobutton(window, text="Video", value=2, command = videoSelect).place(x = 150,y = 90)  

lblbagslimit = tkinter.Label(window, text = "Bags Limit").place(x = 50,y = 0) 

txtbagslimit = tkinter.Text(window,height = 1, width = 30)
txtbagslimit.pack()

btnStart = tkinter.Button(window, text= "Start", command = DrawLine).place(x = 50,y = 240)  

tkinter.mainloop()  