FROM python:3.9

# Install dependencies
RUN apt-get update && apt-get install -y \
libopencv-dev 

# Install Python dependencies
RUN pip install opencv-python numpy paho-mqtt picamera


WORKDIR /app
COPY . /app

CMD ["python", "piCameraPython.py"]



# FROM python:3.9

# # Install system dependencies required for PiCamera
# RUN apt-get update && apt-get install -y \
# #libopencv-dev 

# # Install Python dependencies
# RUN pip install opencv-python numpy paho-mqtt picamera[array]


# WORKDIR /app
# COPY . /app

# CMD ["python", "piCameraPython.py"]

