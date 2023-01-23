# AI-Assignment

input video link - https://drive.google.com/file/d/1goI3aHVE29Gko9lpTzgi_g3CZZPjJq8w/view?usp=share_link  </br>
output video link - https://drive.google.com/file/d/1qMfo-UoDiqdeFLn3Mc0IFQAoG_kGzk9A/view?usp=share_link  </br>

the file "assignment.py" can be run as a script which takes arguments as follows : </br>
python assignment.py -v "path to input video file" -o "name of output video file to be specified"  </br>

The program has provision for feeding a new video which can be easily provided as shown above. The processed video is saved on local hard disk whose path can also be provided as shown above.

The video contains 4 balls of different colours which need to be tracked throughout the video. I used openCV to create masks for different color balls using their respective hsv color space. 
