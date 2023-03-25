# -*- coding: utf8 -*-
"""
module of redactor window
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
)


class RedactorWindow(QWidget):  # type: ignore
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Окно редактирования')
        layout = QVBoxLayout()

        bottom_controls = QGridLayout()

        bottom_controls.addWidget(QLabel("Добавить категорию"), 0, 0)
        self.category_line = QLineEdit()
        bottom_controls.addWidget(self.category_line, 0, 1)

        self.save_button = QPushButton('Добавить')
        # edit_button.clicked.connect(self.show_redactor())
        bottom_controls.addWidget(self.save_button, 0, 2)

        bottom_controls.addWidget(QLabel("Удалить категорию"), 1, 0)
        self.category_delete = QLineEdit()
        bottom_controls.addWidget(self.category_delete, 1, 1)

        self.delete_button = QPushButton('Удалить')
        # edit_button.clicked.connect(self.show_redactor())
        bottom_controls.addWidget(self.delete_button, 1, 2)

        bottom_controls.addWidget(QLabel("Поменять бюджет"), 2, 0)

        self.budget_dropdown = QComboBox()
        self.budget_dropdown.addItems(['День', 'Неделя', 'Месяц'])
        bottom_controls.addWidget(self.budget_dropdown, 3, 1)
        self.set_budget_line = QLineEdit()
        bottom_controls.addWidget(self.set_budget_line, 2, 1)

        self.set_budget_button = QPushButton('Принять')
        bottom_controls.addWidget(self.set_budget_button, 2, 2)

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_controls)

        layout.addWidget(bottom_widget)

        # self.widget = QWidget()
        self.setLayout(layout)

    def on_add_category_clicked(self, slot: Any) -> None:
        """make connection to add new category by clicking button"""
        self.save_button.clicked.connect(slot)

    def on_delete_category_clicked(self, slot: Any) -> None:
        """make connection to delete category by clicking button"""
        self.delete_button.clicked.connect(slot)

    def on_add_budget_clicked(self, slot: Any) -> None:
        """make connection to set new budget on day/week/month by clicking button"""
        self.set_budget_button.clicked.connect(slot)

    def get_add_category(self) -> Any:
        """return amount"""
        return self.category_line.text()

    def get_delete_category(self) -> Any:
        """delete budget"""
        return self.category_delete.text()

    def get_add_budget(self) -> Any:
        """return budget"""
        return self.set_budget_line.text()

    def get_selected_bud(self) -> Any:
        """return current budget in dropdown"""
        return self.budget_dropdown.currentText()
