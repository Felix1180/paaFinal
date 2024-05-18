import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):  # O(1)
    def __init__(self):  # O(1)
        super().__init__()  # O(1)

        self.setWindowTitle("Merge Sort GUI")  # O(1)

        self.central_widget = QWidget()  # O(1)
        self.setCentralWidget(self.central_widget)  # O(1)

        self.layout = QVBoxLayout()  # O(1)
        self.central_widget.setLayout(self.layout)  # O(1)

        # Combo box for sorting options
        self.sort_combo = QComboBox()  # O(1)
        self.sort_combo.addItems(["NIM", "Nama", "IPK"])  # O(1)
        self.layout.addWidget(self.sort_combo)  # O(1)

        # Combo box for grouping by angkatan
        self.group_combo = QComboBox()  # O(1)
        self.group_combo.addItems(["Semua Angkatan"] + [str(year) for year in range(2016, 2024)])  # O(1)
        self.layout.addWidget(self.group_combo)  # O(1)

        # Button to perform sorting
        self.sort_button = QPushButton("Sort")  # O(1)
        self.sort_button.clicked.connect(self.perform_sort)  # O(1)
        self.layout.addWidget(self.sort_button)  # O(1)

        # Table to display sorted data
        self.table = QTableWidget()  # O(1)
        self.layout.addWidget(self.table)  # O(1)

    def merge_sort(self, arr, key):  # O(1)
        if len(arr) <= 1:  # O(1)
            return arr  # O(1)

        mid = len(arr) // 2  # O(1)
        left_half = arr[:mid]  # O(1)
        right_half = arr[mid:]  # O(1)

        left_half = self.merge_sort(left_half, key)  # T(n/2)
        right_half = self.merge_sort(right_half, key)  # T(n/2)

        return self.merge(left_half, right_half, key)  # O(n)

    def merge(self, left, right, key):  # O(1)
        result = []  # O(1)
        left_index, right_index = 0, 0  # O(1)

        while left_index < len(left) and right_index < len(right):  # O(n)
            if key == "NIM":  # O(1)
                left_val = left[left_index][0]  # O(1)
                right_val = right[right_index][0]  # O(1)
            elif key == "Nama":  # O(1)
                left_val = left[left_index][1]  # O(1)
                right_val = right[right_index][1]  # O(1)
            elif key == "IPK":  # O(1)
                right_val = left[left_index][2]  # O(1)
                left_val = right[right_index][2]  # O(1)

            if left_val < right_val:  # O(1)
                result.append(left[left_index])  # O(1)
                left_index += 1  # O(1)
            else:  # O(1)
                result.append(right[right_index])  # O(1)
                right_index += 1  # O(1)

        while left_index < len(left):  # O(n)
            result.append(left[left_index])  # O(1)
            left_index += 1  # O(1)

        while right_index < len(right):  # O(n)
            result.append(right[right_index])  # O(1)
            right_index += 1  # O(1)

        return result  # O(n)

    def perform_sort(self):  # O(1)
        key = self.sort_combo.currentText()  # O(1)
        group_option = self.group_combo.currentText()  # O(1)

        if group_option == "Semua Angkatan":  # O(1)
            filtered_data = self.load_student_data()  # O(n)
        else:  # O(1)
            angkatan = int(group_option)  # O(1)
            filtered_data = [student for student in self.load_student_data() if int(student[0][2:4]) == angkatan % 2000]  # O(n)

        # Sort data
        sorted_data = self.merge_sort(filtered_data, key)  # O(n log n)

        # Display sorted data in table
        self.display_data(sorted_data)  # O(n)

    def display_data(self, data):  # O(1)
        self.table.setRowCount(len(data))  # O(1)
        self.table.setColumnCount(3)  # O(1)
        self.table.setHorizontalHeaderLabels(["NIM", "Nama", "IPK"])  # O(1)

        for row, (nim, nama, ipk) in enumerate(data):  # O(n)
            nim_item = QTableWidgetItem(str(nim))  # O(1)
            nim_item.setTextAlignment(Qt.AlignCenter)  # O(1)
            self.table.setItem(row, 0, nim_item)  # O(1)
            self.table.setItem(row, 1, QTableWidgetItem(nama))  # O(1)
            ipk_item = QTableWidgetItem(str(ipk))  # O(1)
            ipk_item.setTextAlignment(Qt.AlignCenter)  # O(1)
            self.table.setItem(row, 2, ipk_item)  # O(1)

        # Resize the columns to fit content
        self.table.resizeColumnsToContents()  # O(1)

    def load_student_data(self):  # O(1)
        try:  # O(1)
            with open("student_data.txt", "r") as file:  # O(1)
                lines = file.readlines()  # O(n)
                student_data = [tuple(line.strip().split(",")) for line in lines]  # O(n)
            return student_data  # O(1)
        except FileNotFoundError:  # O(1)
            print("File not found.")  # O(1)
            return []  # O(1)

if __name__ == "__main__":  # O(1)
    app = QApplication(sys.argv)  # O(1)

    window = MainWindow()  # O(1)
    window.setGeometry(100, 100, 600, 400)  # O(1)
    window.show()  # O(1)
    sys.exit(app.exec_())  # O(1)