# -*- coding: utf8 -*-
"""
Демонстрация TableView
на основе https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/
"""
import sys

from PySide6.QtWidgets import QApplication  # type: ignore
from bookkeeper.view.expense_view import MainWindow
from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQliteRepository


DB_NAME = 'test.db'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    VIEW = MainWindow()
    MODEL = None
    cat_repo = SQliteRepository[Category](DB_NAME, Category)
    exp_repo = SQliteRepository[Expense](DB_NAME, Expense)
    bud_repo = SQliteRepository[Budget](DB_NAME, Budget)
    bud_repo.add(Budget(limit_on=1000, spent=0))
    bud_repo.add(Budget(limit_on=7000, spent=0))
    bud_repo.add(Budget(limit_on=30000, spent=0))

    window = ExpensePresenter(MODEL, VIEW, [cat_repo, exp_repo, bud_repo])
    window.show()
    app.exec()
