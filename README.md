# Commands (linux)
- xhost local:docker
- docker build -t "crowded_detector" .
- docker run -it --device="/dev/video0:/dev/video0" -e threshold=5 "crowded_detector" [--network="host"]
