from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time
import os

# -------------------------
# 配置
# -------------------------
URLS = [
    "https://upload-agsb-v2py-eexmzvfgekmyfjo6cvjjxq.streamlit.app/",
    "https://lanch.zeabur.app/",
    "https://mywebite.zeabur.app/",
    "https://lanch.wasmer.app/"
]

log_file = "click_log.txt"
log_retention_days = 2  # 日志保留天数

# -------------------------
# 清理旧日志
# -------------------------
def clean_old_logs():
    if not os.path.exists(log_file):
        return
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        cleaned_lines = []
        cutoff = datetime.now() - timedelta(days=log_retention_days)

        for line in lines:
            if line.startswith("["):
                try:
                    timestamp_str = line.split("]")[0][1:]
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    if timestamp >= cutoff:
                        cleaned_lines.append(line)
                except:
                    cleaned_lines.append(line)
            else:
                cleaned_lines.append(line)

        with open(log_file, "w", encoding="utf-8") as f:
            f.writelines(cleaned_lines)
    except Exception as e:
        print(f"日志清理失败：{e}")

clean_old_logs()

# -------------------------
# 初始化浏览器
# -------------------------
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())

# -------------------------
# 主逻辑函数
# -------------------------
def monitor_site(url):
    driver = webdriver.Chrome(service=service, options=options)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n=== 开始监控：{url} ===")

    try:
        driver.get(url)
        print("页面加载中，等待 30 秒...")
        time.sleep(30)

        # 查找按钮
        buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'get this app back up')]")

        if buttons:
            buttons[0].click()
            print("检测到按钮，已点击，等待 45 秒...")
            time.sleep(45)
            log_entry = f"[{timestamp}] URL: {url} —— 按钮已点击，等待45秒完成\n"
        else:
            print("未检测到按钮。")
            log_entry = f"[{timestamp}] URL: {url} —— 未发现按钮\n"

        # 写日志
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

    except Exception as e:
        print(f"错误：{e}")
        error_msg = f"[{timestamp}] URL: {url} —— 错误：{str(e)}\n"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(error_msg)

    finally:
        driver.quit()
        print("浏览器已关闭。")

# -------------------------
# 依次监测全部 3 个 URL
# -------------------------
for url in URLS:
    monitor_site(url)

print("\n全部监测任务已完成！")
