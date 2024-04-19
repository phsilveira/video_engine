import streamlit as st
import zipfile
import os
import tempfile
import subprocess
import json

def display_header():
    st.header("Video Engine")
    # st.subheader("Hello World")
    # st.write("Streamlit App Boilerplate that contains everything you need to get running.")

def handle_file_upload():
    uploaded_file = st.file_uploader("Choose a .zip file", type="zip")
    composition_field = st.text_input("Composition Name", "MAIN")
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
            # Extract the zip file to the /tmp directory
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                zip_ref.extractall('/tmp')
                
                # Get the name of the .aep file
                aep_file = next((f for f in os.listdir('/tmp') if f.endswith('.aep')), None)
                
                if aep_file:
                    # Create the JSON structure
                    data = {
                        "template": {
                            "src": f"file:///tmp/{aep_file}",
                            "composition": "APEAK_Logo"
                        },
                        "actions": {
                            "postrender": [
                                {
                                    "module": "@nexrender/action-encode",
                                    "preset": "mp4",
                                    "output": "encoded.mp4",
                                    "params": {
                                        "-vcodec": "libx264",
                                        "-r": 25
                                    }
                                },
                                {
                                    "module": "@nexrender/action-copy",
                                    "input": "encoded.mp4",
                                    "output": "/tmp/result.mp4"
                                }
                            ]
                        }
                    }
                    
                    # Write the JSON data to a file in the /tmp directory
                    with open('/tmp/main.json', 'w') as json_file:
                        json.dump(data, json_file)
            
                        # Define the updated command
            cmd = r'./nexrender-cli-win64.exe --file /tmp/main.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe"'
            
            # Run the command
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                st.write(f"Error: {stderr.decode('utf-8')}")
            else:
                st.write(f"Output: {stdout.decode('utf-8')}")
                
                # Check if the result.mp4 file exists
                if os.path.isfile('/tmp/result.mp4'):
                    # Create a download button for the result.mp4 file
                    with open('/tmp/result.mp4', 'rb') as file:
                        btn = st.download_button(
                            label="Download result.mp4",
                            data=file,
                            file_name="result.mp4",
                            mime="video/mp4"
                        )

if __name__ == "__main__":
    main()