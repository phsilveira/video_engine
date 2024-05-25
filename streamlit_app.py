import subprocess
import streamlit as st
import pandas as pd
import json
import os


def main():
    st.title('Video Engine - Batch Render')
    
    template = st.selectbox('Select a template', ['Template C'])

    process_running = False

    if not process_running:
        uploaded_file = st.file_uploader("Script file as a .csv format", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)

        for _, row in df.iterrows():
            target = row['target']
            file_path = f'example/{target}.json'
            output_file_path = f'output/{target}.json'

            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data = json_file.read()

                data = data.replace('{narration_audio_url}',str(row['narration_audio_url']))
                data = data.replace('{avatar_video_url}',str(row['avatar_video_url']))
                data = data.replace('{text_1}',str(row['text_1']))
                data = data.replace('{text_2}',str(row['text_2']))
                data = data.replace('{text_3}',str(row['text_3']))
                data = data.replace('{text_4}',str(row['text_4']))

                # create a folder if it does not exist
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                # print(data)

                with open(output_file_path, 'w', encoding='utf-8') as json_file:
                    json_file.write(data)

        st.success('All files have been generated successfully!')

    

    if uploaded_file is not None and st.button('Start Process'):
        process_running = True

        with st.spinner('Running the batch file...'):
            process = subprocess.Popen(['run.bat'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            output_area = st.empty()

            for line in iter(process.stdout.readline, b''):
                output_area.text(line.decode())
                print(line.decode())
                if 'rendering complete!' in line.decode():
                    break
            process.stdout.close()
            # process.wait()

        process_running = False

        st.success('Render complete successfully!')

        # Display the video
        video_file = 'output/output_video2.mp4'
        st.video(video_file)

        # Allow the user to download the video
        with open(video_file, 'rb') as f:
            video_bytes = f.read()
        st.download_button(
            label="Download video",
            data=video_bytes,
            file_name='output_video2.mp4',
            mime='video/mp4'
        )

if __name__ == "__main__":
    main()