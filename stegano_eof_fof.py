import cv2
import math
import numpy as np
import os
import time

def get_file_size_in_kb(file_path):
	if not os.path.exists(file_path):
		print(f"File '{file_path} tidak ditemukan.'")
		return

	file_size_bytes = os.path.getsize(file_path)

	file_size_kb = file_size_bytes / 1024

	return file_size_kb

def insert_action(method):
		message = input("Enter your message: ")
		print(f"message: {message}")

		filename = "original.jpg"

		img = cv2.imread(filename)
		size_awal = get_file_size_in_kb(filename)
		padding = "~"
		message = padding + message + padding

		if (method == "FOF"):
			start_time = time.time()
			img_2 = insert_message_fof(img, message)
			end_time = time.time()

		elif (method == "EOF"):
			start_time = time.time()
			img_2 = insert_message_eof(img, message)
			end_time = time.time()

		cv2.imwrite("stegano.png", img_2, [cv2.IMWRITE_PNG_COMPRESSION, 0])
		size_akhir = get_file_size_in_kb("stegano.png")

		print(f"filename: {filename}")
		print(f"size awal: {size_awal} KB")
		print(f"dimensi awal: {img.shape}")
		print(f"size akhir: {size_akhir} KB")
		print(f"dimensi akhir: {img_2.shape}")
		print(f"elapsed time: {(end_time - start_time):.5f} ms")

def extract_action(method):
	filename = "stegano.png"

	img = cv2.imread(filename)

	if (method == "FOF"):
		start_time = time.time()
		message = extract_message_fof(img)
		end_time = time.time()

	elif (method == "EOF"):
		start_time = time.time()
		message = extract_message_eof(img)
		end_time = time.time()

	print(f"filename: {filename}")
	print(f"hidden message: {message}")
	print(f"elapsed time: {(end_time - start_time):.5f} ms")


# FIRST OF FILE
def insert_message_fof(img, message):
	row, col, ch = img.shape
	m_length = len(message)
	nrow = math.ceil(m_length / 3 / col)
	blank = np.zeros([nrow, col, 3], np.uint8)
	img_fof = np.concatenate((blank, img))
	row, col, ch = img_fof.shape
	pos = 0
	for r in range(row):
		for c in range(col):
			for ch in range(3):
				img_fof[r][c][ch] = ord(message[pos])
				if (pos == m_length - 1):
					return img_fof
				else:
					pos += 1

def extract_message_fof(img):
	row, col, ch = img.shape
	prefix = chr(img[0][0][0])
	if (prefix != "~"):
		return "belum ada pesan yang disisipkan"
	message = ""
	padding_count = 0
	for r in range(row):
		for c in range(col):
			for ch in range(3):
				val = chr(img[r][c][ch])
				if (val == "~"):
					padding_count += 1
					if (padding_count == 2):
						if (message == ""):
							return "belum ada pesan yang disisipkan"
						else:
							return message
				else:
					message += val
	return "belum ada pesan yang disisipkan"


# END OF FILE
def insert_message_eof(img, message):
	row, col, ch = img.shape
	m_length = len(message)
	nrow = math.ceil(m_length / 3 / col)
	blank = np.zeros([nrow, col, 3], np.uint8)
	img_eof = np.concatenate((img, blank))
	pos = 0
	for r in range(row, row + nrow):
		for c in range(col):
			for ch in range(3):
				img_eof[r][c][ch] = ord(message[pos])
				if (pos == m_length - 1):
					return img_eof
				else:
					pos += 1

def extract_message_eof(img):
	row, col, ch = img.shape
	isMessageExist = False
	for c in range(col):
		for ch in range(3):
			suffix = chr(img[row - 1][c][ch])
			if (suffix == "~"):
				isMessageExist = True
				break
	if (not isMessageExist):
		return "belum ada pesan yang disisipkan"
	message = ""
	padding_count = 0
	for r in range(row - 1, -1, -1):
		for c in range(col - 1, -1, -1):
			for ch in range(2, -1, -1):
				val = chr(img[r][c][ch])
				if (val == "~"):
					padding_count += 1
					if (padding_count == 2):
						if (message == ""):
							return "belum ada pesan yang disisipkan"
						else:
							return "".join(reversed(message))
				else:
					if (ord(val) != 0):
						message += val

	return "belum ada pesan yang disisipkan"


def main():
	os.system('cls||clear')
	print("=====STEGANOGRAPHY EOF / FOF=====")
	option = int(input("Choose the method: \n1.) FOF\n2.) EOF\n3.) FOF vs EOF Insertion\n4.) Exit\n"))
	if (option == 1):
		os.system('cls||clear')
		print("=====STEGANOGRAPHY FOF=====")
		action = int(input("Choose the action: \n1.) Insert\n2.) Extract\n3.) Exit\n"))
		if (action == 1):
			insert_action("FOF")
		elif (action == 2):
			extract_action("FOF")
		elif (action == 3):
			return
		else:
			return

	elif (option == 2):
		os.system('cls||clear')
		print("=====STEGANOGRAPHY EOF=====")
		action = int(input("Choose the action: \n1.) Insert\n2.) Extract\n3.) Exit\n"))
		if (action == 1):
			insert_action("EOF")
		elif (action == 2):
			extract_action("EOF")
		elif (action == 3):
			return
		else:
			return

	elif (option == 3):
		os.system('cls||clear')
		print("=====FOF VS EOF Insertion=====")
		filename = "original.jpg"
		img = cv2.imread(filename)
		message = input("Enter your message: ")
		size_awal = get_file_size_in_kb(filename)

		time_start_fof = time.time()
		img_fof = insert_message_fof(img, message)
		time_end_fof = time.time()
		elapsed_time_fof = time_end_fof - time_start_fof
		cv2.imwrite("stegano.png", img_fof, [cv2.IMWRITE_PNG_COMPRESSION, 0])
		size_akhir_fof = get_file_size_in_kb("stegano.png")

		time_start_eof = time.time()
		img_eof = insert_message_eof(img, message)
		time_end_eof = time.time()
		elapsed_time_eof = time_end_eof - time_start_eof
		cv2.imwrite("stegano.png", img_eof, [cv2.IMWRITE_PNG_COMPRESSION, 0])
		size_akhir_eof = get_file_size_in_kb("stegano.png")


		print(f"size awal: {size_awal} KB")
		print(f"size akhir FOF: {size_akhir_fof} KB")
		print(f"elapsed time FOF: {elapsed_time_fof:.5f} ms")
		print("")
		print(f"size awal: {size_awal} KB")
		print(f"size akhir EOF: {size_akhir_eof} KB")
		print(f"elapsed time EOF: {elapsed_time_eof:.5f} ms")

	elif (option == 4):
		return

	else:
		return


if __name__ == '__main__':
	main()