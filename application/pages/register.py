import streamlit as st
from db.firebase_app import register
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

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
st.subheader("irene")
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

form = st.form("login")
email = form.text_input("Enter your email")
password = form.text_input("Enter your password")
clicked_login = st.button("Already registered? Click here to login!")

if clicked_login:
    switch_page("login")
    
submit = form.form_submit_button("Register")
if submit:
    result = register(email, password)
    if result == "success":
        st.success("Registration successful!")
        if st.session_state.profile == "Institute":
            switch_page("institute")
        else:
            switch_page("verifier")
    else:
        st.error("Registration unsuccessful!")