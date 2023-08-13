import streamlit as st
import requests

def page_set():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "main"
    if st.session_state["current_page"] == "main":
        main()
    elif st.session_state["current_page"] == 'sign_up':
        sign_up()

def main():
    st.title("NoteFlip")
    ID = st.text_input("ID")
    PWD = st.text_input("비밀번호")
    col1, col2 = st.columns(2)

    if col1.button("회원가입"):
        st.session_state["current_page"] = 'sign_up'
        st.experimental_rerun()
    if col2.button("로그인"):
        login(ID,PWD)

def login(id,pwd):
    st.write("구현중")

def sign_up():
    st.title("회원가입 후 Note Flip을 이용하세요!")

    ID = st.text_input("ID")
    PWD = st.text_input("PWD")
    PHONE_NUM = st.text_input("PHONE_NUM")
    E_MAIL = st.text_input("E_MAIL")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("뒤로가기"):
            st.session_state["current_page"]= 'main'
            st.experimental_rerun()


    with c2:
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



if __name__ == "__main__":
    page_set()