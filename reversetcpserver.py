import socket
import struct


def reverse_string(s):
    # 接收字符串并反转
    return s[::-1]


def handle_message(client_socket):
    # 接收initialization报文
    initialization = client_socket.recv(6)  # 读6字节数据
    type, block_num = struct.unpack('!HI', initialization)  # 解包
    if type != 1:  # 检查是否为initialization
        print("Do not receive the initialization message.")
        return

    # 发送agree报文
    agree = struct.pack('!H', 2)
    client_socket.sendall(agree)

    # 处理每个块
    for _ in range(block_num):
        # 接收reverseRequest报文
        reverseRequest_header = client_socket.recv(6)  # 读取前6字节
        type, length = struct.unpack('!HI', reverseRequest_header)  # 解包
        if type != 3:  # 检查是否为reverseRequest
            print("Do not receive the reverseRequest message.")
            return

        ascii_text = client_socket.recv(length)  # 接收指定长度数据
        reversed_ascii_text = reverse_string(ascii_text.decode('ascii'))  # 反转

        # 发送reverseAnswer报文
        reverseAnswer = struct.pack('!HI', 4, len(reversed_ascii_text)) + reversed_ascii_text.encode('ascii')
        client_socket.sendall(reverseAnswer)

    client_socket.close()


if __name__ == "__main__":
    server_ip = "localhost"
    server_port = 10101

    # 创建TCP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)  # 最多允许5个连接
    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        client_socket, addr = server_socket.accept()  # 接收
        print(f"Accepted connection from {addr}")
        handle_message(client_socket)  # 处理
