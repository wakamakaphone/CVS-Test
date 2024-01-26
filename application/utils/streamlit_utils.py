import streamlit as st
import base64
import requests
import os
from connection import contract

def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

def view_certificate(certificate_id):
    # Smart Contract Call
    result = contract.functions.getCertificate(certificate_id).call()
    ipfs_hash = result[4]

    pinata_gateway_base_url = 'https://gateway.pinata.cloud/ipfs'
    content_url = f"{pinata_gateway_base_url}/{ipfs_hash}"
    response = requests.get(content_url)
    with open("temp.pdf", 'wb') as pdf_file:
        pdf_file.write(response.content)
    displayPDF("temp.pdf")
    os.remove("temp.pdf")

def hide_icons():
    hide_st_style = """
				<style>
				#MainMenu {visibility: hidden;}
				footer {visibility: hidden;}
                .reportview-container {
                margin-top: -2em;}
                #MainMenu {visibility: hidden;}
                .stDeployButton {display:none;}
                footer {visibility: hidden;}
                #stDecoration {display:none;}
				</style>"""
    st.markdown(hide_st_style, unsafe_allow_html=True)

def hide_sidebar():
    no_sidebar_style = """
    			<style>
        		div[data-testid="stSidebarNav"] {visibility: hidden;}
    			
                [data-testid="collapsedControl"] {
                    display: none}
                </style>"""
    st.markdown(no_sidebar_style, unsafe_allow_html=True)

def remove_whitespaces():
    st.markdown("""
        <style>
           .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>""", unsafe_allow_html=True)
    
def remove_fullscreen_button():
    st.markdown("""
    <style>
        button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def button_styler():
    m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #962F34;color:white;font-size:25px;height:2em;width:17em;border-radius:10px 10px 10px 10px;
    
}
</style>""", unsafe_allow_html=True)