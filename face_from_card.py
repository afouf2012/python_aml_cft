import cv2

ModelPath = 'deepface/tests/dataset/'


def CropImageCard(imagePath):
    # Read the input image
    img = cv2.imread(imagePath)

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load the cascade
    face_cascade = cv2.CascadeClassifier(
        r'C:\Users\ahmed\PycharmProjects\extractFaceFromId\venv\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw rectangle around the faces and crop the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        faces = img[y:y + h, x:x + w]
        #cv2.imshow("face", faces)
        cv2.imwrite('face.jpg', faces)

    cv2.rectangle(img, (270, 150), (470, 200), (0, 0, 255), 2)
    cv2.rectangle(img, (270, 230), (470, 280), (0, 0, 255), 2)

    # img( y ,x )
    firstname = img[150:200, 270:470]
    #cv2.imshow("firstname", firstname)
    cv2.imwrite('firstname.jpg', firstname)

    lastname = img[230:280, 270:470]
    #cv2.imshow("lastname", lastname)
    cv2.imwrite('lastname.jpg', lastname)

    conduct_id = img[100:145, 290:470]
    #cv2.imshow("conduct_id", conduct_id)
    cv2.imwrite('conductId.jpg', conduct_id)

    birthdate = img[280:320, 460:620]
    # cv2.imshow("birthdate", birthdate)
    cv2.imwrite('birthdate.jpg', birthdate)

    cin = img[325:360, 690:830]
    # cv2.imshow("cin", cin)
    cv2.imwrite('cin.jpg', cin)
    #
    # # Display the output
    # cv2.imwrite('image_croped.jpg', img)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
