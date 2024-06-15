import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile

def text_detection(inputfile,outputfile):
    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(inputfile)

    # Retrieve video properties: width, height, and frames per second
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

    # Initialize video writer to save the output video with the specified properties
    out = cv2.VideoWriter(outputfile, cv2.VideoWriter_fourcc(*"MJPG"), fps, (w, h))

    while True:
        # Read a frame from the video
        ret, im0 = cap.read()
        if not ret:
            print("Video frame is empty or video processing has been successfully completed.")
            break
        res = model.predict(im0,conf=0.5,save=True)
        res_plotted = res[0].plot()[:, :, ::-1]
        out.write(res_plotted)
    st.video(data=outputfile)


def app():
    st.title("Upload the video and Click on the Detect Button")
    file = st.file_uploader("Upload PDF file",type=("mp4"))
    if file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name

        st.video(data=file)
    button= st.sidebar.button("Detect")
    output_Path = r"C:\Users\searra\OneDrive - Prolifics Corporation Ltd.,\Desktop\Quick_UI\ouput.mp4"
    if button:
        text_detection(temp_file_path,output_Path)
