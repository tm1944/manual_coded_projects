from dataclasses import dataclass
from typing import Optional

@dataclass
class Header:
	Host: Optional[str] = '' 
	User_Agent: Optional[str] = ''
	Content_Type: Optional[str] = ''
	Content_Length: Optional[int] = 0

@dataclass
class Body:
	data: bytes = b''



class Request:
	def __init__(self):
		self.method: str
		self.version: str
		self.path: str
		self.header = Header()
		self.body = Body() 




	def _set_request_variables(
			self,
			method: str,
			version: str,
			path: str 
		):
		self.method = method
		self.version = version
		self.path = path

	def _set_header_variables(self,param_dict: dict[str,str]):
		for k,v in param_dict.items():
			match k:
				case 'Host':
					self.header.Host = param_dict['Host']
				case 'User-Agent':
					self.header.User_Agent = param_dict['User-Agent']
				case 'Content-Type':
					self.header.Content_Type = param_dict['Content-Type']
				case 'Content-Length':
					self.header.Content_Length = int(param_dict['Content-Length'])

	def set_body_variables(self,body_buffer: bytes):
		self.body.data = body_buffer

	def _list_to_dict(self,arr: list[str])-> dict[str,str]:
		arr_dict = {}
		for string in arr:
			if string == '':
				break
			string_to_list = string.split(': ',1)
			key_str = str(string_to_list[0])
			arr_dict[key_str] = string_to_list[1]
		return arr_dict

	def _remove_parsed_values(self, arr:list[str])->list[str]:
		res = []
		for i in range(len(arr)):
			if arr[i] == '':
				res = arr[i+1:]
		return res

	def _parse_first_header_line(self, lines_arr: list[str]):

		params_arr = lines_arr[0].split(' ')
		lines_arr.pop(0) # remove the variables
		if len(params_arr) == 3:
			self._set_request_variables(method=params_arr[0],path=params_arr[1],version=params_arr[2])
		else:
			print("Error: Corrupted Request")

	#only public function
	def parse_request_str(self,req_str: str):
		lines_arr = req_str.split('\r\n')
		self._parse_first_header_line(lines_arr)
		header_dict = self._list_to_dict(lines_arr)

		self._set_header_variables(header_dict)

		lines_arr = self._remove_parsed_values(lines_arr)


	def print_request_body(self):
		print()
		print(f"method: {self.method}")
		print(f"path: {self.path}")
		print(f"version: {self.version}")

		print() # \n

		print(
			f"headers:\n"
			f"\tHost: {self.header.Host}\n"
			f"\tUser-Agent: {self.header.User_Agent}\n"
			f"\tContent-Type: {self.header.Content_Type}\n"
			f"\tContent-Length: {self.header.Content_Length}\n"
		)

		print() # \n

		print(
			"body:\n"
			f"\t{self.body.data}"
		)
