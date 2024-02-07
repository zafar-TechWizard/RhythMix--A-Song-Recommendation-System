import pandas as pd
import os

# Define the path to the directory containing your audio files
audio_directory = "./Extrafiles/Music"

# Read the original dataset
dataset = pd.read_csv("./Dataset/song.csv")


# Create a new column "song_path" by combining the directory path and song names
dataset['song_path'] = [os.path.join(audio_directory, song + '.mp3') for song in dataset['song']]

# Save the updated dataset
dataset.to_csv("./Dataset/song_with_paths.csv", index=False)
