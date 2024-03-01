import socket, threading

def handle_messages(connection: socket.socket):
    '''
        Nhận các tin nhắn được gửi từ máy chủ và hiển thị chúng cho người dùng
    '''

    while True:
        try:
            msg = connection.recv(1024)

            # Nếu không có tin nhắn, có thể kết nối đã đóng
            # do đó, kết nối sẽ được đóng và một lỗi sẽ được hiển thị.
            # Nếu không, nó sẽ cố gắng giải mã tin nhắn để hiển thị cho người dùng.
            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Lỗi khi xử lý tin nhắn từ máy chủ: {e}')
            connection.close()
            break

def client() -> None:
    '''
        Tiến trình chính để bắt đầu kết nối của khách hàng với máy chủ 
        và xử lý các tin nhắn đầu vào của nó
    '''

    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 12000

    try:
        # Khởi tạo socket và bắt đầu kết nối với máy chủ
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        # Tạo một luồng để xử lý các tin nhắn được gửi bởi máy chủ
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        print('Đã kết nối đến trò chuyện!')

        # Đọc tin nhắn đầu vào của người dùng cho đến khi họ thoát khỏi trò chuyện và đóng kết nối
        while True:
            msg = input()

            if msg == 'quit':
                break

            # Phân tích tin nhắn sang utf-8
            socket_instance.send(msg.encode())

        # Đóng kết nối với máy chủ
        socket_instance.close()

    except Exception as e:
        print(f'Lỗi kết nối đến socket máy chủ {e}')
        socket_instance.close()


if __name__ == "__main__":
    client()
