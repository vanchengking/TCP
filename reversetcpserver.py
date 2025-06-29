import socket
import threading
import struct


def handle_client(client_socket, client_address):
    """
    这个函数将在一个独立的线程中运行，用于处理单个客户端的全部请求。
    """
    print(f"接受来自 {client_address} 的新连接。")
    full_reversed_data = b''  # 用来拼接所有反转后的数据块
    try:
        # Step1. 接收客户端的 Initialization 报文
        header_init = client_socket.recv(6)
        if not header_init:
            print(f"客户端 {client_address} 在发送初始化信息前断开连接。")
            return
        type_init, n = struct.unpack('!HI', header_init)
        if type_init == 1:
            print(f"收到来自 {client_address} 的 Initialization 报文，将接收 {n} 个数据块。")
            # Step2. 发送 Agree 报文
            type_agree = 2
            agree_packet = struct.pack('!H', type_agree)
            client_socket.sendall(agree_packet)
            # Step3. 循环接收 n 个 reverseRequest 报文
            for i in range(n):
                request_header = client_socket.recv(6)
                if not request_header:
                    break
                type_req, length = struct.unpack('!HI', request_header)
                if type_req == 3:
                    data_bytes = client_socket.recv(length)
                    # Part1. 解码：将字节串解码为字符串
                    received_string = data_bytes.decode('utf-8')
                    # Part2. 反转：对字符串进行反转
                    reversed_string = received_string[::-1]
                    # Part3. 编码：将反转后的字符串编码回字节串，准备发送
                    reversed_data_bytes = reversed_string.encode('utf-8')
                    full_reversed_data += reversed_data_bytes  # 拼接
                    # Part4. 发送 reverseAnswer 报文
                    type_ans = 4
                    # 这里的长度应该是编码后字节串的长度
                    answer_header = struct.pack('!HI', type_ans, len(reversed_data_bytes))
                    client_socket.sendall(answer_header + reversed_data_bytes)
                    print(f"已向 {client_address} 发送第 {i + 1}/{n} 个反转块。")
                else:
                    print(f"来自 {client_address} 的报文类型错误，期望 3，收到 {type_req}")
                    break
        else:
            print(f"来自 {client_address} 的第一个报文不是 Initialization 报文。")
    except ConnectionResetError:
        print(f"客户端 {client_address} 强制断开了连接。")
    except Exception as e:
        print(f"处理来自 {client_address} 的请求时发生错误: {e}")
    finally:
        # Step5. 将完整的反转内容写入文件
        if full_reversed_data:
            filename = f"reversed_{client_address[0]}_{client_address[1]}.txt"
            with open(filename, 'wb') as f:
                f.write(full_reversed_data)
            print(f"已将来自 {client_address} 的完整反转内容保存到文件 {filename}")

        # Step6. 关闭与该客户端的连接
        print(f"与 {client_address} 的会话结束，关闭连接。")
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 12345)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print(f"TCP 服务器已启动，正在监听 {server_address}...")

    while True:
        # 等待并接受新的客户端连接
        # accept() 会返回一个新的套接字 client_socket 用于与该客户端通信，以及客户端的地址
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == '__main__':
    main()