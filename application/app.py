import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import requests
import json
import os
import hashlib
from streamlit_extras.switch_page_button import switch_page
from utils.cert_utils import extract_certificate, generate_certificate
from utils.streamlit_utils import view_certificate
from connection import contract, w3
from utils.streamlit_utils import displayPDF, hide_icons, hide_sidebar, remove_whitespaces, remove_fullscreen_button, button_styler
############################################################

#page config
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
#handmade - called from streamlit_utils
hide_icons()
hide_sidebar()
remove_whitespaces()
remove_fullscreen_button()
button_styler()

# !!! To investigate (?)
load_dotenv()
############################################################

#######  Page Elements:
        
############################################################

#University banner & Page Title
institute_banner = Image.open("../assets/institute_banner.png")
st.image(institute_banner, output_format="png", width=550)
st.title("ECE Diploma Validation System")
st.divider()
############################################################

#Title for public - validator
st.subheader("📜 View & Validate Certificates - Public 📜")

#View & Verify certificates Area
options = ("Verify Certificate using PDF", "View/Verify Certificate using Certificate ID")
selected = st.selectbox("", options, label_visibility="hidden")
if selected == options[0]:
    uploaded_file = st.file_uploader("Upload the PDF version of the certificate")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with open("certificate.pdf", "wb") as file:
            file.write(bytes_data)
        try:
            (grad_number, candidate_name, place_of_birth, diploma_mark) = extract_certificate("certificate.pdf")
            displayPDF("certificate.pdf")
            os.remove("certificate.pdf")

            # Calculating hash
            data_to_hash = f"{grad_number}{candidate_name}{place_of_birth}{diploma_mark}".encode('utf-8')
            certificate_id = hashlib.sha256(data_to_hash).hexdigest()

            # Smart Contract Call
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificated validated successfully!")
            else:
                st.error("Invalid Certificate! Certificate might be tampered")
        except Exception as e:
            st.error("Invalid Certificate! Certificate might be tampered")
elif selected == options[1]:
    form_validate = st.form("Validate-Certificate")
    certificate_id = form_validate.text_input("Enter the Certificate ID")
    submit = form_validate.form_submit_button("Validate")
    if submit:
        try:
            view_certificate(certificate_id)
            # Smart Contract Call
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificated validated successfully!")
            else:
                st.error("Invalid Certificate ID!")
        except Exception as e:
            st.error("Invalid Certificate ID!")
############################################################

st.divider()
#Title for uni personel - Generator
st.subheader("🎓 Generate Certificate - for University personel only 🎓")

#Form setup(?)
form_login = st.form("login")
email = form_login.text_input("Enter your email")
password = form_login.text_input("Enter your password", type="password")
submit = form_login.form_submit_button("Login")
#Uni credentials check - Admin login
if submit:
        valid_email = os.getenv("institute_email")
        valid_pass = os.getenv("institute_password")
        if email == valid_email and password == valid_pass:
            switch_page("institute")
        else:
            st.error("Invalid credentials!")
############################################################