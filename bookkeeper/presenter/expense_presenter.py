# -*- coding: utf8 -*-
"""
module that connetn view and repository
"""
import datetime
from typing import Any

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget

BUDGET_LIST = {"День": 1, "Неделя": 2, "Месяц": 3}


class ExpensePresenter:
    """
    class that present and update expenses and budget

    Methods:
        update_expense_data - method that update expense in table
        update_budget_data - method that update budget in table
        show - start point of main window
        handle_expense_add_button_clicked - add expense when button clicked
    """

    def __init__(self, model: Any, view: Any, repo: list[Any]):
        self.model = model
        self.view = view   # [mainWindow, RedactorWindow]
        self.repos = repo  # [0: Category_repo, 1: Expense_repo, 2: Budget_repo]
        # self.bud_data = [[bud.limit_on, bud.spent] for bud in self.repos[2].get_all()]
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.view.on_expense_update_button_clicked(
            self.handle_expense_update_button_clicked)
        self.view.on_expense_delete_button_clicked(
            self.handle_expense_delete_button_clicked)
        self.view.on_redactor_add_button_clicked(self.show_redactor_clicked)

        red_w = self.view.get_redactor()
        red_w.on_add_category_clicked(self.add_category_button_clicked)
        red_w.on_delete_category_clicked(self.delete_category_button_clicked)
        red_w.on_add_budget_clicked(self.add_budget_button_clicked)

    def show(self) -> None:
        """showing all on main view"""
        self.view.show()
        self.update_expense_data()
        self.update_budget_data()
        # cat_data = self.update_category_data()
        cat_data = [[cat.name, cat.parent, cat.pk] for cat in self.repos[0].get_all()]
        self.view.set_category_dropdown(cat_data)

    def update_expense_data(self) -> None:
        """update information of expenses"""
        exp_data = [[tup.added_date,
                     tup.amount,
                     tup.category,
                     tup.comment]
                    for tup in self.repos[1].get_all()]
        # d_m_y = int(str(self.exp_data[-1][0])[:10])
        # for date, amount, cat, com in self.exp_data:
        #     day_sum = day_sum + (amount if d_m_y == int(str(date)[:10]) else 0)
        #     made = by_neki4ar
        #     week_sum =
        self.update_budget_data()
        if not exp_data:
            solo_exp = [[0, 0, '', 'Пока что нет расходов']]
            self.view.set_expense_table(solo_exp)
        else:
            self.view.set_expense_table(exp_data)

    def update_category_data(self) -> None:
        """update categories menu"""
        cat_data = [[cat.name, cat.parent, cat.pk] for cat in self.repos[0].get_all()]
        # return cat_data
        self.view.set_category_dropdown(cat_data)

    def update_budget_data(self) -> None:
        """updates budget"""
        bud_data = [[bud.limit_on, bud.spent] for bud in self.repos[2].get_all()]
        today = f"{datetime.datetime.utcnow():%d-%m-%Y %H:%M}"
        week_day = datetime.datetime.utcnow().weekday()+1

        week_dates = [f"{datetime.datetime.utcnow()-datetime.timedelta(i):%d-%m-%Y %H:%M}"
                      for i in range(week_day)]
        week_data: list[Any] = []
        for date in week_dates:
            week_data = week_data+self.repos[1].get_like({"added_date": f"{date[:10]}%"})

        today_data = [float(day.amount)
                      for day in self.repos[1].get_like({"added_date": f"{today[:10]}%"})]
        week_data = [float(day.amount) for day in week_data]
        month_data = [float(m.amount)
                      for m in self.repos[1].get_like({"added_date": f"%{today[2:10]}%"})]

        data = [
            ['День',   f'{bud_data[0][0]}', sum(today_data)],
            ['Неделя', f'{bud_data[1][0]}', sum(week_data)],
            ['Месяц',  f'{bud_data[2][0]}', sum(month_data)],
        ]
        self.view.set_budget_table(data)

    def handle_expense_add_button_clicked(self) -> None:
        """add expense and update expense on expense_table"""
        amount, category, comment = self.view.get_am_cat_com()
        exp = Expense(amount=float(amount), category=category, comment=comment)
        self.repos[1].add(exp)
        self.update_expense_data()

    def handle_expense_update_button_clicked(self) -> None:
        """updating choosed expense"""
        selected = self.view.get_selected_expenses()
        expense_pk_dict = self.pk_get_all_expense()
        amount, category, comment = self.view.get_am_cat_com()
        ad_date = self.view.get_selected_date()
        # print(date)
        if len(selected) == 1:
            exp = Expense(amount=amount,
                          added_date=ad_date[0],
                          category=category,
                          comment=comment,
                          pk=expense_pk_dict[selected[0]])
            self.repos[1].update(exp)
        else:
            raise AttributeError("can not update more than 1 object at one moment")
        self.update_expense_data()

    def handle_expense_delete_button_clicked(self) -> None:
        """deleting choosed expenses"""
        selected = self.view.get_selected_expenses()
        for exp in selected:
            expense_pk_dict = self.pk_get_all_expense()
            self.repos[1].delete(expense_pk_dict[exp])
        self.update_expense_data()

    def pk_get_all_expense(self) -> dict[str, int]:
        """returning pk of choosed expenses"""
        result = {f"{c.added_date} "
                  f"{c.amount} "
                  f"{c.category} "
                  f"{c.comment}": c.pk for c in self.repos[1].get_all()}
        return result

    def show_redactor_clicked(self, checked: Any) -> None:
        """show redactor window"""
        red_w = self.view.get_redactor()
        if red_w.isVisible():
            red_w.hide()
        else:
            red_w.show()

    def add_category_button_clicked(self) -> None:
        """add new caregory in category"""
        redactor_view = self.view.get_redactor()
        new_cat = Category(redactor_view.get_add_category())
        self.repos[0].add(new_cat)
        self.update_category_data()

    def delete_category_button_clicked(self) -> None:
        """deleting category in category"""
        redactor_view = self.view.get_redactor()
        cat_list = {cat.name: cat.pk for cat in self.repos[0].get_all()}
        cat_delete = redactor_view.get_delete_category()
        self.repos[0].delete(cat_list[cat_delete])
        self.update_category_data()

    def add_budget_button_clicked(self) -> None:
        """ adding new limit in budget"""
        redactor_view = self.view.get_redactor()
        new_bud = redactor_view.get_selected_bud()
        bud_amount = redactor_view.get_add_budget()
        bud = Budget(limit_on=bud_amount, spent=0, pk=BUDGET_LIST[new_bud])
        self.repos[2].update(bud)
        self.update_budget_data()
