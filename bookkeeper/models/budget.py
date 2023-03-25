# -*- coding: utf8 -*-
"""
Описан класс, представляющий бюджет на день/неделю/месяц
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Budget:
    """
    Бюджет
    limit - limit on period
    spent - how much money have been spent in period
    pk - primary key
    """
    limit_on: float
    spent: float
    pk: int = 0
    #
    # def __init__(self, limit, spent, pk):
    #     self.limit = limit
    #     self.spent = spent
    #     self.pk = pk
    #
    # def set_limit_bud(self, limit: float) -> None:
    #     self.limit_on = limit
