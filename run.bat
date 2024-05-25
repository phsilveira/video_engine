@echo off
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_01_intro.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_02_intro.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_03_intro.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_04_intro.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_05_mentor.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_06_pillars.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_07_pillars.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_08_pillars.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_09_pillars.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_10_pillars.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_11_presentation.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_12_presentation.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_13_topics.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_14_conclusion.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_15_conclusion.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup
C:\\Users\\ph\\Documents\\apoia\\video_engine\\nexrender-cli-win64.exe --file C:\\Users\\ph\\Documents\\apoia\\video_engine\\output\\scene_16_brand_signature.json --binary "C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe" --skip-cleanup


ffmpeg -y -f concat -safe 0 -i example/input.txt -c copy output/input_video.mp4

for /f "delims=" %%i in ('ffprobe -v error -show_entries format^=duration -of default^=noprint_wrappers^=1:nokey^=1 output/input_video.mp4') do set "duration=%%i"
echo %duration%

@echo off
for /f %%i in ('powershell -command "%duration% - 2"') do set "fade_start=%%i"
echo %fade_start%

ffmpeg -y -stream_loop -1 -i example/input_audio.wav -i output/input_video.mp4 -filter_complex "[0:a]volume=0.1[a];[a]afade=t=out:st=%fade_start%:d=2[a1];[1:a][a1]amix=inputs=2:duration=first:dropout_transition=2[aout]" -map 1:v -map "[aout]" -c:v copy -c:a aac output/output.mp4

ffmpeg -y -f concat -safe 0 -i example/input2.txt -c copy output/output_video2.mp4
echo 'rendering complete!'  
pause