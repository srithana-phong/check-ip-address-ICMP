import csv
import platform
import subprocess
from datetime import datetime

# ไฟล์ input และ output
INPUT_FILE = "ips.csv"
OUTPUT_FILE = "report.txt"

def ping_ip(ip: str) -> bool:
    """Return True if ping success, False otherwise."""
    system = platform.system().lower()

    # คำสั่ง ping แตกต่างกันตาม OS
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", "1000", ip]
    else:  # linux / macOS
        cmd = ["ping", "-c", "1", "-W", "1", ip]

    try:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False


def main():
    results = []

    # อ่านไฟล์ csv
    with open(INPUT_FILE, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:  # ข้ามแถวว่าง
                continue
            ip = row[0].strip()
            if ip:
                status = "UP" if ping_ip(ip) else "DOWN"
                results.append((ip, status))

    # เขียนผลลัพธ์ลงไฟล์ report
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"ICMP Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*50 + "\n")
        for ip, status in results:
            f.write(f"{ip}: {status}\n")

    print(f"✅ Done! ผลลัพธ์ถูกบันทึกไว้ที่ {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

