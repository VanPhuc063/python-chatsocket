import socket, threading

# Biến toàn cục để duy trì các kết nối của khách hàng
connections = []

def handle_user_connection(connection: socket.socket, address: str) -> None:
    '''
        Nhận kết nối của người dùng để tiếp tục nhận các tin nhắn từ họ và
        gửi đến các người dùng/kết nối khác.
    '''
    while True:
        try:
            # Nhận tin nhắn từ client
            msg = connection.recv(1024)

            # Nếu không có tin nhắn nhận được, có thể kết nối đã kết thúc
            # vì vậy trong trường hợp này, chúng tôi cần đóng kết nối và loại bỏ nó khỏi danh sách kết nối.
            if msg:
                # Ghi nhật ký tin nhắn được gửi bởi người dùng
                print(f'{address[0]}:{address[1]} - {msg.decode()}')

                # Xây dựng định dạng tin nhắn và phát sóng cho các người dùng đã kết nối trên máy chủ
                msg_to_send = f'Từ {address[0]}:{address[1]} - {msg.decode()}'
                broadcast(msg_to_send, connection)

            # Đóng kết nối nếu không có tin nhắn được gửi
            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Lỗi khi xử lý kết nối của người dùng: {e}')
            remove_connection(connection)
            break

def broadcast(message: str, connection: socket.socket) -> None:
    '''
        Phát sóng tin nhắn đến tất cả người dùng kết nối với máy chủ
    '''

    # Lặp qua các kết nối để gửi tin nhắn cho tất cả các client đã kết nối
    for client_conn in connections:
        # Kiểm tra xem kết nối này không phải của người gửi
        if client_conn != connection:
            try:
                # Gửi tin nhắn đến kết nối client
                client_conn.send(message.encode())

            # nếu gửi thất bại, có thể có kết nối socket đã đóng
            except Exception as e:
                print('Lỗi khi phát sóng tin nhắn: {e}')
                remove_connection(client_conn)

def remove_connection(conn: socket.socket) -> None:
    '''
        Loại bỏ kết nối được chỉ định khỏi danh sách kết nối
    '''

    # Kiểm tra xem kết nối có tồn tại trong danh sách kết nối không
    if conn in connections:
        # Đóng kết nối socket và loại bỏ kết nối khỏi danh sách kết nối
        conn.close()
        connections.remove(conn)

def server() -> None:
    '''
        Tiến trình chính để nhận các kết nối của khách hàng và bắt đầu một luồng mới
        để xử lý các tin nhắn của họ
    '''

    LISTENING_PORT = 12000
    
    try:
        # Tạo máy chủ và chỉ định rằng nó chỉ có thể xử lý 4 kết nối cùng một lúc!
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Máy chủ đang chạy!')
        
        while True:

            # Chấp nhận kết nối của client
            socket_connection, address = socket_instance.accept()
            # Thêm kết nối client vào danh sách kết nối
            connections.append(socket_connection)
            # Bắt đầu một luồng mới để xử lý kết nối client và nhận các tin nhắn của họ
            # để gửi đến các kết nối khác
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'Đã xảy ra lỗi khi khởi tạo socket: {e}')
    finally:
        # Trong trường hợp có bất kỳ vấn đề nào, chúng tôi sẽ làm sạch tất cả các kết nối và đóng kết nối máy chủ
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()

if __name__ == "__main__":
    server()
