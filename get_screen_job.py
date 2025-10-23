import time
import json
import os
import psutil
import platform
import matplotlib.pyplot as plt
import hashlib
import datetime
import add_new_activity
import win32gui
import win32process
import win32con
import win32api
import threading
import sys

# 取得今天的日期（格式：YYYYMMDD）
today = datetime.datetime.today().strftime("%Y%m%d")

usage_chart_file = f"src/img/activity/{today}_usage_log.png"
usage_file = f"src/text/usage_log.json"

# 設定 Matplotlib 使用微軟正黑體（適用於 Windows）
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False  # 避免負號顯示錯誤

# 常見應用程式名稱映射表
APP_NAME_MAPPING = {
    "code.exe": "Visual Studio Code",
    "chrome.exe": "Google Chrome",
    "firefox.exe": "Mozilla Firefox",
    "outlook.exe": "Microsoft Outlook",
    "excel.exe": "Microsoft Excel",
    "winword.exe": "Microsoft Word",
    "powerpnt.exe": "Microsoft PowerPoint",
    "notepad.exe": "Notepad",
    "cmd.exe": "Command Prompt",
    "explorer.exe": "File Explorer",
    "teams.exe": "Microsoft Teams"
}

def get_active_window():
    """ 獲取當前前台應用名稱 """
    if platform.system() == "Windows":
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            if proc.info["pid"] == pid:
                return APP_NAME_MAPPING.get(proc.info["name"].lower(), proc.info["name"])
    return None

def save_data(data, file=usage_file):
    """ 儲存數據到 JSON """
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data(file=usage_file):
    """ 讀取 JSON 數據 """
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_color(name):
    """ 根據應用名稱生成固定顏色 """
    hash_val = int(hashlib.md5(name.encode()).hexdigest(), 16)
    return plt.cm.tab10(hash_val % 10)  # 取 tab10 配色方案

def plot_usage(data, output_file=usage_chart_file):
    """ 根據使用時間數據生成長條圖並儲存 """
    if not data:  # 如果沒有數據，直接返回
        return
        
    names = list(data.keys())
    times = [time / 60 for time in data.values()]  # 將秒轉換為分鐘
    colors = [get_color(name) for name in names]  # 根據名稱獲取顏色

    plt.figure(figsize=(10, 6))
    plt.bar(names, times, color=colors)
    plt.xlabel('應用名稱')
    plt.ylabel('使用時間 (分鐘)')
    plt.title('應用使用時間統計')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()  # 關閉圖表，釋放記憶體

class UsageTracker:
    def __init__(self):
        self.log_data = load_data()
        self.last_app = None
        self.start_time = time.time()
        self.running = True

    def save_current_session(self):
        """儲存當前會話的使用時間"""
        if self.last_app:
            elapsed_time = time.time() - self.start_time
            self.log_data[self.last_app] = self.log_data.get(self.last_app, 0) + elapsed_time
            save_data(self.log_data)
            plot_usage(self.log_data)
            add_new_activity.main(today)

    def track_usage(self):
        """追踪應用程式使用時間"""
        while self.running:
            current_app = get_active_window()

            if current_app and current_app != self.last_app:
                if self.last_app:
                    elapsed_time = time.time() - self.start_time
                    self.log_data[self.last_app] = self.log_data.get(self.last_app, 0) + elapsed_time
                    save_data(self.log_data)

                self.last_app = current_app
                self.start_time = time.time()

            time.sleep(1)

class ShutdownHandler:
    def __init__(self, usage_tracker):
        self.usage_tracker = usage_tracker
        
    def wndproc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_QUERYENDSESSION:
            # 系統詢問是否可以關機時保存數據
            self.usage_tracker.save_current_session()
            self.usage_tracker.running = False
            return True
        return True

    def run(self):
        # 註冊窗口類別
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.wndproc
        wc.lpszClassName = "ShutdownListener"
        wc.hInstance = win32api.GetModuleHandle(None)
        
        # 註冊窗口
        class_atom = win32gui.RegisterClass(wc)
        hwnd = win32gui.CreateWindow(
            class_atom,
            "Shutdown Listener",
            0,
            0, 0, 0, 0,
            0,
            0,
            wc.hInstance,
            None
        )
        
        # 開始消息循環
        while True:
            win32gui.PumpMessages()

def main():
    # 創建使用追踪器
    usage_tracker = UsageTracker()
    
    # 創建關機處理器
    shutdown_handler = ShutdownHandler(usage_tracker)
    
    # 在新執行緒中運行關機監聽
    shutdown_thread = threading.Thread(target=shutdown_handler.run)
    shutdown_thread.daemon = True
    shutdown_thread.start()
    
    # 在新執行緒中運行使用追踪
    tracking_thread = threading.Thread(target=usage_tracker.track_usage)
    tracking_thread.daemon = True
    tracking_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        usage_tracker.running = False
        usage_tracker.save_current_session()
        sys.exit(0)

if __name__ == "__main__":
    main()