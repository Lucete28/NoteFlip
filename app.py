import streamlit as st
import requests
import fitz  # PyMuPDF
from PIL import Image
import io

def page_set():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "main"
    if st.session_state["current_page"] == "main":
        main()
    elif st.session_state["current_page"] == 'sign_up':
        sign_up()
    elif st.session_state["current_page"] == 'loadOrCreate':
        loadOrCreate()

def main():
    st.title("NoteFlip")
    ID = st.text_input("아이디")
    PWD = st.text_input("비밀번호")
    col1, col2 = st.columns(2)

    if col1.button("회원가입"):
        st.session_state["current_page"] = 'sign_up'
        st.experimental_rerun()
    if col2.button("로그인"):
        login(ID,PWD)

def loadOrCreate():
    st.title(f"{st.session_state.user_id}님 환영합니다.")
    st.button("생성하기")
    st.button("불러오기")
    st.markdown(
    """
    <style>
    .stButton button {
        font-size: 180px; /* Increase font size */
        padding: 100px 200px; /* Adjust padding (top/bottom, left/right) */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def pdf_read():
    st.title("PDF Viewer with Streamlit")
    
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if pdf_file is not None:
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        num_pages = pdf_document.page_count
        
        page_number = st.slider("Select a page", 1, num_pages, 1)
        
        st.write(f"Displaying page {page_number} of {num_pages}")
        
        page = pdf_document.load_page(page_number - 1)
        pixmap = page.get_pixmap()
        
        # Convert pixmap to PIL Image
        pil_image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        
        # Convert PIL Image to bytes
        image_bytes = io.BytesIO()
        pil_image.save(image_bytes, format="JPEG")
        
        st.image(image_bytes)


def login(id,pwd):
    # FastAPI로 값을 전송하기
    data = {
        "ID": id,
        "PWD": pwd
    }
    response = requests.post("http://127.0.0.1:8000/login", json=data)
    st.write(response)
    if response.status_code == 200:
        st.success("로그인 성공")
        st.session_state.user_id = id
        st.session_state["current_page"]= 'loadOrCreate'
        st.experimental_rerun()
        
    else:
        st.error("로그인 실패")

def sign_up():
    st.title("회원가입 후 Note Flip을 이용하세요!")

    sign_up_ID = st.text_input("ID")
    sign_up_PWD = st.text_input("PWD")
    sign_up_PHONE_NUM = st.text_input("PHONE_NUM")
    sign_up_E_MAIL = st.text_input("E_MAIL")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("뒤로가기"):
            st.session_state["current_page"]= 'main'
            st.experimental_rerun()
    with c2:
        if st.button("회원 등록"):
            data = {
                "ID": sign_up_ID,
                "PWD": sign_up_PWD,
                "PHONE_NUM": sign_up_PHONE_NUM,
                "E_MAIL": sign_up_E_MAIL
            }
            response = requests.post("http://127.0.0.1:8000/insert", json=data)
            if response.status_code == 200:
                st.success("Data inserted successfully")
                st.session_state["current_page"]= 'main'
                st.experimental_rerun()
            else:
                st.error("Failed to insert data")



if __name__ == "__main__":
    page_set()