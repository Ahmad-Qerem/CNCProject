import cv2
captchaer = cv2.VideoCapture("http://192.168.1.9:8080/video")

while True:

    _, frame = captchaer.read()
    cv2.imshow("test",frame)

    if cv2.waitKey(1) == ord('q'):
        break

captchaer.release()
cv2.destroyAllWindows()