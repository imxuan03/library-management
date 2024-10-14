import tkinter as tk
from managers.author_manager import AuthorApp
from managers.book_manager import BookApp

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý Thư viện")
        self.geometry("800x600")

        # Tạo sidebar
        self.sidebar_frame = tk.Frame(self, bg="#2C3E50", width=200)
        self.sidebar_frame.pack(side="left", fill="y")

        # Nút trong sidebar
        btn_book = tk.Button(self.sidebar_frame, text="Quản lý Sách", command=self.show_book_app, bg="#34495E", fg="white", font=("Arial", 12), pady=10)
        btn_book.pack(fill="x")

        btn_author = tk.Button(self.sidebar_frame, text="Quản lý Tác giả", command=self.show_author_app, bg="#34495E", fg="white", font=("Arial", 12), pady=10)
        btn_author.pack(fill="x")

        # Khởi tạo AuthorApp và BookApp
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.author_app = AuthorApp(self.content_frame)
        self.book_app = BookApp(self.content_frame)

        # Hiển thị BookApp mặc định
        self.book_app.pack(fill="both", expand=True)

    def show_author_app(self):
        self.book_app.pack_forget()  # Ẩn BookApp
        self.author_app.pack(fill="both", expand=True)  # Hiển thị AuthorApp

    def show_book_app(self):
        self.author_app.pack_forget()  # Ẩn AuthorApp
        self.book_app.pack(fill="both", expand=True)  # Hiển thị BookApp

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
