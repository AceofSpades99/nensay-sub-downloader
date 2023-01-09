import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from frame.MainWindow import Ui_MainWindow
from frame.ui_decompress import Ui_ToSrtDialog


def windowActions():
	window.setupUi(window)
	# window.download_btn.clicked.connect(# ToDo)
	window.edit_btn.clicked.connect(dialog.open)
	window.exit_btn.clicked.connect(sys.exit)


def dialogActions():
	dialog.setupUi(dialog)
	dialog.browse.clicked.connect(dialog.browse_files)
	dialog.copyFiles.stateChanged.connect(dialog.checker)
	dialog.acceptCancel.accepted.connect(dialog.accepted)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = Ui_MainWindow()
	dialog = Ui_ToSrtDialog()
	windowActions()
	dialogActions()
	widget = QtWidgets.QStackedWidget()
	widget.addWidget(window)
	widget.show()
	sys.exit(app.exec_())
