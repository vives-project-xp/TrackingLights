FROM balenalib/raspberry-pi-python:3.8-buster-build

# Install dependencies
RUN apt-get update && \
    apt-get install -y libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test

# Install Python dependencies
RUN pip install opencv-python-headless numpy paho-mqtt

# Cleanup
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app
COPY . /app

CMD ["python", "TrackingLight.py"]
