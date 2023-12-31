import os
import json
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtChart import QChartView, QChart, QPieSeries
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMainWindow, QComboBox


class MainPage(QWidget):
    """
    Represents the main page of the financial overview.

    This page displays a pie chart representing the distribution of expenses
    across different categories, along with a label showing the total sum of
    expenses. It also provides a button to switch to the editor page.
    """

    def __init__(self):
        """
        Initializes the MainPage class.

        Sets up the layout, loads data, creates the pie chart, total sum label,
        and edit button.
        """
        super().__init__()
        self.setWindowTitle("Financial Overview")
        self.resize(800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.chart = None
        self.editor_window = None

        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(220, 240, 230))
        self.setPalette(palette)

        self.month_combobox = None
        self.current_month = datetime.now().strftime("%B")

        self.load_data()
        self.create_month_combobox()
        self.create_pie_chart()
        self.update_total_sum_label()
        # self.create_total_sum_label()
        self.create_budget_label()
        self.create_edit_button()
        self.create_helper_button()

    def load_data(self):
        """
        Loads data from a JSON file.

        The JSON file is expected to be named 'expenses.json' and located in
        the same directory as the script file. The loaded data is stored in the
        instance variable 'data'.
        """
        file_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'expenses.json')
        with open(file_path) as file:
            self.data = json.load(file)

    def create_month_combobox(self):
        """
        Creates and displays a combobox for selecting the month.
        """
        self.month_combobox = QComboBox()
        self.month_combobox.addItems(self.data.keys())
        self.month_combobox.setCurrentText(self.current_month)
        self.month_combobox.currentTextChanged.connect(
            self.handle_month_combobox)
        self.layout.addWidget(self.month_combobox)

    def handle_month_combobox(self, month):
        """
        Handles the selection of a month in the combobox.
        """
        self.current_month = month
        self.update_pie_chart()
        self.update_total_sum_label()

    def create_pie_chart(self):
        """
        Creates and displays the pie chart.

        The chart represents the distribution of expenses across different
        categories. Each category is represented by a slice in the pie chart.
        """
        if self.chart:
            self.layout.removeWidget(self.chart)
        self.chart = QChart()
        series = QPieSeries()

        categories = list(self.data[self.current_month]["money"].keys())
        amounts = [self.data[self.current_month]["money"][category]["sumOfAmounts"]
                   for category in categories]

        total_amount = sum(amounts)
        colors = [QColor("#FF6F61"), QColor("#6B5B95"), QColor("#88B04B"),
                  QColor("#616664"), QColor("#92A8D1"), QColor("#955251"),
                  QColor("#9F35A3"), QColor('#0A443D'), QColor('#010005'),
                  QColor('#1B09A3'), QColor('#ED891E')]

        for i in range(len(categories)):
            category = categories[i]
            amount = amounts[i]
            slice_label = f"{category} ({amount:.2f})"
            if (total_amount == 0):
                slice_percentage = 0
            else:
                slice_percentage = amount / total_amount * 100
            slice = series.append(slice_label, slice_percentage)
            slice.setBrush(colors[i % len(colors)].lighter(120))

        self.chart.addSeries(series)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignRight)

        chart_view = QChartView(self.chart)
        self.layout.addWidget(chart_view)

    def create_budget_label(self):
        """
        Creates and displays the label showing the budget.
        """
        budget_label = None
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item.widget() and isinstance(item.widget(), QLabel) and item.widget().objectName() == "budget_label":
                budget_label = item.widget()
                break

        if self.data[self.current_month]['budget'] == 0.0:
            window = QMainWindow(self)
            window.setWindowTitle("Enter Budget")

            input_label = QLabel("Enter budget:")
            input_field = QLineEdit()

            confirm_button = QPushButton("Confirm")

            layout = QVBoxLayout()
            layout.addWidget(input_label)
            layout.addWidget(input_field)
            layout.addWidget(confirm_button)

            central_widget = QWidget()
            central_widget.setLayout(layout)

            window.setCentralWidget(central_widget)

            window.show()

            confirm_button.clicked.connect(
                lambda: self.handle_budget_confirmation(input_field, window))

        if budget_label is None:
            budget_label = QLabel(
                f"Budget: {self.data[self.current_month]['budget']}")
            budget_label.setObjectName("budget_label")
            budget_label.setStyleSheet(
                "color: #20553F; font-weight: bold; font-size: 16px;")
            self.layout.addWidget(budget_label)
        else:
            budget_label.setText(
                f"Budget: {self.data[self.current_month]['budget']}")

    def handle_budget_confirmation(self, input_field, window):
        """
        Handles the confirmation of the budget input.
        """
        self.data[self.current_month]['budget'] = float(input_field.text())
        self.update_data(self.data)
        self.save_expenses_to_json()
        window.close()
        self.create_budget_label()

    def create_edit_button(self):
        """
        Creates and displays the button to switch to the editor page.
        """
        self.editor_button = QPushButton("Edit Expenses")
        self.editor_button.setStyleSheet(
            "background-color: #5DA56C; color: white; font-weight: bold; font-size: 14px;")
        self.layout.addWidget(self.editor_button)

    def create_helper_button(self):
        """
        Creates and displays the button to switch to the helper page.
        """
        self.helper_button = QPushButton("Help me with Budget!")
        self.helper_button.setStyleSheet(
            "background-color: #5DA56C; color: white; font-weight: bold; font-size: 14px;")
        self.layout.addWidget(self.helper_button)

    def update_data(self, data):
        """
        Updates the data and refreshes the page.

        Args:
            data: Updated data to be displayed on the page.
        """
        self.data = data
        self.update_pie_chart()
        self.update_total_sum_label()

    def update_pie_chart(self):
        """
        Updates the pie chart with the updated data.
        """
        if self.chart:
            self.chart.removeAllSeries()

        series = QPieSeries()

        categories = list(self.data[self.current_month]["money"].keys())
        amounts = [self.data[self.current_month]["money"][category]["sumOfAmounts"]
                   for category in categories]

        total_amount = sum(amounts)
        colors = [QColor("#FF6F61"), QColor("#6B5B95"), QColor("#88B04B"),
                  QColor("#616664"), QColor("#92A8D1"), QColor("#955251"),
                  QColor("#9F35A3"), QColor('#0A443D'), QColor('#010005'),
                  QColor('#1B09A3'), QColor('#ED891E')]

        for i in range(len(categories)):
            category = categories[i]
            amount = amounts[i]
            slice_label = f"{category} ({amount:.2f})"
            if (total_amount == 0):
                slice_percentage = 0
            else:
                slice_percentage = amount / total_amount * 100
            slice = series.append(slice_label, slice_percentage)
            slice.setBrush(colors[i % len(colors)].lighter(120))

        self.chart.addSeries(series)

    def update_total_sum_label(self):
        """
        Updates the total sum label with the updated total sum value.
        """
        total_sum_label = None
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item.widget() and isinstance(item.widget(), QLabel) and item.widget().objectName() == "total_sum_label":
                total_sum_label = item.widget()
                break

        if total_sum_label is None:
            total_sum_label = QLabel(
                f"Total Sum: {self.data[self.current_month]['totalSum']}")
            total_sum_label.setObjectName("total_sum_label")
            total_sum_label.setStyleSheet(
                "color: #20553F; font-weight: bold; font-size: 16px;")
            self.layout.addWidget(total_sum_label)
        else:
            total_sum_label.setText(
                f"Total Sum: {self.data[self.current_month]['totalSum']}")

    def save_expenses_to_json(self):
        """Saves expenses to a JSON file

        Args:
            filename (str): The name of the JSON file
        """
        json_data = self.data
        file_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'expenses.json')
        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=4)
