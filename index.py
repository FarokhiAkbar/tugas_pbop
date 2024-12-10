import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Konfigurasi koneksi ke database MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Sesuaikan dengan password MySQL Anda
    'database': 'tugas_aplikasi',
}

# Fungsi Koneksi ke Database
def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

# Fungsi untuk mengambil data dari database
def load_data():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data_user")
        rows = cursor.fetchall()
        table.delete(*table.get_children())  # Hapus data di table terlebih dahulu
        for row in rows:
            table.insert("", "end", values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")

# Fungsi untuk menambahkan data
def add_data():
    nama = entry_nama.get().strip()
    email = entry_email.get().strip()
    umur = entry_umur.get().strip()

    # Validasi input
    if not nama or not email or not umur:
        messagebox.showwarning("Peringatan", "Harap isi semua kolom!")
        return
    if not nama.isalpha():
        messagebox.showwarning("Peringatan", "Nama hanya boleh berisi huruf!")
        return
    if "@gmail.com" not in email:
        messagebox.showwarning("Peringatan", "Email harus menggunakan @gmail.com!")
        return
    if not umur.isdigit():
        messagebox.showwarning("Peringatan", "Umur hanya boleh berisi angka!")
        return

    # Periksa apakah data sudah ada
    if data_exists(nama, email):
        messagebox.showwarning("Peringatan", "Data dengan nama dan email ini sudah ada!")
        return

    # Tambah data ke database
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data_user (nama, email, umur) VALUES (%s, %s, %s)", (nama, email, umur))
        conn.commit()
        conn.close()
        load_data()
        clear_fields()
        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menambahkan data: {str(e)}")

# Fungsi untuk memperbarui data
def update_data():
    selected = table.focus()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data yang ingin diperbarui!")
        return
    id_data = table.item(selected)['values'][0]
    nama = entry_nama.get().strip()
    email = entry_email.get().strip()
    umur = entry_umur.get().strip()

    # Validasi input
    if not nama or not email or not umur:
        messagebox.showwarning("Peringatan", "Harap isi semua kolom!")
        return
    if not nama.isalpha():
        messagebox.showwarning("Peringatan", "Nama hanya boleh berisi huruf!")
        return
    if "@gmail.com" not in email:
        messagebox.showwarning("Peringatan", "Email harus menggunakan @gmail.com!")
        return
    if not umur.isdigit():
        messagebox.showwarning("Peringatan", "Umur hanya boleh berisi angka!")
        return

    # Perbarui data di database
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE data_user SET nama=%s, email=%s, umur=%s WHERE id=%s", (nama, email, umur, id_data))
        conn.commit()
        conn.close()
        load_data()
        clear_fields()
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal memperbarui data: {str(e)}")

# Fungsi untuk menghapus data
def delete_data():
    selected = table.focus()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus!")
        return
    id_data = table.item(selected)['values'][0]

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM data_user WHERE id=%s", (id_data,))
        conn.commit()
        conn.close()
        load_data()
        clear_fields()
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menghapus data: {str(e)}")
        
# Fungsi untuk memeriksa apakah data sudah ada dalam database
def data_exists(nama, email):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data_user WHERE nama=%s AND email=%s", (nama, email))
        result = cursor.fetchone()
        conn.close()
        return result is not None  # Jika ada hasil, data sudah ada
    except Exception as e:
        messagebox.showerror("Error", f"Gagal memeriksa data: {str(e)}")
        return False

# Fungsi untuk membersihkan input field
def clear_fields():
    entry_nama.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_umur.delete(0, tk.END)

# Fungsi untuk menampilkan data di field saat baris di klik
def on_row_click(event):
    selected = table.focus()
    data = table.item(selected)['values']
    if data:
        clear_fields()
        entry_nama.insert(0, data[1])
        entry_email.insert(0, data[2])
        entry_umur.insert(0, data[3])

# --- GUI ---
root = tk.Tk()
root.title("Data User")
root.geometry("700x450")
root.configure(bg="#F0F0F0")

# -- Gradient Background --
def set_gradient(bg_color1, bg_color2):
    gradient = tk.PhotoImage(width=700, height=450)
    for y in range(450):
        r = int((255 * y) / 450)
        g = int((255 * (450 - y)) / 450)
        gradient.put("#%02x%02x%02x" % (r, g, 255), (0, y))
    label = tk.Label(root, image=gradient)
    label.image = gradient  # keep a reference
    label.place(x=0, y=0)

set_gradient("#4CAF50", "#FF9800")

# Frame Input Data
frame_input = tk.Frame(root, bg="#F0F0F0", bd=2, relief="groove")
frame_input.pack(pady=20, padx=20, fill=tk.X)

tk.Label(frame_input, text="Nama:", bg="#F0F0F0").grid(row=0, column=0, padx=5, pady=5)
entry_nama = tk.Entry(frame_input, width=30)
entry_nama.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Email:", bg="#F0F0F0").grid(row=1, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_input, width=30)
entry_email.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Umur:", bg="#F0F0F0").grid(row=2, column=0, padx=5, pady=5)
entry_umur = tk.Entry(frame_input, width=30)
entry_umur.grid(row=2, column=1, padx=5, pady=5)

# Tombol CRUD
frame_buttons = tk.Frame(root, bg="#F0F0F0", bd=2, relief="groove")
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Tambah", command=add_data, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="Perbarui", command=update_data, bg="#FF9800", fg="white").grid(row=0, column=1, padx=10)
tk.Button(frame_buttons, text="Hapus", command=delete_data, bg="#F44336", fg="white").grid(row=0, column=2, padx=10)
tk.Button(frame_buttons, text="Bersihkan", command=clear_fields, bg="#9E9E9E", fg="white").grid(row=0, column=3, padx=10)

# Tabel Data
columns = ("ID", "Nama", "Email", "Umur")
table = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150)
table.pack(fill=tk.BOTH, expand=True, padx=20)

# Scrollbar for the table
scrollbar = ttk.Scrollbar(root, orient="vertical", command=table.yview)
table.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

table.bind("<ButtonRelease-1>", on_row_click)

load_data()  # Muat data awal dari database

root.mainloop()