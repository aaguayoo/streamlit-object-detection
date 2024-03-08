"""Streamlit app helper functions."""
import cv2
import pafy
import settings
import streamlit as st
from ultralytics import YOLO


def load_model(model_path: str) -> YOLO:
    """Load YOLOv8 model."""
    return YOLO(model_path)


def _display_detected_frames(conf, model, st_frame, image):
    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720 * (9 / 16))))

    # Predict the objects in the image using the YOLOv8 model
    res = model.predict(image, conf=conf)

    # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(
        res_plotted, caption="Detected Video", channels="BGR", use_column_width=True
    )


def play_youtube_video(conf, model):
    """Play YouTube video."""
    source_youtube = st.sidebar.text_input("YouTube Video url")
    if st.sidebar.button("Detect Objects"):
        try:
            video = pafy.new(source_youtube)
            best = video.getbest(preftype="mp4")
            vid_cap = cv2.VideoCapture(best.url)
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(
                        conf,
                        model,
                        st_frame,
                        image,
                    )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error(f"Error loading video: {str(e)}")


def play_stored_video(conf, model):
    """Play stored video."""
    source_vid = st.sidebar.selectbox("Choose a video...", settings.VIDEOS_DICT.keys())
    with open(settings.VIDEOS_DICT.get(source_vid), "rb") as video_file:
        video_bytes = video_file.read()

    if video_bytes:
        st.video(video_bytes)
    if st.sidebar.button("Detect Video Objects"):
        try:
            vid_cap = cv2.VideoCapture(str(settings.VIDEOS_DICT.get(source_vid)))
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(
                        conf,
                        model,
                        st_frame,
                        image,
                    )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error(f"Error loading video: {str(e)}")
