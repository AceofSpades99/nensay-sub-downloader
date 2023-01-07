from re import search
from pathlib import Path


class EditSub:
	def __init__(self, path, encoding="utf-8"):
		self.__path = path
		self.__encoding = encoding
		self.__subtitles = self.get_subtitles()

	@property
	def subtitles(self):
		return self.__subtitles

	def get_subtitles(self):
		"""
		Gets the subtitles from an .srt file at path with a specific encoding and returns
		it divided in: subtitle number, subtitle timestamp and text

		Returns:
			list[list[str]]: a list consistent of 3 lists:
				[0] the subtitle number,
				[1] it's timestamp,
				[2] it's text
		"""
		subNumber, timestamp, text = [], [], []
		if Path(self.__path).exists() and Path(self.__path).is_file():
			with open(self.__path, encoding=self.__encoding) as file:
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

	def add_subtitles(self):
		# todo

	def del_subtitles(self):
		# todo

	def edit_subtitles(self, component, selected, modified):
		if component == 1:
			self.subtitles[component][selected] = modified
		elif component == 2:
			if not modified.endswith("\n"):
				modified += "\n"
			self.subtitles[component][selected] = modified
		else:
			raise IndexError("Component does not exist. Must be:\n" +
			                 "\t1. Subtitle timestamp\n" +
			                 "\t2. Subtitle text")

	def edit_timestamp(self, selected, starting_time="", ending_time=""):
		if selected in range(len(self.subtitles[1])):
			tmpTimestamp = self.subtitles[1][selected]
			split = tmpTimestamp.split(" --> ")
			if starting_time != "" and ending_time != "" and starting_time < ending_time:
				tmpTimestamp = tmpTimestamp.replace(split[0], starting_time)
				tmpTimestamp = tmpTimestamp.replace(split[1], ending_time)
			elif starting_time != "" and starting_time < split[1]:
				tmpTimestamp = tmpTimestamp.replace(split[0], starting_time)
			elif ending_time != "" and ending_time > split[1]:
				tmpTimestamp = tmpTimestamp.replace(split[1], ending_time)
			self.subtitles[1][selected] = tmpTimestamp

	def save_changes(self):
		with open(self.__path, encoding=self.__encoding, mode="w") as file:
			if len(self.subtitles[0]) == len(self.subtitles[1]) == len(self.subtitles[2]):
				for i in range(len(self.subtitles[0])):
					for j in range(len(self.subtitles)):
						file.write(self.subtitles[j][i] + "\n")

	def __move_subtitles_depending_on_timestamp(self):
		# todo

loadSubs = EditSub("D:\\Games\\downloads\\Blue Bloods 13x09 - Nothing Sacred (English).srt")
print(loadSubs.subtitles[1][0])
loadSubs.edit_timestamp(0, "00:00:07,000")
print(loadSubs.subtitles[1][0])
