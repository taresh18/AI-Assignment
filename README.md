# AI-Assignment

Input video link - https://drive.google.com/file/d/1goI3aHVE29Gko9lpTzgi_g3CZZPjJq8w/view?usp=share_link  </br>
Output video link - https://drive.google.com/file/d/1qMfo-UoDiqdeFLn3Mc0IFQAoG_kGzk9A/view?usp=share_link  </br>

The file "assignment.py" can be run as a script which takes arguments as follows : </br>
python assignment.py -v "path to input video file" -o "name of output video file to be specified"  </br>

The program has provision for feeding a new video which can be easily provided as shown above. The processed video is saved on local hard disk whose path can also be provided as shown above.

The video contains 4 balls of different colours which need to be tracked throughout the video. I used openCV to create masks for different color balls using their respective hsv color space. 

I extracted a sample image called "testImage.png" from the video which contains all 4 balls simultaneously and wrote a program with which we can fine tune the hsv range for different colours present in the image.

![Screenshot (14)](https://user-images.githubusercontent.com/58368119/214177913-128e5881-06e0-4169-b532-e090f03dc00e.png)

After getting the hsv range for different colors, I created masks for each color in each frame and used it to track different balls across the frames in the video. </br>

The program keeps track of the timestamp at which each ball enters or exit the frame and shows it on the video itself.

Additionally, the timestamps of different color balls entering or leaving the frame is also saved in a dataframe which can later be saved as a csv / text file.

