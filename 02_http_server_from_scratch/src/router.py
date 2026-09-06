from src.request import Request

class Router:
	def __init__(self,request: Request):
		self.request = request

	def routing_method_path(self):
		data = [self.request.method,self.request.path]
		print(data)
		match data:
			case ["GET","/"]:
				return self._get_default_path()
			case ["GET","/users"]:
				return self._get_user_path()
			case ["POST", "/echo"]:
				return self._post_body_echo()
			case _:
				return self._unkown_request()

	def _get_default_path(self):
		body = "<h1> Hello from home </h1>"
		http_response = (
			"HTTP/1.1 200 OK\r\n"
			"Content-Type: text/html\r\n"
			f"Content-Length: {len(body)}\r\n"
			"\r\n"
			f"{body}"
		)
		return http_response

	def _get_user_path(self):
		body = "<h1> Hello from Users</h1>"
		http_response = (
			"HTTP/1.1 200 OK\r\n"
			"Content-Type: text/html\r\n"
			f"Content-Length: {len(body)}\r\n"
			"\r\n"
			f"{body}"
		)
		return http_response

	def _post_body_echo(self):
		body = self.request.body.data
		print(body)
		http_response = (
			"HTTP/1.1 200 OK\r\n"
			"Content-Type: text/html\r\n"
			f"Content-Length: {len(body)}\r\n"
			"\r\n"
			f"{body.decode('utf-8')}"
		)
		return http_response

	def _unkown_request(self):
		body = self.request.body.data
		http_response = (
			"HTTP/1.1 404 Not Found\r\n"
			"Content-Type: text/html\r\n"
			f"Content-Length: {len(body)}\r\n"
			"\r\n"
			f"{body}"
		)
		return http_response