import cv2
import os
import HandsTrackingModule as hand
import threading
from random import choice

seconds=5
stop_thread = False
choice_done = False

def event_play():
    global seconds, stop_thread,choice_done
    if not stop_thread:
        seconds-=1
        if seconds<0:
            seconds=5
            choice_done=False
        threading.Timer(1,event_play).start()


def main():
    global seconds,stop_thread,choice_done
    cap = cv2.VideoCapture(0)

    computer_fingers,user_fingers=0,0

    c_point,u_point=0,0

    # Getting the images of hands
    images = os.listdir("Fingers")
    overlayImages = []
    for i in images:
        resizeImg = cv2.resize(cv2.imread(f"Fingers/{i}"), (200, 250))
        overlayImages.append(resizeImg)

    pTime = 0
    game_text={
        0:"Stone",
        2:"Sissor",
        5:"Paper"
    }
    # List of the fingertips Landmarks
    tipList = [4, 8, 12, 16, 20]

    detector = hand.HandDetector(min_detection_confidence=0.75, max_hands=1)

    event_play()

    while True:
        success, img = cap.read()

        # Drawing landmarks and connections
        detector.DrawHands(img, draw=False)

        # Getting all the position of the landmarks
        lmList = detector.givePosition(img=img, draw=False)


        if seconds>0:
            cv2.putText(img, str(seconds), (20, 100), cv2.FONT_HERSHEY_PLAIN, 8, (0, 255, 0), 5)

        # check that the returned list is empty or not
        if len(lmList) != 0:

            countList = []

            # Checking the thumb is open or closed using x axis
            if lmList[tipList[0]][1] > lmList[tipList[0]-1][1]:
                countList.append(1)
            else:
                countList.append(0)

            # Checking the fingers are open or closed using y axis
            for i in range(1, 5):
                if lmList[tipList[i]][2] < lmList[tipList[i]-2][2]:
                    countList.append(1)
                else:
                    countList.append(0)

            # Counting the total open fingers
            totalFingers = countList.count(1)

            # Setting the particular hand image on the frame
            if totalFingers in (0,2,5):
                if seconds==0:
                    if not choice_done:
                        user_fingers=totalFingers
                        computer_fingers=choice([0,2,5])
                        computer_choice=game_text.get(computer_fingers)
                        user_choice=game_text.get(user_fingers)
                        choice_done=True

                        if computer_choice=="Paper" and user_choice=="Sissor":
                            u_point+=1
                        elif computer_choice=="Sissor" and user_choice=="Paper":
                            c_point+=1
                        elif computer_choice=="Sissor" and user_choice=="Stone":
                            u_point+=1
                        elif computer_choice=="Stone" and user_choice=="Sissor":
                            c_point+=1
                        elif computer_choice=="Stone" and user_choice=="Paper":
                            u_point+=1
                        elif computer_choice=="Paper" and user_choice=="Stone":
                            c_point+=1


                    # User Choice
                    h, w, c = overlayImages[user_fingers-1].shape
                    img[0:h, 0:w] = overlayImages[user_fingers-1]
                    # Computer Choice
                    h, w, c = overlayImages[computer_fingers-1].shape
                    h=h+230
                    img[230:h, 0:w] = overlayImages[computer_fingers-1]

                    cv2.putText(img, game_text.get(totalFingers), (150, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
                    cv2.putText(img, game_text.get(computer_fingers), (150, 475), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)

                    cv2.line(img, (203, 0), (203,600), (0, 0, 0), 3) 


        cv2.rectangle(img, (510, 0), (700, 600), (0, 225, 0), cv2.FILLED)
        cv2.putText(img, str(u_point), (525, 160), cv2.FONT_HERSHEY_PLAIN, 10, (0, 0, 0), 5)
        cv2.putText(img, "Player", (525, 220), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

        cv2.putText(img, str(c_point), (525, 395), cv2.FONT_HERSHEY_PLAIN, 10, (0, 0, 0), 5)
        cv2.putText(img, "Robot", (525, 445), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

        cv2.line(img, (510, 0), (510,600), (0, 0, 0), 3) 
        cv2.line(img, (510, 250), (700,250), (0, 0, 0), 3) 

        # Showing the Image
        cv2.imshow("Finger Counter", img)

        # On 'q' press the loop breaks
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_thread=True
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()