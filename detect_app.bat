@echo off
:: 啟動 Conda 環境
call conda activate base

cd /d "D:\AI\hydestory.github.io"
:: 使用 pythonw 執行 Python 檔案（不顯示命令視窗）
python get_screen_job.py
:: 如果想要顯示命令視窗，使用下面這行替代上面那行
:: python usage_tracker.py