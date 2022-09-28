import cv2
import config as cfg
import os, logging, sys
from src.crowded_detector import CrowdedDetector


def main(threshold, api_url, input_capture):
    logging.basicConfig(stream=sys.stderr, level=cfg.LOGGING_MODE)
    print('starting app with threshold {0} on url {1}'.format(threshold, api_url))
    detector = CrowdedDetector(threshold, api_url)
    detector.detect(input_capture)

if __name__=='__main__':
    threshold = int(os.environ['threshold']) if 'threshold' in os.environ else cfg.THRESHOLD
    api_url = os.environ['API_URL'] if 'API_URL' in os.environ else cfg.API_URL
    input_capture = cv2.VideoCapture(0)

    main(threshold, api_url, input_capture)
