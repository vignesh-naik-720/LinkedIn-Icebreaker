# app.py
import streamlit as st
from start import ice_break_with

# Streamlit Application
st.title("LinkedIn Profile Icebreaker Generator")

# Input field for the LinkedIn profile name
name = st.text_input("Enter LinkedIn Profile URL")

# Button to generate the icebreaker
if st.button("Generate Icebreaker"):
    if name:
        with st.spinner("Generating..."):
            try:
                # Call the ice_break_with function and display the result
                result = ice_break_with(name)
                
                # Display the result or any returned error message
                if "Error:" in result:
                    st.error(result)
                else:
                    st.success("Icebreaker generated successfully!")
                    st.write(result)
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.write("Debug info:", e)
    else:
        st.warning("Please enter a valid URL to proceed.")
