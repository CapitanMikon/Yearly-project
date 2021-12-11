SET generated_file_name=normalize_videos_batch2

@echo off
echo Starting generating process of making batch for converting to 30 fps videos....
echo @echo off >> %generated_file_name%.bat
echo echo Starting process converting fps to 30..... >> %generated_file_name%.bat
echo mkdir specimens >> %generated_file_name%.bat
for /f %%f in ('dir /b samples_raw_cut') do echo ffmpeg -i "samples_raw_cut\%%f" -max_muxing_queue_size 4096 -r 30 -y "samples_raw_30fps\%%f" >> %generated_file_name%.bat
echo echo Ended >> %generated_file_name%.bat
echo pause >> %generated_file_name%.bat
echo Ended
pause
