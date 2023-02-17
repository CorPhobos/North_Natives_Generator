import re

from datetime import datetime

now = datetime.now()
py_keywords = ["from", "property"]

def get_formatted_args(input_args: list, use_comments: bool) -> str:
	pattern = "int\\*|float|int|Any|Object|unsigned|BOOL|BOOL\\*|const char\\*|Any\\*|unsigned\\*|char\\*"
	if(use_comments):
		return re.sub(pattern,  '{}:{}'.format(re.search(pattern, input_args[i]).group(0)), input_args[i])
	return re.sub(pattern,  "", input_args[i])

def remove_py_keywords(arg: str) -> str:
	for keyword in py_keywords:
		if(keyword == arg):
			return re.sub(keyword, "_{}".format(keyword), input_args[i])
	return arg

def get_pointer_count(arg) -> int:
	return len(re.findall("(\w+\*)", arg))

def handle_pointers(native_src: list) -> str:
    arr = list(range(get_pointer_count(native_src)))
    for x in range(len(arr)):
        arr[x] = x + 1
    return ", ".join(str(n) for n in arr)

def extract_non_pointer_args(string: str) -> list:
	try:
		result = re.findall(r'(?<=int) (\w+)', string)[0]
	except:
		return ""
	return result

def does_native_have_pointers(native_args: list) -> bool:
	return len(re.findall("int\\*|float\\*|Any\\*|Vector3\\*|BOOL\\*|unsigned\\*", native_args)) != 0

def format_pointer_result(native_args: int) -> str:
	return "(" + ", ".join("result.raw[{}].{}".format(i, "int") for i in range(1, get_pointer_count(native_args) + 1)) + ")"

def get_return_types(src: list) -> list:
	match = re.findall("static (\w+)", src)
	if(len(match)) != 0:
		return match
	return [""]


def get_native_hashes(src: list) -> list:
	match = re.findall(r"//\s?(0x[A-Za-z0-9]+)", src)
	return match

def get_native_args(src: list) -> list:
	match = re.findall("\w+\((.*?)\)", src)
	if(len(match) != 0):
		return match
	return [""]

def get_native_names(src: list) -> list:
	match = re.findall(r"(\w+)\s*\(", src.lower())
	if(match):
		return match
	return [""]

def has_return_type(arg: str) -> bool:
	return "return" if arg != "void" else ""


with open("natives.hpp", "r") as f:
    natives_src = f.read()

return_types 	= 	get_return_types(natives_src)
native_hashes 	= 	get_native_hashes(natives_src)
native_args 	= 	get_native_args(natives_src)
native_names 	= 	get_native_names(natives_src)


pointer_template = """ 
def {}({}):
	native.output_flag({}, [{}])
	result = native.invoke({}, {})
	return {}

"""

arg_template = """ 
def {}({}):
	{} native.invoke({}, {})

"""

no_arg_template = """  
def {}():
	{} native.invoke({})
"""
print(native_names[6493])
print(len(native_names))
#print(len(native_hashes[6492]))
print(range(len(native_hashes)))
print(len(native_hashes))
# print(native_hashes[len(native_hashes) - 1])
# print(native_names[len(native_names) - 1])
with open("natives.py", "a") as natives_file:
	natives_file.write('# Generated By Phobos {}\n'.format(now.strftime("%d/%m/%Y %H:%M:%S")))
	for i in range(len(native_names)):
		#print(i)
		name = native_names[i]
		#print(name)
		args = get_formatted_args(native_args, False)
		extracted_pointer = extract_non_pointer_args(native_args[i])
		hashes = native_hashes[i]
		pointer_result = format_pointer_result(native_args[i])
		if(does_native_have_pointers(native_args[i])):
			natives_file.write(pointer_template.format(name, extracted_pointer, hashes, handle_pointers(native_args[i]), hashes, extracted_pointer, pointer_result))
		elif(native_args[i] != ""):
			natives_file.write(arg_template.format(name, args, has_return_type(native_args[i]), hashes, args))
		else:
			natives_file.write(no_arg_template.format(name, has_return_type(native_args[i]), hashes))