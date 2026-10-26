1. install "ip webcam" on your phone. connect phone + laptop to the same wi-fi and start the stream.

2. activate the venv and the following command to install the required libraries:
   pip install -r requirements.txt

3. copy the video link from the app. put it in a .env file in the blindnav folder:
   CAMERA_STREAM_URL=http://your_phone_ip:port/video

4. add .env to .gitignore so your phone ip doesn't get pushed to github. make sure the code reads camera_stream_url from .env.

5. put your custom yolo model here:
   models/blindnav_best.pt
   create the models folder for your custom models. The pretrained general model is in:
   modals/yolo26n.pt

6. from the blindnav folder, activate .venv and run:
   python test_live_detection.py

7. press q on the detection window to stop.

8. also put the modal name in the.env file as:
   VISION_MODAL=modals/yolo26n.pt
   if custom modal:
   VISION_MODAL=models/modal_name.pt

if the camera doesn't work, check ip webcam and the url in .env. if custom classes don't show up, make sure the code loads models/blindnav_best.pt.