# model.py
import os
from tkinter import StringVar
from tkinter import filedialog as fd
import numpy as np
import matplotlib.pyplot as plt
from IPython.terminal.pt_inputhooks import tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pydub import AudioSegment
from scipy.io import wavfile
from scipy.signal import welch


class Model:
    def __init__(self):
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

    def getfilepath(self):
        self._filepath.set(tk.fd.askopenfilename())

    def load_file(self, filepath):
        try:
            if filepath:
                self.filepath = filepath
                self.convert_to_wav(filepath)
            else:
                raise ValueError('File path cannot be empty.')
        except Exception as e:
            raise ValueError(f'Error during file loading: {e}')

    def convert_to_wav(self, audio_file_path):
        supported_ext = ['.mp3', '.wav']  # audio extensions
        file_ext = os.path.splitext(audio_file_path)[1].lower()

        if file_ext not in supported_ext:  # if file is unsupported
            self.sb(f"Error: Unsupported file format ({file_ext}). Please upload a file with formats {supported_ext}.")
            return
        else:
            try:
                audio_file = AudioSegment.from_file(audio_file_path,
                            format=os.path.splitext(audio_file_path)[-1].strip('.'))
                wav_data = audio_file.raw_data
                self.wav_file = AudioSegment(wav_data, frame_rate=audio_file.frame_rate,
                                sample_width=audio_file.sample_width,
                                channels=audio_file.channels)
                self.wav_file = self.wav_file.set_channels(1)
                self.frame_amount = len(self.wav_file.get_array_of_samples())
                self.wav_file.set_channels(1)
                self.raw_data = np.frombuffer(self.wav_file.raw_data, dtype=np.int16)
                self.get_highest_resonance()
            except Exception as e:
                self.sb(f"Error during conversion: {e}")
        pass

    def time_audio(self):
        if self.wav_file is not None:
            time_duration = len(self.wav_file) / 1000

            time_min = time_duration // 60
            time_sec = round(time_duration % 60)
            time_string = f'{time_min} minutes {time_sec} seconds'
            self.sb(f"The time for the audio file uploaded is: {time_string}")
        else:
            self.sb(f'Please upload an audio file')
        pass

    def waveform_plot(self):
        # audioSpectrum mono only
        # shows waveform and spectrogram
        if self.wav_file is not None:
            sample_rate, data = wavfile.read(self.wav_file)  # reads .wav file

            # plot waveform of .wav file
            length = len(data) / sample_rate
            time = np.linspace(0., length, len(data))
            plt.plot(time, data, label="Mono Channel")
            plt.legend()
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")
            plt.show()
            # plot spectrogram
            spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('OrRd_r'))
            cbar = plt.colorbar(im)
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            cbar.set_label('Intensity (dB)')
            plt.show()
            print(f"Sample rate = {sample_rate} Hz")
            print(f"length = {length} s")
        pass

    def get_highest_resonance(self):
        if self.wav_file is not None:
            sample_rate, data = wavfile.read(self.wav_file)  # reads .wav file
            frequencies, power = welch(data, sample_rate, nperseg=4096)
            dominant_frequency = frequencies[np.argmax(power)]
            # print(f'dominant_frequency is {round(dominant_frequency)} Hz')

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
            plt.yscale('symlog')
            plt.plot(frq, abs(Y))  # plot the power
            plt.xlim(0, 1500)  # limit x-axis to 1.5 kHz
            plt.xlabel('Freq (Hz)')
            plt.ylabel('Power')
            plt.show()
        pass

    def plot_frequency(self):
        if self.wav_file is not None:

            sample_rate = np.array(self.wav_file.get_array_of_samples())  # converts AudioSegment to NumPy array

            # Find the index of the maximum amplitude
            max_amplitude_index = np.argmax(np.abs(sample_rate))

            # Calculate time corresponding to the index
            time_of_max_amplitude = max_amplitude_index / self.wav_file.frame_rate
            self.get_highest_resonance()
            self.sb(f"Highest amplitude happened at {round(time_of_max_amplitude, 2)} and the resonant frequency was {round(float(self.highest_resonance.get()), 2)}")
        else:
            self.sb(f'Make sure to press load')
        pass

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
                global target_frequency
                target_frequency = find_target_frequency(freqs)
                freq_index = np.where(freqs == target_frequency)[0][0]

                data_for_frequency = spectrum[freq_index]

                data_in_db_fun = 10 * np.log10(data_for_frequency + 1)
                return data_in_db_fun

            def find_nearest_value(array, value):
                array = np.asarray(array)
                index = (np.abs(array - value)).argmin()
                return array[index]

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
            self.sb(f'The RT60 reverb time at frequency {int(target_frequency)} Hz is {seconds} seconds')
            self.RT60values[self.count] = seconds

            figure = Figure(figsize=(7, 4), dpi=100)
            plot = figure.add_subplot(1, 1, 1)
            plot.plot(t, data_in_db, linewidth=1, alpha=.7, color='#004bc6')
            plot.plot(t[index_of_max], data_in_db[index_of_max], 'go')
            plot.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')
            plot.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')
            plot.set_xlabel("Time (seconds)")
            plot.set_ylabel("dB")
            plot.set_title("Waveform")

            canvas = FigureCanvasTkAgg(figure, master=self.data_file_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=0, row=3)
        else:
            self.sb(f'Make sure to press load')

        pass

    def calculate_rt60_avg(self):
        if self.wav_file is not None:
            s = 0
            for x in range(3):
                s += self.RT60values[x + 1]
            avg = s / 3
            avg -= 0.5
            self.sb(f'The RT60 minus 0.5 is {round(avg, 3)}')
        else:
            self.sb(f'Make sure to upload the audio file')

        pass

    def calculate_frequency_spectrum(self):
        if self.wav_audio is not None:
            def calculate_frequency_spectrum(sample_rate, frame_rate):
                # Perform Fourier Transform
                fft_result = np.fft.fft(sample_rate)

                # Calculate the frequencies corresponding to the FFT result
                freqs = np.fft.fftfreq(len(fft_result), 1 / frame_rate)

                # Take the absolute value to get the amplitude spectrum
                amplitudes = np.abs(fft_result)

                # Keep only the positive frequencies
                positive_frequencies = frequencies[:len(frequencies) // 2]
                positive_amplitudes = amplitudes[:len(amplitudes) // 2]

                return positive_frequencies, positive_amplitudes

            sample_rate = np.array(self.wav_file.get_array_of_samples())
            frequencies, amplitudes = calculate_frequency_spectrum(sample_rate, self.wav_file.frame_rate)

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
        pass

    def sb(self, param):
        pass
