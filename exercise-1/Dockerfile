FROM duckietown/dt-duckiebot-interface:daffy-arm64v8

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY color_detector.py .

CMD python3 ./color_detector.py

