import math

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
        QSizePolicy, QToolButton, QWidget)

class Button(QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

class Calculator(QWidget):
	NumDigitButtons = 10

	def __init__(self, parent=None):
		# Qwidget __init__ 
		super(Calculator, self).__init__(parent)

		self.pendingAdditiveOperator = ''
		self.pendingMultiplicativeOperator = ''
		
		self.sumSoFar = 0.0
		self.factorSoFar = 0.0
		self.waitingForOperand = True

		# QLineEdit Properties
		self.display = QLineEdit('0')
		self.display.setReadOnly(True)
		self.display.setAlignment(Qt.AlignRight)
		self.display.setMaxLength(15)

		# QLineEdit font Properties
		font = self.display.font()
		font.setPointSize(font.pointSize() + 8)
		self.display.setFont(font)

		# Add Button 
		self.digitButtons = []
		
		for i in range(Calculator.NumDigitButtons):
			self.digitButtons.append(self.createButton(str(i), self.digitClicked))

		self.delButton = self.createButton("Del", self.delClicked)
		self.plusButton = self.createButton("+", self.additiveOperatorClicked)
		self.equalButton = self.createButton("=", self.equalClicked)
		
		self.clearButton = self.createButton("C", self.clear)
		self.divideButton = self.createButton(u"\N{DIVISION SIGN}", 
				self.multiplicativeOperatorClicked)
		self.minusButton = self.createButton("-", self.additiveOperatorClicked)
		self.multiButton = self.createButton(u"\N{MULTIPLICATION SIGN}", 
				self.multiplicativeOperatorClicked)

		mainLayout = QGridLayout()
		mainLayout.setSizeConstraint(QLayout.SetFixedSize)

		# Row, Column, Vertical Size, Horizontal Size
		mainLayout.addWidget(self.display, 0, 0, 1, 6)
		mainLayout.addWidget(self.delButton, 5, 3, 1, 1)

		for i in range(1, Calculator.NumDigitButtons):
			row = ((9 - i) / 3) + 2
			column = ((i - 1) % 3) + 1
			mainLayout.addWidget(self.digitButtons[i], row, column)

		mainLayout.addWidget(self.digitButtons[0], 5, 1, 1, 2)
		mainLayout.addWidget(self.plusButton, 1, 1, 1, 1)
		mainLayout.addWidget(self.minusButton, 1, 2, 1, 1)
		mainLayout.addWidget(self.multiButton, 1, 3, 1, 1)
		mainLayout.addWidget(self.divideButton, 1, 4, 1, 1)
		mainLayout.addWidget(self.clearButton, 2, 4, 2, 1)
		mainLayout.addWidget(self.equalButton, 4, 4, 2, 1)

		self.setLayout(mainLayout)
		self.setWindowTitle("Calculator")

	def digitClicked(self):
		clickedButton = self.sender()
		digitValue = int(clickedButton.text())

		if self.display.text() == '0' and digitValue == 0.0:
			return

		if self.waitingForOperand:
			self.display.clear()
			self.waitingForOperand = False

		self.display.setText(self.display.text() + str(digitValue))

	def createButton(self, text, member):
		button = Button(text)
		button.clicked.connect(member)
		return button

	def delClicked(self):
		if self.waitingForOperand:
			return
		
		text = self.display.text()[:-1]
		if not text:
			text = '0'
			self.waitingForOperand = True

		self.display.setText(text)

	def multiplicativeOperatorClicked(self):
		clickedButton = self.sender()
		clickedOperator = clickedButton.text()
		operand = float(self.display.text())
		
		if self.pendingMultiplicativeOperator:
			if not self.calculate(operand, self.pendingMultiplicativeOperator):
				self.abortOperation()
				return
				
			self.display.setText(str(self.factorSoFar))
		else:
			self.factorSoFar = operand
			
		self.pendingMultiplicativeOperator = clickedOperator
		self.waitingForOperand = True

	def additiveOperatorClicked(self):
		clickedButton = self.sender()
		clickedOperator = clickedButton.text()
		operand = float(self.display.text())

		if self.pendingMultiplicativeOperator:
			if not self.calculate(operand, self.pendingMultiplicativeOperator):
				self.abortOperation()
				return

			self.display.setText(str(self.factorSoFar))
			operand = self.factorSoFar
			self.factorSoFar = 0.0
			self.pendingMultiplicativeOperator = ''

		if self.pendingAdditiveOperator:
			if not self.calculate(operand, self.pendingAdditiveOperator):
				self.abortOperation()
				return

			self.display.setText(str(self.sumSoFar))
		else:
			self.sumSoFar = operand
		
		self.pendingAdditiveOperator = clickedOperator
		self.waitingForOperand = True

	def equalClicked(self):
		operand = float(self.display.text())

		if self.pendingMultiplicativeOperator:
			if not self.calculate(operand, self.pendingMultiplicativeOperator):
				self.abortOperation()
				return

			operand = self.factorSoFar
			self.factorSoFar = 0.0
			self.pendingMultiplicativeOperator = ''

		if self.pendingAdditiveOperator:
			if not self.calculate(operand, self.pendingAdditiveOperator):
				self.abortOperation()
				return

			self.pendingAdditiveOperator = ''
		else:
			self.sumSoFar = operand

		self.display.setText(str(self.sumSoFar))
		self.sumSoFar = 0.0
		self.waitingForOperand = True

	def clear(self):
		self.sumSoFar = 0.0
		self.factorSoFar = 0.0
		self.pendingAdditiveOperator = ''
		self.pendingMultiplicativeOperator = ''
		self.display.setText('0')
		self.waitingForOperand = True

	def calculate(self, rightOperand, pendingOperator):
		if pendingOperator == "+":
			self.sumSoFar += rightOperand
		elif pendingOperator == "-":
			self.sumSoFar -= rightOperand
		elif pendingOperator == u"\N{MULTIPLICATION SIGN}":
			self.factorSoFar *= rightOperand
		elif pendingOperator == u"\N{DIVISION SIGN}":
			if rightOperand == 0.0:
				return False
				
			self.factorSoFar /= rightOperand
		return True


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
