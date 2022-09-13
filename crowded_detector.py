import torch
import cv2 as cv

def crowded_detection(input, threshhold):
    """
    This Function detects people and classifies crowded siituations
    Input: input (Video Capture Objects)
           threshhold: number of people the situation is definded as crowded
    Output: Boolean if Situation is crowded (True) or not (False)
    
    """

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    while(input.isOpened()):
        ret, frame = input.read()

        if ret is False:
            raise Exception("No Video Capture Input available")
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        results = model(frame)

        res_list = results.xyxyn[0].data
        
        # Show Camstream
        print(results) 
        #res_img = results.imgs[0]
        #res_img = cv.cvtColor(res_img, cv.COLOR_RGB2BGR)
        #cv.imshow("Detection", res_img)
        #cv.waitKey(1)
        

        counter = 0
        for entries in res_list:
            if(entries[5] == 0):
                counter += 1
        
        if (counter >= threshhold):
            crowded = True
        else:
            crowded = False

        k = cv.waitKey(1)
        if k == 27:
            input.release()
            break
        print(crowded)
        #return crowded


if __name__ == "__main__":
    crowded_detection(cv.VideoCapture(0), 1)
    
