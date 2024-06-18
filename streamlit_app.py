import subprocess
import streamlit as st
import pandas as pd
import json
import os
import time


def generate_scene_json(row, composition, template="Cursos_Template_B", project_template_path='C:\\Users\Administrator\\Downloads\\Cursos_Template_B_v3\\', output_path="C:\\Users\\Administrator\\Documents\\video_engine\\output\\"):
    output_path = f"{output_path}{template}__{composition}.mp4"
    base_contract = {
        "template": {
            "src": f"file:///{project_template_path}{template}.aep",
            "composition": composition
        },
        "assets": [
            {
                "type": "video",
                "layerName": "avatar_video_url",
                "src": "{avatar_video_url}",
                "params": {
                    "cachePath": "/tmp/my-nexrender-cache"
                }
            },
            {
                "composition": composition,
                "type": "data",
                "layerName": "avatar_video_url",
                "property": "containingComp.workAreaDuration",
                "expression": "layer.source.duration"
            },
            {
                "type": "data",
                "layerName": "title_a",
                "property": "Source Text",
                "value": "{title_a}"
            },
            {
                "type": "data",
                "layerName": "text_1",
                "property": "Source Text",
                "value": "{text_1}"
            },
            {
                "type": "data",
                "layerName": "text_2",
                "property": "Source Text",
                "value": "{text_2}"
            },
            {
                "type": "data",
                "layerName": "text_3",
                "property": "Source Text",
                "value": "{text_3}"
            },
            {
                "type": "data",
                "layerName": "text_4",
                "property": "Source Text",
                "value": "{text_4}"
            },
            {
                "type": "audio",
                "layerName": "narration_audio_url",
                "src": "{narration_audio_url}",
                "params": {
                    "cachePath": "/tmp/my-nexrender-cache"
                }
            },
            {
                "composition": composition,
                "type": "data",
                "layerName": "narration_audio_url",
                "property": "containingComp.workAreaDuration",
                "expression": "layer.source.duration"
            },
            {
                "type": "image",
                "layerName": "image_1_url",
                "src": "{image_1_url}",
                "params": {
                    "cachePath": "/tmp/my-nexrender-cache"
                }
            },
            {
                "type": "image",
                "layerName": "image_2_url",
                "src": "{image_2_url}",
                "params": {
                    "cachePath": "/tmp/my-nexrender-cache"
                }
            },
            {
                "type": "image",
                "layerName": "image_3_url",
                "src": "{image_3_url}",
                "params": {
                    "cachePath": "/tmp/my-nexrender-cache"
                }
            }
        ],

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
                    "output": output_path
                }
            ]
        }
    }

    assets = base_contract['assets']
    assets_used = []

    for key, value in row.items():
        if not pd.isna(value):
            for asset in assets:
                
                if asset['layerName'] == key:
                    if asset['type'] == 'audio':
                        asset['src'] = row[asset['layerName']]
                    if asset['type'] == 'image':
                        asset['src'] = row[asset['layerName']]
                    if asset['type'] == 'video':
                        asset['src'] = row[asset['layerName']]
                    if asset['type'] == 'data':
                        if 'value' in asset:
                            asset['value'] = row[asset['layerName']]

                    if row['use_avatar'] and asset['layerName'] == 'narration_audio_url':
                        continue

                    assets_used.append(asset)
    
    base_contract['assets'] = assets_used
    return base_contract, output_path

def main():
    st.title('Video Engine - Batch Render')
    templates = {
        'Template C': {
            'name':'Cursos_Template_C',
            'project_template_path':'C:\\Users\Administrator\\Downloads\\Cursos_Template_C_v7\\',
            'audio_path':'C:\\Users\\Administrator\\Documents\\video_engine\\example\\template_c\\input_audio.mp4'
        },
        'Template B': {
            'name':'Cursos_Template_B',
            'project_template_path':'C:\\Users\Administrator\\Downloads\\Cursos_Template_B_v3\\',
            'audio_path':'C:\\Users\\Administrator\\Documents\\video_engine\\example\\template_b\\input_audio.mp3'
        },
        # '1.4.4 - Course summary - Quiz interativo': {
        #     ''
        # }
    }

    selected_template = st.selectbox('Select a template', list(templates.keys()))

    process_running = False

    if not process_running:
        uploaded_file = st.file_uploader("Script file as a .csv format", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)

        scenes_path = []
        scenes_script_to_render = []

        for _, row in df.iterrows():
            target = row['target']
            scene_dict, output_video_path = generate_scene_json(row, row['target'], templates[selected_template]['name'], templates[selected_template]['project_template_path'],)

            # output_file_path = f'output/{templates[selected_template]["name"]}/{target}.json'
            output_file_path = f'output/{target}.json'

            # create a folder if it does not exist
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            with open(output_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(scene_dict, json_file, indent=4, ensure_ascii=False)

            scenes_script_to_render.append(output_file_path)
            scenes_path.append(output_video_path)

        scenes_script_to_render.pop()
        scenes_path.pop()

        # export scenes path to .txt
        with open(f'output/scenes_to_render.txt', 'w') as f:
            for item in scenes_path:
                f.write("file '%s'\n" % item)

        st.success('All files have been generated successfully!')

    

    if uploaded_file is not None and st.button('Start Process'):
        process_running = True
        start = time.time()

        for scene in scenes_script_to_render:
            with st.spinner(f'Running the batch file for {scene}...'):
                command = f'C:\\Users\\Administrator\\Documents\\video_engine\\nexrender-cli-win64.exe --file {scene} --binary "C:\\Program Files\\Adobe\\Adobe After Effects 2024\\Support Files\\aerender.exe"'
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                output_area = st.empty()

                for line in iter(process.stdout.readline, b''):
                    output_area.text(line.decode())
                    # output_area.text(f"Comp {scene}: {line.decode()}")
                    print(line.decode())
                    if 'rendering complete!' in line.decode():
                        break
                process.stdout.close()

        with st.spinner('Merging the videos...'):
            command = f'ffmpeg -y -f concat -safe 0 -i C:/Users/Administrator/Documents/video_engine/output/scenes_to_render.txt -c copy C:/Users/Administrator/Documents/video_engine/output/output.mp4'
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output_area = st.empty()

            for line in iter(process.stdout.readline, b''):
                output_area.text(line.decode())
                print(line.decode())
                if 'rendering complete!' in line.decode():
                    break
            process.stdout.close()

            command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 C:/Users/Administrator/Documents/video_engine/output/output.mp4'
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            video_duration = process.stdout.read().decode()
            video_duration = float(video_duration)
            fade_out_start = video_duration - 2

            command = f'ffmpeg -y -stream_loop -1 -i {templates[selected_template]["audio_path"]} -i C:/Users/Administrator/Documents/video_engine/output/output.mp4 -filter_complex "[0:a]volume=1[a];[a]afade=t=out:st={fade_out_start}:d=2[a1];[1:a][a1]amix=inputs=2:duration=first:dropout_transition=2[aout]" -map 1:v -map "[aout]" -c:v copy -c:a aac C:/Users/Administrator/Documents/video_engine/output/output2.mp4'
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            output_area = st.empty()

            for line in iter(process.stdout.readline, b''):
                output_area.text(line.decode())
                print(line.decode())
                if 'rendering complete!' in line.decode():
                    break
            process.stdout.close()

            command = 'ffmpeg -y -f concat -safe 0 -i C:/Users/Administrator/Documents/video_engine/output/final_merge.txt -c copy C:/Users/Administrator/Documents/video_engine/output/output_final.mp4'
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            output_area = st.empty()

            for line in iter(process.stdout.readline, b''):
                output_area.text(line.decode())
                print(line.decode())
                if 'rendering complete!' in line.decode():
                    break
            process.stdout.close()

        process_running = False
        end = time.time()

        st.success(f'Render complete successfully in {round(end-start, 2)}!')

        # Display the video
        video_file = 'C:/Users/Administrator/Documents/video_engine/output/output_final.mp4'
        st.video(video_file)

        # Allow the user to download the video
        with open(video_file, 'rb') as f:
            video_bytes = f.read()
        st.download_button(
            label="Download video",
            data=video_bytes,
            file_name='output_final.mp4',
            mime='video/mp4'
        )

if __name__ == "__main__":
    main()