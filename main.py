#!/usr/bin/env python
"""
Sahibi Budget App - Main Entry Point
A beautiful budget tracking app with category dropdown, custom categories,
salary deduction tracking, and modern Material Design.
"""

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineAvatarIconListItem, TwoLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.chip import MDChip
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Color palette - Modern, professional
PRIMARY_COLOR = "#2C3E50"       # Dark blue-gray
ACCENT_COLOR = "#27AE60"        # Green for income
EXPENSE_COLOR = "#E74C3C"       # Red for expenses
WARNING_COLOR = "#F39C12"       # Orange for warnings
BACKGROUND_COLOR = "#F8F9FA"    # Light gray background
CARD_COLOR = "#FFFFFF"          # White cards
TEXT_PRIMARY = "#2C3E50"
TEXT_SECONDARY = "#7F8C8D"
TEXT_ON_PRIMARY = "#FFFFFF"

# Default categories
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
<CategoryChip@MDChip>
    icon: "checkbox-marked-circle"
    check: False
    on_release: app.select_category(self.text)

<ExpenseItem@TwoLineListItem>
    secondary_text: ""
    _no_ripple_effect: True

<CategoryDialog@MDBoxLayout>
    orientation: "vertical"
    spacing: dp(15)
    adaptive_height: True
    padding: dp(20)

    MDTextField:
        id: category_name
        hint_text: "Category name"
        helper_text: "e.g., Groceries, Electric, Rent"
        helper_text_mode: "on_focus"
        max_text_length: 30

    MDTextField:
        id: category_icon
        hint_text: "Icon name (Material Icons)"
        helper_text: "e.g., cart, flash, home, car"
        helper_text_mode: "on_focus"
        max_text_length: 30
        text: "dots-horizontal"

    MDLabel:
        id: color_label
        text: "Select color:"
        theme_text_color: "Secondary"
        font_size: sp(14)

    MDBoxLayout:
        id: color_container
        orientation: "horizontal"
        spacing: dp(10)
        adaptive_height: True

<SalaryDialog@MDBoxLayout>
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
        max_text_length: 15

    MDTextField:
        id: salary_note
        hint_text: "Note (optional)"
        helper_text: "e.g., January 2024 salary"
        helper_text_mode: "on_focus"
        max_text_length: 50

<ExpenseDialog@MDBoxLayout>
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
        max_text_length: 15

    MDTextField:
        id: expense_note
        hint_text: "Note (optional)"
        helper_text: "What was this for?"
        helper_text_mode: "on_focus"
        max_text_length: 100

<MainScreen>:
    md_bg_color: app.background_color

    MDBoxLayout:
        orientation: "vertical"

        # Top App Bar
        MDTopAppBar:
            id: toolbar
            title: "Sahibi Budget"
            elevation: 4
            md_bg_color: app.primary_color
            right_action_items: [["plus", lambda x: app.show_expense_dialog()], ["cog", lambda x: app.show_settings()]]
            left_action_items: [["menu", lambda x: app.show_drawer()]]

        # Salary Card
        MDCard:
            id: salary_card
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(10)
            size_hint_y: None
            height: dp(140)
            elevation: 3
            radius: [dp(20), dp(20), dp(20), dp(20)]
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

                MDRaisedButton:
                    text: "Add Salary"
                    md_bg_color: app.accent_color
                    text_color: app.text_on_primary
                    on_release: app.show_salary_dialog()
                    size_hint_x: 0.5

                MDRaisedButton:
                    text: "Reset Month"
                    md_bg_color: app.warning_color
                    text_color: app.text_on_primary
                    on_release: app.reset_month()
                    size_hint_x: 0.5

        # Category Filter Chips
        MDCard:
            id: filter_card
            orientation: "vertical"
            padding: dp(15)
            spacing: dp(10)
            size_hint_y: None
            height: dp(100)
            elevation: 1
            radius: [dp(15), dp(15), dp(15), dp(15)]
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

        # Expenses List
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

        # Empty State
        MDBoxLayout:
            id: empty_state
            orientation: "vertical"
            spacing: dp(15)
            padding: dp(40)
            opacity: 0
            visible: False
            size_hint_y: None
            height: dp(200)

            MDIconButton:
                icon: "clipboard-outline"
                icon_size: dp(64)
                theme_text_color: "Hint"
                pos_hint: {"center_x": 0.5}

            MDLabel:
                text: "No expenses yet"
                theme_text_color: "Secondary"
                font_size: sp(18)
                halign: "center"
                bold: True

            MDLabel:
                text: "Tap + to add your first expense"
                theme_text_color: "Hint"
                font_size: sp(14)
                halign: "center"

<NavigationDrawer@MDNavigationDrawer>:
    id: nav_drawer

    MDNavigationDrawerMenu:
        MDNavigationDrawerHeader:
            title: "Sahibi Budget"
            text: "Track your finances"
            spacing: dp(4)
            padding: dp(16)
            md_bg_color: app.primary_color

        MDNavigationDrawerItem:
            icon: "home"
            text: "Dashboard"
            on_release: app.close_drawer()

        MDNavigationDrawerItem:
            icon: "category"
            text: "Manage Categories"
            on_release: app.show_categories_manager()

        MDNavigationDrawerItem:
            icon: "history"
            text: "Expense History"
            on_release: app.show_history()

        MDNavigationDrawerItem:
            icon: "chart-pie"
            text: "Statistics"
            on_release: app.show_statistics()

        MDNavigationDrawerDivider:

        MDNavigationDrawerItem:
            icon: "theme-light-dark"
            text: "Toggle Theme"
            on_release: app.toggle_theme()

        MDNavigationDrawerItem:
            icon: "backup-restore"
            text: "Backup Data"
            on_release: app.backup_data()

        MDNavigationDrawerItem:
            icon: "restore"
            text: "Restore Data"
            on_release: app.restore_data()
'''

class CategoryChip(MDChip):
    pass

class ExpenseItem(TwoLineListItem):
    pass

class CategoryDialog(MDBoxLayout):
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

    # Data
    salary = NumericProperty(0.0)
    expenses = ListProperty([])
    categories = ListProperty([])
    custom_categories = ListProperty([])
    selected_category_filter = StringProperty("All")
    theme_mode = StringProperty("Light")

    # Dialogs
    salary_dialog = None
    expense_dialog = None
    category_dialog = None
    categories_dialog = None
    drawer = None

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

    # Data Persistence
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
            except:
                pass
        self.theme_cls.theme_style = self.theme_mode

    def save_data(self):
        path = self.get_data_path()
        data = {
            'salary': self.salary,
            'expenses': self.expenses,
            'custom_categories': self.custom_categories,
            'theme_mode': self.theme_mode,
        }
        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Save error: {e}")

    # UI Updates
    def update_ui(self):
        # Salary card
        self.root.ids.salary_amount_label.text = f"${self.salary:,.2f}"
        remaining = self.get_remaining()
        self.root.ids.remaining_label.text = f"Remaining: ${remaining:,.2f}"
        self.root.ids.remaining_label.theme_text_color = "Custom"
        self.root.ids.remaining_label.text_color = self.accent_color if remaining >= 0 else self.expense_color

        # Expenses list
        self.refresh_expenses_list()

    def get_total_expenses(self, category_filter=None):
        total = 0.0
        for exp in self.expenses:
            if category_filter and category_filter != "All" and exp.get('category') != category_filter:
                continue
            total += exp.get('amount', 0)
        return total

    def get_remaining(self):
        return self.salary - self.get_total_expenses()

    def refresh_expenses_list(self):
        expenses_list = self.root.ids.expenses_list
        empty_state = self.root.ids.empty_state
        expenses_list.clear_widgets()

        filtered_expenses = self.expenses
        if self.selected_category_filter != "All":
            filtered_expenses = [e for e in self.expenses if e.get('category') == self.selected_category_filter]

        if not filtered_expenses:
            expenses_list.opacity = 0
            empty_state.opacity = 1
            empty_state.visible = True
            empty_state.height = dp(200)
            return

        expenses_list.opacity = 1
        empty_state.opacity = 0
        empty_state.visible = False
        empty_state.height = 0

        # Sort by date (newest first)
        sorted_expenses = sorted(filtered_expenses, key=lambda x: x.get('date', ''), reverse=True)

        for exp in sorted_expenses:
            cat_info = self.get_category_info(exp.get('category', 'Other'))
            item = ExpenseItem(
                text=f"${exp['amount']:,.2f}  •  {exp['category']}",
                secondary_text=f"{exp.get('note', 'No note')}  •  {exp.get('date', '')[:10]}",
                on_release=lambda x, e=exp: self.show_edit_expense_dialog(e),
            )
            # Add category color indicator
            item.add_widget(MDIconButton(
                icon=cat_info['icon'],
                theme_text_color="Custom",
                text_color=cat_info['color'],
                pos_hint={"center_y": 0.5},
                on_release=lambda x, e=exp: self.show_edit_expense_dialog(e),
            ))
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
        all_chip = CategoryChip(
            text="All",
            icon="filter",
            color=self.primary_color if self.selected_category_filter == "All" else self.card_color,
            text_color=self.text_on_primary if self.selected_category_filter == "All" else self.text_primary,
            on_release=lambda x: self.set_category_filter("All"),
        )
        container.add_widget(all_chip)

        # Category chips
        for cat in self.categories:
            is_selected = self.selected_category_filter == cat['name']
            chip = CategoryChip(
                text=cat['name'],
                icon=cat['icon'],
                color=cat['color'] if is_selected else self.card_color,
                text_color=self.text_on_primary if is_selected else self.text_primary,
                on_release=lambda x, c=cat['name']: self.set_category_filter(c),
            )
            container.add_widget(chip)

    def set_category_filter(self, category):
        self.selected_category_filter = category
        self.build_category_chips()
        self.refresh_expenses_list()

    # Dialogs
    def show_salary_dialog(self):
        if not self.salary_dialog:
            content = SalaryDialog()
            self.salary_dialog = MDDialog(
                title="Set Monthly Salary",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="Cancel", on_release=lambda x: self.salary_dialog.dismiss()),
                    MDRaisedButton(text="Save", md_bg_color=self.accent_color, on_release=lambda x: self.save_salary(content)),
                ],
            )
        else:
            self.salary_dialog.content_cls.ids.salary_amount.text = str(self.salary)
        self.salary_dialog.open()

    def save_salary(self, content):
        try:
            amount = float(content.ids.salary_amount.text or 0)
            note = content.ids.salary_note.text or ""
            self.salary = amount
            # Add salary as income entry
            self.expenses.append({
                'amount': -amount,  # Negative = income
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
        if not self.expense_dialog:
            content = ExpenseDialog()
            self.expense_dialog = MDDialog(
                title="Add Expense" if not expense else "Edit Expense",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="Cancel", on_release=lambda x: self.expense_dialog.dismiss()),
                    MDRaisedButton(text="Save", md_bg_color=self.expense_color, on_release=lambda x: self.save_expense(content, expense)),
                ],
            )

        # Set category dropdown
        if expense:
            content.ids.expense_amount.text = str(abs(expense['amount']))
            content.ids.expense_note.text = expense.get('note', '')

        self.expense_dialog.open()

    def save_expense(self, content, editing_expense=None):
        try:
            amount = float(content.ids.expense_amount.text or 0)
            note = content.ids.expense_note.text or ""
            category = self.selected_category_filter if self.selected_category_filter != "All" else "Other"

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
        if not self.categories_dialog:
            content = MDBoxLayout(orientation="vertical", spacing=dp(10), padding=dp(10), adaptive_height=True)

            # Add category button
            add_btn = MDRaisedButton(
                text="+ Add New Category",
                md_bg_color=self.accent_color,
                on_release=lambda x: self.show_add_category_dialog(),
            )
            content.add_widget(add_btn)

            # Categories list
            self.categories_list = MDBoxLayout(orientation="vertical", spacing=dp(5), adaptive_height=True)
            content.add_widget(self.categories_list)

            self.refresh_categories_list()

            self.categories_dialog = MDDialog(
                title="Manage Categories",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="Close", on_release=lambda x: self.categories_dialog.dismiss()),
                ],
            )
        else:
            self.refresh_categories_list()
        self.categories_dialog.open()

    def refresh_categories_list(self):
        if hasattr(self, 'categories_list'):
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
        content = CategoryDialog()
        self.category_dialog = MDDialog(
            title="Add Category",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: self.category_dialog.dismiss()),
                MDRaisedButton(text="Add", md_bg_color=self.accent_color, on_release=lambda x: self.add_category(content)),
            ],
        )

        # Add color chips
        color_container = content.ids.color_container
        color_container.clear_widgets()
        colors = [("#E74C3C", "Red"), ("#F39C12", "Orange"), ("#3498DB", "Blue"),
                  ("#9B59B6", "Purple"), ("#E91E63", "Pink"), ("#00BCD4", "Cyan"),
                  ("#FF5722", "Deep Orange"), ("#95A5A6", "Gray")]
        self.selected_cat_color = colors[0][0]
        for color_hex, color_name in colors:
            btn = MDIconButton(
                icon="circle",
                theme_text_color="Custom",
                text_color=color_hex,
                icon_size=dp(24),
                on_release=lambda x, c=color_hex: self.select_cat_color(c, color_container),
            )
            if color_hex == self.selected_cat_color:
                btn.icon = "check-circle"
            color_container.add_widget(btn)

        self.category_dialog.open()

    def select_cat_color(self, color, container):
        self.selected_cat_color = color
        for child in container.children:
            child.icon = "check-circle" if child.text_color == color else "circle"

    def add_category(self, content):
        name = content.ids.category_name.text.strip()
        icon = content.ids.category_icon.text.strip() or "dots-horizontal"
        color = self.selected_cat_color

        if name and name not in [c['name'] for c in self.categories]:
            new_cat = {"name": name, "icon": icon, "color": color}
            self.custom_categories.append(new_cat)
            self.categories.append(new_cat)
            self.save_data()
            self.refresh_categories_list()
            self.build_category_chips()
            self.category_dialog.dismiss()

    def delete_category(self, category):
        if category in self.custom_categories:
            self.custom_categories.remove(category)
            self.categories.remove(category)
            # Move expenses to "Other"
            for exp in self.expenses:
                if exp['category'] == category['name']:
                    exp['category'] = "Other"
            self.save_data()
            self.refresh_categories_list()
            self.build_category_chips()
            self.refresh_expenses_list()

    def reset_month(self):
        from kivymd.uix.dialog import MDDialog
        dialog = MDDialog(
            title="Reset Month?",
            text="This will clear all expenses and salary for a fresh start.",
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text="Reset", md_bg_color=self.expense_color, on_release=lambda x: self.confirm_reset(dialog)),
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
        # Quick settings dialog
        pass

    def show_history(self):
        # Navigate to history screen
        pass

    def show_statistics(self):
        # Show stats dialog
        pass

    def toggle_theme(self):
        self.theme_mode = "Dark" if self.theme_mode == "Light" else "Light"
        self.theme_cls.theme_style = self.theme_mode
        self.save_data()

    def backup_data(self):
        # Export to file
        pass

    def restore_data(self):
        # Import from file
        pass


if __name__ == '__main__':
    SahibiBudgetApp().run()