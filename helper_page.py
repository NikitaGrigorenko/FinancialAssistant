import os
import json
import numpy as np
from PyQt5.QtCore import Qt
from sklearn.cluster import KMeans
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton


class HelperPage(QWidget):
    """
    A helper page widget for generating spending reduction recommendations.
    """

    def __init__(self):
        """
        Initialize the HelperPage widget.
        """
        super().__init__()
        self.data = None
        self.categories = None
        self.category_names = None
        self.spendings = None
        self.X = None
        self.labels = None
        self.budget = None
        self.reduction_categories = []
        self.reduction_amounts = []
        self.recommendations = []

        self.layout = QVBoxLayout()
        self.resize(800, 600)
        self.setLayout(self.layout)

        self.read_expenses_data()
        self.create_return_main_button()
        self.prepare_data()
        self.perform_clustering()
        self.identify_reductions()
        self.generate_recommendations()
        self.display_gui()

        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(220, 240, 230))
        self.setPalette(palette)

    def read_expenses_data(self):
        """
        Read the expenses data from a JSON file.
        """
        file_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'expenses.json')
        with open(file_path, 'r') as file:
            self.data = json.load(file)

    def create_return_main_button(self):
        """
        Create a button for returning to the main page.
        """
        self.return_main_button = QPushButton("Back to Main Page")
        self.layout.addWidget(self.return_main_button)
        self.return_main_button.setStyleSheet(
            "background-color: #5DA56C; color: white; font-weight: bold; font-size: 14px;")

    def prepare_data(self):
        """
        Prepare the data for clustering.
        """
        self.categories = self.data['money']
        self.category_names = list(self.categories.keys())
        self.spendings = [self.categories[category]['sumOfAmounts']
                          for category in self.category_names]
        self.X = np.array(self.spendings).reshape(-1, 1)

    def perform_clustering(self, n_clusters=2):
        """Perform clustering on the data using K-means algorithm.

        Args:
            n_clusters (int): Number of clusters for K-means algorithm.

        """
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(self.X)
        self.labels = kmeans.labels_

    def identify_reductions(self):
        """
        Identify categories that require spending reductions based on budget constraints.
        """
        self.budget = self.data['budget']
        for i, category in enumerate(self.category_names):
            items = self.categories[category]['items']
            if len(items) > 0:
                cluster_label = self.labels[i]
                cluster_spending = np.mean(
                    self.X[self.labels == cluster_label])
                average_spending = self.categories[category]['sumOfAmounts'] / len(
                    items)
                if average_spending > self.budget:
                    self.reduction_categories.append(category)
                    reduction_amount = average_spending - self.budget
                    self.reduction_amounts.append(reduction_amount)

    def generate_recommendations(self):
        """
        Generate spending reduction recommendations for identified categories.
        """
        for category, reduction_amount in zip(self.reduction_categories, self.reduction_amounts):
            recommendation = f"Reduce spending in {category} by ${reduction_amount:.2f}"
            self.recommendations.append(recommendation)

    def display_gui(self):
        """
        Display the spending reduction recommendations on the GUI.
        """
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        self.layout.addStretch(1)

        for recommendation in self.recommendations:
            label = QLabel(recommendation)
            label.setStyleSheet(
                "color: #20553F; font-weight: bold; font-size: 20px;")
            label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(label)

        self.layout.addStretch(1)

        self.layout.addWidget(self.return_main_button)
