import cv2

#Now creates an OpenCV image
image = cv2.imread("image.jpg")#cv2.imdecode(buff, 1)

#Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier('faces.xml')

#Convert to grayscale
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#Look for faces in the image using the loaded cascade file
faces = face_cascade.detectMultiScale(gray, 1.1, 5)

print("Found "+str(len(faces))+" face(s)")
##
##if len(faces) > 0:
##    run_command("fire", tdelay)
##

#Draw a rectangle around every found face
for (x,y,w,h) in faces:
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)


#Save the result image
cv2.imwrite('result.jpg',image)

#show image
cv2.imshow("image",image)
