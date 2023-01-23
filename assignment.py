# import necessary files
import cv2
import math
import imutils
import numpy as np
import pandas as pd
import argparse
import warnings
warnings.filterwarnings("ignore")


# for parsing 
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-o", "--output", help="name of the output video file",default="output.mp4")
args = vars(ap.parse_args())

# specifying the hsv value range (min and max) for different colors to be tracked in the video
lower = {'white':(20, 17, 158), 'blue':(45, 67, 0), 'yellow':(12, 121, 37), 'orange':(5, 68, 169)} 
upper = {'white':(80,118,255), 'blue':(98,202,255), 'yellow':(39,255,216), 'orange':(8,255,255)}

# specifying the color of circles (boudning box) to be shown on tracked objects in the video
colors = {'white':(0,0,0), 'blue':(255,0,0), 'yellow':(0, 255, 217), 'orange':(0,140,255)}

# some helper variables used in the program
flag = {'white':0, 'blue':0, 'yellow':0, 'orange':0}
timestamp = {'white':'0', 'blue':'0', 'yellow':'0', 'orange':'0', 'curr':'0'}
margin = {'white':0, 'blue':20, 'yellow':40, 'orange':60}

# capturing the video file using opencv 
cap = cv2.VideoCapture(args['video'])
cap.set(3,640)
cap.set(4,360)

curr_frame_num = 0
fps = cap.get(cv2.CAP_PROP_FPS)  # get the fps of the input video
curr_timestamp = str(math.ceil((curr_frame_num/fps)*100)/100)

# making a dataframe to record all the timestamps and entry/exit information regarding different objects
df = pd.DataFrame(columns = ['Timestamp', 'Color', 'Entry/Exit'])

# specifying the parameters for the output video file
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(args['output'], fourcc, fps, (640, 360))

# loop till video doesn't end
while True:
    _, frame = cap.read()
    if frame is None:
        break
 
    # resize the frame, blur it, and convert it to the HSV
    frame = imutils.resize(frame, width=640)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # print the elapsed time on the video itself
    timestamp['curr'] = str(math.ceil((curr_frame_num/fps)*100)/100)
    cv2.putText(frame, "time elapsed : "+timestamp['curr'],(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.55,(255,255,255),1)
    curr_frame_num += 1

    #for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary, then perform a series of dilations and erosions to remove any small blobs left in the mask
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
       
        # find contours in the mask and initialize the current (x, y) center of the ball
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        # only proceed if at least one contour was found
        if len(contours) > 0:
            # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
            largest_contour = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
            Moments = cv2.moments(largest_contour)
            center = (int(Moments["m10"] / Moments["m00"]), int(Moments["m01"] / Moments["m00"]))
            
            # print the timestaps and information regarding entry of different objects in the video itself
            if flag[key]==1:
                flag[key]=0            
                timestamp[key] = timestamp['curr']
            cv2.putText(frame, timestamp[key] + " : "+ key +" -> entry", (10,260+margin[key]), cv2.FONT_HERSHEY_SIMPLEX, 0.55,colors[key],2)
            df = df.append({'Timestamp' : timestamp[key], 'Color' : key, 'Entry/Exit' : 'Entry'}, ignore_index = True)
        
            if radius > 0.5:
                # draw circle representing the tracked object along with its color
                cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                cv2.putText(frame,key, (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
        
        else:
            # print the timestaps and information regarding exit of different objects in the video itself
            if flag[key] == 0:
                flag[key] = 1
                timestamp[key] = timestamp['curr']
            cv2.putText(frame, timestamp[key] + " : "+ key + " -> exit", (10,260+margin[key]), cv2.FONT_HERSHEY_SIMPLEX, 0.55,colors[key],2)
            df = df.append({'Timestamp' : timestamp[key], 'Color' : key, 'Entry/Exit' : 'Exit'}, ignore_index = True)
        
     
    writer.write(frame) 
    cv2.imshow("Frame", frame)
    
    # user can press q button to prematurely exit the video
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# releasing all the cv2 objects and destroying cv2 windows used
cap.release()
writer.release()
cv2.destroyAllWindows()

# in the dataframe generated, removing all the duplicate rows and saving the data to a csv file
df.drop_duplicates(keep='first', inplace=True)
df.to_csv('timestamps.csv', index=False)

