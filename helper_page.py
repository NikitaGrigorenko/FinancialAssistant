import os
import json
from datetime import datetime
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QMainWindow


class HelperPage(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Spending Reduction Categories")

        # Set the initial size of the window
        self.resize(800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Get the current month
        self.current_month = datetime.now().strftime("%B")

        # Load the expense data from the JSON file
        file_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'expenses.json')
        with open(file_path) as file:
            self.data = json.load(file)

        # Get the budget, total sum, and money data for the current month
        self.budget = self.data[self.current_month]['budget']
        self.total_sum = self.data[self.current_month]['totalSum']
        self.money = self.data[self.current_month]['money']

        # Set up the user interface
        self.setup_ui()
        self.create_return_main_button()

        # Set the background color of the window
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(220, 240, 230))
        self.setPalette(palette)

    def setup_ui(self):
        """
        Set up the user interface with the categories to reduce spending.
        """
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Find categories to reduce spending
        categories_to_reduce = []
        for category, details in self.money.items():
            sum_of_amounts = details['sumOfAmounts']
            if sum_of_amounts > 0 and sum_of_amounts > self.budget:
                categories_to_reduce.append(category)

        # Add a label for the categories to reduce spending
        label = QLabel(
            f'Categories to reduce spending in {self.current_month}:')
        label.setStyleSheet(
            "color: black; font-weight: bold; font-size: 16px;")
        self.layout.addWidget(label)

        # Add labels for each category to reduce spending
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

