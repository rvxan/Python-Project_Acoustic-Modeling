"""Upload_.py uses Tkinter to create a dialog box for file selection and upload"""
import tkinter as tk
from pathlib import Path
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
from pydub import AudioSegment

# create the root window
root = tk.Tk()
root.title('Sound App File Upload')  # dialog box title: Open File
root.resizable(False, False)
root.geometry('600x300')

'''
tkinter.filedialog.askopenfilenames(**options)
Create an Open dialog and return the selected filename(s) that correspond to existing file(s).
'''


def select_file():
    filetypes = (('audio files', '*.wav'), ('audio files', '*.mp3'))  # only accepts '.wav' and '.mp3' files
    filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    # tkinter.messagebox — Tkinter message prompts
    showinfo(title='Selected File', message=filename)  # placeholder 1

    filename_label = ttk.Label(root, text=filename)  # placeholder 2
    filename_label.pack(side="bottom")



def audiofileChannels(filename):
    raw_audio = AudioSegment.from_file("pt.wav", format="wav")
    channel_count = raw_audio.channels
    print(channel_count)

    mono_wav = raw_audio.set_channels(1)
    mono_wav.export("pt_mono.wav", format="wav")
    mono_wav_audio = AudioSegment.from_file("pt_mono.wav", format="wav")

    channel_count = mono_wav_audio.channels
    print(channel_count)


# open button
open_button = ttk.Button(root, text=' Upload an Audio File ', command=select_file)

open_button.pack(expand=True)

# run application
root.mainloop()
