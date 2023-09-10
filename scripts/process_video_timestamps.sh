#!/bin/bash
ffmpeg -i $1 -ss 00:00:40 -t 00:00:59 -vf scale=640:480 ../backend/assets/output_file.mp4
