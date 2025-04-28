import tkinter as tk
import pyperclip
import keyboard
from tkinter import ttk, scrolledtext

class ClipboardTool:
    def __init__(self):
        self.current_index = 0
        self.parts = []
        
        # Tạo cửa sổ chính
        self.root = tk.Tk()
        self.root.title('Công cụ xử lý Clipboard')
        self.root.geometry('600x400')
        
        # Tạo vùng hiển thị thông tin
        self.log_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=15)
        self.log_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Tạo frame chứa các nút điều khiển
        control_frame = ttk.Frame(self.root)
        control_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # Tạo các nút điều khiển
        ttk.Label(control_frame, text='Phím tắt:').pack(side=tk.LEFT, padx=5)
        ttk.Label(control_frame, text='Ctrl+C - Sao chép | Ctrl+V - Dán | ESC - Thoát').pack(side=tk.LEFT, padx=5)
        
        # Hiển thị trạng thái
        self.status_label = ttk.Label(self.root, text='Sẵn sàng')
        self.status_label.pack(pady=5)
        
        # Đăng ký các phím tắt
        keyboard.add_hotkey('ctrl+c', self.on_ctrl_c)
        keyboard.on_press_key('v', self.on_ctrl_v, suppress=True)
        keyboard.add_hotkey('esc', self.on_exit)
        
        # Thêm thông tin khởi động
        self.log('Công cụ đã sẵn sàng!')
        self.log('Hãy sử dụng:')
        self.log('- Ctrl+C để sao chép và phân tích dữ liệu')
        self.log('- Ctrl+V để paste từng phần dữ liệu đã tách')
        self.log('- ESC để thoát chương trình\n')
    
    def log(self, message):
        self.log_area.insert(tk.END, message + '\n')
        self.log_area.see(tk.END)
    
    def analyze_clipboard(self):
        clipboard_data = pyperclip.paste()
        
        if clipboard_data:
            self.parts = [part.strip() for part in clipboard_data.split('|')]
            self.current_index = 0
            
            self.log(f'\nĐã nhận dữ liệu mới: {clipboard_data}')
            self.log('Đã phân tích và tách dữ liệu thành công!\n')
            self.log(f'Số phần dữ liệu: {len(self.parts)}')
            self.log('Nhấn Ctrl+V để paste từng phần.\n')
            
            self.status_label.config(text=f'Đã phân tích: {len(self.parts)} phần')
        else:
            self.log('\nKhông có dữ liệu trong clipboard.')
            self.status_label.config(text='Không có dữ liệu')
    
    def on_ctrl_c(self):
        keyboard.call_later(self.analyze_clipboard, delay=0.1)
    
    def on_ctrl_v(self, e):
        if self.parts:
            if self.current_index < len(self.parts):
                e.suppress = True
                current_data = self.parts[self.current_index]
                keyboard.write(current_data)
                
                self.log(f'Đã paste phần {self.current_index + 1}: {current_data}')
                self.status_label.config(text=f'Đã paste {self.current_index + 1}/{len(self.parts)}')
                
                self.current_index += 1
            else:
                self.log('\nĐã paste hết tất cả các phần dữ liệu!')
                self.log('Hãy sao chép dữ liệu mới (Ctrl+C) để tiếp tục.\n')
                self.current_index = 0
                self.status_label.config(text='Đã paste hết dữ liệu')
        else:
            self.log('\nChưa có dữ liệu nào được phân tích!')
            self.log('Hãy sử dụng Ctrl+C để sao chép và phân tích dữ liệu trước.\n')
            self.status_label.config(text='Chưa có dữ liệu')
    
    def on_exit(self):
        self.root.quit()
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = ClipboardTool()
    app.run()
