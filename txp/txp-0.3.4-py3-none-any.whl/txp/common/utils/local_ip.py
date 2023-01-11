"""
Exposes a method to retrieve the machines local IP programmatically.
"""
import socket


def get_local_ip() -> str:
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


if __name__ == '__main__':
    add = get_local_ip()
    print(f'Your local IP: {add}')
