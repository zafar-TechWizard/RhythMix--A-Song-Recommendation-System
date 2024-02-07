import os
import pandas as pd
import time
import pygame
from termcolor import colored
import sys
import threading


#load the dataset and name file
dataset = pd.read_csv("./Dataset/song_with_paths.csv")
user_name_file = "./Extrafiles/user_name.txt"

# Giving name for this system
system_name = colored("RhythMix", 'cyan', attrs=['bold'])

# Initializing some global variables
user_name = ""
user_emotion = ""
user_tempo = ""


def loading_animation():
    print("")
    animation = "|/-\\"
    for i in range(26):
        print(f"Loading {animation[i % len(animation)]}", end="\r")
        time.sleep(0.1)



#funtion to show typing effet on print 
def slow_print(text, delay=0.007):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


# Function to load user name from a file
def load_user_name():
    global user_name
    if os.path.exists(user_name_file):
        with open(user_name_file, 'r') as file:
            user_name = file.read().strip()


# Function to save user name to a file
def save_user_name():
    with open(user_name_file, 'w') as file:
        file.write(user_name)


# Function to play audio using pygame
def PlayAudio(audio):
    pygame.mixer.init() # initializing pygame mixer
    pygame.mixer.set_num_channels(0)  # This line will suppress the pygame welcome message
    duration_in_seconds = pygame.mixer.Sound.get_length(pygame.mixer.Sound(audio)) # Get the duration in seconds
    # Convert duration to hours, minutes, and seconds
    hour, remainder = divmod(duration_in_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_duration = "{:0>2}:{:0>2}".format(int(minutes), int(seconds)) # Format the result as a string
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play() #Playing Music with Pygame
    slow_print(f"   {system_name}: The recommended song has been played, The duration of the song is {formatted_duration}.") 
    time.sleep(1.5)


# Function to stop audio playback
def StopAudio():
    time.sleep(0.5)
    pygame.mixer.music.stop()


# Function to get user emotion and tempo preferences
def preferences():
    global user_emotion, user_tempo
    print("")
    time.sleep(0.7)
    slow_print(f"""   {system_name}: Hey there, 
             I'm here to tailor the tunes to your emotions! 🎵
             What kind of music are you in the mood for?
             e.g: sad, happy, romantic, energetic, calm.""")
    print("")
    user_emotion = input(f"      {user_name}: ").lower()
    print()
    if "sad" in user_emotion:
        time.sleep(0.8)
        slow_print(f"""   {system_name}: Let the calm melodies be your companion during moments of thinking. \n             Together, we'll embrace the depth of emotions. 🎷😌""")
    
    elif "happy" in user_emotion:
        time.sleep(0.8)
        slow_print(f"""   {system_name}: Ah, happiness! I've got the perfect playlist to lift your spirits. \n             Get ready for a musical journey filled with joy! 🎷😄""")
    
    elif "romantic" in user_emotion:
        time.sleep(0.8)
        slow_print(f"""   {system_name}: Romance is in the air! \n             I will serenade you with heartwarming melodies. 🎷❤️""")
    
    elif "energetic" in user_emotion:
        time.sleep(0.8)
        slow_print(f"""   {system_name}: Ready to feel the energy? \n             Let's crank up the tempo and get your day pulsating with lively beats! 🎷💪""")
    
    elif "calm" in user_emotion:
        time.sleep(0.8)
        slow_print(f"""   {system_name}: Looking for calm and peace..! \n             Immerse yourself in calming tunes that will gently guide you to a state of peace and serenity. 🎶🍃""")

    else:
        time.sleep(0.8)
        slow_print(f"   {system_name}: I'm here to tailor the tunes to your emotions! \n             But you have not given the correct emotion input.")
        preferences()
    
    slow_print(f"""\n   {system_name}: Now, tell me about the tempo you prefer (numeric value):""")
    
    user_tempo = int(input(f"      {user_name}: "))
    print("")
    if 10 <= user_tempo <= 80:
        time.sleep(0.8)
        slow_print(colored(f"   {system_name}: Opting for a relaxed tempo! Get ready to unwind with soothing tunes. 🎶🍃", 'blue'))
    
    elif 80 < user_tempo <= 120:
        time.sleep(0.8)
        slow_print(colored(f"   {system_name}: Going for a moderate pace! I've got just the right rhythm to keep you grooving. 🎶🕺", 'blue'))
    
    elif user_tempo > 120:
        time.sleep(0.8)
        slow_print(colored(f"   {system_name}: Feeling the need for speed! Let's rev up the tempo and make your day dynamic. 🎶🚀", 'blue'))
    
    else:
        time.sleep(0.8)
        slow_print(colored(f"   {system_name}: Please provide a numeric value only. Let's try that again.", 'blue'))
    

# Function to greet the user
def greet_user():
    global user_name, user_emotion
    load_user_name()
    time.sleep(0.4)
    slow_print(colored(f"""
                🎷 Welcome to RhythMix! 🎸\n""", 'green', attrs=['bold']))
    time.sleep(0.7)
    if not user_name:
        slow_print(f"""
        Hey there! I'm the {system_name}'s assistant. \n        """)
        user_name = input(f"        What's your name?: ")
        save_user_name()
        time.sleep(0.7)
        slow_print(f"""\n        Fantastic, that's a cool name, {user_name}! 🌟""")
        preferences()

    else:
        slow_print(f"""   {system_name}: Welcome back, {user_name}! Would you like to change your name? (yes/no):""")
        change_name = input(f"      {user_name}: ").strip().lower()
        if change_name == "yes":
            time.sleep(0.8)
            user_name = input(f"    {system_name}: Sure thing! What's your new name? \n       {user_name}: ")
            save_user_name()
            time.sleep(0.7)
            slow_print(f"   {system_name}: Great, {user_name}! 💫 ")
            preferences()
        else:
            preferences()


# Function to recommend songs based on user preferences
def recommend_songs():
    global user_emotion, user_tempo, dataset

    # Find songs with matching mood in the dataset (case-insensitive)
    matching_songs = dataset[dataset['mood'].str.strip().str.lower() == user_emotion]

    if matching_songs.empty:
        time.sleep(0.9)
        slow_print(f"   {system_name}: Sorry, we don't have songs for that mood in our dataset.")
    else:
        # Find the song with the closest tempo to the user's preference
        recommended_song = matching_songs.iloc[(matching_songs['tempo'] - user_tempo).abs().argsort()[:1]]
        time.sleep(1.1)
        slow_print("\n   Recommended Song:")
        time.sleep(0.8)
        slow_print(recommended_song[['song', 'tempo']].to_string(index=False, justify='center', formatters={'song': lambda x: f"{x.title(): >30}"}))

        # # Playing the recommended song
        recommended_song_path = recommended_song['song_path'].values[0]  # Adjust the column name accordingly
        time.sleep(0.5)
        print("")
        slow_print(f"   {system_name}: Would you like to play this song? (Yes/No):")
        desire = input(f"      {user_name}: ").lower()
        if "yes" in desire:
            PlayAudio(recommended_song_path)
            time.sleep(0.4)
            while True:
                slow_print(f"   {system_name}: Type 'stop' to stop the music:")
                user_input = input(f"      {user_name}: ").strip().lower()
                if user_input == 'stop':
                    slow_print(f"   {system_name}: Allright stoping the song, please wait..!")
                    time.sleep(0.9)
                    print("")
                    StopAudio()
                    break  # Exit the loop when the user enters 'stop'
                else:
                    time.sleep(0.8)
                    slow_print(f"   {system_name}: I didn't recognize that command. Please type 'stop' to stop the music.")
        else:
            time.sleep(0.6)
            slow_print(f"   {system_name}: Ok, closing the system. GoodBye")
            time.sleep(1)
            print("")
            sys.exit()


if __name__ == "__main__":
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()

    time.sleep(1)  # Delay to make program more interacting

    loading_thread.join()  # Wait for the loading animation to finish

    print("")
    greet_user()
    recommend_songs()
