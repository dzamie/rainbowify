import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file")
parser.add_argument("-o", "--output", help="output file")
parser.add_argument("-t", "--text", help="input text")
args = parser.parse_args()

# Starting color for text. Begins on red, #880000
color = ['88','00','00']

# turns the string array into a hexcode
def color_to_str(color):
	out = "#"
	for c in color:
		out += c
	return out

# given the color triplet as input, returns the next in sequence
def next_rainbow(rainbow):
	out = ['a','a','a']
	for i in range(0,3):
		if rainbow[i] == '88':
			if rainbow[(i+1)%3] == '88':
				out[i] = '44' # if next is full, this is "fading away"
			else:
				out[i] = '88' # if next is not full, this stays full
		elif rainbow[i] == '44':
			if rainbow[i-1] == '00': # this was fading away
				out[i] = '00' # and now it finishes
			else:
				out[i] = '88' # otherwise it must be building up
		else:
			if rainbow[i-1] == '88' and rainbow[i-2] == '00': # prevents building before i-2 has faded
				out[i] = '44'
			else:
				out[i] = '00' # if it's not time to build up, it stays at 0
	return out

out = ""

if args.text: # text provided on cmd line rather than via file
	for c in args.text:
		out += '<span style="color:' + color_to_str(color) + '">' + c + '</span>'
		color = next_rainbow(color)
	if args.output:
		with open(args.output,"w") as file:
			file.write(out)
	else:
		print(out)
elif args.input: # text provided via file rather than on cmd line
	with open(args.input,"r") as in_file:
		text = in_file.read()
		for c in text:
			out += '<span style="color:' + color_to_str(color) + '">' + c + '</span>'
			color = next_rainbow(color)
		if args.output:
			with open(args.output,"w") as file:
				file.write(out)
		else:
			print(out)
else: # text provided neither by file or cmd line. no input.
	print("Error: no input supplied. Exiting...")