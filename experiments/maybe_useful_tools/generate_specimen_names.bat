SET prefix_path=%CD%\specimens
SET generated_file_name=specimen_names2

@echo off
echo Starting process of making filepaths ....
for /f %%f in ('dir /b specimens\') do echo %%f - >>%generated_file_name%.txt
echo Ended
pause
