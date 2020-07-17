import main_window
from PyQt5 import QtWidgets


class MainWnd(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		ui = main_window.Ui_MainWindow()
		ui.setupUi(self)


if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWnd().show()
	sys.exit(app.exec_())
