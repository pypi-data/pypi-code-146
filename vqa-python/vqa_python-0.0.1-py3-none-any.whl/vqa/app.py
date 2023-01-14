import streamlit as st
import random 
if "answer_generation" not in st.session_state:
    from vqa.src.init import setup
    from vqa.src.answer_generation import AnswerGeneration
    setup()
    st.session_state.answer_generation = AnswerGeneration()

st.set_page_config(page_title="mVQA webapp", layout="wide", page_icon = "https://huggingface.co/spaces/flax-community/Multilingual-VQA/resolve/main/misc/mvqa-logo-2.png")
hide_menu_style = """
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html= True)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        margin-left: -400px;
    }
     
    """,
    unsafe_allow_html=True,
)
image = st.file_uploader("Choose an image")

# print(np.array(image.read()))
# cv2.imshow("Ss", np.array(image))
try:
    imshow, quesshow = st.columns(2)
    imshow.image(image)
    quesshow.write("")
    question = quesshow.text_input("Question")
    answer = st.session_state.answer_generation.answer_generation(image, question)
    print(answer)
    if question:
        quesshow.write(f"Answer: {answer}")
except:
    pass