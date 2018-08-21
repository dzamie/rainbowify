import argparse

default_grad = 'darkbow'

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file")
parser.add_argument("-c", "--color", help="specify gradient")
parser.add_argument("-o", "--output", help="output file")
parser.add_argument("-t", "--text", help="input text")
parser.add_argument("-l", "--list", help="list all gradients", action="store_true")
parser.add_argument("-w", "--word", help="change per word, not per character", action="store_true")
args = parser.parse_args()

colors_dict = {}
colors_dict['darkbow'] = ['880000','884400','888800','448800','008800','008844','008888','004488','000088','440088','880088','880044']
colors_dict['rainbow'] = ['ff0000','ff8800','ffff00','88ff00','00ff00','00ff88','00ffff','0088ff','0000ff','8800ff','ff00ff','ff0088']
colors_dict['hs_kids'] = ['0715cd','4ac925','e00707','b536da']
colors_dict['hs_trol'] = ['a10000','a15000','a1a100','416600','008141','008282','005682','000056','2b0057','6a006a','77003c','626262']
colors_dict['hs_horn'] = ['ffba29','ffba29','ffba29','ff9000','ff9000','ff9000','ff4200','ff4200','ff4200','ff9000','ff9000','ff9000']

if args.color:
	gradient = colors_dict[args.color]
else:
	gradient = colors_dict[default_grad]

if args.list:
	for s in colors_dict:
		print(s)
	exit()

out = ""

i = 0
tag_flag = False
word_flag = True

if args.text: # text provided on cmd line rather than via file
	for c in args.text:
		if c == '<': 		# disable style insertion for existing html tags
			tag_flag = True
		elif c == '>': # technically <<>> fucks with this but normal html shouldn't have that
			tag_flag = False
			out += c
			continue
		if tag_flag:
			out += c
		else:
			if (args.word and word_flag and c.isalpha()) or c == ' ':
				# activates only if:
				# 1. word option is on
				# 2. prev char is alpha (in a word)
				# 3. curr char is alpha (still in a word)
				# or if it's a space because otherwise it keeps "skipping"
				i -= 1
			i = (i + 1) % len(gradient) # increment index, looping if needed
			word_flag = c.isalpha() # still advances when not still in a word
			out += '<span style="color:#' + gradient[i] + '">' + c + '</span>'
	if args.output:
		with open(args.output,"w") as file:
			file.write(out)
	else:
		print(out)
elif args.input: # text provided via file rather than on cmd line
	with open(args.input,"r") as in_file:
		text = in_file.read()
		for c in text:
			if c == '<':
				tag_flag = True
			elif c == '>': # technically <<>> fucks with this but normal html shouldn't have that
				tag_flag = False
				out += c
				continue
			if tag_flag:
				out += c
			else:
				if (args.word and word_flag and c.isalpha()) or c == ' ':
					# activates only if:
					# 1. word option is on
					# 2. prev char is alpha (in a word)
					# 3. curr char is alpha (still in a word)
					# or if it's a space because otherwise it keeps "skipping"
					i -= 1
				i = (i + 1) % len(gradient) # increment index, looping if needed
				word_flag = c.isalpha() # still advances when not still in a word
				out += '<span style="color:#' + gradient[i] + '">' + c + '</span>'
		if args.output:
			with open(args.output,"w") as file:
				file.write(out)
		else:
			print(out)
else: # text provided neither by file or cmd line. no input.
	print("Error: no input supplied. Exiting...")