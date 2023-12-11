import os.path
import scipy
from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
from matplotlib.figure import Figure
from pydub import AudioSegment
import wave
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.io import wavfile
from scipy.signal import welch
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np


class RT60_AnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RT60 Audio Analyzer")
        self.mainframe = None
        self.load_file_frame = None
        self.status_frame = None
        self.choose_file_text = None

        self.filepath = None
        self.wav_file = None
        self.raw_data = None

        self.RT60values = None
        self.count = 0
        self.RT60values = {1: None, 2: None, 3: None}
        self.frame_amount = None
        self.highest_resonance = StringVar()

        self._filepath = StringVar()
        self.str_filepath = None
        self._status_msg = StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.root.geometry('1000x700')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.mainframe = ttk.Frame(self.root, padding='5 5 5 5')
        self.mainframe.grid(row=0, column=0, sticky="NEWS")
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0, weight=1)

        self.load_file_frame = ttk.LabelFrame(self.mainframe, padding='5 5 5 5', text='Choose File')
        self.load_file_frame.grid(column=0, row=0, sticky='NEW')
        self.load_file_frame.columnconfigure(0, weight=1)
        self.load_file_frame.rowconfigure(0, weight=1)

        choose_file_label = ttk.Label(self.load_file_frame, text='Please input a WAV file you would like to analyze:')
        choose_file_label.grid(column=0, row=0, columnspan=1, sticky='NEWS')

        self.choose_file_text = ttk.Entry(self.load_file_frame, width=70, textvariable=self._filepath)
        self.choose_file_text.grid(column=0, row=1, sticky='NEWS')

        choose_file_button = ttk.Button(self.load_file_frame, text="Browse", command=self.get_filepath)
        choose_file_button.grid(row=2, column=0, sticky='W')

        load_file_button = ttk.Button(self.load_file_frame, text="Upload", command=self.upload_filepath)
        load_file_button.grid(row=1, column=1, sticky='E')

        self.data_file_frame = ttk.LabelFrame(self.mainframe, padding='5 5 5 5', text='Data')
        self.data_file_frame.grid(column=0, row=1, sticky='NEW')
        self.data_file_frame.rowconfigure(1, weight=1)
        self.data_file_frame.columnconfigure(0, weight=1)

        show_plot = ttk.Button(self.data_file_frame, text='Plot Waveform', command=self.waveform_plot)
        show_plot.grid(column=0, row=2, sticky='WN')

        show_time = ttk.Button(self.data_file_frame, text='Time', command=self.time_duration)
        show_time.grid(column=0, row=3, sticky='WN')

        show_plot2 = ttk.Button(self.data_file_frame, text='Highest Resonance Frequency ',
                                command=self.get_highest_resonance)
        show_plot2.grid(column=0, row=4, sticky='EN')

        show_plot2 = ttk.Button(self.data_file_frame, text='Resonance Frequency ', command=self.PlotFrequency)
        show_plot2.grid(column=0, row=4, sticky='WN')

        show_plot3 = ttk.Button(self.data_file_frame, text='RT60 Plot', command=self.rt60)
        show_plot3.grid(column=0, row=5, sticky='WN')

        show_plot3 = ttk.Button(self.data_file_frame, text='Frequency and Amplitude', command=self.Frequency)
        show_plot3.grid(column=0, row=6, sticky='EN')

        show_plot3 = ttk.Button(self.data_file_frame, text='RT60 Average', command=self.rt60_avg)
        show_plot3.grid(column=0, row=7, sticky='WN')

        show_plot4 = ttk.Button(self.data_file_frame, text='Frequency Spectrogram', command=self.spectrogram())
        show_plot4.grid(column=0, row=7, sticky='EN')

        self.status_frame = ttk.Frame(self.root, relief='sunken', padding='2 2 2 2')
        self.status_frame.grid(row=1, column=0, sticky='EWS')
        self._status_msg.set('')
        status = ttk.Label(self.status_frame, textvariable=self._status_msg, anchor=W)
        status.grid(row=0, column=0, sticky='EW')

        self.highest_resonance.set('')

    def get_wavdata(self, audio_file):
        wav_file = wave.open(audio_file, 'rb')
        audio_data = wav_file.readframes(wav_file.getnframes())
        return np.frombuffer(audio_data, np.int16)

    def get_filepath(self):
        self._filepath.set(tk.filedialog.askopenfilename())

    def upload_filepath(self):
        try:
            if str(self.choose_file_text.get()) != '':
                self._filepath.set(self.choose_file_text.get())
                self.sb(f'File path set as \"{self._filepath.get()}\"')
                self.convert_to_wav(self._filepath.get())
            else:
                self.sb('File path cannot be empty.')
        except Exception as e:
            self.sb(f'The error is {e}')

    def sb(self, msg):
        self._status_msg.set(msg)

    def convert_to_wav(self, audio_file_path):  # file convert from .mp3 to .wav does not work
        if not os.path.isfile(audio_file_path):
            self.sb(f"Error: File {audio_file_path} not found.")
            return

        supported_ext = ['.mp3', '.wav']  # audio extensions, program only works with .wav file
        file_ext = os.path.splitext(audio_file_path)[1].lower()

        if file_ext not in supported_ext:
            self.sb(f"Error: Unsupported file format ({file_ext}). Please upload a file with formats {supported_ext}.")
            return
        else:
            try:
                audio_file = AudioSegment.from_file(
                    audio_file_path,
                    format=os.path.splitext(audio_file_path)[-1].strip('.')
                )
                wav_data = audio_file.raw_data
                self.wav_file = AudioSegment(
                    wav_data,
                    frame_rate=audio_file.frame_rate,
                    sample_width=audio_file.sample_width,
                    channels=audio_file.channels
                )
                self.wav_file = self.wav_file.set_channels(1)
                self.frame_amount = len(self.wav_file.get_array_of_samples())
                self.wav_file.set_channels(1)
                self.raw_data = np.frombuffer(self.wav_file.raw_data, dtype=np.int16)
                self.get_highest_resonance()
            except Exception as e:
                self.sb(f"Error during conversion: {e}")

    def time_duration(self):
        if self.wav_file is not None:
            time_duration = len(self.wav_file) / 1000

            time_min = time_duration // 60
            time_sec = round(time_duration % 60)

            time_string = f'{time_min} minutes {time_sec} seconds'
            self.sb(f"The time duration for the audio file uploaded is: {time_string}")
        else:
            self.sb(f'Please upload an audio file')

    def waveform_plot(self):
        # audioSpectrum mono only
        # shows waveform and spectrogram
        if self.wav_file is not None:
            samples = np.array(self.wav_file.get_array_of_samples())
            # Calculate time values for x-axis
            length = len(self.wav_file) / 1000  # duration in seconds
            time = np.linspace(0, length, num=len(samples))

            # Plot the waveform
            figure = Figure(figsize=(7, 4), dpi=100)
            plot = figure.add_subplot(1, 1, 1)
            plot.plot(time, samples)
            plot.set_xlabel("Time (seconds)")
            plot.set_ylabel("Amplitude")
            plot.set_title('Waveform Plot')

            canvas = FigureCanvasTkAgg(figure, master=self.data_file_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=0, row=3)
        else:
            self.sb(f'Make sure to press load')

    def get_highest_resonance(self):
        if self.wav_file is not None:
            sample_rate, data = wavfile.read(self._filepath.get())  # reads .wav file from file path not Audio Segment
            frequencies, power = welch(data, sample_rate, nperseg=4096)
            dominant_frequency = frequencies[np.argmax(power)]

            self.highest_resonance.set(str(dominant_frequency))

            # define variables for plot
            n = len(data)  # length of signal
            k = np.arange(n)
            T = n / sample_rate
            frq = k / T  # two sides frequency range
            frq = frq[:len(frq) // 2]  # one side frequency range
            Y = np.fft.fft(data) / n  # dft and normalization
            Y = Y[:n // 2]

            # plot
            figure = Figure(figsize=(7, 4), dpi=100)
            plot = figure.add_subplot(1, 1, 1)
            plt.yscale('symlog')
            plt.title('Resonance')
            plt.plot(frq, abs(Y))  # plot the power
            plt.xlim(0, 1500)  # limit x-axis to 1.5 kHz
            plt.xlabel('Freq (Hz)')
            plt.ylabel('Power')

            canvas = FigureCanvasTkAgg(figure, master=self.data_file_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=0, row=3)

    def PlotFrequency(self):
        if self.wav_file is not None:
            # Convert AudioSegment to NumPy array
            samples = np.array(self.wav_file.get_array_of_samples())

            # Find the index of the maximum amplitude
            max_amplitude_index = np.argmax(np.abs(samples))

            # Calculate time corresponding to the index
            time_of_max_amplitude = max_amplitude_index / self.wav_file.frame_rate
            self.get_highest_resonance()
            self.sb(
                f"Highest amplitude happened at {round(time_of_max_amplitude, 2)} and resonance frequency was {round(float(self.highest_resonance.get()), 2)}")
        else:
            self.sb(f'Press upload for file')

    def rt60(self):
        if self.wav_file is not None:
            sample_rate = self.wav_file.frame_rate
            data = np.array(self.wav_file.get_array_of_samples())
            spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024)
            plt.close()

            def find_target_frequency(freqs):
                for x in freqs:
                    if x > 1000:
                        break
                return x

            def frequency_check(target_freq):
                global target_frequency  # sets as a global var
                target_frequency = find_target_frequency(freqs)
                index_of_frequency = np.where(freqs == target_frequency)[0][0]

                data_for_frequency = spectrum[index_of_frequency]

                data_in_db_fun = 10 * np.log10(data_for_frequency + 1)
                return data_in_db_fun

            def find_nearest_value(array, value):
                array = np.asarray(array)
                idx = (np.abs(array - value)).argmin()
                return array[idx]

            loop = {1: 20, 2: 1000, 3: 5000}
            self.count += 1
            self.count = self.count % 3 + 1
            data_in_db = frequency_check(loop[self.count])

            index_of_max = np.argmax(data_in_db)

            value_of_max = data_in_db[index_of_max]

            sliced_array = data_in_db[index_of_max:]
            value_of_max_less_5 = value_of_max - 5

            value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
            index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

            value_of_max_less_25 = value_of_max - 25
            value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
            index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)

            rt60 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]

            seconds = np.round(abs(rt60), 3)
            self.sb(f'The RT60 reverb time at freq {int(target_frequency)} Hz is {seconds} seconds')
            self.RT60values[self.count] = seconds

            figure = Figure(figsize=(7, 4), dpi=100)
            plot = figure.add_subplot(1, 1, 1)
            plot.plot(t, data_in_db, linewidth=1, alpha=.7, color='#004bc6')
            plot.plot(t[index_of_max], data_in_db[index_of_max], 'go', label='Max Index')
            plot.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo', label='5 dB Less')
            plot.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro', label='25 db Less')
            plot.set_xlabel("Time (seconds)")
            plot.set_ylabel("dB")
            plot.set_title("Audio Waveform")
            plot.legend()

            canvas = FigureCanvasTkAgg(figure, master=self.data_file_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=0, row=3)
        else:
            self.sb(f'Make sure to press load')

    def rt60_avg(self):
        try:
            if self.wav_file is not None:
                s = 0
                for x in range(3):
                    s += self.RT60values[x + 1]
                avg = s / 3
                avg -= 0.5
                self.sb(f'The RT60 minus 0.5 is {round(avg, 3)}')
            else:
                self.sb(f'Make sure to press load')
        except Exception as e:
            self.sb(f"Press RT60 plot at least 3 times first")

    def Frequency(self):
        if self.wav_file is not None:
            def calculate_frequency_spectrum(sample_rate, frame_rate):
                # Perform Fourier Transform
                fft_result = np.fft.fft(samples)

                # Calculate the frequencies corresponding to the FFT result
                frequencies = np.fft.fftfreq(len(fft_result), 1 / frame_rate)

                # Take the absolute value to get the amplitude spectrum
                amplitudes = np.abs(fft_result)

                # Keep only the positive frequencies
                positive_frequencies = frequencies[:len(frequencies) // 2]
                positive_amplitudes = amplitudes[:len(amplitudes) // 2]

                return positive_frequencies, positive_amplitudes

            samples = np.array(self.wav_file.get_array_of_samples())
            frequencies, amplitudes = calculate_frequency_spectrum(samples, self.wav_file.frame_rate)

            # Filter frequencies within the specified range
            mask = np.logical_and(frequencies >= 20, frequencies <= 20000)
            filtered_frequencies = frequencies[mask]
            filtered_amplitudes = amplitudes[mask]

            # Plot the specific frequencies
            figure = Figure(figsize=(7, 4), dpi=100)
            plot = figure.add_subplot(1, 1, 1)
            plot.plot(filtered_frequencies, filtered_amplitudes)

            plot.set_xlabel("Frequency (Hz)")
            plot.set_ylabel("Amplitude")
            plot.set_title(f"Frequency Spectrum ({20} Hz to {20000} Hz)")

            canvas = FigureCanvasTkAgg(figure, master=self.data_file_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=0, row=3)
        else:
            self.sb(f'Make sure to press load')

    def spectrogram(self):
        if self.wav_file is not None:
            sample_rate, data = wavfile.read(self._filepath.get())  # reads .wav file from file path not Audio Segment
            # plot spectrogram
            spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('OrRd_r'))
            cbar = plt.colorbar(im)
            figure = Figure(figsize=(7, 4), dpi=100)
            plot = figure.add_subplot(1, 1, 1)
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            cbar.set_label('Intensity (dB)')

            canvas = FigureCanvasTkAgg(figure, master=self.data_file_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=0, row=3)

        else:
            self.sb(f'Make sure to press load')


if __name__ == "__main__":
    root = Tk()
    app = RT60_AnalyzerApp(root)
    root.mainloop()
