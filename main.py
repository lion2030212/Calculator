import tkinter as tk
import re

# الألوان
COLOR_BG = "#000000"
COLOR_NUM = "#1A1A1A"
COLOR_TEXT_WHITE = "#FFFFFF"
COLOR_TEXT_GREY = "#888888"
COLOR_GREEN = "#4CAF50"
COLOR_RED = "#D32F2F"
COLOR_EQUAL = "#2E7D32"

class SamsungCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("Samsung Calculator")
        
        # إصلاح 1: جعل النافذة تأخذ حجم الشاشة كاملاً في الأندرويد
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        self.root.geometry(f"{screen_w}x{screen_h}")
        self.root.configure(bg=COLOR_BG)

        self.display = tk.Text(
            root, font=("Helvetica", 32), bg=COLOR_BG, fg=COLOR_TEXT_WHITE,
            borderwidth=0, highlightthickness=0, padx=20, pady=20,
            height=3, wrap="char", spacing1=5,
            insertbackground=COLOR_GREEN, state="disabled", 
            cursor="arrow", takefocus=False
        )
        self.display.tag_configure("right", justify='right')
        self.display.pack(fill="x", pady=(30, 0))

        self.lower_label = tk.Label(
            root, text="", font=("Helvetica", 24),
            bg=COLOR_BG, fg=COLOR_TEXT_GREY, anchor="e", padx=25
        )
        self.lower_label.pack(fill="x")

        self.tool_frame = tk.Frame(root, bg=COLOR_BG)
        self.tool_frame.pack(fill="x", padx=20, pady=5)
        self.btn_back = tk.Button(
            self.tool_frame, text="⌫", font=("Helvetica", 18),
            bg=COLOR_BG, fg=COLOR_GREEN, bd=0, highlightthickness=0,
            command=self.backspace
        )
        self.btn_back.pack(side="right")

        self.grid_frame = tk.Frame(root, bg=COLOR_BG)
        # إصلاح 2: جعل فريم الأزرار يتوسع ليملأ باقي الشاشة
        self.grid_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.setup_grid()

    def setup_grid(self):
        # إصلاح 3: التأكد من إعطاء وزن لكل عمود وصف لضمان توزيع الشبكة
        for i in range(4): self.grid_frame.grid_columnconfigure(i, weight=1)
        for i in range(5): self.grid_frame.grid_rowconfigure(i, weight=1)

        buttons = [
            ('C', 0, 0, COLOR_RED), ('( )', 0, 1, COLOR_GREEN), ('%', 0, 2, COLOR_GREEN), ('÷', 0, 3, COLOR_GREEN),
            ('7', 1, 0, COLOR_TEXT_WHITE), ('8', 1, 1, COLOR_TEXT_WHITE), ('9', 1, 2, COLOR_TEXT_WHITE), ('×', 1, 3, COLOR_GREEN),
            ('4', 2, 0, COLOR_TEXT_WHITE), ('5', 2, 1, COLOR_TEXT_WHITE), ('6', 2, 2, COLOR_TEXT_WHITE), ('-', 2, 3, COLOR_GREEN),
            ('1', 3, 0, COLOR_TEXT_WHITE), ('2', 3, 1, COLOR_TEXT_WHITE), ('3', 3, 2, COLOR_TEXT_WHITE), ('+', 3, 3, COLOR_GREEN),
            ('+/-', 4, 0, COLOR_TEXT_WHITE), ('0', 4, 1, COLOR_TEXT_WHITE), ('.', 4, 2, COLOR_TEXT_WHITE), ('=', 4, 3, COLOR_EQUAL)
        ]

        for (text, r, c, fg) in buttons:
            bg = COLOR_NUM if text.isdigit() or text in ['.', '+/-'] else COLOR_BG
            btn = tk.Button(
                self.grid_frame, text=text, font=("Helvetica", 22),
                bg=bg, fg=fg, bd=0, highlightthickness=0, activebackground="#333333",
                command=lambda x=text: self.handle_click(x)
            )
            # استخدام sticky="nsew" ضروري جداً هنا لتمدد الزر
            btn.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)

    def get_content(self):
        return self.display.get("1.0", "end-1c").replace('\n', '')

    def update_font_size(self):
        length = len(self.get_content())
        size = 32 if length <= 12 else 26 if length <= 22 else 20
        self.display.config(font=("Helvetica", size))

    def update_display(self, action, value=None):
        self.display.config(state="normal")
        changeable_ops = ['+', '-', '×', '÷']
        
        if action == "insert":
            pos = self.display.index(tk.INSERT)
            last_char = self.display.get(f"{pos}-1c", pos)
            
            if value == ".":
                current_text = self.get_content()[:int(pos.split('.')[1])]
                current_number = re.split(r'[\+\-\×\÷\%\(\)]', current_text)[-1]
                if "." in current_number:
                    self.display.config(state="disabled")
                    return

            if value in changeable_ops and last_char in changeable_ops:
                self.display.delete(f"{pos}-1c", pos)
            
            self.display.insert(tk.INSERT, value)
            
        elif action == "delete_all":
            self.display.delete("1.0", tk.END)
        elif action == "backspace":
            curr_pos = self.display.index(tk.INSERT)
            if curr_pos != "1.0": self.display.delete(f"{curr_pos}-1c", curr_pos)
        elif action == "replace_all":
            self.display.delete("1.0", tk.END)
            self.display.insert("1.0", value)

        self.display.tag_add("right", "1.0", tk.END)
        self.update_font_size()
        self.display.config(state="disabled")
        self.update_live_preview()

    def handle_click(self, char):
        if char == 'C':
            self.update_display("delete_all")
            self.lower_label.config(text="")
        elif char == '.':
            text = self.get_content()
            pos = self.display.index(tk.INSERT)
            last_char = self.display.get(f"{pos}-1c", pos) if text else ""
            if not text or last_char in ['+', '-', '×', '÷', '(', '%']:
                self.update_display("insert", "0.")
            else:
                self.update_display("insert", ".")
        elif char == '( )':
            text = self.get_content()
            symbol = '(' if text.count('(') <= text.count(')') else ')'
            self.update_display("insert", symbol)
        elif char == '+/-':
            self.toggle_sign()
        elif char == '=':
            try:
                res = self.calculate_smart_logic(self.get_content())
                self.update_display("replace_all", str(res))
                self.lower_label.config(text="")
            except: pass
        else:
            self.update_display("insert", char)

    def calculate_smart_logic(self, exp):
        if not exp: return ""
        temp_exp = exp
        if temp_exp.count('(') > temp_exp.count(')'):
            temp_exp += ')' * (temp_exp.count('(') - temp_exp.count(')'))
        clean_exp = temp_exp.replace('×', '*').replace('÷', '/')
        try:
            percent_pattern = re.compile(r'(.+)([-+])(\d+(\.\d+)?)%')
            match = percent_pattern.search(clean_exp)
            if match:
                base_expr = match.group(1)
                operator = match.group(2)
                perc_val = match.group(3)
                base_res = eval(base_expr)
                final_formula = f"{base_res} {operator} ({base_res} * ({perc_val} / 100))"
                result = eval(final_formula)
            else:
                clean_exp = re.sub(r'(\d+(\.\d+)?)\s*%', r'(\1/100)', clean_exp)
                clean_exp = clean_exp.rstrip('+-*/.(')
                result = eval(clean_exp)
            return int(result) if result == int(result) else round(result, 8)
        except: return "Error"

    def toggle_sign(self):
        self.display.config(state="normal")
        text = self.get_content()
        pos = self.display.index(tk.INSERT)
        if not text:
            self.display.insert(tk.INSERT, "(-")
        else:
            idx = int(pos.split('.')[1])
            match = re.search(r'(\(-?\d*\.?\d*|\d+\.?\d*)$', text[:idx])
            if match:
                val = match.group(0)
                start_index = f"1.0 + {match.start()} c"
                end_index = f"1.0 + {match.end()} c"
                new_val = val.replace("(-", "") if val.startswith("(-") else f"(-{val}"
                self.display.delete(start_index, end_index)
                self.display.insert(start_index, new_val)
            else:
                self.display.insert(tk.INSERT, "(-")
        self.display.tag_add("right", "1.0", tk.END)
        self.display.config(state="disabled")
        self.update_live_preview()

    def backspace(self):
        self.update_display("backspace")

    def update_live_preview(self):
        exp = self.get_content()
        try:
            if any(op in exp for op in ['+', '-', '×', '÷', '%']):
                preview = self.calculate_smart_logic(exp)
                self.lower_label.config(text=str(preview) if preview != "Error" else "")
            else: self.lower_label.config(text="")
        except: self.lower_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = SamsungCalc(root)
    root.mainloop()
