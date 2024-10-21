import tkinter as tk
from managers.book_manager import BookApp
from managers.publisher_manager import PublisherApp
from managers.borrow_manager import BorrowReturnApp

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

        btn_publisher = tk.Button(self.sidebar_frame, text="Quản lý Nhà xuất bản", command=self.show_publisher_app, bg="#34495E", fg="white", font=("Arial", 12), pady=10)
        btn_publisher.pack(fill="x")

        btn_borrow = tk.Button(self.sidebar_frame, text="Quản lý Mượn trả Sách", command=self.show_borrow_app, bg="#34495E", fg="white", font=("Arial", 12), pady=10)
        btn_borrow.pack(fill="x")

        # Khởi tạo AuthorApp và BookApp
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.book_app = BookApp(self.content_frame)
        self.publisher_app = PublisherApp(self.content_frame)
        self.borrow_app = BorrowReturnApp(self.content_frame)


        # Hiển thị BookApp mặc định
        self.book_app.pack(fill="both", expand=True)

    def show_book_app(self):
        self.publisher_app.pack_forget()  # Ẩn AuthorApp
        self.borrow_app.pack_forget()  # Ẩn BorrowApp
        self.book_app.pack(fill="both", expand=True)  # Hiển thị BookApp

    def show_publisher_app(self):
        self.book_app.pack_forget()  # Ẩn BookApp
        self.borrow_app.pack_forget()  # Ẩn BorrowApp
        self.publisher_app.pack(fill="both", expand=True)  # Hiển thị PublisherApp
    
    def show_borrow_app(self):
        self.publisher_app.pack_forget()  # Ẩn AuthorApp
        self.book_app.pack_forget()  # Ẩn BookApp
        self.borrow_app.pack(fill="both", expand=True)  # Hiển thị BorrowApp

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
