# Yearly project

Use
```
process_to_signal(filename) from VideoReader class
```
to convert desired video file into signal representing its luminance frame by frame in outputted txt file 

## Sample
- Sample001.mp4 is very short 5 frame video
- Order of frames and its overall rgb value is rgb(0,0,0), rgb(255,255,255), rgb(254,0,0), rgb(0,254,0), rgb(0,0,254)
- outputted file \processed\sample001_luminance.txt contains luminance of each frame
