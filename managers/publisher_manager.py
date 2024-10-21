import tkinter as tk
from tkinter import ttk
import mysql.connector

class PublisherApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_publisher_list(self)
        self.create_publisher_info(self)

    def create_publisher_list(self, parent):
        title = tk.Label(parent, text="QUẢN LÝ NHÀ XUẤT BẢN", font=("Arial", 16, "bold"), fg="blue", bg="white")
        title.pack(pady=10)

        # Frame chứa bảng danh sách
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", padx=20)

        # Tạo bảng Nhà xuất bản
        columns = ("Mã NXB", "Tên NXB", "Địa chỉ", "Email", "Người đại diện")
        self.publisher_table = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)

        # Cấu hình tiêu đề và độ rộng cột
        for col in columns:
            self.publisher_table.heading(col, text=col)
            self.publisher_table.column(col, anchor="center", width=150)

        # Nạp dữ liệu từ MySQL
        self.load_publisher_data()

        self.publisher_table.pack(side="left", fill="both")

        # Thêm thanh cuộn dọc cho bảng
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.publisher_table.yview)
        self.publisher_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.publisher_table.bind('<<TreeviewSelect>>', self.on_publisher_select)

    def load_publisher_data(self):
        """Nạp dữ liệu nhà xuất bản từ MySQL."""
        try:
            connection = mysql.connector.connect(
                host='localhost',      
                user='root',          
                password='111111', 
                database='qlthuvien'  
            )

            cursor = connection.cursor()
            cursor.execute("SELECT MaNXB, TenNXB, DiaChi, Email, NguoiDaiDien FROM NhaXuatBan")

            # Xóa dữ liệu hiện tại trong bảng
            self.publisher_table.delete(*self.publisher_table.get_children())

            # Chèn dữ liệu mới
            for (pub_id, pub_name, address, email, rep) in cursor:
                self.publisher_table.insert('', 'end', values=(pub_id, pub_name, address, email, rep))

        except mysql.connector.Error as err:
            print(f"Lỗi khi kết nối MySQL: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def on_publisher_select(self, event):
        """Xử lý sự kiện khi chọn một nhà xuất bản trong bảng."""
        selected_item = self.publisher_table.selection()
        if selected_item:
            publisher_data = self.publisher_table.item(selected_item, 'values')
            self.publisher_code_entry.delete(0, tk.END)
            self.publisher_code_entry.insert(0, publisher_data[0])
            self.publisher_name_entry.delete(0, tk.END)
            self.publisher_name_entry.insert(0, publisher_data[1])
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, publisher_data[2])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, publisher_data[3])
            self.rep_entry.delete(0, tk.END)
            self.rep_entry.insert(0, publisher_data[4])

    def create_publisher_info(self, parent):
        info_frame = tk.Frame(parent)
        info_frame.pack(side="right", padx=20, pady=10)

        info_label = tk.Label(info_frame, text="THÔNG TIN NHÀ XUẤT BẢN", font=("Arial", 12, "bold"))
        info_label.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(info_frame, text="Mã NXB:").grid(row=1, column=0, sticky="e")
        self.publisher_code_entry = tk.Entry(info_frame)
        self.publisher_code_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Tên NXB:").grid(row=2, column=0, sticky="e")
        self.publisher_name_entry = tk.Entry(info_frame)
        self.publisher_name_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Địa chỉ:").grid(row=3, column=0, sticky="e")
        self.address_entry = tk.Entry(info_frame)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Email:").grid(row=4, column=0, sticky="e")
        self.email_entry = tk.Entry(info_frame)
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(info_frame, text="Người đại diện:").grid(row=5, column=0, sticky="e")
        self.rep_entry = tk.Entry(info_frame)
        self.rep_entry.grid(row=5, column=1, padx=10, pady=5)

        # Nút chức năng
        btn_frame = tk.Frame(info_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)

        add_button = tk.Button(btn_frame, text="THÊM", width=8, command=self.add_publisher)
        add_button.grid(row=0, column=0, padx=5)

        save_button = tk.Button(btn_frame, text="CẬP NHẬT", width=8, command=self.update_publisher)
        save_button.grid(row=0, column=1, padx=5)

        delete_button = tk.Button(btn_frame, text="XÓA", width=8, command=self.delete_publisher)
        delete_button.grid(row=0, column=2, padx=5)

        reset_button = tk.Button(btn_frame, text="RESET", width=8, command=self.reset_entries)
        reset_button.grid(row=0, column=3, padx=5)

        # Phần tìm kiếm
        search_label = tk.Label(info_frame, text="TÌM KIẾM", font=("Arial", 12, "bold"))
        search_label.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Label(info_frame, text="Tên NXB:").grid(row=8, column=0, sticky="e")
        self.search_name_entry = tk.Entry(info_frame)
        self.search_name_entry.grid(row=8, column=1, padx=10, pady=5)

        search_button = tk.Button(info_frame, text="TÌM KIẾM", width=10, command=self.search_publisher)
        search_button.grid(row=9, column=0, columnspan=2, pady=5)

        cancel_button = tk.Button(info_frame, text="HỦY TÌM KIẾM", width=10, command=self.reset_search)
        cancel_button.grid(row=10, column=0, columnspan=2, pady=5)

    def add_publisher(self):
        """Thêm nhà xuất bản mới vào cơ sở dữ liệu."""
        pub_id = self.publisher_code_entry.get()
        pub_name = self.publisher_name_entry.get()
        address = self.address_entry.get()
        email = self.email_entry.get()
        rep = self.rep_entry.get()

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='111111',
                database='qlthuvien'
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO NhaXuatBan (MaNXB, TenNXB, DiaChi, Email, NguoiDaiDien) VALUES (%s, %s, %s, %s, %s)", 
                           (pub_id, pub_name, address, email, rep))
            connection.commit()

            # Xóa bảng cũ và nạp lại dữ liệu sau khi thêm
            self.load_publisher_data()
            self.reset_entries()
        except mysql.connector.Error as err:
            print(f"Lỗi khi thêm nhà xuất bản: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def update_publisher(self):
        """Cập nhật thông tin nhà xuất bản đã chọn."""
        selected_item = self.publisher_table.selection()
        if not selected_item:
            return  # Không có nhà xuất bản nào được chọn

        pub_id = self.publisher_code_entry.get()
        pub_name = self.publisher_name_entry.get()
        address = self.address_entry.get()
        email = self.email_entry.get()
        rep = self.rep_entry.get()

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='111111',
                database='qlthuvien'
            )
            cursor = connection.cursor()
            cursor.execute("UPDATE NhaXuatBan SET TenNXB=%s, DiaChi=%s, Email=%s, NguoiDaiDien=%s WHERE MaNXB=%s", 
                           (pub_name, address, email, rep, pub_id))
            connection.commit()

            # Xóa bảng cũ và nạp
            # Xóa bảng cũ và nạp lại dữ liệu sau khi cập nhật
            self.load_publisher_data()
            self.reset_entries()
        except mysql.connector.Error as err:
            print(f"Lỗi khi cập nhật nhà xuất bản: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def delete_publisher(self):
        """Xóa nhà xuất bản đã chọn khỏi cơ sở dữ liệu."""
        selected_item = self.publisher_table.selection()
        if not selected_item:
            return  # Không có nhà xuất bản nào được chọn

        pub_id = self.publisher_table.item(selected_item, 'values')[0]

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='111111',
                database='qlthuvien'
            )
            cursor = connection.cursor()
            cursor.execute("DELETE FROM NhaXuatBan WHERE MaNXB=%s", (pub_id,))
            connection.commit()

            # Xóa bảng cũ và nạp lại dữ liệu sau khi xóa
            self.load_publisher_data()
            self.reset_entries()
        except mysql.connector.Error as err:
            print(f"Lỗi khi xóa nhà xuất bản: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def reset_entries(self):
        """Đặt lại các trường nhập liệu."""
        self.publisher_code_entry.delete(0, tk.END)
        self.publisher_name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.rep_entry.delete(0, tk.END)

    def search_publisher(self):
        """Tìm kiếm nhà xuất bản theo tên."""
        search_name = self.search_name_entry.get()
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='111111',
                database='qlthuvien'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT MaNXB, TenNXB, DiaChi, Email, NguoiDaiDien FROM NhaXuatBan WHERE TenNXB LIKE %s", 
                           ('%' + search_name + '%',))

            self.publisher_table.delete(*self.publisher_table.get_children())  # Xóa dữ liệu hiện có
            for (pub_id, pub_name, address, email, rep) in cursor:
                self.publisher_table.insert('', 'end', values=(pub_id, pub_name, address, email, rep))

        except mysql.connector.Error as err:
            print(f"Lỗi khi tìm kiếm nhà xuất bản: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def reset_search(self):
        """Đặt lại tìm kiếm và nạp lại dữ liệu."""
        self.search_name_entry.delete(0, tk.END)
        self.load_publisher_data()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý Nhà xuất bản")
    app = PublisherApp(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
