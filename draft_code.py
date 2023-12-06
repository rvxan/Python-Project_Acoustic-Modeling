import tkinter as tk
from tkinter import filedialog
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pydub import AudioSegment
import wave

class RT60Analyzer:
    def __init__(self, master):
        self.master = master
        self.master.title("RT60 Analyzer")

        self.load_button = tk.Button(master, text="Load File", command=self.load_file)
        self.load_button.pack()

        self.fig, self.ax = plt.subplots(3, 2, figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3")])
        if file_path:
            # Load and preprocess the audio file
            sample_rate, data = self.process_audio(file_path)

            # Plot waveform
            self.plot_waveform(data, sample_rate)

            # Analyze RT60
            rt60_low, rt60_mid, rt60_high, freq_max_amp, rt60_diff = self.analyze_rt60(data, sample_rate)

            # Plot RT60 for Low, Mid, High frequencies
            self.plot_rt60(rt60_low, rt60_mid, rt60_high, freq_max_amp, rt60_diff)

    def process_audio(self, file_path):
        # Read the audio file
        if file_path.lower().endswith(('.mp3', '.aac')):
            # Convert to WAV if the file is not in WAV format
            # Add your code to convert mp3/aac to wav
            pass
        sample_rate, data = wav.read(file_path)

        # Check for multi-channel and convert to one channel
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)

        return sample_rate, data

    # works only with .wav files
    def remove_metadata(self, file_path):
        # Open the input WAV file
        with wave.open(file_path, 'rb') as file_wave:
            # Get the parameters of the input WAV file
            params = file_wave.getparams()

            # Create a new WAV file for writing
            with wave.open(file_path, 'wb') as output_wave:
                # Set the parameters for the output WAV file
                output_wave.setparams(params)

                # Read and write audio frames
                frames = file_wave.readframes(params.nframes)
                output_wave.writeframes(frames)

    def plot_waveform(self, data, sample_rate):
        time = np.arange(0, len(data)) / sample_rate
        self.ax[0, 0].cla()
        self.ax[0, 0].plot(time, data)
        self.ax[0, 0].set_title("Waveform")
        self.canvas.draw()

    def analyze_rt60(self, data, sample_rate):
        # Implement RT60 analysis and return relevant values
        # Add your code to calculate RT60, frequency of greatest amplitude, RT60 differences
        pass

    def plot_rt60(self, rt60_low, rt60_mid, rt60_high, freq_max_amp, rt60_diff):
        # Implement plotting RT60 for Low, Mid, High frequencies
        # Add your code to create the necessary plots
        pass


if __name__ == '__main__':
    root = tk.Tk()
    app = RT60Analyzer(root)
    root.mainloop()
