# -*- coding: utf8 -*-
# pylint: disable=protected-access
# pylint: disable=too-many-instance-attributes
"""
Главный файл, отвечающий за внешний вид
"""
from typing import Any

from PySide6.QtWidgets import (  # type: ignore
    QVBoxLayout,
    QLabel,
    QWidget,
    QGridLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
    QMainWindow
)
from PySide6 import QtCore, QtWidgets  # type: ignore
from bookkeeper.repository.abstract_repository import T
from bookkeeper.view.redactor_view import RedactorWindow


class TableModel(QtCore.QAbstractTableModel):  # type: ignore
    """
    class that making tables to view
    data
    rowCount
    columnCount
    headerData
    """
    def __init__(self, data: list[Any], columns: list[str]):
        super().__init__()
        self._data = data
        self.columns = columns

    def data(self, index: Any, role: Any) -> Any | None:
        """
        See below for the nested-list data structure.
        .row() indexes into the outer list,
        .column() indexes into the sub-list
        """
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def rowCount(self, index: Any) -> Any:
        """The length of the outer list."""
        return len(self._data)

    def columnCount(self, index: Any) -> Any:
        """
        The following takes the first sub-list, and returns
        the length (only works if all rows are an equal length)
        """
        return len(self._data[0])

    def headerData(self, section: Any, orientation: Any, role: Any) -> str | None:
        """section is the index of the column/row."""
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.columns[section])
        return None


class MainWindow(QMainWindow):  # type: ignore
    """
    MainWindow class of editing Main Window
    Methods:
        set_expense_table
        set_budget_tabel
        set_category_dropdown
        on_expense_add_button_clicked
        get_amount
        get_selected_cat
        get_comment
        get_am_cat_com
    """
    def __init__(self) -> None:
        super().__init__()

        self.item_model = None

        self.redactor_w = RedactorWindow()

        self.setWindowTitle("Программа для ведения бюджета")
        self.setFixedSize(500, 700)

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('Последние расходы'))

        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        self.layout.addWidget(QLabel('Бюджет'))
        self.budget_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.budget_grid)

        self.bottom_controls = QGridLayout()
        self.bottom_controls.addWidget(QLabel('Сумма'), 0, 0)

        self.amount_line_edit = QLineEdit()

        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)
        self.bottom_controls.addWidget(QLabel('Категория'), 1, 0)

        self.category_dropdown = QComboBox()

        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.edit_button = QPushButton('Редактировать')
        self.bottom_controls.addWidget(self.edit_button, 1, 2)

        self.bottom_controls.addWidget(QLabel('Комментарий'), 2, 0)

        self.commentary_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.commentary_line_edit, 2, 1)

        self.expense_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 3, 1)

        self.expense_update_button = QPushButton('Обновить')
        self.bottom_controls.addWidget(self.expense_update_button, 3, 0)

        self.expense_delete_button = QPushButton('Удалить')
        self.bottom_controls.addWidget(self.expense_delete_button, 3, 2)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_expense_table(self, data: list[T]) -> None:
        """making expense table on main window"""
        expense_header = ['Дата', 'Сумма', 'Категория', 'Комментарий']
        self.item_model = TableModel(data[::-1], expense_header)  # type: ignore
        self.expenses_grid.setModel(self.item_model)
        header = self.expenses_grid.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.expenses_grid.horizontalHeader().setStretchLastSection(True)

    def set_budget_table(self, data: list[T]) -> None:
        """making budget table on main window"""
        bud_data = TableModel(data, ['', 'Бюджет', 'Потрачено'])
        self.budget_grid.setModel(bud_data)
        header = self.budget_grid.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        v_header = self.budget_grid.verticalHeader()
        v_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        v_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        v_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        # self.budget_grid.horizontalHeader().setStretchLastSection(True)
        # self.budget_grid.verticalHeader().setStretchLastSection(True)

    def set_category_dropdown(self, data: list[str]) -> None:
        """make dropdown of categories on main window"""
        self.category_dropdown.clear()
        self.category_dropdown.addItems([tup[0] for tup in data])

    def on_expense_add_button_clicked(self, slot: Any) -> None:
        """connect to funtion slot after clicking button"""
        self.expense_add_button.clicked.connect(slot)

    def on_expense_update_button_clicked(self, slot: Any) -> None:
        """connect to funtion slot after clicking button"""
        self.expense_update_button.clicked.connect(slot)

    def on_expense_delete_button_clicked(self, slot: Any) -> None:
        """delete Expense when button delete clicked"""
        self.expense_delete_button.clicked.connect(slot)

    def on_redactor_add_button_clicked(self, slot: Any) -> None:
        """open new window of redaction"""
        self.edit_button.clicked.connect(slot)

    def get_redactor(self) -> Any:
        """return RedactorWindow of Main window"""
        return self.redactor_w

    def get_amount(self) -> float:
        """return amount"""
        return float(self.amount_line_edit.text())

    def get_selected_cat(self) -> Any:
        """return category"""
        return self.category_dropdown.currentText()

    def get_comment(self) -> Any:
        """return comment"""
        return self.commentary_line_edit.text()

    def get_am_cat_com(self) -> list[Any]:
        """return list[amount, category, comment]"""
        return [self.get_amount(), self.get_selected_cat(), self.get_comment()]

    def __get_selected_row_indices(self) -> list[int]:
        """retrun list of ids of selected rows"""
        indexes = self.expenses_grid.selectionModel().selection().indexes()
        return [qmi.row() for qmi in set(indexes)]

    def get_selected_expenses(self) -> list[str] | None:
        """return list of expenses that selected"""
        idx = self.__get_selected_row_indices()
        if not idx:
            return None
        if self.item_model is None:
            return None
        return [" ".join(x for x in self.item_model._data[i]) for i in idx]

    def get_selected_date(self) -> list[str] | None:
        """return date in selected row"""
        idx = self.__get_selected_row_indices()
        if not idx:
            return None
        if self.item_model is None:
            return None
        return [self.item_model._data[i][0] for i in idx]
