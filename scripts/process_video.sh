#!/bin/bash
ffmpeg -i $1 -filter:v "crop=w=640:h=480:x=0:y=0" ../assets/output_file.mp4
