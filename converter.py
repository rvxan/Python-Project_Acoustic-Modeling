import tkinter as tk
from pathlib import Path
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
import ffmpeg
from pydub import AudioSegment


def audiofileConverter(filename):
    # check if the file uploaded is a .wav file or an .mp3 file
    if Path(filename).suffix == '.wav':
        audiofile = filename
        print('File is correct!')

    elif Path(filename).suffix == '.mp3':
        src = filename
        dst = "audiofile.wav"

        # converts .mp3 to .wav
        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")
        audiofile = dst
        print('File has been converted >:[ ')

audiofileConverter()
'''
def audiofileChannels(filename):
    raw_audio = AudioSegment.from_file("pt.wav", format="wav")
    channel_count = raw_audio.channels
    print(channel_count)

    mono_wav = raw_audio.set_channels(1)
    mono_wav.export("pt_mono.wav", format="wav")
    mono_wav_audio = AudioSegment.from_file("pt_mono.wav", format="wav")

    channel_count = mono_wav_audio.channels
    print(channel_count)
'''
