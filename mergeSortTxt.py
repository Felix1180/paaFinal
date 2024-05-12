import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Merge Sort GUI")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Combo box for sorting options
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["NIM", "Nama", "IPK"])
        self.layout.addWidget(self.sort_combo)

        # Combo box for grouping by angkatan
        self.group_combo = QComboBox()
        self.group_combo.addItems(["Semua Angkatan"] + [str(year) for year in range(2016, 2024)])
        self.layout.addWidget(self.group_combo)

        # Button to perform sorting
        self.sort_button = QPushButton("Sort")
        self.sort_button.clicked.connect(self.perform_sort)
        self.layout.addWidget(self.sort_button)

        # Table to display sorted data
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    def merge_sort(self, arr, key):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        left_half = self.merge_sort(left_half, key)
        right_half = self.merge_sort(right_half, key)

        return self.merge(left_half, right_half, key)

    def merge(self, left, right, key):
        result = []
        left_index, right_index = 0, 0

        while left_index < len(left) and right_index < len(right):
            if key == "NIM":
                left_val = left[left_index][0]
                right_val = right[right_index][0]
            elif key == "Nama":
                left_val = left[left_index][1]
                right_val = right[right_index][1]
            elif key == "IPK":
                right_val = left[left_index][2]  # ini kutukar left sama rightnya biar IPK nya sortnya dari atas ke bawah
                left_val = right[right_index][2]

            if left_val < right_val:
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1

        while left_index < len(left):
            result.append(left[left_index])
            left_index += 1

        while right_index < len(right):
            result.append(right[right_index])
            right_index += 1

        return result

    def perform_sort(self):
        key = self.sort_combo.currentText()
        group_option = self.group_combo.currentText()

        if group_option == "Semua Angkatan":
            filtered_data = self.load_student_data()
        else:
            angkatan = int(group_option)
            filtered_data = [student for student in self.load_student_data() if int(student[0][2:4]) == angkatan % 2000]

        # Sort data
        sorted_data = self.merge_sort(filtered_data, key)

        # Display sorted data in table
        self.display_data(sorted_data)

    def display_data(self, data):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["NIM", "Nama", "IPK"])

        for row, (nim, nama, ipk) in enumerate(data):
            nim_item = QTableWidgetItem(str(nim))
            nim_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, nim_item)
            self.table.setItem(row, 1, QTableWidgetItem(nama))
            ipk_item = QTableWidgetItem(str(ipk))
            ipk_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, ipk_item)

    def load_student_data(self):
        try:
            with open("student_data.txt", "r") as file:
                lines = file.readlines()
                student_data = [tuple(line.strip().split(",")) for line in lines]
            return student_data
        except FileNotFoundError:
            print("File not found.")
            return []

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setGeometry(100, 100, 600, 400)
    window.show()
    sys.exit(app.exec_())
