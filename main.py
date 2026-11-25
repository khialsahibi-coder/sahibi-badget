#!/usr/bin/env python
"""
Sahibi Budget App - Main Entry Point (KivyMD 2.x Compatible)
"""

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.chip import MDChip, MDChipText
from kivymd.uix.navigationdrawer import (
    MDNavigationDrawer,
    MDNavigationDrawerMenu,
    MDNavigationDrawerItem,
    MDNavigationDrawerItemText,
    MDNavigationDrawerItemLeadingIcon,
)
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
import json
import os
from datetime import datetime

# Color palette
PRIMARY_COLOR = "#2C3E50"
ACCENT_COLOR = "#27AE60"
EXPENSE_COLOR = "#E74C3C"
WARNING_COLOR = "#F39C12"
BACKGROUND_COLOR = "#F8F9FA"
CARD_COLOR = "#FFFFFF"
TEXT_PRIMARY = "#2C3E50"
TEXT_SECONDARY = "#7F8C8D"
TEXT_ON_PRIMARY = "#FFFFFF"

DEFAULT_CATEGORIES = [
    {"name": "Groceries", "icon": "cart", "color": "#E74C3C"},
    {"name": "Electric", "icon": "flash", "color": "#F39C12"},
    {"name": "Transport", "icon": "bus", "color": "#3498DB"},
    {"name": "Entertainment", "icon": "movie", "color": "#9B59B6"},
    {"name": "Healthcare", "icon": "medical-bag", "color": "#E91E63"},
    {"name": "Education", "icon": "book-open", "color": "#00BCD4"},
    {"name": "Shopping", "icon": "shopping", "color": "#FF5722"},
    {"name": "Other", "icon": "dots-horizontal", "color": "#95A5A6"},
]

KV = '''
<CategoryChip@MDChip>:
    MDChipText:
        id: chip_text
        text: root.text
    md_bg_color: root.md_bg_color

<ExpenseItem@TwoLineListItem>:
    _no_ripple_effect: True

<SalaryDialog@MDBoxLayout>:
    orientation: "vertical"
    spacing: dp(15)
    adaptive_height: True
    padding: dp(20)

    MDTextField:
        id: salary_amount
        hint_text: "Monthly Salary"
        helper_text: "Enter your monthly income"
        helper_text_mode: "on_focus"
        input_filter: "float"

    MDTextField:
        id: salary_note
        hint_text: "Note (optional)"
        helper_text: "e.g., January 2024 salary"
        helper_text_mode: "on_focus"

<ExpenseDialog@MDBoxLayout>:
    orientation: "vertical"
    spacing: dp(15)
    adaptive_height: True
    padding: dp(20)

    MDTextField:
        id: expense_amount
        hint_text: "Amount"
        helper_text: "Enter expense amount"
        helper_text_mode: "on_focus"
        input_filter: "float"

    MDTextField:
        id: expense_note
        hint_text: "Note (optional)"
        helper_text: "What was this for?"
        helper_text_mode: "on_focus"

    MDTextField:
        id: expense_category
        hint_text: "Category"
        helper_text: "Tap to select category"
        helper_text_mode: "on_focus"
        readonly: True
        on_focus: if self.focus: app.open_category_dropdown(self)

<MainScreen>:
    md_bg_color: app.background_color

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            id: toolbar
            title: "Sahibi Budget"
            elevation: 4
            md_bg_color: app.primary_color
            right_action_items: [["plus", lambda x: app.show_expense_dialog()], ["cog", lambda x: app.show_settings()]]
            left_action_items: [["menu", lambda x: app.show_drawer()]]

        MDCard:
            id: salary_card
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(10)
            size_hint_y: None
            height: dp(160)
            elevation: 3
            radius: [dp(20)]
            md_bg_color: app.primary_color
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.95

            MDBoxLayout:
                orientation: "horizontal"
                spacing: dp(15)

                MDIconButton:
                    icon: "currency-usd"
                    theme_text_color: "Custom"
                    text_color: app.text_on_primary
                    icon_size: dp(32)

                MDBoxLayout:
                    orientation: "vertical"
                    spacing: dp(2)

                    MDLabel:
                        id: salary_label
                        text: "Monthly Salary"
                        theme_text_color: "Custom"
                        text_color: app.text_on_primary
                        font_size: sp(14)
                        opacity: 0.9

                    MDLabel:
                        id: salary_amount_label
                        text: "$0.00"
                        theme_text_color: "Custom"
                        text_color: app.text_on_primary
                        font_size: sp(28)
                        bold: True

                    MDLabel:
                        id: remaining_label
                        text: "Remaining: $0.00"
                        theme_text_color: "Custom"
                        text_color: app.accent_color
                        font_size: sp(14)

            MDBoxLayout:
                orientation: "horizontal"
                spacing: dp(10)
                padding: [dp(0), dp(10), dp(0), dp(0)]

                MDButton:
                    style: "filled"
                    md_bg_color: app.accent_color
                    on_release: app.show_salary_dialog()
                    size_hint_x: 0.5
                    MDButtonText:
                        text: "Add Salary"

                MDButton:
                    style: "filled"
                    md_bg_color: app.warning_color
                    on_release: app.reset_month()
                    size_hint_x: 0.5
                    MDButtonText:
                        text: "Reset Month"

        MDCard:
            id: filter_card
            orientation: "vertical"
            padding: dp(15)
            spacing: dp(10)
            size_hint_y: None
            height: dp(100)
            elevation: 1
            radius: [dp(15)]
            md_bg_color: app.card_color
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.95

            MDLabel:
                text: "Filter by Category"
                theme_text_color: "Primary"
                font_size: sp(14)
                bold: True

            MDScrollView:
                do_scroll_x: True
                do_scroll_y: False

                MDBoxLayout:
                    id: category_chips_container
                    orientation: "horizontal"
                    spacing: dp(8)
                    padding: [dp(5), dp(0), dp(5), dp(0)]
                    size_hint_x: None
                    width: self.minimum_width
                    adaptive_height: True

        MDLabel:
            id: expenses_title
            text: "Expenses"
            theme_text_color: "Primary"
            font_size: sp(18)
            bold: True
            padding: [dp(20), dp(15), dp(20), dp(5)]
            size_hint_y: None
            height: dp(40)

        MDScrollView:
            id: expenses_scroll
            do_scroll_x: False
            do_scroll_y: True

            MDList:
                id: expenses_list
                padding: [dp(15), dp(0), dp(15), dp(20)]
                spacing: dp(10)

<NavigationDrawer@MDNavigationDrawer>:
    id: nav_drawer

    MDNavigationDrawerMenu:
        MDNavigationDrawerItem:
            on_release: app.close_drawer()
            MDNavigationDrawerItemLeadingIcon:
                icon: "home"
            MDNavigationDrawerItemText:
                text: "Dashboard"

        MDNavigationDrawerItem:
            on_release: app.show_categories_manager()
            MDNavigationDrawerItemLeadingIcon:
                icon: "category"
            MDNavigationDrawerItemText:
                text: "Manage Categories"

        MDNavigationDrawerItem:
            on_release: app.show_statistics()
            MDNavigationDrawerItemLeadingIcon:
                icon: "chart-pie"
            MDNavigationDrawerItemText:
                text: "Statistics"

        MDNavigationDrawerItem:
            on_release: app.toggle_theme()
            MDNavigationDrawerItemLeadingIcon:
                icon: "theme-light-dark"
            MDNavigationDrawerItemText:
                text: "Toggle Theme"
'''


class CategoryChip(MDChip):
    pass

class ExpenseItem(TwoLineListItem):
    pass

class SalaryDialog(MDBoxLayout):
    pass

class ExpenseDialog(MDBoxLayout):
    pass

class MainScreen(MDScreen):
    pass

class NavigationDrawer(MDNavigationDrawer):
    pass


class SahibiBudgetApp(MDApp):
    primary_color = PRIMARY_COLOR
    accent_color = ACCENT_COLOR
    expense_color = EXPENSE_COLOR
    warning_color = WARNING_COLOR
    background_color = BACKGROUND_COLOR
    card_color = CARD_COLOR
    text_primary = TEXT_PRIMARY
    text_secondary = TEXT_SECONDARY
    text_on_primary = TEXT_ON_PRIMARY

    salary = NumericProperty(0.0)
    expenses = ListProperty([])
    categories = ListProperty([])
    custom_categories = ListProperty([])
    selected_category_filter = StringProperty("All")
    theme_mode = StringProperty("Light")

    salary_dialog = None
    expense_dialog = None
    categories_dialog = None
    drawer = None
    category_menu = None

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Green"
        self.theme_cls.theme_style = "Light"
        self.load_data()
        self.categories = DEFAULT_CATEGORIES + self.custom_categories
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_once(lambda dt: self.update_ui(), 0.1)
        Clock.schedule_once(lambda dt: self.build_category_chips(), 0.2)

    def get_data_path(self):
        from kivy.utils import platform
        if platform == 'android':
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), 'budget_data.json')
        return os.path.join(self.user_data_dir, 'budget_data.json')

    def load_data(self):
        path = self.get_data_path()
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    self.salary = data.get('salary', 0.0)
                    self.expenses = data.get('expenses', [])
                    self.custom_categories = data.get('custom_categories', [])
                    self.theme_mode = data.get('theme_mode', 'Light')
            except Exception:
                pass
        self.theme_cls.theme_style = self.theme_mode

    def save_data(self):
        data = {
            'salary': self.salary,
            'expenses': self.expenses,
            'custom_categories': self.custom_categories,
            'theme_mode': self.theme_mode,
        }
        try:
            with open(self.get_data_path(), 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Save error: {e}")

    def update_ui(self):
        self.root.ids.salary_amount_label.text = f"${self.salary:,.2f}"
        remaining = self.get_remaining()
        self.root.ids.remaining_label.text = f"Remaining: ${remaining:,.2f}"
        self.root.ids.remaining_label.text_color = (
            self.accent_color if remaining >= 0 else self.expense_color
        )
        self.refresh_expenses_list()

    def get_total_expenses(self, category_filter=None):
        total = 0.0
        for exp in self.expenses:
            if exp.get('type') == 'income':
                continue
            if category_filter and category_filter != "All" and exp.get('category') != category_filter:
                continue
            total += exp.get('amount', 0)
        return total

    def get_remaining(self):
        return self.salary - self.get_total_expenses()

    def refresh_expenses_list(self):
        expenses_list = self.root.ids.expenses_list
        expenses_list.clear_widgets()

        filtered = [e for e in self.expenses if e.get('type') != 'income']
        if self.selected_category_filter != "All":
            filtered = [e for e in filtered if e.get('category') == self.selected_category_filter]

        if not filtered:
            return

        for exp in sorted(filtered, key=lambda x: x.get('date', ''), reverse=True):
            cat_info = self.get_category_info(exp.get('category', 'Other'))
            item = ExpenseItem(
                text=f"${exp['amount']:,.2f}  •  {exp['category']}",
                secondary_text=f"{exp.get('note', 'No note')}  •  {exp.get('date', '')[:10]}",
                on_release=lambda x, e=exp: self.show_edit_expense_dialog(e),
            )
            expenses_list.add_widget(item)

    def get_category_info(self, name):
        for cat in self.categories:
            if cat['name'] == name:
                return cat
        return {"name": name, "icon": "dots-horizontal", "color": TEXT_SECONDARY}

    def build_category_chips(self):
        container = self.root.ids.category_chips_container
        container.clear_widgets()

        # "All" chip
        is_all = self.selected_category_filter == "All"
        all_chip = CategoryChip(
            md_bg_color=self.primary_color if is_all else self.card_color,
        )
        all_chip.ids.chip_text.text = "All"
        all_chip.ids.chip_text.text_color = self.text_on_primary if is_all else self.text_primary
        all_chip.bind(on_release=lambda x: self.set_category_filter("All"))
        container.add_widget(all_chip)

        for cat in self.categories:
            is_selected = self.selected_category_filter == cat['name']
            chip = CategoryChip(
                md_bg_color=cat['color'] if is_selected else self.card_color,
            )
            chip.ids.chip_text.text = cat['name']
            chip.ids.chip_text.text_color = self.text_on_primary if is_selected else self.text_primary
            chip.bind(on_release=lambda x, c=cat['name']: self.set_category_filter(c))
            container.add_widget(chip)

    def set_category_filter(self, category):
        self.selected_category_filter = category
        self.build_category_chips()
        self.refresh_expenses_list()

    def show_salary_dialog(self):
        if not self.salary_dialog:
            content = SalaryDialog()
            self.salary_dialog = MDDialog(
                title="Set Monthly Salary",
                type="custom",
                content_cls=content,
                buttons=[
                    MDButton(
                        MDButtonText(text="Cancel"),
                        style="text",
                        on_release=lambda x: self.salary_dialog.dismiss(),
                    ),
                    MDButton(
                        MDButtonText(text="Save"),
                        style="filled",
                        md_bg_color=self.accent_color,
                        on_release=lambda x: self.save_salary(content),
                    ),
                ],
            )
        self.salary_dialog.content_cls.ids.salary_amount.text = str(self.salary) if self.salary else ""
        self.salary_dialog.open()

    def save_salary(self, content):
        try:
            amount = float(content.ids.salary_amount.text or 0)
            note = content.ids.salary_note.text or ""
            self.salary = amount
            # Remove old income records
            self.expenses = [e for e in self.expenses if e.get('type') != 'income']
            self.expenses.append({
                'amount': -amount,
                'category': 'Salary',
                'note': note or f"Salary - {datetime.now().strftime('%B %Y')}",
                'date': datetime.now().isoformat(),
                'type': 'income',
            })
            self.save_data()
            self.update_ui()
            self.salary_dialog.dismiss()
        except ValueError:
            pass

    def show_expense_dialog(self, expense=None):
        content = ExpenseDialog()
        if expense:
            content.ids.expense_amount.text = str(abs(expense['amount']))
            content.ids.expense_note.text = expense.get('note', '')
            content.ids.expense_category.text = expense.get('category', 'Other')
        else:
            content.ids.expense_category.text = (
                self.selected_category_filter if self.selected_category_filter != "All" else "Other"
            )

        self.expense_dialog = MDDialog(
            title="Add Expense" if not expense else "Edit Expense",
            type="custom",
            content_cls=content,
            buttons=[
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=lambda x: self.expense_dialog.dismiss(),
                ),
                MDButton(
                    MDButtonText(text="Save"),
                    style="filled",
                    md_bg_color=self.expense_color,
                    on_release=lambda x: self.save_expense(content, expense),
                ),
            ],
        )
        self.expense_dialog.open()

    def open_category_dropdown(self, field):
        if self.category_menu:
            self.category_menu.dismiss()
        items = [{"text": cat["name"], "viewclass": "OneLineListItem", "on_release": lambda x=cat["name"]: self.set_expense_category(field, x)} for cat in self.categories]
        from kivymd.uix.menu import MDDropdownMenu
        self.category_menu = MDDropdownMenu(caller=field, items=items, width_mult=4)
        self.category_menu.open()

    def set_expense_category(self, field, category_name):
        field.text = category_name
        field.focus = False
        if self.category_menu:
            self.category_menu.dismiss()

    def save_expense(self, content, editing_expense=None):
        try:
            amount = float(content.ids.expense_amount.text or 0)
            note = content.ids.expense_note.text or ""
            category = content.ids.expense_category.text or "Other"

            if editing_expense:
                editing_expense['amount'] = amount
                editing_expense['note'] = note
                editing_expense['category'] = category
                editing_expense['date'] = datetime.now().isoformat()
            else:
                self.expenses.append({
                    'amount': amount,
                    'category': category,
                    'note': note,
                    'date': datetime.now().isoformat(),
                    'type': 'expense',
                })

            self.save_data()
            self.update_ui()
            self.expense_dialog.dismiss()
        except ValueError:
            pass

    def show_edit_expense_dialog(self, expense):
        self.show_expense_dialog(expense)

    def show_categories_manager(self):
        if self.categories_dialog:
            self.categories_dialog.dismiss()
        content = MDBoxLayout(orientation="vertical", spacing=dp(10), padding=dp(10), adaptive_height=True)
        add_btn = MDButton(
            MDButtonText(text="+ Add New Category"),
            style="filled",
            md_bg_color=self.accent_color,
            on_release=lambda x: self.show_add_category_dialog(),
        )
        content.add_widget(add_btn)

        self.categories_list = MDBoxLayout(orientation="vertical", spacing=dp(5), adaptive_height=True)
        content.add_widget(self.categories_list)
        self.refresh_categories_list()

        self.categories_dialog = MDDialog(
            title="Manage Categories",
            type="custom",
            content_cls=content,
            buttons=[
                MDButton(
                    MDButtonText(text="Close"),
                    style="text",
                    on_release=lambda x: self.categories_dialog.dismiss(),
                ),
            ],
        )
        self.categories_dialog.open()

    def refresh_categories_list(self):
        if not hasattr(self, 'categories_list'):
            return
        self.categories_list.clear_widgets()
        for cat in self.categories:
            is_custom = cat in self.custom_categories
            item = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(50), padding=[dp(10), dp(5)])
            item.add_widget(MDIconButton(
                icon=cat['icon'],
                theme_text_color="Custom",
                text_color=cat['color'],
            ))
            item.add_widget(MDLabel(
                text=cat['name'],
                theme_text_color="Primary",
                bold=True,
            ))
            if is_custom:
                item.add_widget(MDIconButton(
                    icon="delete",
                    theme_text_color="Custom",
                    text_color=self.expense_color,
                    on_release=lambda x, c=cat: self.delete_category(c),
                ))
            self.categories_list.add_widget(item)

    def show_add_category_dialog(self):
        content = MDBoxLayout(orientation="vertical", spacing=dp(15), padding=dp(20), adaptive_height=True)
        name_field = MDTextField(hint_text="Category name", helper_text="e.g., Rent", helper_text_mode="on_focus")
        icon_field = MDTextField(hint_text="Icon name", helper_text="e.g., cart, flash, home", helper_text_mode="on_focus", text="dots-horizontal")
        content.add_widget(name_field)
        content.add_widget(icon_field)

        dialog = MDDialog(
            title="Add Category",
            type="custom",
            content_cls=content,
            buttons=[
                MDButton(MDButtonText(text="Cancel"), style="text", on_release=lambda x: dialog.dismiss()),
                MDButton(
                    MDButtonText(text="Add"),
                    style="filled",
                    md_bg_color=self.accent_color,
                    on_release=lambda x: self.add_category(name_field.text, icon_field.text, dialog),
                ),
            ],
        )
        dialog.open()

    def add_category(self, name, icon, dialog):
        name = name.strip()
        icon = icon.strip() or "dots-horizontal"
        if name and name not in [c['name'] for c in self.categories]:
            new_cat = {"name": name, "icon": icon, "color": "#3498DB"}
            self.custom_categories.append(new_cat)
            self.categories.append(new_cat)
            self.save_data()
            self.refresh_categories_list()
            self.build_category_chips()
            dialog.dismiss()

    def delete_category(self, category):
        if category in self.custom_categories:
            self.custom_categories.remove(category)
            self.categories.remove(category)
            for exp in self.expenses:
                if exp.get('category') == category['name']:
                    exp['category'] = "Other"
            self.save_data()
            self.refresh_categories_list()
            self.build_category_chips()
            self.refresh_expenses_list()

    def reset_month(self):
        dialog = MDDialog(
            title="Reset Month?",
            text="This will clear all expenses and salary for a fresh start.",
            buttons=[
                MDButton(MDButtonText(text="Cancel"), style="text", on_release=lambda x: dialog.dismiss()),
                MDButton(
                    MDButtonText(text="Reset"),
                    style="filled",
                    md_bg_color=self.expense_color,
                    on_release=lambda x: self.confirm_reset(dialog),
                ),
            ],
        )
        dialog.open()

    def confirm_reset(self, dialog):
        self.salary = 0.0
        self.expenses = []
        self.save_data()
        self.update_ui()
        dialog.dismiss()

    def show_drawer(self):
        if not self.drawer:
            self.drawer = NavigationDrawer()
        self.drawer.set_state("open")

    def close_drawer(self):
        if self.drawer:
            self.drawer.set_state("close")

    def show_settings(self):
        pass

    def show_statistics(self):
        pass

    def toggle_theme(self):
        self.theme_mode = "Dark" if self.theme_mode == "Light" else "Light"
        self.theme_cls.theme_style = self.theme_mode
        self.save_data()


if __name__ == '__main__':
    SahibiBudgetApp().run()
