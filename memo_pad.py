import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import os

class FindReplaceDialog(tk.Toplevel):
    def __init__(self, master, text_widget):
        super().__init__(master)
        self.text_widget = text_widget
        self.title("찾기 및 바꾸기")
        self.transient(master)

        tk.Label(self, text="찾을 내용:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.find_entry = tk.Entry(self)
        self.find_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="바꿀 내용:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.replace_entry = tk.Entry(self)
        self.replace_entry.grid(row=1, column=1, padx=5, pady=5)

        find_button = tk.Button(self, text="다음 찾기", command=self.find_next)
        find_button.grid(row=0, column=2, padx=5, pady=5)

        replace_button = tk.Button(self, text="바꾸기", command=self.replace)
        replace_button.grid(row=1, column=2, padx=5, pady=5)

        replace_all_button = tk.Button(self, text="모두 바꾸기", command=self.replace_all)
        replace_all_button.grid(row=2, column=2, padx=5, pady=5)
        
        self.find_entry.focus_set()

    def find_next(self):
        self.text_widget.tag_remove('found', '1.0', tk.END)
        start = self.text_widget.search(self.find_entry.get(), '1.0', stopindex=tk.END)
        if start:
            end = f"{start}+{len(self.find_entry.get())}c"
            self.text_widget.tag_add('found', start, end)
            self.text_widget.mark_set("insert", end)
            self.text_widget.see(end)
            self.text_widget.focus_set()

    def replace(self):
        if self.text_widget.tag_ranges('found'):
            start = self.text_widget.index('found.first')
            end = self.text_widget.index('found.last')
            self.text_widget.delete(start, end)
            self.text_widget.insert(start, self.replace_entry.get())
            self.find_next()

    def replace_all(self):
        content = self.text_widget.get('1.0', tk.END)
        new_content = content.replace(self.find_entry.get(), self.replace_entry.get())
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', new_content)


class MemoPad:
    def __init__(self, root):
        self.root = root
        self.root.title("메모장")
        self.current_font_size = 12
        self.new_tab_count = 1
        self.recent_files = []

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        self.notebook.enable_traversal()

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # 파일 메뉴
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="파일", menu=self.file_menu)
        self.file_menu.add_command(label="새 탭", command=self.new_tab, accelerator="Ctrl+T")
        self.file_menu.add_command(label="새 창", command=self.new_window, accelerator="Ctrl+N")
        self.file_menu.add_command(label="열기", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="저장", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="다른 이름으로 저장", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.recent_files_menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label="최근 파일", menu=self.recent_files_menu)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="종료", command=self.exit_app)

        # 편집 메뉴
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="편집", menu=self.edit_menu)
        self.edit_menu.add_command(label="실행 취소", command=lambda: self.get_current_text_area().edit_undo(), accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="다시 실행", command=lambda: self.get_current_text_area().edit_redo(), accelerator="Ctrl+Y")

        # 찾기 메뉴
        self.find_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="찾기", menu=self.find_menu)
        self.find_menu.add_command(label="찾기", command=self.show_find_replace_dialog, accelerator="Ctrl+F")
        self.find_menu.add_command(label="바꾸기", command=self.show_find_replace_dialog, accelerator="Ctrl+H")

        # 보기 메뉴
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="보기", menu=self.view_menu)
        self.zoom_menu = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label="확대/축소", menu=self.zoom_menu)
        self.zoom_menu.add_command(label="확대", command=self.zoom_in, accelerator="Ctrl+=")
        self.zoom_menu.add_command(label="축소", command=self.zoom_out, accelerator="Ctrl+-")
        self.zoom_menu.add_command(label="기본값으로 복원", command=self.reset_zoom, accelerator="Ctrl+0")

        self.new_tab()
        self.load_recent_files()
        self.update_recent_files_menu()

        self.root.bind("<Control-t>", lambda event: self.new_tab())
        self.root.bind("<Control-n>", lambda event: self.new_window())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda event: self.save_as_file())
        self.root.bind("<Control-z>", lambda event: self.get_current_text_area().edit_undo())
        self.root.bind("<Control-y>", lambda event: self.get_current_text_area().edit_redo())
        self.root.bind("<Control-f>", lambda event: self.show_find_replace_dialog())
        self.root.bind("<Control-h>", lambda event: self.show_find_replace_dialog())
        self.root.bind("<Control-=>", lambda event: self.zoom_in())
        self.root.bind("<Control-minus>", lambda event: self.zoom_out())
        self.root.bind("<Control-0>", lambda event: self.reset_zoom())

    def get_current_text_area(self):
        selected_tab = self.notebook.select()
        if not selected_tab:
            return None
        return self.notebook.nametowidget(selected_tab).winfo_children()[0]

    def new_tab(self, file_path=None):
        frame = tk.Frame(self.notebook)
        text_area = tk.Text(frame, undo=True)
        text_area.pack(expand=True, fill='both')
        text_area.config(font=font.Font(size=self.current_font_size))

        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                text_area.insert(tk.END, file.read())
            self.notebook.add(frame, text=os.path.basename(file_path))
            frame.file_path = file_path
        else:
            title = f"새 탭_{self.new_tab_count}"
            self.notebook.add(frame, text=title)
            frame.file_path = None
            self.new_tab_count += 1
        
        self.notebook.select(frame)
        self.add_close_button_to_tab(frame)

    def add_close_button_to_tab(self, tab_frame):
        close_button = tk.Button(tab_frame, text="X", command=lambda: self.close_tab(tab_frame), relief=tk.FLAT)
        self.notebook.add(tab_frame)
        tab_id = self.notebook.index(tab_frame)
        self.notebook.tab(tab_id, text=self.notebook.tab(tab_id, "text"))
        close_button.place(in_=self.notebook.tabs()[tab_id], relx=1.0, rely=0, anchor="ne")

    def close_tab(self, tab_frame):
        text_area = tab_frame.winfo_children()[0]
        if text_area.edit_modified():
            result = messagebox.askyesnocancel("저장", f"{self.notebook.tab(tab_frame, 'text')} 파일을 저장하시겠습니까?")
            if result is True:
                self.save_file()
                self.notebook.forget(tab_frame)
            elif result is False:
                self.notebook.forget(tab_frame)
        else:
            self.notebook.forget(tab_frame)

    def new_window(self):
        new_root = tk.Toplevel()
        MemoPad(new_root)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.* ")]
        )
        if file_path:
            self.new_tab(file_path)
            self.add_recent_file(file_path)

    def save_file(self):
        frame = self.notebook.nametowidget(self.notebook.select())
        if hasattr(frame, 'file_path') and frame.file_path:
            with open(frame.file_path, "w", encoding="utf-8") as file:
                file.write(self.get_current_text_area().get(1.0, tk.END))
            self.notebook.tab(self.notebook.select(), text=os.path.basename(frame.file_path))
            self.get_current_text_area().edit_modified(False)
        else:
            self.save_as_file()

    def save_as_file(self):
        frame = self.notebook.nametowidget(self.notebook.select())
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.* ")]
        )
        if file_path:
            frame.file_path = file_path
            self.save_file()
            self.add_recent_file(file_path)

    def exit_app(self):
        if messagebox.askokcancel("종료", "메모장을 종료하시겠습니까?"):
            self.save_recent_files()
            self.root.destroy()

    def update_font(self):
        for tab_id in self.notebook.tabs():
            frame = self.notebook.nametowidget(tab_id)
            text_area = frame.winfo_children()[0]
            text_area.config(font=font.Font(size=self.current_font_size))

    def zoom_in(self):
        self.current_font_size += 2
        self.update_font()

    def zoom_out(self):
        if self.current_font_size > 2:
            self.current_font_size -= 2
            self.update_font()

    def reset_zoom(self):
        self.current_font_size = 12
        self.update_font()

    def show_find_replace_dialog(self):
        text_area = self.get_current_text_area()
        if text_area:
            FindReplaceDialog(self.root, text_area)

    def add_recent_file(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:10] # 최근 10개 파일만 저장
        self.update_recent_files_menu()

    def update_recent_files_menu(self):
        self.recent_files_menu.delete(0, tk.END)
        for file_path in self.recent_files:
            self.recent_files_menu.add_command(label=file_path, command=lambda p=file_path: self.new_tab(p))

    def load_recent_files(self):
        try:
            with open("recent_files.txt", "r") as f:
                self.recent_files = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            pass

    def save_recent_files(self):
        with open("recent_files.txt", "w") as f:
            for file_path in self.recent_files:
                f.write(file_path + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoPad(root)
    root.mainloop()
