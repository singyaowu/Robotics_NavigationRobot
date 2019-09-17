#!/usr/bin/env python
from __future__ import print_function
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv_bridge
import face_recognition
import time
import threading

detect_pub = rospy.Publisher("face_detect", String, queue_size=1)


def image_callback(data):
    bridge = cv_bridge.CvBridge()

    try:
        image = bridge.imgmsg_to_cv2(data, "bgr8")
    except cv_bridge.CvBridgeError as e:
        print(e)
    
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_image = image[:, :, ::-1]
    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_image)

    # Loop through each face in this frame of video
    for face_location in face_locations:

    # Print the location of each face in this image
        top, right, bottom, left = face_location
        name = "Person"
        # Draw a box around the face
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        # Draw a label with a name below the face
        cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow("Image window", image)


    # Publishe the message to the topic 
    if len(face_locations) > 0:
        string = "Detected"
        print("extract_from_kinect.py: Face detected")
        detect_pub.publish(string)
        #rospy.signal_shutdown("face detected")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        return

def extract_image():
    rospy.init_node("image", anonymous=True, disable_signals=True)

    #t = threading.Thread(target=cal_time)
    #t.start()

    rospy.Subscriber("/camera/rgb/image_color", Image, image_callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == "__main__":
    try:
        extract_image()
    except rospy.ROSInterruptException:
        print("Keyboard Interrupt")