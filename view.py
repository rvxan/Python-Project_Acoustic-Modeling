# view.py
import tkinter as tk
from tkinter import filedialog, ttk


class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # GUI components
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

        choose_file_button = ttk.Button(self.load_file_frame, text="Browse", command=self.getfilepath)
        choose_file_button.grid(row=2, column=0, sticky='W')

        load_file_button = ttk.Button(self.load_file_frame, text="Upload", command=self.loadfilepath)
        load_file_button.grid(row=1, column=1, sticky='E')

        self.data_file_frame = ttk.LabelFrame(self.mainframe, padding='5 5 5 5', text='Data')
        self.data_file_frame.grid(column=0, row=1, sticky='NEW')
        self.data_file_frame.rowconfigure(1, weight=1)
        self.data_file_frame.columnconfigure(0, weight=1)

        show_plot = ttk.Button(self.data_file_frame, text='Plot Waveform', command=self.createplot)
        show_plot.grid(column=0, row=2, sticky='WN')

        show_time = ttk.Button(self.data_file_frame, text='Time', command=self.extracttime)
        show_time.grid(column=0, row=3, sticky='WN')

        show_plot2 = ttk.Button(self.data_file_frame, text='Resonance Frequency ', command=self.PlotFrequency)
        show_plot2.grid(column=0, row=4, sticky='WN')

        show_plot3 = ttk.Button(self.data_file_frame, text='RT60 Plot', command=self.RT60)
        show_plot3.grid(column=0, row=5, sticky='WN')

        show_plot3 = ttk.Button(self.data_file_frame, text='Frequency and Amplitude', command=self.Frequency)
        show_plot3.grid(column=0, row=6, sticky='WN')

        show_plot3 = ttk.Button(self.data_file_frame, text='RT60 Average', command=self.RT60avg)
        show_plot3.grid(column=0, row=7, sticky='WN')

        self.status_frame = ttk.Frame(self.root, relief='sunken', padding='2 2 2 2')
        self.status_frame.grid(row=1, column=0, sticky='EWS')
        self._status_msg.set('')
        status = ttk.Label(self.status_frame, textvariable=self._status_msg, anchor=W)
        status.grid(row=0, column=0, sticky='EW')

        self.highest_resonance.set('')

    def get_filepath(self):
        return self.choose_file_text.get()
