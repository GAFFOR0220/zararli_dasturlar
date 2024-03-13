import os
from docx import Document
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def count_lines(file_path):
    """Berilgan fayldagi qatorlar sonini hisoblash."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)

def calculate_directory_stats(directory_path):
    """Direktoriyadagi barcha fayllarning hajmini va qatorlar sonini hisoblash."""
    file_stats = []
    bat_files = []  # .bat fayllarini saqlash uchun ro'yxat

    try:
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                size = os.path.getsize(file_path)
                num_lines = 0

                if file_name.endswith('.docx'):
                    doc = Document(file_path)
                    num_lines = len(doc.paragraphs)
                else:
                    num_lines = count_lines(file_path)

                file_stats.append((file_name, size, num_lines))

                # .bat fayllarini tekshirish
                if file_name.endswith('.bat'):
                    bat_files.append(file_name)

            # Katalog ichidagi papkalarni hisoblash
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                subdir_files, subdir_bat_files = calculate_directory_stats(dir_path)
                file_stats.extend(subdir_files)
                bat_files.extend(subdir_bat_files)
    except Exception as e:
        print(f"Xato ro'y berdi: {e}")
    return file_stats, bat_files

def delete_bat_file(directory_path, file_name):
    """Berilgan papka ichidagi .bat faylini o'chirish."""
    file_path = os.path.join(directory_path, file_name)
    try:
        os.remove(file_path)
        messagebox.showinfo("O'chirildi", f"{file_name} fayli o'chirildi.")
    except Exception as e:
        messagebox.showerror("Xato", f"Fayl o'chirishda xatolik yuz berdi: {e}")

def main():
    root = tk.Tk()
    root.title("Fayl Statistikasi va .bat Faylni O'chirish")

    def choose_directory():
        """Foydalanuvchi katalogni tanlash uchun funksiya."""
        directory_path = filedialog.askdirectory()
        if directory_path:
            # Katalog statistikasini hisoblash
            directory_stats, bat_files = calculate_directory_stats(directory_path)

            if directory_stats:
                # Natijalarni korsatish
                result_text.config(state='normal')
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Papka yo'li: {directory_path}\n")
                for file_name, size, num_lines in directory_stats:
                    result_text.insert(tk.END, f"{file_name} - Hajmi: {size} bayt, Qatorlar soni: {num_lines}\n")
                
                if bat_files:
                    # Agar .bat fayllari topsilgan bo'lsa
                    result_text.insert(tk.END, "\n Viruslar: ")
                    for bat_file in bat_files:
                        result_text.insert(tk.END, f"{bat_file}, ")

                    # O'chirish tugmasi
                    delete_button.config(state='normal', command=lambda: delete_bat_file(directory_path, bat_files[0]))
                else:
                    result_text.insert(tk.END, "\n .bat fayli topilmadi.")

                result_text.config(state='disabled')
            else:
                result_text.config(state='normal')
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "Katalogda fayl topilmadi yoki xatolik yuz berdi.")
                result_text.config(state='disabled')

    # Interfeys oynasi yaratish
    label = tk.Label(root, text="Papka tanlash:")
    label.pack(pady=10)

    browse_button = tk.Button(root, text="Papka tanlash", command=choose_directory)
    browse_button.pack(pady=5)

    result_text = tk.Text(root, height=30, width=50, bg='black', fg='white')
    result_text.pack(pady=15)
    result_text.config(state='disabled')
    delete_button = tk.Button(root, text=" .bat faylni o'chirish", state='disabled')
    delete_button.pack(pady=5)

    root.mainloop()

if __name__ == "main":
    main()