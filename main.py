"""
Sahibi Budget App
A modern budget tracker with category dropdown, custom categories and salary tracking.
"""

import json
import os
from datetime import datetime

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.utils import get_color_from_hex

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar

PRIMARY = "#1E3A5F"
ACCENT = "#2ECC71"
DANGER = "#E74C3C"
WARN = "#F39C12"
BG = "#F4F6F8"
CARD = "#FFFFFF"

DEFAULT_CATEGORIES = [
    {"name": "Groceries", "icon": "cart", "color": "#E74C3C"},
    {"name": "Electric", "icon": "flash", "color": "#F39C12"},
    {"name": "Water", "icon": "water", "color": "#3498DB"},
    {"name": "Transport", "icon": "bus", "color": "#2980B9"},
    {"name": "Fuel", "icon": "gas-station", "color": "#D35400"},
    {"name": "Rent", "icon": "home", "color": "#8E44AD"},
    {"name": "Internet", "icon": "wifi", "color": "#16A085"},
    {"name": "Phone", "icon": "cellphone", "color": "#2C3E50"},
    {"name": "Healthcare", "icon": "medical-bag", "color": "#E91E63"},
    {"name": "Education", "icon": "school", "color": "#00BCD4"},
    {"name": "Shopping", "icon": "shopping", "color": "#FF5722"},
    {"name": "Entertainment", "icon": "movie", "color": "#9B59B6"},
    {"name": "Dining", "icon": "silverware-fork-knife", "color": "#F1C40F"},
    {"name": "Other", "icon": "dots-horizontal", "color": "#95A5A6"},
]

KV = """
<NavRow@OneLineIconListItem>:
    _no_ripple_effect: True

<MainScreen>:
    md_bg_color: app.bg_color

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Sahibi Budget"
            elevation: 3
            md_bg_color: app.primary_color
            left_action_items: [["dots-vertical", lambda x: app.open_menu()]]

        MDScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(12)
                padding: dp(12)
                size_hint_y: None
                height: self.minimum_height

                # ---- Salary card ----
                MDCard:
                    size_hint_y: None
                    height: dp(150)
                    radius: [dp(18)]
                    elevation: 3
                    md_bg_color: app.primary_color
                    padding: dp(16)
                    orientation: "vertical"

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(12)
                        size_hint_y: None
                        height: dp(70)

                        MDIconButton:
                            icon: "wallet"
                            icon_size: dp(34)
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            pos_hint: {"center_y": .5}
                            on_release: app.show_salary_dialog()

                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(2)

                            MDLabel:
                                text: "MONTHLY SALARY"
                                font_style: "Overline"
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, .7
                                size_hint_y: None
                                height: dp(18)

                            MDLabel:
                                id: salary_label
                                text: "$0.00"
                                font_style: "H4"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 1
                                size_hint_y: None
                                height: dp(40)

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(8)

                        MDLabel:
                            id: remaining_label
                            text: "Remaining  $0.00"
                            font_style: "Subtitle2"
                            theme_text_color: "Custom"
                            text_color: app.accent_color
                            adaptive_height: True

                        MDLabel:
                            id: spent_label
                            text: "Spent  $0.00"
                            font_style: "Subtitle2"
                            halign: "right"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, .85
                            adaptive_height: True

                # ---- Add expense button ----
                MDRaisedButton:
                    text: "  ADD EXPENSE"
                    icon: "plus"
                    size_hint_x: 1
                    size_hint_y: None
                    height: dp(52)
                    md_bg_color: app.accent_color
                    font_style: "Button"
                    on_release: app.show_expense_dialog()

                # ---- Filter row ----
                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: dp(48)

                    MDLabel:
                        text: "Transactions"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: app.primary_color

                    MDFlatButton:
                        id: filter_button
                        text: "All Categories"
                        theme_text_color: "Custom"
                        text_color: app.primary_color
                        on_release: app.open_filter_menu(self)

                MDLabel:
                    id: empty_label
                    text: "No transactions yet.\\nTap ADD EXPENSE to begin."
                    halign: "center"
                    theme_text_color: "Hint"
                    font_style: "Body1"
                    size_hint_y: None
                    height: dp(120)

                MDBoxLayout:
                    id: expense_list
                    orientation: "vertical"
                    spacing: dp(8)
                    size_hint_y: None
                    height: self.minimum_height

<EntryCard@MDCard>:
    size_hint_y: None
    height: dp(72)
    radius: [dp(14)]
    elevation: 1
    md_bg_color: app.card_color
    padding: [dp(12), dp(8)]
    orientation: "horizontal"
    spacing: dp(10)

    MDIconButton:
        icon: root.cat_icon
        theme_text_color: "Custom"
        text_color: root.cat_color
        pos_hint: {"center_y": .5}
        on_release: root.get_parent_window() and app.edit_entry(root.entry_index)

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(1)
        pos_hint: {"center_y": .5}

        MDLabel:
            text: root.entry_title
            font_style: "Body1"
            bold: True
            theme_text_color: "Primary"
            size_hint_y: None
            height: dp(22)

        MDLabel:
            text: root.entry_sub
            font_style: "Caption"
            theme_text_color: "Secondary"
            size_hint_y: None
            height: dp(18)

    MDLabel:
        text: root.entry_amount
        font_style: "Subtitle1"
        bold: True
        halign: "right"
        valign: "center"
        theme_text_color: "Custom"
        text_color: root.amount_color
        size_hint_x: None
        width: dp(90)

    MDIconButton:
        icon: "delete-outline"
        theme_text_color: "Custom"
        text_color: app.text_secondary
        pos_hint: {"center_y": .5}
        on_release: app.delete_entry(root.entry_index)

<SalaryDialogContent@MDBoxLayout>:
    orientation: "vertical"
    spacing: dp(12)
    adaptive_height: True
    size_hint_y: None
    height: dp(160)

    MDTextField:
        id: salary_field
        hint_text: "Monthly salary amount"
        input_filter: "float"
        mode: "rectangle"

    MDTextField:
        id: salary_note
        hint_text: "Note (optional)"
        mode: "rectangle"

<ExpenseDialogContent@MDBoxLayout>:
    orientation: "vertical"
    spacing: dp(12)
    adaptive_height: True
    size_hint_y: None
    height: dp(230)

    MDTextField:
        id: amount_field
        hint_text: "Amount"
        input_filter: "float"
        mode: "rectangle"

    MDTextField:
        id: category_field
        hint_text: "Category"
        text: "Groceries"
        mode: "rectangle"
        on_focus: if self.focus: app.open_category_dropdown(self)

    MDTextField:
        id: note_field
        hint_text: "Note (optional)"
        mode: "rectangle"

<CategoryDialogContent@MDBoxLayout>:
    orientation: "vertical"
    spacing: dp(12)
    adaptive_height: True
    size_hint_y: None
    height: dp(160)

    MDTextField:
        id: name_field
        hint_text: "Category name"
        mode: "rectangle"

    MDTextField:
        id: icon_field
        hint_text: "Icon name (e.g. cart, home, car)"
        text: "dots-horizontal"
        mode: "rectangle"
"""


class MainScreen(MDScreen):
    pass


class EntryCard(MDCard):
    entry_index = NumericProperty(0)
    entry_title = StringProperty("")
    entry_sub = StringProperty("")
    entry_amount = StringProperty("")
    cat_icon = StringProperty("dots-horizontal")
    cat_color = ListProperty([0.5, 0.5, 0.5, 1])
    amount_color = ListProperty([0.1, 0.1, 0.1, 1])


class SalaryDialogContent(MDBoxLayout):
    pass


class ExpenseDialogContent(MDBoxLayout):
    pass


class CategoryDialogContent(MDBoxLayout):
    pass


class SahibiBudgetApp(MDApp):
    salary = NumericProperty(0.0)
    entries = ListProperty([])
    custom_categories = ListProperty([])
    category_filter = StringProperty("All")

    primary_color = PRIMARY
    accent_color = ACCENT
    danger_color = DANGER
    warn_color = WARN
    bg_color = BG
    card_color = CARD
    text_secondary = "#7F8C8D"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.salary_dialog = None
        self.expense_dialog = None
        self.category_dialog = None
        self.category_menu = None
        self.filter_menu = None
        self.main_menu = None
        self._editing_index = None

    def build(self):
        self.theme_cls.primary_palette = "BlueGrey"
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        self.load_data()
        return Builder.load_string(KV)

    def on_start(self):
        self.refresh()

    # ---------------- categories ----------------

    @property
    def categories(self):
        return DEFAULT_CATEGORIES + self.custom_categories

    def category_info(self, name):
        for c in self.categories:
            if c["name"] == name:
                return c
        return {"name": name, "icon": "dots-horizontal", "color": "#95A5A6"}

    # ---------------- storage ----------------

    def data_path(self):
        return os.path.join(self.user_data_dir, "budget_data.json")

    def load_data(self):
        path = self.data_path()
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.salary = float(data.get("salary", 0.0))
            self.entries = list(data.get("entries", []))
            self.custom_categories = list(data.get("custom_categories", []))
        except Exception:
            pass

    def save_data(self):
        try:
            with open(self.data_path(), "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "salary": self.salary,
                        "entries": self.entries,
                        "custom_categories": self.custom_categories,
                    },
                    f,
                )
        except Exception:
            pass

    # ---------------- totals ----------------

    def total_spent(self):
        total = 0.0
        for e in self.entries:
            if self.category_filter != "All" and e.get("category") != self.category_filter:
                continue
            total += float(e.get("amount", 0))
        return total

    def remaining(self):
        return self.salary - sum(float(e.get("amount", 0)) for e in self.entries)

    # ---------------- ui ----------------

    def refresh(self):
        screen = self.root
        if not screen:
            return
        ids = screen.ids
        ids.salary_label.text = f"${self.salary:,.2f}"

        rem = self.remaining()
        ids.remaining_label.text = f"Remaining  ${rem:,.2f}"
        ids.remaining_label.text_color = get_color_from_hex(ACCENT if rem >= 0 else DANGER)
        ids.spent_label.text = f"Spent  ${self.total_spent():,.2f}"

        container = ids.expense_list
        container.clear_widgets()

        visible = [
            (i, e) for i, e in enumerate(self.entries)
            if self.category_filter == "All" or e.get("category") == self.category_filter
        ]
        visible.sort(key=lambda p: p[1].get("date", ""), reverse=True)

        ids.empty_label.opacity = 0 if visible else 1

        for index, entry in visible:
            info = self.category_info(entry.get("category", "Other"))
            note = entry.get("note") or entry.get("category", "")
            date = entry.get("date", "")[:10]
            card = EntryCard(
                entry_index=index,
                entry_title=entry.get("category", "Other"),
                entry_sub=f"{note}   ·   {date}",
                entry_amount=f"-${float(entry.get('amount', 0)):,.2f}",
                cat_icon=info["icon"],
                cat_color=get_color_from_hex(info["color"]),
                amount_color=get_color_from_hex(DANGER),
            )
            container.add_widget(card)

    # ---------------- salary ----------------

    def show_salary_dialog(self):
        if not self.salary_dialog:
            content = SalaryDialogContent()
            self.salary_dialog = MDDialog(
                title="Set Monthly Salary",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        on_release=lambda x: self.salary_dialog.dismiss(),
                    ),
                    MDRaisedButton(
                        text="Save",
                        md_bg_color=get_color_from_hex(ACCENT),
                        on_release=lambda x: self.save_salary(content),
                    ),
                ],
            )
        content = self.salary_dialog.content_cls
        content.ids.salary_field.text = f"{self.salary:.2f}" if self.salary else ""
        content.ids.salary_note.text = ""
        self.salary_dialog.open()

    def save_salary(self, content):
        try:
            value = float(content.ids.salary_field.text or 0)
        except ValueError:
            value = 0.0
        self.salary = value
        self.save_data()
        self.refresh()
        self.salary_dialog.dismiss()

    # ---------------- expenses ----------------

    def show_expense_dialog(self, index=None):
        self._editing_index = index

        if not self.expense_dialog:
            content = ExpenseDialogContent()
            self.expense_dialog = MDDialog(
                title="Add Expense",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        on_release=lambda x: self.expense_dialog.dismiss(),
                    ),
                    MDRaisedButton(
                        text="Save",
                        md_bg_color=get_color_from_hex(ACCENT),
                        on_release=lambda x: self.save_expense(content),
                    ),
                ],
            )

        content = self.expense_dialog.content_cls
        content.ids.amount_field.text = ""
        content.ids.note_field.text = ""
        content.ids.category_field.text = "Groceries"

        if index is not None and 0 <= index < len(self.entries):
            entry = self.entries[index]
            content.ids.amount_field.text = f"{float(entry.get('amount', 0)):.2f}"
            content.ids.note_field.text = entry.get("note", "")
            content.ids.category_field.text = entry.get("category", "Groceries")
            self.expense_dialog.title = "Edit Expense"
        else:
            self.expense_dialog.title = "Add Expense"

        self.expense_dialog.open()

    def save_expense(self, content):
        try:
            amount = float(content.ids.amount_field.text or 0)
        except ValueError:
            return
        if amount <= 0:
            return

        category = content.ids.category_field.text or "Other"
        note = content.ids.note_field.text or ""

        if self._editing_index is not None and 0 <= self._editing_index < len(self.entries):
            entry = self.entries[self._editing_index]
            entry["amount"] = amount
            entry["category"] = category
            entry["note"] = note
            entry["date"] = datetime.now().isoformat()
        else:
            self.entries.append(
                {
                    "amount": amount,
                    "category": category,
                    "note": note,
                    "date": datetime.now().isoformat(),
                }
            )

        self._editing_index = None
        self.save_data()
        self.refresh()
        self.expense_dialog.dismiss()

    def edit_entry(self, index):
        self.show_expense_dialog(index)

    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            self.entries.pop(index)
            self.save_data()
            self.refresh()

    # ---------------- dropdown menus ----------------

    def open_category_dropdown(self, field):
        items = [
            {
                "text": c["name"],
                "leading_icon": c["icon"],
                "viewclass": "OneLineListItem",
                "on_release": lambda name=c["name"]: self.pick_category(name),
            }
            for c in self.categories
        ]
        items.append(
            {
                "text": "+ New category",
                "leading_icon": "plus-circle-outline",
                "viewclass": "OneLineListItem",
                "on_release": self.open_new_category_from_dropdown,
            }
        )
        self.category_menu = MDDropdownMenu(
            caller=field,
            items=items,
            width_mult=4,
        )
        self.category_menu.open()

    def pick_category(self, name):
        if self.expense_dialog:
            self.expense_dialog.content_cls.ids.category_field.text = name
        if self.category_menu:
            self.category_menu.dismiss()

    def open_new_category_from_dropdown(self):
        if self.category_menu:
            self.category_menu.dismiss()
        Clock.schedule_once(lambda dt: self.show_category_dialog(), 0.2)

    def open_filter_menu(self, button):
        names = ["All"] + [c["name"] for c in self.categories]
        items = [
            {
                "text": n,
                "viewclass": "OneLineListItem",
                "on_release": lambda name=n: self.pick_filter(name),
            }
            for n in names
        ]
        self.filter_menu = MDDropdownMenu(caller=button, items=items, width_mult=4)
        self.filter_menu.open()

    def pick_filter(self, name):
        self.category_filter = name
        self.root.ids.filter_button.text = (
            "All Categories" if name == "All" else name
        )
        if self.filter_menu:
            self.filter_menu.dismiss()
        self.refresh()

    # ---------------- categories manager ----------------

    def show_category_dialog(self):
        if not self.category_dialog:
            content = CategoryDialogContent()
            self.category_dialog = MDDialog(
                title="New Category",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        on_release=lambda x: self.category_dialog.dismiss(),
                    ),
                    MDRaisedButton(
                        text="Add",
                        md_bg_color=get_color_from_hex(ACCENT),
                        on_release=lambda x: self.add_category(content),
                    ),
                ],
            )
        content = self.category_dialog.content_cls
        content.ids.name_field.text = ""
        content.ids.icon_field.text = "dots-horizontal"
        self.category_dialog.open()

    def add_category(self, content):
        name = (content.ids.name_field.text or "").strip()
        icon = (content.ids.icon_field.text or "").strip() or "dots-horizontal"
        if not name:
            return
        if name in [c["name"] for c in self.categories]:
            return
        palette = ["#E74C3C", "#F39C12", "#3498DB", "#9B59B6", "#1ABC9C", "#FF5722"]
        self.custom_categories.append(
            {
                "name": name,
                "icon": icon,
                "color": palette[len(self.custom_categories) % len(palette)],
            }
        )
        self.save_data()
        self.category_dialog.dismiss()
        if self.expense_dialog:
            self.expense_dialog.content_cls.ids.category_field.text = name

    # ---------------- app menu ----------------

    def open_menu(self):
        items = [
            {
                "text": "Manage categories",
                "leading_icon": "shape-outline",
                "viewclass": "OneLineListItem",
                "on_release": lambda: (self.main_menu.dismiss(), self.show_category_dialog()),
            },
            {
                "text": "Reset this month",
                "leading_icon": "refresh",
                "viewclass": "OneLineListItem",
                "on_release": lambda: (self.main_menu.dismiss(), self.confirm_reset()),
            },
        ]
        self.main_menu = MDDropdownMenu(
            caller=self.root.ids.get("toolbar", None) or self.root,
            items=items,
            width_mult=4,
        )
        if self.main_menu.caller is None:
            self.menu_dismiss = None
            return
        self.main_menu.open()

    def confirm_reset(self):
        dialog = MDDialog(
            title="Reset month?",
            text="This clears the salary and every transaction.",
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="Reset",
                    md_bg_color=get_color_from_hex(DANGER),
                    on_release=lambda x: self.do_reset(dialog),
                ),
            ],
        )
        dialog.open()

    def do_reset(self, dialog):
        self.salary = 0.0
        self.entries = []
        self.category_filter = "All"
        if self.root:
            self.root.ids.filter_button.text = "All Categories"
        self.save_data()
        self.refresh()
        dialog.dismiss()


if __name__ == "__main__":
    SahibiBudgetApp().run()
