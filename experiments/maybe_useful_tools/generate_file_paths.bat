SET prefix_path=%CD%\specimens
SET generated_file_name=specimen_full_paths2

@echo off
echo Starting process of making filepaths ....
for /f %%f in ('dir /b specimens\') do echo %prefix_path%\%%f>>%generated_file_name%.txt
echo Ended
pause
