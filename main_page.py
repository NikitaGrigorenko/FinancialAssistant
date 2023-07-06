import os
import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtChart import QChartView, QChart, QPieSeries
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMainWindow


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

        self.load_data()
        self.create_pie_chart()
        self.create_total_sum_label()
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

    def create_total_sum_label(self):
        """
        Creates and displays the label showing the total sum of expenses.
        """
        total_sum_label = QLabel(f"Total Sum: {self.data['totalSum']}")
        total_sum_label.setStyleSheet(
            "color: #20553F; font-weight: bold; font-size: 16px;")
        self.layout.addWidget(total_sum_label)

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

        if self.data['budget'] == 0.0:
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
            budget_label = QLabel(f"Budget: {self.data['budget']}")
            budget_label.setObjectName("budget_label")
            budget_label.setStyleSheet(
                "color: #20553F; font-weight: bold; font-size: 16px;")
            self.layout.addWidget(budget_label)
        else:
            budget_label.setText(f"Budget: {self.data['budget']}")

    def handle_budget_confirmation(self, input_field, window):
        """
        Handles the confirmation of the budget input.
        """
        self.data['budget'] = float(input_field.text())
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

        categories = list(self.data["money"].keys())
        amounts = [self.data["money"][category]["sumOfAmounts"]
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
        total_sum_label = self.layout.itemAt(1).widget()
        total_sum_label.setText(f"Total Sum: {self.data['totalSum']}")

    def save_expenses_to_json(self):
        """Saves expenses to a JSON file

        Args:
            filename (str): The name of the JSON file
        """
        json_data = {'money': self.data['money'],
                     'totalSum': self.data['totalSum'],
                     'budget': self.data['budget']}
        file_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'expenses.json')
        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=4)
