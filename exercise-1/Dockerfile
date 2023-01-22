# FROM duckietown/dt-duckiebot-interface:daffy-arm32v8
FROM ubuntu:22.04


ENV DISPLAY=${DISPLAY}

# Don't need the next two if you're using the duckiebot interface
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential ffmpeg libsm6 libxext6  



COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY color_detector.py .

CMD python3 ./color_detector.py

