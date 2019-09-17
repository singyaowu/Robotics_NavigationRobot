#!/usr/bin/env python
from __future__ import print_function
import roslib
import rospy
import actionlib
import pygame
import time
from sensor_msgs.msg import Image
import subprocess
from std_msgs.msg import String
import cv_bridge
import cv2
from threading import Lock
#move_base_msgs
from move_base_msgs.msg import *

number = [
        [-10.4856575, 1.6023758, 0.3547281, 0.9349695],   # 413
        [-8.8595602, 0.171826564, 0.4369427, 0.8994894], # left 412
        [-2.5813604, -7.24782841, 0.360037238, 0.932937933]  #right 412 
    ]
not_detected = True
occupied = False
cnt = 1

#number = [
#        [2.68418028507, 6.32836545207, 0.995296423679, 0.0968763594063],   # 251
#        [2.97993330195, 7.78973598536, 0.989846215693, 0.142142426034],     # 252
#        [5.90723436272, 11.3865553893, -0.259246136482, 0.965811286287],    # 255
#        [4.65333389466, 8.9399562701, -0.268687279702, 0.963227463129],     # 254
#        [3.67297275746, 5.9756919696, -0.274823414105, 0.961494717125]      # 255
#            ]

#between = [
#    [5.93028237029, 11.497519954, -0.827577087007, 0.561277344421], #after 255
#    [4.6901158, 8.90323, -0.762108, 0.64744938], #after 254
#    [3.6016501, 6.0969845, -0.8243698, 0.566051] #after 253
#]

def detect_callback(data):
    global not_detected, occupied, cnt, lock
    
    lock.acquire()
    if cnt == 1:
        cnt = 0
    lock.release()
    #pygame.mixer.music.stop()
    #occupied = True
    return 0

def image_callback(data):
    bridge = cv_bridge.CvBridge()
    
    try:
        image = bridge.imgmsg_to_cv2(data, "bgr8")
    except cv_bridge.CvBridgeError as e:
        print(e)


    # Display the resulting image
    
    cv2.imshow("Image window", image)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        return
    

def simple_move():
    global not_detected, cnt, lock
            
    #Simple Action Client
    sac = actionlib.SimpleActionClient('move_base', MoveBaseAction )

    #create goal
    goal = MoveBaseGoal()
    #rate = rospy.Rate(10)
    i = 0
    while not rospy.is_shutdown():
        '''
        #set goal
        not_detected = True
        goal.target_pose.pose.position.x = number[i][0]
        goal.target_pose.pose.position.y = number[i][1]
        goal.target_pose.pose.orientation.z = number[i][2]
        goal.target_pose.pose.orientation.w = number[i][3]
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()

        #start listner
        sac.wait_for_server()

        #send goal
        sac.send_goal(goal)

        #finish
        result = sac.wait_for_result()
        
        #print result
        print(result)#sac.get_result())
        
        
        '''
        result = True
        print("Round", i)
        if result:
            lock.acquire()
            cnt = 1
            lock.release()
            start_time = time.time()
            pygame.mixer.music.load('/home/shinyao/catkin_ws/knock.mp3')
            pygame.mixer.music.play(-1)

            '''
            if i != 1:
                while time.time() - start_time < 20.0:    
                    pass
            else:
                time.sleep(20)

                if cnt == 0:
                pygame.mixer.music.load('/home/shinyao/catkin_ws/newyear.mp3')
                pygame.mixer.music.play(-1)
                print('i see you')
    
                time.sleep(10)
        
                print("Ready to leave the door")
            '''

            while time.time() - start_time < 20.0:
                if cnt == 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('/home/shinyao/catkin_ws/newyear.mp3')
                    pygame.mixer.music.play(-1)
                    print('i see you')

                    time.sleep(10)
                    break





            pygame.mixer.music.stop()
            #time.sleep(11)
            #cv2.destroyAllWindows()
            #not_detected = True
        else:
            print("failed to reach goal")
        
        print("Round",i," bye")
        i += 1
        if i >= len(number):
            return
        #rate.sleep()

'''
goal.target_pose.pose.position.x = 3.42265447927
goal.target_pose.pose.position.y = 1.09429176934
goal.target_pose.pose.orientation.z = -0.491279655277
goal.target_pose.pose.orientation.w = 0.871001894551
'''


if __name__ == '__main__':
    try:
        lock = Lock()
        pygame.init()
        
        #pygame.mixer.music.play(0)
             
        rospy.init_node('simple_move')
        rospy.Subscriber("face_detect", String, detect_callback)
        #rospy.spin()
        simple_move()
    except rospy.ROSInterruptException:
        print("Keyboard Interrupt")
