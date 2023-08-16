import streamlit as st
from datetime import datetime, timedelta

def main():
    st.title("Custom Time Input")

    hour = st.slider("Hour", 0, 23)
    minute = st.slider("Minute", 0, 59)
    second = st.slider("Second", 0, 59)

    selected_time = datetime.now().replace(hour=hour, minute=minute, second=second)
    st.write("Selected time:", selected_time)

if __name__ == "__main__":
    main()
