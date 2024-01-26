import streamlit as st
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

#page config
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

#to hide sidebar
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

#to hide Deploy button (?)
st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;}
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

#to hide fullscreen button of images
st.markdown("""
    <style>
        button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

#to allign columns
st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1)
        {
            text-align: end;
        } 
    </style>
    """,unsafe_allow_html=True
)

#Button styling
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #962F34;color:white;font-size:25px;height:2em;width:17em;border-radius:10px 10px 10px 10px;
    
}
</style>""", unsafe_allow_html=True)




#tittles
#st.title("Σύστημα πιστοποίησης διπλωμάτων Πανεπιστημίου Πατρών")
#st.subheader("Select your role")

########################
#add university banner
institute_banner = Image.open("../assets/institute_banner.png")

col1, col2 = st.columns([1, 2])
with col1:
    st.image(institute_banner, output_format="png", width=550)
with col2:
    st.title("Σύστημα πιστοποίησης διπλωμάτων Πανεπιστημίου Πατρών")
    

########################
    
#Verify & Generate certificates buttons
col1, col2 = st.columns([1, 2])
with col1:
    clicked_verifier = st.button("🧾 View & Validate Certificate")
with col2:
    clicked_institute = st.button("🎓 Generate Certificate - for University personel only")

#button actions
if clicked_institute:
    st.session_state.profile = "Institute"
    switch_page('login')
elif clicked_verifier:
    st.session_state.profile = "Verifier"
    switch_page('login')