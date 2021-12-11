SET generated_file_name=cut_videos_batch2

@echo off
echo Starting generating process of making batch for cut videos....
echo @echo off >> %generated_file_name%.bat
echo echo Starting process cutting videos..... >> %generated_file_name%.bat
echo mkdir samples_raw_cut >> %generated_file_name%.bat
for /f %%f in ('dir /b samples_raw') do echo ffmpeg -ss 00:00:00 -i "samples_raw\%%f" -t 60 -c copy "samples_raw_cut\%%f" >> %generated_file_name%.bat
echo echo Ended >> %generated_file_name%.bat
echo pause >> %generated_file_name%.bat
echo Ended
pause
