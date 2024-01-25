import streamlit as st
from PIL import Image
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
# hide_icons()
hide_sidebar()
# remove_whitespaces()


def hide_anchor_link():
    st.markdown(
        body="""
        <style>
            /* Replace '.correct-selector' with the actual class or structure */
            .correct-selector {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    

hide_anchor_link()

st.title("Certificate Validation System")
st.write("")
st.subheader("Select Your Role")
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
st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)


st.markdown('''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
''', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .reportview-container {
        background: #fff
    }
   .sidebar .sidebar-content {
        background: #fff
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)
institite_logo = Image.open("../assets/institute_logo.png")
with col1:
    st.image(institite_logo, output_format="jpg", width=230)
    clicked_institute = st.button("Institute")

company_logo = Image.open("../assets/company_logo.jpg")
with col2:
    st.image(company_logo, output_format="jpg", width=230)
    clicked_verifier = st.button("Verifier")

if clicked_institute:
    st.session_state.profile = "Institute"
    switch_page('login')
elif clicked_verifier:
    st.session_state.profile = "Verifier"
    switch_page('login')
