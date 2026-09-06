import socket
from datetime import datetime
from src.request import Request
from src.router import Router

HOST = "127.0.0.1"
PORT = 8080


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
	s.bind((HOST,PORT))
	s.listen()

	print(f"Listening on http://{HOST}:{PORT}")
	while True:
		conn,addr = s.accept()
		with conn:

			request = Request() #Request Object
			buffer = b""
			header = b""
			body = b""
			while True:
				req = conn.recv(1024)

				if not req:
					print("Connection Closed")
					break
					
				buffer += req
				if b"\r\n\r\n" in buffer:
					header, body = buffer.split(b"\r\n\r\n",1)
					request.parse_request_str(header.decode('utf-8'))
					while len(body) < request.header.Content_Length:
						req = conn.recv(1024)
						if not req:
							break
						body += req
					request.set_body_variables(body)
					break


			request.print_request_body()

			router = Router(request)
			http_response = router.routing_method_path()

			'''
			body = "<h1>Hello from server :-D </h1>"
			http_response = (
				"HTTP/1.1 200 OK\r\n"
				f"Server: http//{HOST}:{PORT}\r\n"
				f"Date: {datetime.today().strftime('%Y-%m-%d')}\r\n"
				f"Content-Length: {len(body)}\r\n"
				"\r\n"
				f"{body}"
			)'''
			conn.sendall(http_response.encode('utf-8'))