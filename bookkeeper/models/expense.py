"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: float
    category: int
    expense_date: datetime = field(default_factory=datetime.now)
    added_date: str = f'{datetime.now():%d-%m-%Y %H:%M}'
    # expense_date: str = f'{datetime.now():%d-%m-%Y %H:%M}'
    # fixed by: str = f'{nek_i_4_ar}'
    # added_date: str = f'{datetime.now():%d-%m-%Y %H:%M}'
    comment: str = ''
    pk: int = 0
