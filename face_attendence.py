import cv2
import face_recognition
import glob

# Note: This model will work only on Ubuntu or MacOS platform


# first we will make encodings of all the images that have been registered before,
# to register a user simply put their image in registered folder with enrolment number as the name of image
# there is a folder named registered user, in that folder we will have all the people that are registered previously
# the file are named based on their enrolment number
# for e.g. kishan's image will be named 124125512.jpg, where 124125512 is the enrolment number
# there will be a dictionary though which we will get the name based on the enrolment number

# step-1
# get the image path and their names
paths = glob.glob("registered_users/*.jpg")
image_names = []
for path in paths:
    temp = path.split("/")[1]
    image_names.append(temp.split(".")[0])


print(image_names)

# step-2 load the image and store their encodings into a list
registered_encodings = []
for path in paths:
    image = face_recognition.load_image_file(path)
    encoding_of_image = face_recognition.face_encodings(image)[0]
    # as we know that all these registered images contains only one image that is why we are selecting first encoding
    # say a photo consist of more than one face then also the [0] index will select only one encoding
    # add this encoding to the registered_encodings
    registered_encodings.append(encoding_of_image)

# now we have the encoding of the all registered users in registered_encodings

# now we will scan for the input if the registered user came then we this model will recognize them because
# it has their encodings and it will mark their attendence
# if an unregistered user it won't recognize them and won't do anything
# at the end of the program we will get a text file having all those that were present

# processing an image through camera is very costly so instead of checking every frame we will only check the other frame
# that is if first frame has been processed then second frame will not be processed and after that third frame will be processed

# the image that we will read can have more than one faces so we need to take care of that also
face_locations = []
face_encodings = []
face_enrolments = []
temp_enrolments = []
enrolment_found = "unregistered_user"
# let me explain every variable to you,
# face_locations is a list which will contain all the face location in the image, say if the image has three faces then it will contain the location of three faces
# face_encodings is also a list it will basically find the encodings of those faces that were find the input image based on their locations
# face_enrolment is a list that will update whenn there is a registered user is encountered

# for e.g. if a registered user comes then their face location will be stored in the list and their encoding based on the
# face location will be stored in the face_encodings, which then will be compared to the list of registered_encodings
# if the encoding matched then their enrolment will be listed in the face_enrolment

# step-3 
# get the image from camera
video_capture = cv2.VideoCapture(0)

# as we don't want every frame to be processed we will create a variable
should_i_process_this = True

while True:
    # get a single frame from the video
    ret, frame = video_capture.read()
    # here ret hold bool which suggest whether we were successfull in reading the image

    # as the size of the image could be large, so we need to resize the image so that we can process the image fastly
    # we will resize the image by a factor of 4
    resized_frame = cv2.resize(frame, (0, 0), fx=1 / 4, fy=1 / 4)

    # now we have got our resized frame, but their is a problem with the color encoding
    # OpenCV uses BGR but the face_recognition uses RGB, so we need to manipulate that
    # as you know if we can reverse the current color encoding(BGR) we can get the required result(RGB)
    # to reverse a list we use python [::-1] feature
    # for e.g. if you want to reverse a string A = "Hello", just type B = A[::-1] and it will print B = "olleH"

    rgb_resized_frame = resized_frame[:, :, ::-1]

    # check whether we need to process this frame
    if should_i_process_this:
        # now find all the face locations in the current image
        face_locations = face_recognition.face_locations(rgb_resized_frame)
        # now get the encodings of all the face based on their location
        face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations)
        # face_encodings("photo","face_locations")

        # now check whether these encodings match with our encodings or not
        for encoding in face_encodings:
            # check this encoding with the registered_encoding, if this matches then mark the attendance
            match_list = face_recognition.compare_faces(registered_encodings, encoding)
            # match_list will be a list containing a list of True and False
            # if there will be a match then there will be a True present in it otherwise every element will be False
            enrolment_found = "unregistered_user"  # initialise
            temp_enrolments = []
            if True in match_list:
                # it means there is a True in the list so we have at least one employee matched
                # but it may also be possible that more than two matches occur, but we will only mark attendence one at time
                first_match = match_list.index(True)  # this will return the index
                enrolment_found = image_names[first_match]

            face_enrolments.append(enrolment_found)
            temp_enrolments.append(enrolment_found)

    should_i_process_this = not should_i_process_this  # do not process the next frame

    # Now to end the process we need something, because it cannot go for infinite
    # if user present 'q' key it will quit the attendance

    # display the result
    for (top, right, bottom, left), name in zip(face_locations, temp_enrolments):
        # scale the image back to it's original size, as we had re-sized it to 1 / 4
        # we need to multiply it by 4
        top *= 4
        right *=4
        bottom *=4
        left *= 4

        # draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        # let's show their enrolment number beneath their image
        cv2.rectangle(frame, (left, bottom - 40), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, enrolment_found, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# turn of the camera
video_capture.release()
cv2.destroyAllWindows()

# now display the result of the attendance
attendance = list(set(face_enrolments))
try:
    attendance.remove("unregistered_user")
    print(attendance)
except:
    print("No records found")

