import requests
import logging
import torch
import cv2
import json
from src.my_utils import convert_yolo_preds


class CrowdedDetector():
    def __init__(self, threshold, api_url, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.threshold = threshold
        self.api_url = api_url
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.crowded_flg = False


    def is_crowded(self, labels):
        return True if len(labels) >= self.threshold else False


    def set_crowded_flg(self, labels):
        self.crowded_flg = True if self.is_crowded(labels) else False


    def get_result(self, boxes, labels, scores):
        return json.dumps({
            "crowded": self.crowded_flg,
            "object-list": {
                "boxes": boxes,
                "labels": labels,
                "scores": scores
            }
        })


    def send_json_message_to_frontend(self, json_message):
        headers = {'accept': '*/*', 'Content-type': 'application/json'}
        payload = json_message
        try:
            res = requests.post(self.api_url, headers=headers, data=payload)
            self.logger.debug('sent request to server with response: {}.'.format(res.json()))
            self.logger.info('successfully sent data.')
        except:
            self.logger.info("Somewith went wrong.. cannot reach server..")
        return


    def detect(self, input):
        """
        This Function detects people and classifies crowded siituations
        Input: input (Video Capture Objects)
        Output: Sends message to frontend -- Boolean if Situation is crowded (True) or not (False)
        """
        while(input.isOpened()):
            ret, frame = input.read()

            if ret is False:
                raise Exception("No Input available..")
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            detections = self.model(frame)
            boxes, labels, scores = convert_yolo_preds(detections.xyxy[0].data)
    
            self.set_crowded_flg(labels)

            result = self.get_result(boxes, labels, scores)
            self.send_json_message_to_frontend(result)
    
            cv2.waitKey(1)
        return 1


