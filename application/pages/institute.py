import streamlit as st
import requests
import json
from PIL import Image
import os
from dotenv import load_dotenv
import hashlib
from utils.cert_utils import generate_certificate
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

#Pinata keys - call from .env
api_key = os.getenv("PINATA_API_KEY")
api_secret = os.getenv("PINATA_API_SECRET")

# Function to upload file to pinata - !!! Investigate
def upload_to_pinata(file_path, api_key, api_secret):
    # Set up the Pinata API endpoint and headers
    pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }

    # Prepare the file for upload
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file)}

        # Make the request to Pinata
        response = requests.post(pinata_api_url, headers=headers, files=files)

        # Parse the response
        result = json.loads(response.text)

        if "IpfsHash" in result:
            ipfs_hash = result["IpfsHash"]
            print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
            return None
############################################################

#Form Options - Generate or View
options = ("Έκδωση Νέου Πιστοποιητικού", "Επισκόπηση Πιστοποιητικού")
selected = st.selectbox("", options, label_visibility="hidden")

#Applies options: Generate
if selected == options[0]:
    # forn wating for user input
    form = st.form("Generate-Certificate", clear_on_submit=True)
    candidate_name = form.text_input(label="Ονοματεπώνυμο και Πατρώνυμο (πχ: ΣΤΡΑΤΟΣ ΛΑΪΝΑΣ ΤΟΥ ΑΛΕΞΑΝΔΡΟΥ)")
    grad_number = form.text_input(label="Αριθμός Μητρώου Διπλωματούχου")
    place_of_birth = form.text_input(label="Τόπος Γέννησης")
    diploma_mark_num = form.number_input(label="Βαθμός", min_value=5.00, max_value=10.00)
    diploma_mark = form.text_input(label="Βαθμός (ολογράφως)")
    # Submit - Button and Function
    submit = form.form_submit_button("Υποβολή")
    if submit:
        pdf_file_path = f"certificate{grad_number}.pdf"
        institute_logo_path = "../assets/logo.jpg"
        generate_certificate(pdf_file_path, grad_number, candidate_name, place_of_birth, diploma_mark, institute_logo_path)

        # Upload the PDF to Pinata
        ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
        os.remove(pdf_file_path)
        data_to_hash = f"{grad_number}{candidate_name}{place_of_birth}{diploma_mark}".encode('utf-8')
        certificate_id = hashlib.sha256(data_to_hash).hexdigest()

        # Smart Contract Call
        contract.functions.generateCertificate(certificate_id, grad_number, candidate_name, place_of_birth, diploma_mark, ipfs_hash).transact({'from': w3.eth.accounts[0]})
        st.success(f"Certificate successfully generated with Certificate ID: {certificate_id}")

else:
    form = st.form("View-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Submit")
    if submit:
        try:
            view_certificate(certificate_id)
        except Exception as e:
            st.error("Invalid Certificate ID!")
        
