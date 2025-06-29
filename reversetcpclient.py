import socket
import struct
import sys
import os
import random

if len(sys.argv) != 6:
    print("使用方法: python reversetcpclient.py <服务器IP> <服务器端口> <文件名> <Lmin> <Lmax>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
FILENAME = sys.argv[3]
LMIN = int(sys.argv[4])
LMAX = int(sys.argv[5])

if LMIN > LMAX:
    print("错误: Lmin 不能大于 Lmax。")
    sys.exit(1)

if not os.path.exists(FILENAME):
    print(f"错误: 文件 '{FILENAME}' 不存在。")
    sys.exit(1)

# Step1. 读取文件内容并随机分块
with open(FILENAME, 'rb') as f:
    full_data = f.read()

chunks = []
pointer = 0
while pointer < len(full_data):
    chunk_size = random.randint(LMIN, LMAX)
    chunk = full_data[pointer: pointer + chunk_size]
    chunks.append(chunk)
    pointer += len(chunk)

N = len(chunks)
print(f"文件已成功读取并分割成 {N} 个块。")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print(f"已成功连接到服务器 {SERVER_IP}:{SERVER_PORT}")

    # Step2. 发送 Initialization 报文
    type_init = 1
    init_packet = struct.pack('!HI', type_init, N)
    client_socket.sendall(init_packet)
    print("Initialization 报文已发送。")

    # Step3. 接收 Agree 报文
    agree_header = client_socket.recv(2)
    if not agree_header:
        print("服务器未发送 Agree 报文，连接已关闭。")
        sys.exit(1)

    type_agree, = struct.unpack('!H', agree_header)

    if type_agree == 2:
        print("收到服务器的 Agree 报文。开始发送数据块...")
        # Step4. 循环发送数据块并接收反转后的结果
        for i, chunk in enumerate(chunks):
            type_req = 3
            length = len(chunk)
            request_packet = struct.pack('!HI', type_req, length) + chunk
            client_socket.sendall(request_packet)

            answer_header = client_socket.recv(6)
            if not answer_header:
                print("在接收答复时服务器断开连接。")
                break

            type_ans, length_ans = struct.unpack('!HI', answer_header)

            if type_ans == 4:
                reversed_chunk = client_socket.recv(length_ans)
                print(f"第 {i + 1} 块: {reversed_chunk.decode('utf-8')}")
            else:
                print(f"收到未知的报文类型: {type_ans}")
                break
    else:
        print(f"收到未知的报文类型: {type_agree}，期望收到 Agree(2)。")

except ConnectionRefusedError:
    print("连接被服务器拒绝。请确保服务器正在运行并且地址/端口正确。")
except Exception as e:
    print(f"发生错误: {e}")
finally:
    # Step5. 关闭连接
    print("所有数据块处理完毕，关闭连接。")
    client_socket.close()