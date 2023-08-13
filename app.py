import streamlit as st
import requests

st.title("Database Interaction with Streamlit and FastAPI")

ID = st.text_input("ID")
PWD = st.text_input("PWD")
PHONE_NUM = st.text_input("PHONE_NUM")
E_MAIL = st.text_input("E_MAIL")


if st.button("회원 등록"):
    data = {
        "ID": ID,
        "PWD": PWD,
        "PHONE_NUM": PHONE_NUM,
        "E_MAIL": E_MAIL
    }
    response = requests.post("http://127.0.0.1:8000/insert", json=data)
    if response.status_code == 200:
        st.success("Data inserted successfully")
    else:
        st.error("Failed to insert data")
