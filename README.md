# Commands (linux)
- xhost local:docker
- docker build -t "crowded_detector" .
- docker run -it --device="/dev/video0:J/dev/video0" "crowded_detector" 
