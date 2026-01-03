import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import threading
import time

class PriceMonitorTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Price Monitor Tool - by Dumok Data Lab")
        self.root.geometry("1100x800")
        self.root.configure(bg='#0d1b2a')
        
        # 스타일
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#0d1b2a', foreground='white')
        style.configure('TLabel', background='#0d1b2a', foreground='white', font=('Arial', 10))
        
        self.monitors = []
        self.monitoring = False
        self.monitor_thread = None
        
        self.create_widgets()
        self.load_monitors()
        
    def create_widgets(self):
        # 헤더
        header = tk.Frame(self.root, bg='#1b263b', pady=20)
        header.pack(fill='x')
        
        title = ttk.Label(header, text="💰 Website Price Monitor", style='Title.TLabel')
        title.pack()
        
        subtitle = ttk.Label(header, text="Track prices and get notified when they drop",
                           font=('Arial', 10))
        subtitle.pack()
        
        # 메인 컨테이너
        main_frame = tk.Frame(self.root, bg='#0d1b2a', padx=25, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # 좌측: 모니터 추가
        left_frame = tk.Frame(main_frame, bg='#0d1b2a')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # 새 모니터 추가
        add_section = tk.LabelFrame(left_frame, text=" ➕ Add New Monitor ",
                                    bg='#1b263b', fg='white', font=('Arial', 11, 'bold'),
                                    padx=15, pady=15)
        add_section.pack(fill='x', pady=(0, 15))
        
        ttk.Label(add_section, text="Product Name:").pack(anchor='w', pady=(0, 5))
        self.name_entry = tk.Entry(add_section, font=('Arial', 10),
                                   bg='#415a77', fg='white', relief='flat',
                                   insertbackground='white')
        self.name_entry.pack(fill='x', ipady=6, pady=(0, 10))
        
        ttk.Label(add_section, text="Product URL:").pack(anchor='w', pady=(0, 5))
        self.url_entry = tk.Entry(add_section, font=('Arial', 10),
                                  bg='#415a77', fg='white', relief='flat',
                                  insertbackground='white')
        self.url_entry.pack(fill='x', ipady=6, pady=(0, 10))
        
        ttk.Label(add_section, text="Price CSS Selector:").pack(anchor='w', pady=(0, 5))
        self.selector_entry = tk.Entry(add_section, font=('Arial', 10),
                                      bg='#415a77', fg='white', relief='flat',
                                      insertbackground='white')
        self.selector_entry.pack(fill='x', ipady=6, pady=(0, 10))
        self.selector_entry.insert(0, ".price")
        
        ttk.Label(add_section, text="Alert When Price Below:").pack(anchor='w', pady=(0, 5))
        self.target_entry = tk.Entry(add_section, font=('Arial', 10),
                                    bg='#415a77', fg='white', relief='flat',
                                    insertbackground='white')
        self.target_entry.pack(fill='x', ipady=6, pady=(0, 10))
        
        add_btn = tk.Button(add_section, text="➕ Add Monitor", command=self.add_monitor,
                          bg='#e63946', fg='white', font=('Arial', 10, 'bold'),
                          relief='flat', pady=10, cursor='hand2')
        add_btn.pack(fill='x')
        
        # 모니터 리스트
        list_section = tk.LabelFrame(left_frame, text=" 📋 Active Monitors ",
                                     bg='#1b263b', fg='white', font=('Arial', 11, 'bold'),
                                     padx=15, pady=15)
        list_section.pack(fill='both', expand=True)
        
        # 트리뷰
        columns = ('name', 'current', 'target', 'status')
        self.tree = ttk.Treeview(list_section, columns=columns, show='headings', height=10)
        
        self.tree.heading('name', text='Product')
        self.tree.heading('current', text='Current Price')
        self.tree.heading('target', text='Target Price')
        self.tree.heading('status', text='Status')
        
        self.tree.column('name', width=200)
        self.tree.column('current', width=100, anchor='center')
        self.tree.column('target', width=100, anchor='center')
        self.tree.column('status', width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(list_section, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        btn_frame = tk.Frame(list_section, bg='#1b263b')
        btn_frame.pack(fill='x', pady=(10, 0))
        
        self.remove_btn = tk.Button(btn_frame, text="🗑️ Remove Selected",
                                    command=self.remove_monitor,
                                    bg='#415a77', fg='white', font=('Arial', 9),
                                    relief='flat', pady=6, cursor='hand2')
        self.remove_btn.pack(side='left', padx=(0, 10))
        
        self.check_btn = tk.Button(btn_frame, text="🔍 Check Now",
                                   command=self.check_now,
                                   bg='#457b9d', fg='white', font=('Arial', 9),
                                   relief='flat', pady=6, cursor='hand2')
        self.check_btn.pack(side='left')
        
        # 우측: 제어 및 로그
        right_frame = tk.Frame(main_frame, bg='#0d1b2a', width=400)
        right_frame.pack(side='right', fill='both')
        right_frame.pack_propagate(False)
        
        # 모니터링 제어
        control_section = tk.LabelFrame(right_frame, text=" 🎮 Control ",
                                       bg='#1b263b', fg='white', font=('Arial', 11, 'bold'),
                                       padx=15, pady=15)
        control_section.pack(fill='x', pady=(0, 15))
        
        ttk.Label(control_section, text="Check Interval (minutes):").pack(anchor='w', pady=(0, 5))
        
        self.interval_var = tk.IntVar(value=5)
        interval_frame = tk.Frame(control_section, bg='#1b263b')
        interval_frame.pack(fill='x', pady=(0, 15))
        
        tk.Radiobutton(interval_frame, text="5 min", variable=self.interval_var, value=5,
                      bg='#1b263b', fg='white', selectcolor='#415a77',
                      font=('Arial', 9), activebackground='#1b263b').pack(side='left', padx=(0, 10))
        
        tk.Radiobutton(interval_frame, text="15 min", variable=self.interval_var, value=15,
                      bg='#1b263b', fg='white', selectcolor='#415a77',
                      font=('Arial', 9), activebackground='#1b263b').pack(side='left', padx=(0, 10))
        
        tk.Radiobutton(interval_frame, text="60 min", variable=self.interval_var, value=60,
                      bg='#1b263b', fg='white', selectcolor='#415a77',
                      font=('Arial', 9), activebackground='#1b263b').pack(side='left')
        
        self.start_btn = tk.Button(control_section, text="▶️ Start Monitoring",
                                   command=self.start_monitoring,
                                   bg='#06d6a0', fg='#0d1b2a', font=('Arial', 12, 'bold'),
                                   relief='flat', pady=12, cursor='hand2')
        self.start_btn.pack(fill='x')
        
        self.stop_btn = tk.Button(control_section, text="⏸️ Stop Monitoring",
                                  command=self.stop_monitoring,
                                  bg='#ef476f', fg='white', font=('Arial', 12, 'bold'),
                                  relief='flat', pady=12, cursor='hand2',
                                  state='disabled')
        self.stop_btn.pack(fill='x', pady=(10, 0))
        
        self.status_label = ttk.Label(control_section, text="● Idle",
                                     font=('Arial', 11, 'bold'), foreground='#778da9')
        self.status_label.pack(pady=(15, 0))
        
        # 활동 로그
        log_section = tk.LabelFrame(right_frame, text=" 📝 Activity Log ",
                                   bg='#1b263b', fg='white', font=('Arial', 11, 'bold'),
                                   padx=10, pady=10)
        log_section.pack(fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_section, font=('Consolas', 9),
                                                  bg='#415a77', fg='white',
                                                  relief='flat')
        self.log_text.pack(fill='both', expand=True)
        self.log("Price Monitor Tool initialized")
        self.log("Add products to start monitoring")
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def add_monitor(self):
        name = self.name_entry.get().strip()
        url = self.url_entry.get().strip()
        selector = self.selector_entry.get().strip()
        target = self.target_entry.get().strip()
        
        if not all([name, url, selector, target]):
            messagebox.showwarning("Missing Info", "Please fill all fields")
            return
        
        try:
            target_price = float(target)
        except:
            messagebox.showerror("Invalid Input", "Target price must be a number")
            return
        
        monitor = {
            'id': str(int(time.time() * 1000)),
            'name': name,
            'url': url,
            'selector': selector,
            'target_price': target_price,
            'current_price': None,
            'last_check': None,
            'status': 'Pending'
        }
        
        self.monitors.append(monitor)
        self.update_tree()
        self.save_monitors()
        
        self.log(f"Added monitor: {name}")
        
        # 입력 필드 초기화
        self.name_entry.delete(0, tk.END)
        self.url_entry.delete(0, tk.END)
        self.target_entry.delete(0, tk.END)
        
    def remove_monitor(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a monitor to remove")
            return
        
        item = self.tree.item(selection[0])
        name = item['values'][0]
        
        self.monitors = [m for m in self.monitors if m['name'] != name]
        self.update_tree()
        self.save_monitors()
        self.log(f"Removed monitor: {name}")
        
    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for monitor in self.monitors:
            current = f"${monitor['current_price']:.2f}" if monitor['current_price'] else "N/A"
            target = f"${monitor['target_price']:.2f}"
            
            self.tree.insert('', 'end', values=(
                monitor['name'],
                current,
                target,
                monitor['status']
            ))
    
    def check_prices(self, single=False):
        for monitor in self.monitors:
            try:
                self.log(f"Checking {monitor['name']}...")
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(monitor['url'], headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                price_elem = soup.select_one(monitor['selector'])
                
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # 숫자 추출
                    price_match = re.search(r'[\d,]+\.?\d*', price_text)
                    
                    if price_match:
                        price = float(price_match.group().replace(',', ''))
                        monitor['current_price'] = price
                        monitor['last_check'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        if price <= monitor['target_price']:
                            monitor['status'] = '🎯 TARGET!'
                            self.log(f"✅ {monitor['name']}: ${price:.2f} (TARGET REACHED!)")
                            self.show_alert(monitor)
                        else:
                            monitor['status'] = '👀 Watching'
                            self.log(f"  Current: ${price:.2f}")
                    else:
                        monitor['status'] = '⚠️ Error'
                        self.log(f"  Could not parse price")
                else:
                    monitor['status'] = '❌ Not Found'
                    self.log(f"  Element not found")
                    
            except Exception as e:
                monitor['status'] = '❌ Error'
                self.log(f"  Error: {str(e)}")
        
        self.root.after(0, self.update_tree)
        self.save_monitors()
        
        if single:
            self.log("Manual check completed")
    
    def check_now(self):
        if not self.monitors:
            messagebox.showinfo("No Monitors", "Add monitors first")
            return
        
        thread = threading.Thread(target=lambda: self.check_prices(single=True))
        thread.daemon = True
        thread.start()
    
    def start_monitoring(self):
        if not self.monitors:
            messagebox.showinfo("No Monitors", "Add monitors first")
            return
        
        self.monitoring = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_label.config(text="● Monitoring", foreground='#06d6a0')
        
        self.log("=" * 40)
        self.log("Monitoring started")
        
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        self.monitoring = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="● Idle", foreground='#778da9')
        self.log("Monitoring stopped")
        self.log("=" * 40)
    
    def monitor_loop(self):
        while self.monitoring:
            self.check_prices()
            
            interval = self.interval_var.get() * 60
            for i in range(interval):
                if not self.monitoring:
                    break
                time.sleep(1)
    
    def show_alert(self, monitor):
        self.root.after(0, lambda: messagebox.showinfo(
            "Price Alert!",
            f"🎯 Target price reached!\n\n"
            f"Product: {monitor['name']}\n"
            f"Current: ${monitor['current_price']:.2f}\n"
            f"Target: ${monitor['target_price']:.2f}\n\n"
            f"URL: {monitor['url']}"
        ))
    
    def save_monitors(self):
        try:
            with open('price_monitors.json', 'w') as f:
                json.dump(self.monitors, f, indent=2)
        except:
            pass
    
    def load_monitors(self):
        try:
            with open('price_monitors.json', 'r') as f:
                self.monitors = json.load(f)
            self.update_tree()
            self.log(f"Loaded {len(self.monitors)} saved monitors")
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PriceMonitorTool(root)
    root.mainloop()