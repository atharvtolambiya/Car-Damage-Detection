import streamlit as st
from model_helper import predict

st.title('Car Damage Detection')
uploaded_image  = st.file_uploader('Upload the images',type = ['jpg','png','jpeg'])
if uploaded_image:
    image_path = 'temp_file.jpg'
    with open(image_path,'wb') as f:

        f.write(uploaded_image.getbuffer())

    st.image(uploaded_image,caption = 'uploaded file',use_container_width=True)
    prediction = predict(image_path)
    st.info(f'predicted class is :{prediction}')