import pygame
import random
import time

# Initialize Pygame mixer
pygame.mixer.init()

# Dictionary to map notes to their corresponding sound files
notes_sounds = {
    'C': 'static/audio/piano-c_C_major.wav',
    'D': 'static/audio/piano-d.wav',
    'E': 'static/audio/piano-e.wav',
    'F': 'static/audio/piano-f.wav',
    'G': 'static/audio/piano-g.wav',
    'A': 'static/audio/piano-a.wav',
    'B': 'static/audio/piano-b.wav'
}


def play_random_note():
    # Select a random note
    note = random.choice(list(notes_sounds.keys()))

    # Load and play the sound
    sound_path = notes_sounds[note]
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

    # Wait for the sound to complete
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    return note


# Test the functionality by running it directly
if __name__ == '__main__':
    random_note = play_random_note()
    user_guess = input(f'What note did you hear? ').strip().lower()

    if user_guess == random_note.lower():
        print('Correct!')
    else:
        print(f'Incorrect. The correct answer was: {random_note}')
