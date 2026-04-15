import pyaudio
import struct       # auido from binary to integers
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

CHUNK = 1024 * 4   # how many audio samples per frame to display
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100        # samples per second

class AudioVisulaizer(FigureCanvas):

    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

        p = pyaudio.PyAudio()       # main pyaudio object

        # stream object
        self.stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK
        )
        plt.ion()
        # self.fig, ax = plt.subplots()
        
        x = np.arange(0, 2 * CHUNK, 2)
        self.line, = self.ax.plot(x, np.random.rand(CHUNK)) # CHUNK length because we sliced it [::2]
        # line, = ax.plot(x, np.zeros(CHUNK), '-', lw=1)
        self.ax.set_ylim(-255, 255)
        self.ax.set_xlim(0, CHUNK)

        self.on = False

    def update(self):
        while self.on:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            # print(data)
            # data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='B')[::2] + 127
            data_int = np.frombuffer(data, dtype=np.int16)
            self.line.set_ydata(data_int)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    def turnOn(self):
        self.on = True

    def turnOff(self):
        self.on = False

