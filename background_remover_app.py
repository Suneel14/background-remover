import streamlit as st
from rembg import remove
from PIL import Image, ImageOps
import io
import requests


def remove_bg(image, bg_color):
    output_image = remove(image)
    img = Image.open(io.BytesIO(output_image)).convert("RGBA")

    colored_bg = Image.new("RGBA", img.size, bg_color + (255,))
    final_img = Image.alpha_composite(colored_bg, img)

    return final_img.convert("RGB")


def main():
    logo_url = "https://i.ibb.co/QMKDV8Z/App-icon.png"
    st.image(logo_url, width=200)
    st.title("Background Removal App")

    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    url = st.text_input("...or paste an Image URL here")

    bg_color = st.color_picker("Choose background color", "#FFFFFF")
    bg_color = tuple(int(bg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    if uploaded_file is not None or url:
        try:
            if uploaded_file is not None:
                image_data = uploaded_file.getvalue()
                original_image = Image.open(io.BytesIO(image_data))
            else:
                response = requests.get(url)
                image_data = response.content
                original_image = Image.open(io.BytesIO(image_data))

            st.image(original_image, caption='Original Image', use_column_width=True)

            with st.spinner('Processing image...'):
                result_image = remove_bg(image_data, bg_color)

            col1, col2 = st.columns(2)

            with col1:
                st.image(original_image, caption='Original Image', use_column_width=True)

            with col2:
                st.image(result_image, caption='Image with Custom Background', use_column_width=True)

            buffered = io.BytesIO()
            result_image.save(buffered, format="PNG")
            st.download_button(label="Download Output Image", data=buffered.getvalue(), mime="image/png")

        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
