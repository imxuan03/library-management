import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

class BorrowReturnApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_borrow_list(self)
        self.create_borrow_info(self)

    def create_borrow_list(self, parent):
        title = tk.Label(parent, text="QUẢN LÝ MƯỢN TRẢ SÁCH", font=("Arial", 16, "bold"), fg="green", bg="white")
        title.pack(pady=10)

        # Frame chứa bảng danh sách
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", padx=20)

        # Tạo bảng Mượn trả
        columns = ("Mã Mượn", "Số Thẻ", "Mã NV", "Ngày Mượn", "Mã Sách", "Ghi Chú", "Đã Trả", "Ngày Trả")
        self.borrow_table = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)

        # Cấu hình tiêu đề và độ rộng cột
        for col in columns:
            self.borrow_table.heading(col, text=col)
            self.borrow_table.column(col, anchor="center", width=90)

        # Nạp dữ liệu từ MySQL
        self.load_borrow_data()

        self.borrow_table.pack(side="left", fill="both")

        # Thêm thanh cuộn dọc cho bảng
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.borrow_table.yview)
        self.borrow_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.borrow_table.bind('<<TreeviewSelect>>', self.on_borrow_select)

    def load_borrow_data(self):
        """Nạp dữ liệu mượn trả từ MySQL."""
        try:
            connection = mysql.connector.connect(
                host='localhost',      
                user='root',          
                password='111111', 
                database='QLThuVien'  
            )

            cursor = connection.cursor()
            cursor.execute("""
                SELECT MuonTra.MaMT, MuonTra.SoThe, MuonTra.MaNV, MuonTra.NgayMuon, CTMuonTra.MaSach, CTMuonTra.GhiChu, CTMuonTra.DaTra, CTMuonTra.NgayTra
                FROM MuonTra
                INNER JOIN CTMuonTra ON MuonTra.MaMT = CTMuonTra.MaMT
            """)

            # Xóa dữ liệu hiện tại trong bảng
            self.borrow_table.delete(*self.borrow_table.get_children())

            # Chèn dữ liệu mới
            for (borrow_id, card_id, staff_id, borrow_date, book_id, note, returned, return_date) in cursor:
                self.borrow_table.insert('', 'end', values=(borrow_id, card_id, staff_id, borrow_date, book_id, note, returned, return_date))

        except mysql.connector.Error as err:
            print(f"Lỗi khi kết nối MySQL: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def on_borrow_select(self, event):
        """Xử lý sự kiện khi chọn một phiếu mượn trả trong bảng."""
        selected_item = self.borrow_table.selection()
        if selected_item:
            borrow_data = self.borrow_table.item(selected_item, 'values')
            self.borrow_code_entry.delete(0, tk.END)
            self.borrow_code_entry.insert(0, borrow_data[0])
            self.card_code_entry.delete(0, tk.END)
            self.card_code_entry.insert(0, borrow_data[1])
            self.staff_code_entry.delete(0, tk.END)
            self.staff_code_entry.insert(0, borrow_data[2])
            self.borrow_date_entry.delete(0, tk.END)
            self.borrow_date_entry.insert(0, borrow_data[3])
            self.book_code_entry.delete(0, tk.END)
            self.book_code_entry.insert(0, borrow_data[4])
            self.note_entry.delete(0, tk.END)
            self.note_entry.insert(0, borrow_data[5])
            self.returned_var.set(borrow_data[6])
            self.return_date_entry.delete(0, tk.END)
            self.return_date_entry.insert(0, borrow_data[7])

    def create_borrow_info(self, parent):
        info_frame = tk.Frame(parent)
        info_frame.pack(side="right", padx=20, pady=10)

        info_label = tk.Label(info_frame, text="THÔNG TIN MƯỢN TRẢ", font=("Arial", 12, "bold"))
        info_label.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(info_frame, text="Mã Mượn:").grid(row=1, column=0, sticky="e")
        self.borrow_code_entry = tk.Entry(info_frame)
        self.borrow_code_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Số Thẻ:").grid(row=2, column=0, sticky="e")
        self.card_code_entry = tk.Entry(info_frame)
        self.card_code_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Mã NV:").grid(row=3, column=0, sticky="e")
        self.staff_code_entry = tk.Entry(info_frame)
        self.staff_code_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Ngày Mượn:").grid(row=4, column=0, sticky="e")
        self.borrow_date_entry = tk.Entry(info_frame)
        self.borrow_date_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Mã Sách:").grid(row=5, column=0, sticky="e")
        self.book_code_entry = tk.Entry(info_frame)
        self.book_code_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Ghi Chú:").grid(row=6, column=0, sticky="e")
        self.note_entry = tk.Entry(info_frame)
        self.note_entry.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Đã Trả:").grid(row=7, column=0, sticky="e")
        self.returned_var = tk.BooleanVar()
        self.returned_check = tk.Checkbutton(info_frame, variable=self.returned_var)
        self.returned_check.grid(row=7, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Ngày Trả:").grid(row=8, column=0, sticky="e")
        self.return_date_entry = tk.Entry(info_frame)
        self.return_date_entry.grid(row=8, column=1, padx=10, pady=5)

        # Nút chức năng
        btn_frame = tk.Frame(info_frame)
        btn_frame.grid(row=9, column=0, columnspan=2, pady=10)

        add_button = tk.Button(btn_frame, text="THÊM", width=8, command=self.add_borrow)
        add_button.grid(row=0, column=0, padx=5)

        save_button = tk.Button(btn_frame, text="LƯU", width=8, command=self.update_borrow)
        save_button.grid(row=0, column=1, padx=5)

        delete_button = tk.Button(btn_frame, text="XÓA", width=8, command=self.delete_borrow)
        delete_button.grid(row=0, column=2, padx=5)

        reset_button = tk.Button(btn_frame, text="RESET", width=8, command=self.reset_entries)
        reset_button.grid(row=0, column=3, padx=5)

    def add_borrow(self):
        """Thêm phiếu mượn mới vào cơ sở dữ liệu."""
        borrow_id = self.borrow_code_entry.get()
        card_id = self.card_code_entry.get()
        staff_id = self.staff_code_entry.get()
        borrow_date = self.borrow_date_entry.get()
        book_id = self.book_code_entry.get()
        note = self.note_entry.get()
        returned = self.returned_var.get()
        return_date = self.return_date_entry.get()

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='111111',
                database='QLThuVien'
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO MuonTra (MaMT, SoThe, MaNV, NgayMuon) VALUES (%s, %s, %s, %s)",
                           (borrow_id, card_id, staff_id, borrow_date))
            cursor.execute("INSERT INTO CTMuonTra (MaMT, MaSach, GhiChu, DaTra, NgayTra) VALUES (%s, %s, %s, %s, %s)",
                           (borrow_id, book_id, note, returned, return_date))
            connection.commit()

            # Xóa bảng cũ và nạp lại dữ liệu sau khi thêm
            self.load_borrow_data()
            self.reset_entries()
        except mysql.connector.Error as err:
            print(f"Lỗi khi thêm phiếu mượn: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def update_borrow(self):
        """Cập nhật phiếu mượn."""
        selected_item = self.borrow_table.selection()
        if not selected_item:
            return  # Không có phiếu mượn nào được chọn

        borrow_id = self.borrow_code_entry.get()
        card_id = self.card_code_entry.get()
        staff_id = self.staff_code_entry.get()
        borrow_date = self.borrow_date_entry.get()
        book_id = self.book_code_entry.get()
        note = self.note_entry.get()
        returned = self.returned_var.get()
        return_date = self.return_date_entry.get()

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='111111',
                database='QLThuVien'
            )
            cursor = connection.cursor()
            cursor.execute("UPDATE MuonTra SET SoThe=%s, MaNV=%s, NgayMuon=%s WHERE MaMT=%s",
                           (card_id, staff_id, borrow_date, borrow_id))
            cursor.execute("UPDATE CTMuonTra SET MaSach=%s, GhiChu=%s, DaTra=%s, NgayTra=%s WHERE MaMT=%s",
                           (book_id, note, returned, return_date, borrow_id))
            connection.commit()

            # Xóa bảng cũ và nạp lại dữ liệu sau khi cập nhật
            self.load_borrow_data()
            self.reset_entries()
        except mysql.connector.Error as err:
            print(f"Lỗi khi cập nhật phiếu mượn: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def delete_borrow(self):
        """Xóa phiếu mượn đã chọn khỏi cơ sở dữ liệu."""
        selected_item = self.borrow_table.selection()
        if not selected_item:
            return  # Không có phiếu mượn nào được chọn

        borrow_id = self.borrow_table.item(selected_item, 'values')[0]

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='111111',
                database='QLThuVien'
            )
            cursor = connection.cursor()
            cursor.execute("DELETE FROM CTMuonTra WHERE MaMT=%s", (borrow_id,))
            cursor.execute("DELETE FROM MuonTra WHERE MaMT=%s", (borrow_id,))
            connection.commit()

            # Xóa bảng cũ và nạp lại dữ liệu sau khi xóa
            self.load_borrow_data()
            self.reset_entries()
        except mysql.connector.Error as err:
            print(f"Lỗi khi xóa phiếu mượn: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def reset_entries(self):
        """Đặt lại các trường nhập liệu."""
        self.borrow_code_entry.delete(0, tk.END)
        self.card_code_entry.delete(0, tk.END)
        self.staff_code_entry.delete(0, tk.END)
        self.borrow_date_entry.delete(0, tk.END)
        self.book_code_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)
        self.returned_var.set(False)
        self.return_date_entry.delete(0, tk.END)
