# FROM python:3.9

# # Install dependencies
# RUN apt-get update && apt-get install -y \
# libopencv-dev 
# #libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test


# # Install Python dependencies
# RUN pip install opencv-python numpy paho-mqtt 


# WORKDIR /app
# COPY . /app

# CMD ["python", "TrackingLight.py"]



FROM python:3.9

# Install system dependencies required for PiCamera
RUN apt-get update && apt-get install -y 

# Install Python dependencies
RUN pip install opencv-python numpy paho-mqtt 


WORKDIR /app
COPY . /app

CMD ["python", "piCameraPython.py"]

