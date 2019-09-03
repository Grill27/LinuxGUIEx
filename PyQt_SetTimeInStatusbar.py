import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDate, Qt, QTime
class MyApp(QMainWindow):
	def __init__(self):
		super().__init__()
		self.date = QDate.currentDate()
		self.initUI()
	
	def initUI(self):
		time = QTime.currentTime()
		self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate)
				+ " " + time.toString())
		self.setWindowTitle('Date')
		self.setGeometry(300, 300, 400, 200)
		self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
