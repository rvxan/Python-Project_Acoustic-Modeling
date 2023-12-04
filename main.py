import tkinter as tk
from tkinter import filedialog
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pydub import AudioSegment
import ffmpeg

# use model-controller-view-app design
# create sound app
class SoundApp(tk.Tk):
    def __init__(self, root):
        super().__init__()

        self.root = root
        self.root.title('Sound App: Reverb Time Analyzer')
        self.root.geometry('200x100')

        # choose file button
        self.upload_button = tk.Button(root, text=' Upload an Audio File ', command=self.upload_file)
        self.upload_button.pack()

        self.fig, self.ax = plt.subplots(3, 2, figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def upload_file(self):
        # only accepts '.wav' and '.mp3' files
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3")])

    def audio_converter(self, file_path):
        # check if the file uploaded is a .wav file or an .mp3 file
        if file_path.lower().endswith('.mp3'):
            src = file_path
            dst = f'{file_path}.wav'

            # converts .mp3 to .wav
            sound = AudioSegment.from_mp3(src)
            sound.export(dst, format="wav")
            file_path = dst
            pass

        sample_rate, data = wav.read(file_path)  # audio file uploaded by user

        # check if the file uploaded has > 1 channel
        raw_audio = AudioSegment.from_file("pt.wav", format="wav")
        channel_count = raw_audio.channels

        mono_wav = raw_audio.set_channels(1)
        mono_wav.export("pt_mono.wav", format="wav")
        mono_wav_audio = AudioSegment.from_file("pt_mono.wav", format="wav")

        channel_count = mono_wav_audio.channels
        data = channel_count
        # data = np.mean(data, axis=1)

        return sample_rate, data

    def analyze_reverb(self, data, sample_rate):

        spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))


if __name__ == '__main__':
    root = tk.Tk()
    app = SoundApp(root)
    root.mainloop()
