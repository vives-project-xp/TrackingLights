FROM python:3.9

# Install dependencies
# RUN apt-get update && apt-get install -y 
# libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test

# Cleanup
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Python dependencies
RUN pip install opencv-python-headless numpy paho-mqtt

WORKDIR /app
COPY . /app

CMD ["python", "TrackingLight.py"]
