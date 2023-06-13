import cv2
import numpy
import numpy as np


def setValues(x):
    print("x")


cv2.namedWindow("Invisible Cloak")
cv2.createTrackbar("Upper Hue", "Invisible Cloak", 110, 180, setValues)
cv2.createTrackbar("Upper Saturation", "Invisible Cloak", 255, 255, setValues)
cv2.createTrackbar("Upper Value", "Invisible Cloak", 255, 255, setValues)
cv2.createTrackbar("Lower Hue", "Invisible Cloak", 68, 180, setValues)
cv2.createTrackbar("Lower Saturation", "Invisible Cloak", 55, 255, setValues)
cv2.createTrackbar("Lower Value", "Invisible Cloak", 54, 255, setValues)


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    while True:
        cv2.waitKey(1000)
        ret, init_frame = cap.read()
        if ret:
            break

    # Iterate until the user presses the ESC key
    while True:
        try:
            # frame = get_frame(cap)
            ret, frame = cap.read()

            # Convert the HSV colorspace
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            u_hue = cv2.getTrackbarPos("Upper Hue", "Invisible Cloak")
            u_saturation = cv2.getTrackbarPos("Upper Saturation", "Invisible Cloak")
            u_value = cv2.getTrackbarPos("Upper Value", "Invisible Cloak")

            l_hue = cv2.getTrackbarPos("Lower Hue", "Invisible Cloak")
            l_saturation = cv2.getTrackbarPos("Lower Saturation", "Invisible Cloak")
            l_value = cv2.getTrackbarPos("Lower Value", "Invisible Cloak")

            kernel = np.ones((3, 3), numpy.uint8)

            # Define 'color' range in HSV colorspace
            Upper_hsv = np.array([u_hue, u_saturation, u_value])
            Lower_hsv = np.array([l_hue, l_saturation, l_value])

            # Threshold the HSV image to get only selected color
            mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)

            # Bitwise AND mask and original image
            res = cv2.medianBlur(mask, 3)
            res_inv = 255-res
            res = cv2.dilate(res, kernel, 5)

            b = frame[:, :, 0]
            g = frame[:, :, 1]
            r = frame[:, :, 2]

            b = cv2.bitwise_and(res_inv, b)
            g = cv2.bitwise_and(res_inv, g)
            r = cv2.bitwise_and(res_inv, r)
            frame_inv = cv2.merge((b, g, r))

            b = init_frame[:, :, 0]
            g = init_frame[:, :, 1]
            r = init_frame[:, :, 2]

            b = cv2.bitwise_and(b, res)
            g = cv2.bitwise_and(g, res)
            r = cv2.bitwise_and(r, res)
            blanket_area = cv2.merge((b, g, r))

            final_frame = cv2.bitwise_or(frame_inv, blanket_area)

            cv2.imshow("Invisible Cloak", final_frame)
            cv2.imshow("Original", frame)

            # Check if the user pressed ESC key
            c = cv2.waitKey(5)
            if c == 27:
                break
        except KeyboardInterrupt as e:
            print(str(e))
            print("Turning off camera.")
            cap.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
