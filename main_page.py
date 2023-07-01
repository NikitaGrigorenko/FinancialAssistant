import os
import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtChart import QChartView, QChart, QPieSeries
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


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
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.chart = None
        self.editor_window = None

        self.load_data()
        self.create_pie_chart()
        self.create_total_sum_label()
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

        categories = list(self.data["money"].keys())
        amounts = [self.data["money"][category]["sumOfAmounts"]
                   for category in categories]

        total_amount = sum(amounts)
        colors = [Qt.cyan, Qt.blue, Qt.green, Qt.yellow, Qt.darkCyan,
                  Qt.gray, Qt.darkYellow]

        for i in range(len(categories)):
            category = categories[i]
            amount = amounts[i]
            slice_label = f"{category} ({amount:.2f})"
            if (total_amount == 0):
                slice_percentage = 0
            else:
                slice_percentage = amount / total_amount * 100
            slice = series.append(slice_label, slice_percentage)
            slice.setBrush(QColor(colors[i % len(colors)]))

        self.chart.addSeries(series)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignRight)

        chart_view = QChartView(self.chart)
        self.layout.addWidget(chart_view)

    def create_total_sum_label(self):
        """
        Creates and displays the label showing the total sum of expenses.
        """
        total_sum_label = QLabel(f"Total Sum: {self.data['totalSum']}")
        self.layout.addWidget(total_sum_label)

    def create_edit_button(self):
        """
        Creates and displays the button to switch to the editor page.
        """
        self.editor_button = QPushButton("Edit Expenses")
        self.layout.addWidget(self.editor_button)

    def create_helper_button(self):
        """
        Creates and displays the button to switch to the helper page.
        """
        self.helper_button = QPushButton("Help me with Budget!")
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

        categories = list(self.data["money"].keys())
        amounts = [self.data["money"][category]["sumOfAmounts"]
                   for category in categories]

        total_amount = sum(amounts)
        colors = [Qt.cyan, Qt.blue, Qt.green, Qt.yellow, Qt.darkCyan,
                  Qt.gray, Qt.darkYellow]

        for i in range(len(categories)):
            category = categories[i]
            amount = amounts[i]
            slice_label = f"{category} ({amount:.2f})"
            if (total_amount == 0):
                slice_percentage = 0
            else:
                slice_percentage = amount / total_amount * 100
            slice = series.append(slice_label, slice_percentage)
            slice.setBrush(QColor(colors[i % len(colors)]))

        self.chart.addSeries(series)

    def update_total_sum_label(self):
        """
        Updates the total sum label with the updated total sum value.
        """
        total_sum_label = self.layout.itemAt(1).widget()
        total_sum_label.setText(f"Total Sum: {self.data['totalSum']}")
