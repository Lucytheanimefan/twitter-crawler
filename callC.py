import subprocess


def call_C():
	subprocess.call(["cd","c"])
	subprocess.call(["make","PROG1"])


if __name__ == '__main__':
	call_C()