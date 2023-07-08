import os
import json
from datetime import datetime
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QMainWindow

class HelperPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spending Reduction Categories")

        self.resize(800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.current_month = datetime.now().strftime("%B")

        # Read the JSON file
        file_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'expenses.json')
        with open(file_path) as file:
            self.data = json.load(file)


        self.budget = self.data[self.current_month]['budget']
        self.total_sum = self.data[self.current_month]['totalSum']
        self.money = self.data[self.current_month]['money']
        
        self.setup_ui()
        self.create_return_main_button()

        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(220, 240, 230))
        self.setPalette(palette)
        

    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Calculate the remaining amount to fulfill the budget
        remaining_amount = self.budget - self.total_sum

        # Identify the categories with excessive spending
        categories_to_reduce = []
        for category, details in self.money.items():
            sum_of_amounts = details['sumOfAmounts']
            if sum_of_amounts > 0 and sum_of_amounts > self.budget:
                categories_to_reduce.append(category)

        # Display the categories to reduce spending
        label = QLabel("Categories to reduce spending:")
        label.setStyleSheet("color: black; font-weight: bold; font-size: 16px;")
        self.layout.addWidget(label)

        for category in categories_to_reduce:
            category_label = QLabel(category)
            category_label.setStyleSheet("color: black;")
            self.layout.addWidget(category_label)

        central_widget.setLayout(self.layout)


    def create_return_main_button(self):
        """
        Create a button for returning to the main page.
        """
        self.return_main_button = QPushButton("Back to Main Page")
        self.layout.addWidget(self.return_main_button)
        self.return_main_button.setStyleSheet(
            "background-color: #5DA56C; color: white; font-weight: bold; font-size: 14px;")
