# Podcast Episoder Splitter

## Why I made this

The aux cord cord port in my car broke. Instead of getting a Bluetooth car adapter, I figured I could plug a thumb drive into the USB port my car has to listen to my podcasts.

## What this script does

1. This goes through each the MP3 files in a given input folder.
1. Creates a folder with the name of the MP3 (without the file ending).
1. Puts 10 minute segments of that podcast in said folder.

## Setup

1. Install FFmpeg.
1. Install the Python dependencies in `requirements.txt`.

## Usage

`python3 main.py <input directory>`
