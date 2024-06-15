import streamlit as st
from ultralytics import YOLO
import PIL

def text_detection(file):
    model = YOLO("yolov8n.pt")
    uploaded_image = PIL.Image.open(file)
    res = model.predict(uploaded_image,conf=0.5,save=True)
    box = res[0].boxes.xyxy.tolist()
    res_plotted = res[0].plot()[:, :, ::-1]
    st.image(res_plotted, caption='Text Detections',use_column_width=True)
    st.write("Number of the Detections : "+str(len(box)))
    return uploaded_image


def app():
    st.title("Upload the image and Click on the Detect Button")
    file = st.file_uploader("Upload PDF file",type=("jpg", "jpeg", "png"))
    if file is not None:
        st.image(image=file,caption='Selected Plan',use_column_width=True)
    button= st.sidebar.button("Detect")
    if button:
        text_detection(file)
