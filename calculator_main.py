import sys
from PyQt5.QtWidgets import *

left_number = 0
mid_op = ''
flag = False
stk = []


class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QGridLayout()

        # 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_clear_equal = QGridLayout()
        layout_number = QGridLayout()
        layout_operation = QGridLayout()
        layout_equation_solution = QFormLayout()

        # label_number 레이아웃에 수식, 답 위젯을 추가
        # 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        label_number = QLabel("Number: ")
        self.number_display = QLineEdit("0")
        layout_equation_solution.addRow(label_number, self.number_display)

        # %, =, clear, backspace 버튼 생성
        # %, =, clear, backspace 버튼 클릭 시 시그널 설정
        button_Percentage = QPushButton("%")
        button_Percentage.clicked.connect(self.button_Percentage_clicked)

        button_clear = QPushButton("C")
        button_clear.clicked.connect(self.button_clear_clicked)

        button_clear2 = QPushButton("CE")
        button_clear2.clicked.connect(self.button_clear_clicked)

        button_equal = QPushButton("=")
        button_equal.clicked.connect(self.button_equal_clicked)

        button_backspace = QPushButton("BackSpace")
        button_backspace.clicked.connect(self.button_backspace_clicked)

        # %, =, clear, backspace 버튼을 layout_clear_equal 레이아웃에 추가
        layout_number.addWidget(button_Percentage, 0, 0)
        layout_number.addWidget(button_clear, 0, 1)
        layout_number.addWidget(button_clear2, 0, 2)
        layout_number.addWidget(button_backspace, 0, 3)
        layout_number.addWidget(button_equal, 0, 4)

        # 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        # 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}

        for number in range(10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(
                lambda state, num=number: self.number_button_clicked(num))
            if number > 0:
                x, y = divmod(number-1, 3)
                layout_number.addWidget(
                    number_button_dict[number], x + 1, y)
            elif number == 0:
                layout_number.addWidget(number_button_dict[number], 4, 1)

        # 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(
            lambda state, num=".": self.number_button_clicked(num))
        layout_number.addWidget(button_dot, 4, 2)

        button_double_zero = QPushButton("00")
        button_double_zero.clicked.connect(
            lambda state, num="00": self.number_button_clicked(num))
        layout_number.addWidget(button_double_zero, 4, 0)

        # 사칙연상 버튼 생성
        button_plus = QPushButton("+")
        button_plus.clicked.connect(
            lambda state, operation="+": self.button_operation_clicked(operation))
        layout_number.addWidget(button_plus, 1, 3)

        button_minus = QPushButton("-")
        button_minus.clicked.connect(
            lambda state, operation="-": self.button_operation_clicked(operation))
        layout_number.addWidget(button_minus, 2, 3)

        button_product = QPushButton("x")
        button_product.clicked.connect(
            lambda state, operation="*": self.button_operation_clicked(operation))
        layout_number.addWidget(button_product, 3, 3)

        button_division = QPushButton("/")
        button_division.clicked.connect(
            lambda state, operation="/": self.button_operation_clicked(operation))
        layout_number.addWidget(button_division, 4, 3)

        # 사칙연산 버튼을 layout_operation 레이아웃에 추가
        layout_operation.addWidget(button_plus)
        layout_operation.addWidget(button_minus)
        layout_operation.addWidget(button_product)
        layout_operation.addWidget(button_division)

        # 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution, 0, 0)
        main_layout.addLayout(layout_clear_equal, 1, 0)
        main_layout.addLayout(layout_number, 2, 0)
        main_layout.addLayout(layout_operation, 3, 0)
        self.setLayout(main_layout)

        self.show()

    #################
    ### functions ###
    #################

    def button_Percentage_clicked(self):
        equation = self.equation.text()
        equation = round((equation / 100), 2)
        self.equation.setText(equation)

    def number_button_clicked(self, num):
        temp = ""
        if stk:  # 이전에 계산한 값이 있는경우 또는 숫자를 입력 후 연산자를 입력하지 않고, '='를 누른 경우
            temp += stk.pop()
        equation = self.number_display.text()
        if int(equation) + int(num) == 0:
            self.number_display.setText("0")
        else:
            if equation[0] == '0':
                equation = equation[1:] + str(num)
            else:
                equation += str(num)
            self.number_display.setText(equation[len(temp):])

    def button_operation_clicked(self, operation):
        global left_number, mid_op, flag
        equation = self.number_display.text()
        left_number += int(equation)
        mid_op += operation
        equation = "0"
        flag = True
        self.number_display.setText(equation)

    def button_equal_clicked(self):
        equation = self.number_display.text()
        global flag, left_number, mid_op, stk

        if flag:
            if mid_op == '+':
                equation = left_number + int(equation)
            elif mid_op == '-':
                equation = left_number - int(equation)
            elif mid_op == '*':
                equation = left_number * int(equation)
            elif mid_op == '/':
                equation = left_number / int(equation)

        self.number_display.setText(str(equation))
        left_number = 0
        mid_op = ""
        flag = False
        stk.append(str(equation))

    def button_clear_clicked(self):
        self.number_display.setText("0")

    def button_backspace_clicked(self):
        equation = self.number_display.text()
        equation = equation[:-1]
        self.number_display.setText(equation)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()

    sys.exit(app.exec_())
