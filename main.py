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


def split_mp3(input_file, output_folder, segment_duration=900):
    """Split the MP3 into segments of the specified duration (default 900 seconds = 15 minutes)."""

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the duration of the MP3 file
    total_duration = get_mp3_duration(input_file)

    if total_duration is None:
        print("Unable to retrieve the MP3 duration.")
        return

    # Calculate the number of segments needed
    num_segments = math.ceil(total_duration / segment_duration)

    # Loop through and create segments
    for i in range(num_segments):
        start_time = i * segment_duration
        output_file = os.path.join(output_folder, f"segment_{i+1}.mp3")

        try:
            ffmpeg.input(input_file, ss=start_time, t=segment_duration).output(
                output_file).run(overwrite_output=True)
            print(f"Segment {i+1} created: {output_file}")
        except ffmpeg.Error as e:
            print(f"Error occurred while creating segment {i+1}: {e}")

    print("MP3 splitting complete.")


def process_all_mp3_files(input_directory, output_directory, segment_duration=900):
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
            split_mp3(input_file, output_folder, segment_duration)


def main(argv):
    if len(sys.argv) < 2:
        print('Usage: main.py <input directory> <segment duration>')
        sys.exit(1)

    input_directory = argv[1]
    segment_duration = argv[2] * 60

    process_all_mp3_files(input_directory, input_directory, segment_duration)


if __name__ == '__main__':
    main(sys.argv)
