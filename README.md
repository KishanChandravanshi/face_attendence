# face_attendence

## Note: This model will work only on Ubuntu or MacOS platform

<p>
  
<b> To know the requirements please see the requirements.txt file</b>

 Make sure you have <b>opencv</b> and <b>face_recognition</b> installed on your system, if not follow the steps. To check open your terminal and type:
 <br>
 `$python3`
 <br>
 `$import cv2`
 <br>
 if you don't get any errors it means it's already installed, now check for face_recognition library
 <br>
 `$import face_recogniton`
 <br>
 again, no errors means already installed,
 <br>
 if you do get errors follow the following steps mentioned below:
<br>

 Open the terminal, and type the following commands
 <br>
 `$pip3 install opencv-python`
 <br>
 `$pip3 install face_recognition`
 
</p>

### Step-1

<p>
  <ul>
    <li> <i>First we will make encodings of all the images that have been registered before</i></li>
    <li> <i>To register a user simply put their image in registered folder with enrolment number as the name of image</i></li>
    <li> <i>There is a folder named registered user, in that folder we will have all the people that are registered previously, the file are named based on their enrolment number</i></li>
  </ul>
 <b>for e.g. kishan's image will be named 124125512.jpg, where 124125512 is the enrolment number</b>
</p>

### Step-2
<ul>
<li> <i>Run the model, it will show the enrolment number if you are already registered otherwise it will show unregistered user</i></li>
  <li><i> To quit the scanning process simply press 'q'</i> </li>
  <li> <i>You will get a txt file named <b>present.txt</b>, that will contain the ennrolment of those that were processed in the frame and identified correclty by the model</i></li>
  </ul>
