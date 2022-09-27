import requests
import torch
import cv2 as cv
import os
import json
import config as cfg


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
    url = 'https://fivesafe-warning.5hojhh7jd94bq.eu-central-1.cs.amazonlightsail.com/api/WarningIssuer/IssueWarningStatus'
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
        # xmin, ymin, xmax, ymax, confidence, class
        # TODO Classname instead of name
        
        # Show Camstream
        #res_img = results.imgs[0]
        #res_img = cv.cvtColor(res_img, cv.COLOR_RGB2BGR)
        #cv.imshow("Detection", res_img)
        #cv.waitKey(1)

        print(results.xyxy[0])
        

        counter = 0
        for entries in res_list:
            if(entries[5] == 0):
                counter += 1
        
        if (counter >= threshhold):
            crowded = True
        else:
            crowded = False

        #TODO Local Config

        if previous_crowded != crowded:
            print('state change!')
            #headers = {'accept': '*/*', 'Content-type': 'application/json'}
            #payload = json.dumps(crowded)
            #payload = json.dumps({"crowded": crowded, "object_list": res_list})
            #r = requests.post(url, headers=headers, data=payload)
            #print('request done: ', r)
            #print(r.json())
            

        k = cv.waitKey(1)
        if k == 27:
            input.release()
            break
        #return crowded


if __name__ == "__main__":
    threshold = int(os.environ['threshold']) if 'threshold' in os.environ else cfg.THRESHOLD
    api_url = os.environ['API_URL'] if 'API_URL' in os.environ else cfg.API_URL
    api_port = os.environ['API_PORT'] if 'API_PORT' in os.environ else cfg.API_PORT

    print('starting app with threshold {0} on url {1}:{2}'.format(threshold, api_url, api_port))

    crowded_detection(cv.VideoCapture(0), threshold, api_url, api_port)
    
