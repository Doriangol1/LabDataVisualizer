import cv2;
import pandas as pd


fileName = "/Users/dorian/Documents/Lab/K8061421_SFD_03_1of1_noaudio_re-encoded.mp4"

# Get experiment ID from file name
splitDir = fileName.split("/")
splitString = splitDir[len(splitDir)-1].split("_")
ExperimentID = splitString[0] + "_" + splitString[1] + "_" + splitString[2]
print("Experiment ID: ", ExperimentID)

cap = cv2.VideoCapture(fileName)
csv = "/Users/dorian/Documents/Lab/SFD_dlc_data_500ms_20231004.csv"
data = pd.read_csv(csv)

# Find the first instance of the experiment ID in the csv file
def findExperimentID(data, ExperimentID):
    for i in range(0, len(data["Experiment"])):
        if data["Experiment"][i] == ExperimentID:
            return i

firstIndex = findExperimentID(data, ExperimentID)
index = firstIndex
print("Index: ", index)

if (cap.isOpened() == False):
    print("Error opening video file")

else:

    # Get the frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Frame rate: ", fps)

    # Get the width and height of frame
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Frame size: ", width, "x", height)

    # Get the number of frames in the video file
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Frame count: ", frameCount)

    # Get the duration of the video file
    duration = frameCount / fps
    print("Duration: ", duration, "seconds")

    while cap.isOpened():

        ret, frame = cap.read();

        if ret == True:

            # Get the current time position of the video file in seconds
            timeInSec = cap.get(cv2.CAP_PROP_POS_MSEC) * 0.001
            timeInSec = round(timeInSec, 3)
            cv2.putText(frame, "Time: " + str(timeInSec) + " seconds", (width-400, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 255, 0), 2)
            cv2.putText(frame, "Experiment: " + ExperimentID, (width-400, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 255, 0), 2)
            
            
            BorisState = "rollOver"
            AngleState = "rollOver"
            tRoundedDown = 0
            
            #start by getting correct time (and row index)
            while index < len(data["Experiment"]) and data["Experiment"][index] == ExperimentID and data["seconds"][index] < timeInSec:
                tRoundedDown = data["seconds"][index]
                index += 1
            
            if index - 1 < firstIndex:
                BorisState = "rollOver"
                AngleState = "rollOver"
            else:

                # Get the Boris and Angle states at the current time
                BorisState = data["BORIS_state"][index-1]
                AngleState = data["angle_state"][index-1]
            
            cv2.putText(frame, "Angle state: " + str(AngleState), (width-400, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 255, 0), 2)
            cv2.putText(frame, "BORIS state: " + str(BorisState), (width-400, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 255, 0), 2)
            


            cv2.imshow("Frame", frame)
            # Press Q on keyboard to exit   
            k = cv2.waitKey(10)
            if k == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
