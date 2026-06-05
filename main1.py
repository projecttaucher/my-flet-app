import flet as ft
import flet.colors as colors  # استيراد صريح للألوان لحل مشكلة الـ AttributeError
import json
import os
import ssl
from datetime import datetime

# تجاوز فحص الـ SSL الصارم لتحميل محرك الرسوميات
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

DATA_FILE = "hassala_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
            except:
                return {}
    return {}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass

def main(page: ft.Page):
    page.title = "الحصالة"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    title = ft.Text("🪙 الحصالة 🪙", size=28, weight=ft.FontWeight.BOLD, color=colors.ORANGE_700)
    
    animals_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("🦆", size=30),
                ft.Text("🦁", size=30),
                ft.Text("🦒", size=30),
                ft.Text("🐒", size=30),
                ft.Text("🐦", size=30),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        margin=10,
        padding=10,
        bgcolor=colors.GREEN_50,
        border_radius=15,
        border=ft.border.all(1, colors.GREEN_200)
    )

    list_container = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def refresh_ui():
        list_container.controls.clear()
        current_data = load_data()
        
        if not current_data:
            list_container.controls.append(ft.Text("الحصالة فارغة حالياً.", color=colors.GREY_500, size=16))
        else:
            for key, info in current_data.items():
                card = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"💰 {info['name']} {info['lastname']}", size=18, weight=ft.FontWeight.BOLD, color=colors.GREEN_800),
                            ft.Text(f"الرصيد: {info['balance']} د.ج", size=16, weight=ft.FontWeight.W_500)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([
                            ft.ElevatedButton("إيداع", bgcolor=colors.GREEN_100, color=colors.GREEN_900, on_click=lambda e, k=key: show_money_dialog(k, "add")),
                            ft.ElevatedButton("سحب", bgcolor=colors.RED_100, color=colors.RED_900, on_click=lambda e, k=key: show_money_dialog(k, "sub")),
                            ft.IconButton(ft.icons.DELETE, icon_color=colors.RED_400, on_click=lambda e, k=key: delete_item(k))
                        ], alignment=ft.MainAxisAlignment.END)
                    ]),
                    padding=15,
                    bgcolor=colors.YELLOW_50,
                    border_radius=10,
                    border=ft.border.all(1, colors.YELLOW_200),
                    width=400
                )
                list_container.controls.append(card)
        page.update()

    def add_child_dialog(e):
        name_input = ft.TextField(label="الاسم الأول", text_align=ft.TextAlign.CENTER)
        last_input = ft.TextField(label="اللقب", text_align=ft.TextAlign.CENTER)
        
        def save_new(e):
            n = name_input.value.strip()
            ln = last_input.value.strip()
            if n and ln:
                data = load_data()
                child_id = f"{n}_{ln}"
                if child_id not in data:
                    data[child_id] = {"name": n, "lastname": ln, "balance": 0, "history": []}
                    save_data(data)
                    page.dialog.open = False
                    refresh_ui()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("موجود سابقاً!"))
                    page.snack_bar.open = True
                    page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("إضافة طفل جديد"),
            content=ft.Column([name_input, last_input], height=120),
            actions=[ft.TextButton("حفظ", on_click=save_new)]
        )
        page.dialog.open = True
        page.update()

    def show_money_dialog(child_id, op_type):
        amount_input = ft.TextField(label="المبلغ", keyboard_type=ft.KeyboardType.NUMBER, text_align=ft.TextAlign.CENTER)
        
        def process(e):
            try:
                amt = float(amount_input.value.strip())
                if amt <= 0: return
                data = load_data()
                if op_type == "add":
                    data[child_id]['balance'] += amt
                else:
                    if data[child_id]['balance'] >= amt:
                        data[child_id]['balance'] -= amt
                    else:
                        return
                save_data(data)
                page.dialog.open = False
                refresh_ui()
            except:
                pass

        page.dialog = ft.AlertDialog(
            title=ft.Text("إيداع مبلغ" if op_type == "add" else "سحب مبلغ"),
            content=amount_input,
            actions=[ft.TextButton("تأكيد", on_click=process)]
        )
        page.dialog.open = True
        page.update()

    def delete_item(child_id):
        data = load_data()
        if child_id in data:
            del data[child_id]
            save_data(data)
            refresh_ui()

    add_btn = ft.FloatingActionButton(icon=ft.icons.ADD, text="أضف طفل", on_click=add_child_dialog, bgcolor=colors.BLUE_400)
    page.add(title, animals_row, list_container, add_btn)
    refresh_ui()

if __name__ == "__main__":
    ft.app(main)