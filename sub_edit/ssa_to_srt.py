from os import scandir, remove, makedirs
from pathlib import Path
from shutil import copyfile
from zipfile import ZipFile
from pyasstosrt import Subtitle
from pyunpack import Archive
# it is necessary to have installed the patool package to use pyunpack (pip install patool)


def zipToSRT(path):
	"""Uncompress the zip file obtained from the sub-downloader defined by the path into the corresponding .srt
	subtitles

	Parameters:
		path (str): zip filePath
	Raises:
		FileNotFoundError: if the file does not exist
	"""
	if Path(path).exists():
		tempPath = path[:path.rindex("\\") + 1] + "tmp"
		# first it opens and extracts the file once
		with ZipFile(path, 'r') as target:
			target.extractall(path=tempPath)
		# then it extracts the resulting .rar file(s)
		[Archive(route.path).extractall(tempPath) for route in scandir(tempPath) if route.path.endswith(".rar")]
		# after that it converts all .ass and .ssa files into .srt
		[Subtitle(Path(route)).export(tempPath) for route in scandir(tempPath) if route.path.endswith(".ass") or route.path.endswith(".ssa")]
		# and finally it deletes all files that are not .srt subtitles
		[remove(route) for route in scandir(tempPath) if not route.path.endswith("srt")]
	else:
		raise FileNotFoundError("Requested file not found, make sure of the route of the file")


def listLanguages(path):
	"""From the temp folder created with zipToSRT read the file names searching for [language] and return the
	languages as a list, it will return an empty list if the naming convention is not followed

	Parameters:
		path (str): temp folderPath as a string
	Returns:
		list: languages list
	Raises:
		FileNotFoundError: if the folder route is incorrect
	"""
	if Path(path).exists():
		return [language.path[language.path.index("[") + 1: language.path.rindex("]")] for language in scandir(path)]
	else:
		raise FileNotFoundError("Incorrect path (it does not exist)")


def selectLanguage(path, language, targetPath):
	"""From the temp folder created with zipToSRT, selecting one of the languages form listLanguages
	and giving a path to copy the files to: copy the selected language subtitles to the destination folder,
	if the folder does not exist it will create it along with all needed parent directories

	Parameters:
		path (str): temp folderPath
		language (str): selected language from listLanguages
		targetPath (str): destination folder to copy the corresponding files to
	"""
	if not Path(targetPath).exists():
		makedirs(targetPath)
	[copyfile(filePath, targetPath + filePath.path[filePath.path.rindex("\\"):]) for filePath in scandir(path) if filePath.path.__contains__(language)]


# testing
zipToSRT("C:\\Users\\Admin\\Downloads\\test\\Mob Psycho100 II Sub 09.zip")
print(listLanguages("C:\\Users\\Admin\\Downloads\\test\\tmp"))
selectLanguage("C:\\Users\\Admin\\Downloads\\test\\tmp", "Español (España)", "C:\\Users\\Admin\\Downloads\\test")
