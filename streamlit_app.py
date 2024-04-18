import streamlit as st
import zipfile
import os
import tempfile

def display_header():
    st.header("Video Engine")
    # st.subheader("Hello World")
    # st.write("Streamlit App Boilerplate that contains everything you need to get running.")

def handle_file_upload():
    uploaded_file = st.file_uploader("Choose a .zip file", type="zip")
    if uploaded_file is not None:
        st.write("You have uploaded a file!")
        return uploaded_file
    return None

def extract_and_display_files(uploaded_file):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Open the zip file
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            # Extract all the contents of zip file in the temporary directory
            zip_ref.extractall(tmpdir)
            
            # Iterate over the files in the temporary directory
            files = os.listdir(tmpdir)
            for filename in files:
                st.write(f"File in zip: {filename}")

            # If there are any files, create a download button for the first one
            if files:
                first_file_path = os.path.join(tmpdir, files[0])
                st.download_button(
                    label="Download first image",
                    data=first_file_path,
                    file_name=files[0],
                )
            

def main():
    display_header()
    uploaded_file = handle_file_upload()
    if uploaded_file:
        if st.button('Submit'):
            extract_and_display_files(uploaded_file)

if __name__ == "__main__":
    main()