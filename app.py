# app.py
import streamlit as st
from PIL import Image
import numpy as np
import cv2
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Document Scanner", layout="centered")

st.title("📄 Adobe Scan Style Document Scanner")
st.write("Upload a document image, convert it to black & white, and download it as a PDF.")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

def process_image(image):
    """
    Convert image to Adobe Scan style black & white
    """
    # Convert PIL image to OpenCV format
    img = np.array(image)

    # Convert RGB to BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive threshold for scanned effect
    scanned = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return scanned

def save_pdf(image_path, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(0)
    pdf.add_page()

    pdf.image(image_path, x=10, y=10, w=190)

    pdf.output(output_pdf)

if uploaded_file is not None:

    # Open image
    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to Black & White"):

        processed = process_image(image)

        st.subheader("Processed Document")
        st.image(processed, clamp=True, use_container_width=True)

        # Save temporary processed image
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        cv2.imwrite(temp_img.name, processed)

        # Create PDF
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

        save_pdf(temp_img.name, temp_pdf.name)

        # Download button
        with open(temp_pdf.name, "rb") as pdf_file:
            st.download_button(
                label="📥 Download PDF",
                data=pdf_file,
                file_name="scanned_document.pdf",
                mime="application/pdf"
            )

        # Cleanup
        os.unlink(temp_img.name)
        os.unlink(temp_pdf.name)
