import os
import socket
import struct
import random
import sys


def send_reverse_request(client_socket, block_content, block_index):
    # 发送reverseRequest报文
    reverseRequest = struct.pack('!HI', 3, len(block_content)) + block_content.encode('ascii')
    client_socket.sendall(reverseRequest)

    # 接收reverseAnswer报文
    reverseAnswer_header = client_socket.recv(6)  # 接收6字节报文头
    type, length = struct.unpack('!HI', reverseAnswer_header)
    if type != 4:  # 检查报文类型是否为reverseAnswer
        print("Do not receive the reverseAnswer message.")
        sys.exit(1)

    reverseAnswer_reversed_text = client_socket.recv(length).decode('ascii')  # 接收指定长度的反转数据
    print(f"{block_index}: {reverseAnswer_reversed_text}")
    return reverseAnswer_reversed_text


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Correct usage: python reversetcpclient.py <server_ip> <server_port> <file_path> <lmin> <lmax>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    file_path = sys.argv[3]
    lmin = int(sys.argv[4])
    lmax = int(sys.argv[5])

    # 读取文件
    with open(file_path, 'r') as file:
        ascii_text = file.read()

    # 创建TCP套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    blocks = []
    i = 0
    while i < len(ascii_text):  # 将文件内容分块
        block_size = random.randint(lmin, lmax)  # 随机确定每块的大小，闭区间
        blocks.append(ascii_text[i:i + block_size])  # 将块添加到列表中，左闭右开
        i += block_size

    block_num = len(blocks)  # 计算块数
    # 发送initialization报文
    # 打包函数，！：大端字节序；H：2字节；I：4字节，后面是打包内容
    # sendall确保全部发出
    initialization = struct.pack('!HI', 1, block_num)
    client_socket.sendall(initialization)

    # 接收agree报文
    agree = client_socket.recv(2)  # 接收2字节Agree报文
    # 将接收的agree解包为大端字节序2字节，结果是元组，取第一个元素type
    type = struct.unpack('!H', agree)[0]
    if type != 2:  # 检查报文类型是否为Agree
        print("Do not receive the agree message.")
        sys.exit(1)

    reversed_ascii_text = ""
    for index, block_content in enumerate(blocks):
        # 发送每块的reverseRequest报文并接收反转后的数据
        reversed_ascii_text += send_reverse_request(client_socket, block_content, index + 1)

    client_socket.close()

    # 获取文件目录和文件名
    # 分成了目录与文件名
    directory, file_name = os.path.split(file_path)
    new_file_name = 'reversed_' + file_name
    new_file_path = os.path.join(directory, new_file_name)

    with open(new_file_path, 'w') as file:  # 将反转后的内容写入新文件
        file.write(reversed_ascii_text)
