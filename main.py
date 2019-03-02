

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal
from yahoo_fin import stock_info as si

import pyqtgraph as pg
import numpy as np
from threading import Thread
import time
import collections

class SignalViewer(QApplication):
	emitter_signal = pyqtSignal(object)

	def __init__(self, num_signals):
		super().__init__([])
		# save number of signals
		self.nplots = num_signals
		# set number of samples to be displayed per signal at a time
		self.nsamples = 500
		# connect the signal to be emitted by the feeder to the slot of the plotWidget that will update the signals
		self.emitter_signal.connect(lambda values: self.update(values))
		# buffer to store the data from all signals
		self.buff = np.zeros((self.nplots, self.nsamples))
		# create a main window of the UI
		self.window = QMainWindow()
		# create a plot widget inside the main window
		self.p = pg.PlotWidget()
		self.window.setCentralWidget(self.p)
		# create curves for the signals
		self.curves = []
		for i in range(self.nplots):
			c = pg.PlotCurveItem(pen=(i, self.nplots * 1.3))
			self.p.addItem(c)
			self.curves.append(c)

	def update(self, data):
		# update buffer
		self.buff = np.concatenate([self.buff[:, 1:], np.reshape(data, (-1, 1))], axis=1)
		# update plots
		for i in range(self.nplots):
			self.curves[i].setData(self.buff[i])

	def start(self):
		self.window.show()
		self.exec_()

	def update_signals(self, values):
		self.emitter_signal.emit(values)

def start_feeder():
	while True:
		time.sleep(0.033)
		viewer.emitter_signal.emit(np.random.beta(1, 0.1, size=1))

if __name__ == "__main__":
	viewer = SignalViewer(num_signals=1)
	# launch feeder thread
	feeder_thread = Thread(target=start_feeder)
	feeder_thread.start()
	# start UI
	viewer.start()

