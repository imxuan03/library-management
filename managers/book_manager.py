import tkinter as tk
from tkinter import ttk
import mysql.connector

class BookApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_book_list(self)
        self.create_book_info(self)

    def create_book_list(self, parent):
        title = tk.Label(parent, text="QUẢN LÝ SÁCH", font=("Arial", 16, "bold"), fg="green", bg="white")
        title.pack(pady=10)

        # Frame chứa bảng danh sách
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", padx=20)

        # Tạo bảng Sách
        columns = ("Mã Sách", "Tên Sách", "Mã Tác Giả", "Mã Thể Loại", "Mã NXB", "Năm XB")
        self.book_table = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)

        # Cấu hình tiêu đề và độ rộng cột
        for col in columns:
            self.book_table.heading(col, text=col)
            self.book_table.column(col, anchor="center", width=100)

        # Nạp dữ liệu từ MySQL
        self.load_book_data()

        self.book_table.pack(side="left", fill="both")

        # Thêm thanh cuộn dọc cho bảng
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.book_table.yview)
        self.book_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.book_table.bind('<<TreeviewSelect>>', self.on_book_select)

    def load_book_data(self):
        """Nạp dữ liệu sách từ MySQL."""
        try:
            connection = mysql.connector.connect(
                host='localhost',      
                user='root',          
                password='111111', 
                database='qlthuvien'  
            )

            cursor = connection.cursor()
            cursor.execute("SELECT MaSach, TenSach, MaTG, MaTL, MaNXB, NamXB FROM Sach")

            # Xóa dữ liệu hiện tại trong bảng
            self.book_table.delete(*self.book_table.get_children())

            # Chèn dữ liệu mới
            for (book_id, book_name, author_id, genre_id, publisher_id, year) in cursor:
                self.book_table.insert('', 'end', values=(book_id, book_name, author_id, genre_id, publisher_id, year))

        except mysql.connector.Error as err:
            print(f"Lỗi khi kết nối MySQL: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def on_book_select(self, event):
        """Xử lý sự kiện khi chọn một sách trong bảng."""
        selected_item = self.book_table.selection()
        if selected_item:
            book_data = self.book_table.item(selected_item, 'values')
            self.book_code_entry.delete(0, tk.END)
            self.book_code_entry.insert(0, book_data[0])
            self.book_name_entry.delete(0, tk.END)
            self.book_name_entry.insert(0, book_data[1])
            self.author_code_combo.set(book_data[2])
            self.genre_code_combo.set(book_data[3])
            self.publisher_code_combo.set(book_data[4])
            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, book_data[5])

    def create_book_info(self, parent):
        info_frame = tk.Frame(parent)
        info_frame.pack(side="right", padx=20, pady=10)

        info_label = tk.Label(info_frame, text="THÔNG TIN SÁCH", font=("Arial", 12, "bold"))
        info_label.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(info_frame, text="Mã Sách:").grid(row=1, column=0, sticky="e")
        self.book_code_entry = tk.Entry(info_frame)
        self.book_code_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Tên Sách:").grid(row=2, column=0, sticky="e")
        self.book_name_entry = tk.Entry(info_frame)
        self.book_name_entry.grid(row=2, column=1, padx=10, pady=5)

        # Dropdown cho Mã Tác Giả
        tk.Label(info_frame, text="Mã Tác Giả:").grid(row=3, column=0, sticky="e")
        self.author_code_combo = ttk.Combobox(info_frame, state="readonly")
        self.author_code_combo.grid(row=3, column=1, padx=10, pady=5)

        # Dropdown cho Mã Thể Loại
        tk.Label(info_frame, text="Mã Thể Loại:").grid(row=4, column=0, sticky="e")
        self.genre_code_combo = ttk.Combobox(info_frame, state="readonly")
        self.genre_code_combo.grid(row=4, column=1, padx=10, pady=5)

        # Dropdown cho Mã NXB
        tk.Label(info_frame, text="Mã NXB:").grid(row=5, column=0, sticky="e")
        self.publisher_code_combo = ttk.Combobox(info_frame, state="readonly")
        self.publisher_code_combo.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Năm XB:").grid(row=6, column=0, sticky="e")
        self.year_entry = tk.Entry(info_frame)
        self.year_entry.grid(row=6, column=1, padx=10, pady=5)

        # Nút chức năng
        btn_frame = tk.Frame(info_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

        add_button = tk.Button(btn_frame, text="THÊM", width=8, command=self.add_book)
        add_button.grid(row=0, column=0, padx=5)

        save_button = tk.Button(btn_frame, text="CẬP NHẬT", width=8, command=self.update_book)
        save_button.grid(row=0, column=1, padx=5)

        delete_button = tk.Button(btn_frame, text="XÓA", width=8, command=self.delete_book)
        delete_button.grid(row=0, column=2, padx=5)

        reset_button = tk.Button(btn_frame, text="RESET", width=8, command=self.reset_entries)
        reset_button.grid(row=0, column=3, padx=5)

        # Phần tìm kiếm
        search_label = tk.Label(info_frame, text="TÌM KIẾM", font=("Arial", 12, "bold"))
        search_label.grid(row=8, column=0, columnspan=2, pady=10)

        tk.Label(info_frame, text="Tên Sách:").grid(row=9, column=0, sticky="e")
        self.search_name_entry = tk.Entry(info_frame)
        self.search_name_entry.grid(row=9, column=1, padx=10, pady=5)

        search_button = tk.Button(info_frame, text="TÌM KIẾM", width=10, command=self.search_book)
        search_button.grid(row=10, column=0, columnspan=2, pady=5)

        cancel_button = tk.Button(info_frame, text="HỦY TÌM KIẾM", width=10, command=self.reset_search)
        cancel_button.grid(row=11, column=0, columnspan=2, pady=5)

        # Nạp dữ liệu cho các combobox từ MySQL
        self.load_combobox_data()

    def load_combobox_data(self):
        """Nạp dữ liệu cho các combobox từ cơ sở dữ liệu."""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='111111',
                database='qlthuvien'
            )
            cursor = connection.cursor()

            # Nạp Mã Tác Giả
            cursor.execute("SELECT MaTG FROM TacGia")
            authors = [row[0] for row in cursor.fetchall()]
            self.author_code_combo['values'] = authors

            # Nạp Mã Thể Loại
            cursor.execute("SELECT MaTL FROM TheLoai")
            genres = [row[0] for row in cursor.fetchall()]
            self.genre_code_combo['values'] = genres

            # Nạp Mã Nhà Xuất Bản
            cursor.execute("SELECT MaNXB FROM NhaXuatBan")
            publishers = [row[0] for row in cursor.fetchall()]
            self.publisher_code_combo['values'] = publishers

        except mysql.connector.Error as err:
            print(f"Lỗi khi nạp dữ liệu combobox: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def add_book(self):
        """Thêm sách mới vào cơ sở dữ liệu."""
        book_id = self.book_code_entry.get()
        book_name = self.book_name_entry.get()
        author_id = self.author_code_combo.get()
        genre_id = self.genre_code_combo.get()
        publisher_id = self.publisher_code_combo.get()
        year = self.year_entry.get()

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='111111',
                database='qlthuvien'
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Sach (MaSach, TenSach, MaTG, MaTL, MaNXB, NamXB) VALUES (%s, %s, %s, %s, %s, %s)", 
                           (book_id, book_name, author_id, genre_id, publisher_id, year))
            connection.commit()

            # Xóa bảng cũ và nạp lại dữ liệu sau khi thêm
            self.load_book_data()
            self.reset_entries()
        except mysql.connector.Error as err:
            print(f"Lỗi khi thêm sách: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def update_book(self):
        """Cập nhật thông tin sách đã chọn."""
        selected_item = self.book_table.selection()
        if not selected_item:
            return  # Không có sách nào được chọn

        book_id = self.book_code_entry.get()
        book_name = self.book_name_entry.get()
        author_id = self.author_code_combo.get()
        genre_id = self.genre_code_combo.get()
        publisher_id = self.publisher_code_combo.get()
        year = self.year_entry.get()

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='111111',
                database='qlthuvien'
            )
            cursor = connection.cursor()
            cursor.execute("UPDATE Sach SET TenSach=%s, MaTG=%s, MaTL=%s, MaNXB=%s, NamXB=%s WHERE MaSach=%s", 
                           (book_name, author_id, genre_id, publisher_id, year, book_id))
            connection.commit()

            # Xóa bảng cũ và nạp lại dữ liệu sau khi cập nhật
            self.load_book_data()
            self.reset_entries()
        except mysql.connector.Error as err:
            print(f"Lỗi khi cập nhật sách: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def delete_book(self):
        """Xóa sách đã chọn khỏi cơ sở dữ liệu."""
        selected_item = self.book_table.selection()
        if not selected_item:
            return  # Không có sách nào được chọn

        book_id = self.book_table.item(selected_item, 'values')[0]

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='111111',
                database='qlthuvien'
            )
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Sach WHERE MaSach=%s", (book_id,))
            connection.commit()

            # Xóa bảng cũ và nạp lại dữ liệu sau khi xóa
            self.load_book_data()
            self.reset_entries()
        except mysql.connector.Error as err:
            print(f"Lỗi khi xóa sách: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def reset_entries(self):
        """Đặt lại các trường nhập liệu."""
        self.book_code_entry.delete(0, tk.END)
        self.book_name_entry.delete(0, tk.END)
        self.author_code_combo.set('')
        self.genre_code_combo.set('')
        self.publisher_code_combo.set('')
        self.year_entry.delete(0, tk.END)

    def search_book(self):
        """Tìm kiếm sách theo tên."""
        search_name = self.search_name_entry.get()
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='111111',
                database='qlthuvien'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT MaSach, TenSach, MaTG, MaTL, MaNXB, NamXB FROM Sach WHERE TenSach LIKE %s", 
                           ('%' + search_name + '%',))

            self.book_table.delete(*self.book_table.get_children())  # Xóa dữ liệu hiện có
            for (book_id, book_name, author_id, genre_id, publisher_id, year) in cursor:
                self.book_table.insert('', 'end', values=(book_id, book_name, author_id, genre_id, publisher_id, year))

        except mysql.connector.Error as err:
            print(f"Lỗi khi tìm kiếm sách: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def reset_search(self):
        """Đặt lại tìm kiếm và nạp lại dữ liệu."""
        self.search_name_entry.delete(0, tk.END)
        self.load_book_data()
