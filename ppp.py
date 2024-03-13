import os
from docx import Document
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def count_lines(file_path):
    """Berilgan fayldagi qatorlar sonini hisoblash."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)

def scan_directory(directory_path):
    """Berilgan direktoriyadagi fayllarning hajmini va qatorlar sonini hisoblash."""
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

        return file_stats, bat_files
    except Exception as e:
        print(f"Xato ro'y berdi: {e}")
        return [], []

def main():
    root = tk.Tk()
    root.title("Fayl Statistikasi va .bat Faylni O'chirish")

    def scan_and_display_results(directory_path):
        """Papka skanini amalga oshirish va natijalarni korsatish."""
        directory_stats, bat_files = scan_directory(directory_path)
        display_results(directory_stats)
        display_bat_files(bat_files)

    def choose_directory():
        """Foydalanuvchi katalogni tanlash uchun funksiya."""
        directory_path = filedialog.askdirectory()
        if directory_path:
            # Papka yo'lini korsatish
            result_text.config(state='normal')
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Papka yo'li: {directory_path}\n")
            result_text.config(state='disabled')

            # Skaner tugmasini faollashtirish va skan qilish
            scan_and_display_results(directory_path)

    def display_results(directory_stats):
        """Fayl statistikasini korsatish."""
        result_text.config(state='normal')
        result_text.delete(1.0, tk.END)
        if directory_stats:
            for file_name, size, num_lines in directory_stats:
                result_text.insert(tk.END, f"{file_name} - Hajmi: {size} bayt, Qatorlar soni: {num_lines}\n")
        else:
            result_text.insert(tk.END, "Katalogda fayl topilmadi yoki xatolik yuz berdi.")
        result_text.config(state='disabled')

    def display_bat_files(bat_files):
        """Bat fayllarini korsatish."""
        if bat_files:
            messagebox.showinfo("Bat Fayllari", "\n".join(bat_files))
        else:
            messagebox.showinfo("Bat Fayllari", "Bat fayllari topilmadi.")

    # Interfeys oynasi yaratish
    label = tk.Label(root, text="Papka tanlash:")
    label.pack(pady=10)

    browse_button = tk.Button(root, text="Papka tanlash", command=choose_directory)
    browse_button.pack(pady=5)

    result_text = tk.Text(root, height=30, width=80, bg='grey', fg='white')
    result_text.pack(pady=15)
    result_text.config(state='disabled')

    # Yangi label va button qo'shish
    info_label = tk.Label(root, text="Natijalarni ko'rish uchun papka tanlanganidan so'ng skan tugmasini bosing.")
    info_label.pack(pady=5)

    scan_button = tk.Button(root, text="Skan qilish", command=lambda: scan_and_display_results(directory_path))
    scan_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
