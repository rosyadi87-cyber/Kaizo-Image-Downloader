import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
from bs4 import BeautifulSoup, SoupStrainer
import os
import threading
from concurrent.futures import ThreadPoolExecutor
import time
from pathlib import Path
import subprocess
import sys

THEMES = {
    "Dark Soft": {
        "bg_main": "#1e1e1e", "bg_panel": "#252526", "fg_text": "#e0e0e0", "fg_sub": "#aaaaaa",
        "accent": "#007acc", "accent_hover": "#0098ff", "success": "#4caf50", "error": "#f44336",
        "warning": "#ff9800", "info": "#b388ff", "input_bg": "#3c3c3c", "input_fg": "#ffffff", "caret": "white"
    },
    "Light Pro": {
        "bg_main": "#ffffff", "bg_panel": "#f3f3f3", "fg_text": "#333333", "fg_sub": "#666666",
        "accent": "#0078d7", "accent_hover": "#42a5f5", "success": "#2e7d32", "error": "#d32f2f",
        "warning": "#ef6c00", "info": "#7b1fa2", "input_bg": "#ffffff", "input_fg": "#000000", "caret": "black"
    },
    "Ocean Breeze": {
        "bg_main": "#e0f7fa", "bg_panel": "#b2ebf2", "fg_text": "#006064", "fg_sub": "#00838f",
        "accent": "#00bcd4", "accent_hover": "#26c6da", "success": "#00695c", "error": "#c62828",
        "warning": "#ff8f00", "info": "#7e57c2", "input_bg": "#e0f2f1", "input_fg": "#004d40", "caret": "black"
    },
    "Matrix": {
        "bg_main": "#000000", "bg_panel": "#0d0d0d", "fg_text": "#00ff41", "fg_sub": "#008f11",
        "accent": "#003b00", "accent_hover": "#005500", "success": "#00ff41", "error": "#ff0000",
        "warning": "#ffff00", "info": "#00ff41", "input_bg": "#001a00", "input_fg": "#00ff41", "caret": "#00ff41"
    },
    "Midnight Blue": {
        "bg_main": "#0f172a", "bg_panel": "#1e293b", "fg_text": "#e2e8f0", "fg_sub": "#94a3b8",
        "accent": "#38bdf8", "accent_hover": "#7dd3fc", "success": "#22c55e", "error": "#ef4444",
        "warning": "#f59e0b", "info": "#a78bfa", "input_bg": "#334155", "input_fg": "#f8fafc", "caret": "white"
    }
}

LANG = {
    "ID": {
        "title": "Kaizo Image Downloader",
        "lbl_input": "DAFTAR LINK:",
        "lbl_folder": "LOKASI PENYIMPANAN:",
        "lbl_thread": "KONEKSI:",
        "lbl_theme": "TEMA:",
        "btn_load": "📂 Load File .txt",
        "btn_change": "Ubah",
        "btn_open": "Buka",
        "btn_start": "MULAI DOWNLOAD",
        "btn_stop": "BERHENTI",
        "col_url": "URL",
        "col_stat": "Status",
        "col_file": "Nama File",
        "stat_wait": "Antrian",
        "stat_ok": "Selesai",
        "stat_fail": "Gagal",
        "stat_skip": "Skip",
        "stat_conn": "Koneksi...",
        "msg_done": "Selesai!",
        "msg_err": "Dibatalkan user.",
        "msg_empty": "Link kosong!",
        "dash_total": "TOTAL",
        "dash_done": "SUKSES",
        "dash_err": "GAGAL",
        "dash_size": "UKURAN",
        "dash_spd": "SPEED",
        "dash_dur": "DURASI",
    },
    "EN": {
        "title": "Kaizo Image Downloader",
        "lbl_input": "LINK LIST:",
        "lbl_folder": "SAVE LOCATION:",
        "lbl_thread": "CONNECTIONS:",
        "lbl_theme": "THEME:",
        "btn_load": "📂 Load .txt File",
        "btn_change": "Change",
        "btn_open": "Open",
        "btn_start": "START DOWNLOAD",
        "btn_stop": "STOP PROCESS",
        "col_url": "URL",
        "col_stat": "Status",
        "col_file": "Filename",
        "stat_wait": "Queued",
        "stat_ok": "Done",
        "stat_fail": "Failed",
        "stat_skip": "Skip",
        "stat_conn": "Connect...",
        "msg_done": "Completed!",
        "msg_err": "Stopped by user.",
        "msg_empty": "List is empty!",
        "dash_total": "TOTAL",
        "dash_done": "DONE",
        "dash_err": "ERROR",
        "dash_size": "SIZE",
        "dash_spd": "SPEED",
        "dash_dur": "TIME",
    }
}

class UniversalDownloader:
    def __init__(self, root):
        self.root = root
        self.current_lang = "EN"
        self.current_theme_name = "Ocean Breeze"
        self.colors = THEMES[self.current_theme_name]
        
        self.root.title("Kaizo Image Downloader")
        self.root.geometry("1250x670")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.is_running = False
        self.save_path = tk.StringVar(value=self.get_default_path())
        self.thread_count = tk.IntVar(value=8)
        self.total_size_bytes = 0
        self.download_speed_bytes = 0 
        self.start_time = 0
        
        self.stats = {
            "total": tk.StringVar(value="0"),
            "done": tk.StringVar(value="0"),
            "error": tk.StringVar(value="0"),
            "size": tk.StringVar(value="0 MB"),
            "speed": tk.StringVar(value="0 KB/s"),
            "duration": tk.StringVar(value="00:00:00"),
        }

        self.setup_layout()
        self.apply_theme(self.current_theme_name)
        self.check_all_connections()

    def get_default_path(self):
        path = os.path.join(Path.home(), "Downloads", "Image Downloader")
        if not os.path.exists(path):
            try: os.makedirs(path)
            except: pass
        return path

    def setup_layout(self):
        self.sidebar = tk.Frame(self.root, width=350, padx=15, pady=15)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_area = tk.Frame(self.root, padx=20, pady=20)
        self.main_area.pack(side="right", fill="both", expand=True)

        self.lbl_logo = tk.Label(self.sidebar, text="⬇ Kaizo Image Downloader", font=("Segoe UI Black", 14))
        self.lbl_logo.pack(anchor="w")
        self.lbl_ver = tk.Label(self.sidebar, text="Image Downloader For imgbox, imagebam, ibb & postimg", font=("Segoe UI", 9))
        self.lbl_ver.pack(anchor="w", pady=(0, 20))

        self.create_label_header(self.sidebar, "lbl_input")
        self.text_area = tk.Text(self.sidebar, height=8, borderwidth=0, font=("Consolas", 9))
        self.text_area.pack(fill="x", pady=(5, 5))
        self.btn_load = self.create_button(self.sidebar, "btn_load", self.load_file)
        self.btn_load.pack(fill="x", pady=(0, 15))

        self.create_label_header(self.sidebar, "lbl_folder")
        self.entry_path = tk.Entry(self.sidebar, textvariable=self.save_path, state="readonly", borderwidth=0)
        self.entry_path.pack(fill="x", pady=(5, 5), ipady=3)
        self.frame_path_btns = tk.Frame(self.sidebar)
        self.frame_path_btns.pack(fill="x", pady=(0, 15))
        self.btn_change = self.create_button(self.frame_path_btns, "btn_change", self.change_directory, width=10)
        self.btn_change.pack(side="left", padx=(0, 5))
        self.btn_open = self.create_button(self.frame_path_btns, "btn_open", self.open_current_folder, width=10)
        self.btn_open.pack(side="left")

        self.create_label_header(self.sidebar, "lbl_thread")
        self.frame_threads = tk.Frame(self.sidebar)
        self.frame_threads.pack(fill="x", pady=5)
        self.spin_thread = tk.Spinbox(self.frame_threads, from_=1, to=50, textvariable=self.thread_count, width=5)
        self.spin_thread.pack(side="left")
        self.lbl_max = tk.Label(self.frame_threads, text="(Max 50)", font=("Segoe UI", 8))
        self.lbl_max.pack(side="left", padx=5)

        self.create_label_header(self.sidebar, "lbl_theme")
        self.theme_var = tk.StringVar(value=self.current_theme_name)
        self.combo_theme = ttk.Combobox(self.sidebar, textvariable=self.theme_var, values=list(THEMES.keys()), state="readonly")
        self.combo_theme.pack(fill="x", pady=5)
        self.combo_theme.bind("<<ComboboxSelected>>", lambda e: self.apply_theme(self.theme_var.get()))

        self.lbl_stat_head = tk.Label(self.sidebar, text="SERVER STATUS", font=("Segoe UI", 8, "bold"))
        self.lbl_stat_head.pack(anchor="w", pady=(5, 5))
        self.frame_status = tk.Frame(self.sidebar)
        self.frame_status.pack(fill="x")
        self.stat_lbl_net = self.create_status_dot(self.frame_status, "Internet", 0, 0)
        self.stat_lbl_post = self.create_status_dot(self.frame_status, "PostImg", 0, 1)
        self.stat_lbl_box = self.create_status_dot(self.frame_status, "ImgBox", 1, 0)
        self.stat_lbl_ibb = self.create_status_dot(self.frame_status, "Ibb.co", 1, 1)
        self.stat_lbl_bam = self.create_status_dot(self.frame_status, "ImageBam", 0, 2)

        self.btn_action = tk.Button(self.sidebar, text="MULAI DOWNLOAD", command=self.toggle_process, 
                                    font=("Segoe UI", 11, "bold"), relief="flat", pady=10, cursor="hand2")
        self.btn_action.pack(side="bottom", fill="x", pady=10)
        self.btn_lang = tk.Button(self.sidebar, text="EN / ID", command=self.toggle_language, relief="flat", font=("Segoe UI", 8))
        self.btn_lang.pack(side="bottom")

        self.frame_dash = tk.Frame(self.main_area)
        self.frame_dash.pack(fill="x", pady=(0, 20))
        
        self.card_total = self.create_dashboard_card(self.frame_dash, "dash_total", self.stats["total"])
        self.card_done = self.create_dashboard_card(self.frame_dash, "dash_done", self.stats["done"])
        self.card_err = self.create_dashboard_card(self.frame_dash, "dash_err", self.stats["error"])
        self.card_size = self.create_dashboard_card(self.frame_dash, "dash_size", self.stats["size"])
        self.card_spd = self.create_dashboard_card(self.frame_dash, "dash_spd", self.stats["speed"])
        self.card_dur = self.create_dashboard_card(self.frame_dash, "dash_dur", self.stats["duration"])

        frame_table = tk.Frame(self.main_area)
        frame_table.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(frame_table, columns=("url", "status", "file"), show="headings", style="Treeview")
        self.tree.heading("url", text="URL")
        self.tree.heading("status", text="STATUS")
        self.tree.heading("file", text="FILENAME")
        self.tree.column("url", width=350)
        self.tree.column("status", width=150)
        self.tree.column("file", width=200)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.progress = ttk.Progressbar(self.main_area, mode="determinate", style="Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(15, 0))
        
        self.update_text_language()

    def apply_theme(self, theme_name):
        self.current_theme_name = theme_name
        c = THEMES[theme_name]
        self.colors = c
        
        self.root.configure(bg=c["bg_main"])
        self.sidebar.configure(bg=c["bg_panel"])
        self.main_area.configure(bg=c["bg_main"])
        
        for widget in [self.lbl_logo, self.lbl_ver, self.lbl_max, self.lbl_stat_head]:
            widget.configure(bg=c["bg_panel"], fg=c["fg_text"] if widget != self.lbl_logo else c["accent"])
            if widget == self.lbl_ver or widget == self.lbl_max: widget.configure(fg=c["fg_sub"])
            
        for key in ["lbl_input", "lbl_folder", "lbl_thread", "lbl_theme"]:
            getattr(self, f"ui_{key}").configure(bg=c["bg_panel"], fg=c["fg_text"])

        for frame in [self.frame_path_btns, self.frame_threads, self.frame_status]:
            frame.configure(bg=c["bg_panel"])

        self.text_area.configure(bg=c["input_bg"], fg=c["input_fg"], insertbackground=c["caret"])
        self.entry_path.configure(bg=c["input_bg"], fg=c["input_fg"], readonlybackground=c["input_bg"])
        self.spin_thread.configure(bg=c["input_bg"], fg=c["input_fg"], buttonbackground=c["bg_panel"])

        for lbl in [self.stat_lbl_net, self.stat_lbl_post, self.stat_lbl_box, self.stat_lbl_ibb, self.stat_lbl_bam]:
             lbl.master.configure(bg=c["bg_panel"])
             lbl.configure(bg=c["bg_panel"]) 
             lbl.master.winfo_children()[1].configure(bg=c["bg_panel"], fg=c["fg_sub"])

        for btn, col_bg, col_fg in [(self.btn_load, c["input_bg"], c["fg_text"]), (self.btn_change, c["input_bg"], c["fg_text"]), (self.btn_lang, c["bg_panel"], c["fg_sub"])]:
            btn.configure(bg=col_bg, fg=col_fg)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=c["accent_hover"]))
            btn.bind("<Leave>", lambda e, b=btn, orig=col_bg: b.config(bg=orig))

        self.btn_open.configure(bg=c["accent"], fg="white")
        self.btn_open.bind("<Enter>", lambda e: self.btn_open.config(bg=c["accent_hover"]))
        self.btn_open.bind("<Leave>", lambda e: self.btn_open.config(bg=c["accent"]))
        
        if self.is_running: self.btn_action.configure(bg=c["error"])
        else: self.btn_action.configure(bg=c["success"])

        self.frame_dash.configure(bg=c["bg_main"])
        for card_tuple in [self.card_total, self.card_done, self.card_err, self.card_size, self.card_spd, self.card_dur]:
            card_frame, lbl_t, lbl_v, color_def = card_tuple
            card_frame.configure(bg=c["bg_panel"])
            lbl_t.configure(bg=c["bg_panel"], fg=c["fg_sub"])
            lbl_v.configure(bg=c["bg_panel"], fg=color_def)

        self.style.configure("Treeview", background=c["bg_main"], foreground=c["fg_text"], fieldbackground=c["bg_main"], borderwidth=0)
        self.style.configure("Treeview.Heading", background=c["bg_panel"], foreground=c["fg_text"], relief="flat")
        self.style.map("Treeview", background=[('selected', c["accent"])])
        self.style.configure("Vertical.TScrollbar", background=c["bg_panel"], troughcolor=c["bg_main"])
        self.style.configure("Horizontal.TProgressbar", background=c["success"], troughcolor=c["bg_panel"])

    def create_label_header(self, parent, text_key):
        lbl = tk.Label(parent, text=LANG[self.current_lang][text_key], font=("Segoe UI", 8, "bold"))
        lbl.pack(anchor="w")
        setattr(self, f"ui_{text_key}", lbl)

    def create_button(self, parent, text_key, cmd, width=None):
        btn = tk.Button(parent, text=LANG[self.current_lang].get(text_key, text_key), command=cmd, 
                        relief="flat", font=("Segoe UI", 9), cursor="hand2", width=width)
        setattr(self, f"ui_{text_key}", btn)
        return btn

    def create_status_dot(self, parent, name, row, col):
        f = tk.Frame(parent, padx=5, pady=2)
        f.grid(row=row, column=col, sticky="w", padx=5, pady=2)
        dot = tk.Label(f, text="●", font=("Arial", 12), fg=self.colors["input_bg"])
        dot.pack(side="left")
        lbl = tk.Label(f, text=name, font=("Segoe UI", 8))
        lbl.pack(side="left")
        return dot

    def create_dashboard_card(self, parent, title_key, var):
        c = self.colors
        if "total" in title_key: col = c["input_bg"]
        elif "done" in title_key: col = c["success"]
        elif "err" in title_key: col = c["error"]
        elif "size" in title_key: col = c["accent"]
        elif "spd" in title_key: col = c["warning"]
        else: col = c["info"]

        card = tk.Frame(parent, padx=15, pady=10)
        card.pack(side="left", fill="x", expand=True, padx=5)
        lbl_title = tk.Label(card, text=LANG[self.current_lang][title_key], font=("Segoe UI", 8))
        lbl_title.pack(anchor="w")
        lbl_val = tk.Label(card, textvariable=var, font=("Segoe UI", 16, "bold"))
        lbl_val.pack(anchor="w")
        setattr(self, f"ui_{title_key}", lbl_title)
        return (card, lbl_title, lbl_val, col)

    def update_text_language(self):
        L = LANG[self.current_lang]
        for key in ["lbl_input", "lbl_folder", "lbl_thread", "lbl_theme", "dash_total", "dash_done", "dash_err", "dash_size", "dash_spd", "dash_dur"]:
            if hasattr(self, f"ui_{key}"): getattr(self, f"ui_{key}").config(text=L[key])
        for key in ["btn_load", "btn_change", "btn_open"]:
            if hasattr(self, f"ui_{key}"): getattr(self, f"ui_{key}").config(text=L[key])
        
        if self.is_running: self.btn_action.config(text=L["btn_stop"], bg=self.colors["error"])
        else: self.btn_action.config(text=L["btn_start"], bg=self.colors["success"])

        self.tree.heading("url", text=L["col_url"])
        self.tree.heading("status", text=L["col_stat"])
        self.tree.heading("file", text=L["col_file"])

    def toggle_language(self):
        self.current_lang = "EN" if self.current_lang == "ID" else "ID"
        self.update_text_language()

    def update_status_indicator(self, label, is_online):
        color = self.colors["success"] if is_online else self.colors["error"]
        label.config(fg=color)

    def check_all_connections(self):
        targets = [("https://8.8.8.8", self.stat_lbl_net), ("https://postimg.cc", self.stat_lbl_post), ("https://imgbox.com", self.stat_lbl_box), ("https://ibb.co.com", self.stat_lbl_ibb), ("https://www.imagebam.com", self.stat_lbl_bam)]
        def _check_single(url, label):
            try:
                verify_ssl = False if url == "https://8.8.8.8" else True
                requests.head(url, timeout=5, verify=verify_ssl)
                self.root.after(0, lambda: self.update_status_indicator(label, True))
            except:
                self.root.after(0, lambda: self.update_status_indicator(label, False))
        for url, lbl in targets:
            lbl.config(fg=self.colors["warning"])
            threading.Thread(target=_check_single, args=(url, lbl), daemon=True).start()

    def change_directory(self):
        d = filedialog.askdirectory()
        if d: self.save_path.set(d)

    def open_current_folder(self):
        path = self.save_path.get()
        if os.path.isdir(path):
            try:
                if os.name == 'nt': os.startfile(path)
                else: 
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, path])
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showwarning("Info", "Folder not found.")

    def load_file(self):
        f = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if f:
            with open(f, "r") as file:
                self.text_area.insert(tk.END, file.read() + "\n")

    def toggle_process(self):
        if not self.is_running: self.start_download()
        else: self.stop_download()

    def stop_download(self):
        self.is_running = False
        self.btn_action.config(text=LANG[self.current_lang]["btn_stop"] + "...", bg=self.colors["warning"])

    def start_download(self):
        links = self.text_area.get("1.0", tk.END).strip().split('\n')
        links = [l.strip() for l in links if l.strip()]
        if not links:
            messagebox.showwarning("Warning", LANG[self.current_lang]["msg_empty"])
            return

        self.is_running = True
        self.stats["total"].set(str(len(links)))
        self.stats["done"].set("0")
        self.stats["error"].set("0")
        self.stats["speed"].set("0 KB/s")
        self.stats["size"].set("0 MB")
        self.stats["duration"].set("00:00:00")
        self.total_size_bytes = 0
        self.start_time = time.time()
        
        self.update_text_language()
        self.tree.delete(*self.tree.get_children())
        self.progress["maximum"] = len(links)
        self.progress["value"] = 0
        
        self.check_all_connections()

        items_map = {}
        for url in links:
            iid = self.tree.insert("", "end", values=(url, LANG[self.current_lang]["stat_wait"], "-"))
            items_map[iid] = url

        threading.Thread(target=self.run_workers, args=(items_map,), daemon=True).start()
        threading.Thread(target=self.speed_monitor, daemon=True).start()

    def speed_monitor(self):
        while self.is_running:
            time.sleep(1)
            speed_kb = self.download_speed_bytes / 1024
            speed_mb = speed_kb / 1024
            if speed_mb >= 1: speed_txt = f"{speed_mb:.2f} MB/s"
            else: speed_txt = f"{speed_kb:.0f} KB/s"
            self.root.after(0, lambda s=speed_txt: self.stats["speed"].set(s))
            self.download_speed_bytes = 0
            
            elapsed = int(time.time() - self.start_time)
            dur_str = time.strftime('%H:%M:%S', time.gmtime(elapsed))
            self.root.after(0, lambda d=dur_str: self.stats["duration"].set(d))

    def update_item(self, iid, status, filename="-"):
        try:
            self.tree.set(iid, "status", status)
            if filename != "-": self.tree.set(iid, "file", filename)
        except: pass

    def run_workers(self, items_map):
        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"})
        with ThreadPoolExecutor(max_workers=self.thread_count.get()) as executor:
            futures = [executor.submit(self.process_url, session, url, iid) for iid, url in items_map.items()]
            for f in futures:
                if not self.is_running: break
                f.result()
        self.is_running = False
        self.root.after(0, lambda: self.apply_theme(self.current_theme_name))
        self.root.after(0, self.finish_ui)

    def resolve_direct_link(self, session, url, iid):
        if "postimg.cc" in url:
            parse_only = SoupStrainer("a", id="download")
            resp = session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser", parse_only=parse_only)
            btn = soup.find("a", id="download")
            if btn and btn.get('href'): return btn['href']
        elif "imgbox.com" in url:
            parse_only = SoupStrainer("img", class_="image-content")
            resp = session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser", parse_only=parse_only)
            img_tag = soup.find("img", class_="image-content")
            if img_tag and img_tag.get('src'): return img_tag['src']
        elif "ibb.co" in url:
            resp = session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            btn = soup.find("a", class_="btn-download")
            if btn and btn.get('href'): return btn['href']
        elif "imagebam.com" in url:
            resp = session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            img = soup.find("img", class_="main-image")
            if img and img.get('src'): return img['src']
            anchor = soup.select_one("#continue > a")
            if anchor and anchor.get('href'):
                self.root.after(0, self.update_item, iid, LANG[self.current_lang]["stat_conn"])
                session.cookies.set('sfw_inter', '1', domain='imagebam.com')
                session.cookies.set('sfw_inter', '1', domain='www.imagebam.com')
                next_url = anchor['href']
                resp2 = session.get(next_url, timeout=10)
                soup2 = BeautifulSoup(resp2.text, "html.parser")
                img2 = soup2.find("img", class_="main-image")
                if img2 and img2.get('src'): return img2['src']
        return None

    def process_url(self, session, url, iid):
        if not self.is_running: return
        L = LANG[self.current_lang]
        folder = self.save_path.get()
        if not os.path.exists(folder): os.makedirs(folder)

        supported_domains = ["postimg.cc", "imgbox.com", "ibb.co", "imagebam.com"]
        if not any(domain in url for domain in supported_domains):
            self.root.after(0, self.update_item, iid, L["stat_skip"])
            self.root.after(0, self.increment_error)
            return

        self.root.after(0, self.update_item, iid, L["stat_conn"])
        
        for attempt in range(1, 6):
            if not self.is_running: return
            try:
                orig_url = self.resolve_direct_link(session, url, iid)
                if not orig_url: raise Exception("Link Missing")
                filename = orig_url.split('/')[-1].split('?')[0]
                if not filename: filename = f"img_{int(time.time())}.jpg"
                final_path = os.path.join(folder, filename)
                temp_path = final_path + ".tmp"

                if os.path.exists(final_path) and os.path.getsize(final_path) > 0:
                    self.root.after(0, self.update_item, iid, L["stat_ok"] + " (Exist)", filename)
                    self.root.after(0, self.increment_done)
                    return
                
                dl_headers = {}
                if "imgbox.com" in url: dl_headers["Referer"] = "https://imgbox.com/"

                with session.get(orig_url, headers=dl_headers, stream=True, timeout=30) as r:
                    r.raise_for_status()
                    total_length = r.headers.get('content-length')
                    with open(temp_path, 'wb') as f:
                        if total_length is None:
                            f.write(r.content)
                            self.total_size_bytes += len(r.content)
                        else:
                            dl = 0
                            total_length = int(total_length)
                            last_percent = 0
                            for chunk in r.iter_content(chunk_size=131072):
                                if not self.is_running:
                                    f.close()
                                    os.remove(temp_path)
                                    return
                                dl += len(chunk)
                                f.write(chunk)
                                self.total_size_bytes += len(chunk)
                                self.download_speed_bytes += len(chunk)
                                percent = int(100 * dl / total_length)
                                if percent - last_percent >= 5 or percent == 100:
                                    last_percent = percent
                                    self.root.after(0, self.update_item, iid, f"{percent}%", filename)
                if os.path.exists(final_path): os.remove(final_path)
                os.replace(temp_path, final_path)
                self.root.after(0, self.update_item, iid, L["stat_ok"], filename)
                self.root.after(0, self.increment_done)
                return
            except Exception as e:
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    try: os.remove(temp_path)
                    except: pass
                if attempt < 5:
                    self.root.after(0, self.update_item, iid, f"Retry {attempt}/5")
                    time.sleep(1.5)
                else:
                    self.root.after(0, self.update_item, iid, L["stat_fail"])
                    self.root.after(0, self.increment_error)

    def increment_done(self):
        current = int(self.stats["done"].get())
        self.stats["done"].set(str(current + 1))
        self.progress["value"] += 1
        
        total_mb = self.total_size_bytes / (1024 * 1024)
        if total_mb > 1024: self.stats["size"].set(f"{total_mb/1024:.2f} GB")
        else: self.stats["size"].set(f"{total_mb:.2f} MB")

    def increment_error(self):
        current = int(self.stats["error"].get())
        self.stats["error"].set(str(current + 1))
        self.progress["value"] += 1

    def finish_ui(self):
        self.update_text_language()
        if int(self.stats["done"].get()) + int(self.stats["error"].get()) == int(self.stats["total"].get()):
            messagebox.showinfo("Info", LANG[self.current_lang]["msg_done"])
        else:
            messagebox.showinfo("Info", LANG[self.current_lang]["msg_err"])

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalDownloader(root)
    root.mainloop()
