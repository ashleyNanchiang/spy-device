import numpy as np
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets  # Added QtWidgets
import pyqtgraph as pg
import struct
import pyaudio
from scipy.fftpack import fft
import sys

class AudioStream(object):
    def __init__(self):
        # 1. Initialize the Application FIRST
        self.app = QtWidgets.QApplication(sys.argv)
        
        # pyqtgraph stuff
        pg.setConfigOptions(antialias=True)
        self.traces = dict()
        
        # Use GraphicsLayoutWidget for an easier layout management
        self.win = pg.GraphicsLayoutWidget(title='Spectrum Analyzer')
        self.win.setWindowTitle('Spectrum Analyzer')
        self.win.setGeometry(5, 115, 1910, 1070)
        self.win.show() # Make sure the window actually shows

        # Axis setup
        wf_xlabels = [(0, '0'), (2048, '2048'), (4096, '4096')]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        self.waveform = self.win.addPlot(
            title='WAVEFORM', row=1, col=1, axisItems={'bottom': wf_xaxis}
        )
        
        self.spectrum = self.win.addPlot(
            title='SPECTRUM', row=2, col=1
        )

        # pyaudio setup
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )
        
        self.x = np.arange(0, 2 * self.CHUNK, 2)
        self.f = np.linspace(0, self.RATE / 2, int(self.CHUNK / 2))

    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setYRange(0, 255, padding=0)
                self.waveform.setXRange(0, 2 * self.CHUNK, padding=0.005)
            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen='m', width=3)
                self.spectrum.setLogMode(x=True, y=True)
                self.spectrum.setYRange(-4, 0, padding=0)
                self.spectrum.setXRange(np.log10(20), np.log10(self.RATE / 2), padding=0.005)

    def update(self):
        try:
            wf_data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            # Unpack as signed shorts 'h' for 16-bit audio rather than 'B'
            wf_data = struct.unpack(str(self.CHUNK) + 'h', wf_data)
            wf_data = np.array(wf_data, dtype='int16')
            
            # Normalize for visualization
            wf_plot = (wf_data * 0.005) + 128 
            self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_plot)

            # FFT Logic
            sp_data = fft(wf_data)
            sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]) * 2 / (32768 * self.CHUNK)
            self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)
        except Exception as e:
            print(f"Error updating: {e}")

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        # 2. Use the app instance to start the event loop
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            sys.exit(self.app.exec_())

if __name__ == '__main__':
    audio_app = AudioStream()
    audio_app.animation()