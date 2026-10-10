import streamlit as st
from ai import enhance

st.title("Prompt Enhancer")

raw_prompt = st.text_area("Raw prompt:")
context = st.text_area("Context:")

if st.button("Enhance"):
    if raw_prompt.strip()=="":
        st.write("Enter a prompt")
        st.stop()
    if len(raw_prompt)+len(context)>5000:
        st.write("Input is too long")
        st.stop()    
    try:
        with st.spinner("Flabbergating..."):
         result = enhance(raw_prompt, context.strip() or "None provided")
    except Exception as e:
        st.error("The model is busy or something went wrong. Wait a few seconds and try again.")
        st.caption(f"Technical detail: {e}")
        st.stop()

    st.subheader("Improved Prompt")
    st.code(result.improved_prompt, language=None)

    st.subheader("Changes Made")
    for item in result.changes_made:
        st.write("-", item)

    st.subheader("Needed Context")
    for item in result.needed_context:
        st.write("-", item)
