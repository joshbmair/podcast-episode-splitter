import ffmpeg
import math
import os
import sys


def get_mp3_duration(input_file):
    """Get the duration of the MP3 file using ffmpeg."""

    try:
        probe = ffmpeg.probe(input_file)
        duration = float(probe['format']['duration'])
        return duration
    except ffmpeg.Error as e:
        print(f"Error occurred: {e}")
        return None


def split_mp3(input_file, output_folder, segment_duration=600):
    """Split the MP3 file into segments using the -f segment option."""

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Construct the output file pattern
    output_file_pattern = os.path.join(output_folder, 'segment_%03d.mp3')

    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file_pattern, f='segment', segment_time=segment_duration, c='copy', reset_timestamps=1)
            .run(overwrite_output=True)
        )
        print(f"MP3 splitting complete: segments saved to {output_folder}")
    except ffmpeg.Error as e:
        print(f"Error occurred while splitting the MP3: {e}")

    print("MP3 splitting complete.")


def process_all_mp3_files(input_directory, output_directory):
    """Process all MP3 files in the input directory, create a folder for each file's parts, and split them into segments."""

    # Iterate through all files in the input directory
    for filename in os.listdir(input_directory):
        # Check if the file is an MP3
        if filename.endswith('.mp3'):
            input_file = os.path.join(input_directory, filename)

            # Create a folder inside the output directory to store the parts of the current MP3 file
            output_folder = os.path.join(
                output_directory, os.path.splitext(filename)[0] + '_parts')

            # Ensure the output folder exists
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            print(f"Processing {filename}...")
            # Split the MP3 file into segments and save them in the created folder
            split_mp3(input_file, output_folder)


def main(argv):
    if len(sys.argv) < 1:
        print('Usage: main.py <input directory> [segment duration]')
        sys.exit(1)

    input_directory = argv[1]
    # segment_duration = float(argv[2]) * 60

    process_all_mp3_files(input_directory, input_directory)


if __name__ == '__main__':
    main(sys.argv)
