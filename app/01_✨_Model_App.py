"""App main page."""
import helper
import PIL
import settings
import streamlit as st

# Setting page layout
st.set_page_config(
    page_title="Fire Gun Detection",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Main page heading
st.title("Object Detection using YOLOv8")

# Sidebar
st.sidebar.header("ML Model Config")

# Model Options
model_path = st.sidebar.selectbox(
    "Choose de model to load:",
    [f"{settings.MODELS}large.pt", f"{settings.MODELS}small.pt"],
    index=0,
)

confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)
st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio("Select Source", settings.SOURCES_LIST)
source_img = None

# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", "bmp", "webp")
    )
    col1, col2 = st.columns(2)
    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                uploaded_image = PIL.Image.open(default_image_path)
                st.image(
                    default_image_path, caption="Default Image", use_column_width=True
                )
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image", use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)
    with col2:
        if st.sidebar.button("Detect Objects"):
            res = model.predict(uploaded_image, conf=confidence)
            boxes = res[0].boxes
            res_plotted = res[0].plot()[:, :, ::-1]
            st.image(res_plotted, caption="Detected Image", use_column_width=True)
            try:
                with st.expander("Detection Results"):
                    for box in boxes:
                        st.write(box.data)
            except Exception:
                # st.write(ex)
                st.write("No image is uploaded yet!")

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

else:
    st.error("Please select a valid source type!")
