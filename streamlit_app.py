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

def extract_zip_file(uploaded_file, temp_dir):
    # Extract the zip file to the temp directory
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

def get_aep_file(temp_dir):
    # Get the name of the .aep file
    return next((f for f in os.listdir(temp_dir) if f.endswith('.aep')), None)

def create_json_structure(aep_file, composition_name, temp_dir):
    print(f"Creating JSON structure for {aep_file} for composition {composition_name}")
    # Create the JSON structure
    return {
        "template": {
            "src": f"file:///C:\\Users\\ph\\Documents\\apoia\\video_engine\\temp\\{aep_file}",
            "composition": composition_name
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
                    "output": "C:\\Users\\ph\\Documents\\apoia\\video_engine\\temp\\result.mp4"
                }
            ]
        }
    }

def write_json_to_file(data, temp_dir):
    # Write the JSON data to a file in the temp directory
    with open(f'{temp_dir}/main.json', 'w') as json_file:
        json.dump(data, json_file)
            
def remove_all_files_from_temp_dir(temp_dir):
    # Remove all files from the temp directory
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))

def run_command_and_handle_output(temp_dir):
    # Define the command
    cmd = f'C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\temp\\main.json --binary "C:\\Program Files\\Adobe\\Adobe After Effects 2024\\Support Files\\aerender.exe"'
    
    # Run the command
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        st.write(f"Error: {stderr.decode('utf-8')}")
    else:
        # st.write(f"Output: {stdout.decode('utf-8')}")
        st.write(f"Success! The video has been rendered.")
        
        # Check if the result.mp4 file exists
        if os.path.isfile(f'{temp_dir}/result.mp4'):
            # Create a download button for the result.mp4 file
            with open(f'{temp_dir}/result.mp4', 'rb') as file:
                btn = st.download_button(
                    label="Download result.mp4",
                    data=file,
                    file_name="result.mp4",
                    mime="video/mp4"
                )

def main():
    display_header()
    # uploaded_file = handle_file_upload()
    uploaded_file = st.file_uploader("Choose a .zip file", type="zip")
    composition_field = st.text_input("Composition Name", "MAIN")
    if uploaded_file is not None:
        st.write("You have uploaded a file!")
        # return uploaded_file

    if uploaded_file:
        if st.button('Submit'):
            with st.spinner('Processing...'):
                # Define the temp directory
                temp_dir = r'.\temp'

                # remove_all_files_from_temp_dir(temp_dir)
                                # Remove all files and folders inside the temp directory
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))

                
                extract_zip_file(uploaded_file, temp_dir)
                aep_file = get_aep_file(temp_dir)
                
                if aep_file:
                    data = create_json_structure(aep_file, composition_field, temp_dir)
                    write_json_to_file(data, temp_dir)
                    run_command_and_handle_output(temp_dir)

if __name__ == "__main__":
    main()