import requests
import torch
import cv2 as cv
import os


def crowded_detection(input, threshhold, api_url, api_port):
    """
    This Function detects people and classifies crowded siituations
    Input: input (Video Capture Objects)
           threshhold: number of people the situation is definded as crowded
    Output: Boolean if Situation is crowded (True) or not (False)
    
    """

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    url = 'http://{}:{}/api/WarningIssuer/IssueWarningStatus'.format(api_url,
                                                                     api_port)
    print('url: ', url)
    crowded=False
    while(input.isOpened()):
        previous_crowded = crowded

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

        if previous_crowded != crowded:
            print('state change!')
            payload = {'crowded': crowded}
            r = requests.post(url, data=payload)
            print('request done: ', r)
            

        k = cv.waitKey(1)
        if k == 27:
            input.release()
            break
        print(crowded)
        #return crowded


if __name__ == "__main__":
    if os.environ.get('threshold') is not None:
        threshold = int(os.environ['threshold'])
    else:
        threshold = 1

    if os.environ.get('API_URL') and os.environ.get('API_PORT') is not None:
        api_url = os.environ['API_URL']
        api_port = os.environ['API_PORT']
    else:
        api_url = '127.0.0.1'
        api_port = '5000'

    crowded_detection(cv.VideoCapture(0), threshold, api_url, api_port)
    
