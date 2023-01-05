from re import search
from pathlib import Path


def get_subtitles(path, encoding="utf-8"):
	"""
	Gets the subtitles from an .srt file at path with a specific encoding and returns
	it divided in: subtitle number, subtitle timestamp and text

	Parameters:
		path (str): path to the .srt file
		encoding (str): encoding of the subtitle file, utf-8 by default
	Returns:
		list[list[str]]: a list consistent of 3 lists:
			[0] the subtitle number,
			[1] it's timestamp,
			[2] it's text
	"""
	subNumber, timestamp, text = [], [], []
	if Path(path).exists() and Path(path).is_file():
		with open(path, encoding=encoding) as file:
			for line in file.readlines():
				noSuffix = line.removesuffix("\n")
				if noSuffix.isdecimal():
					subNumber.append(noSuffix)
				elif search("^\\d{2}:", noSuffix):
					timestamp.append(noSuffix)
				elif line != "\n":
					if not text:
						text.append(line)
					else:
						text.insert(len(text), text.pop() + line)
				else:
					text.append("")
			if text[-1] == "":
				text.pop()
		return [subNumber, timestamp, text]


getSubs = get_subtitles("C:\\Users\\Admin\\Downloads\\test\\Mob Psycho 100 II - 9 [ Español (España)].srt")
for i in range(len(getSubs[0])):
	print(getSubs[0][i])
	print(getSubs[1][i])
	print(getSubs[2][i])
