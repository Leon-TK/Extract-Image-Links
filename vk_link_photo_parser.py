from typing import NamedTuple
import enum
from abc import ABC, abstractmethod

class ILinkParser(ABC):

	@abstractmethod
	def parse (self, text_to_parse: str) -> str:
		pass

	@abstractmethod
	def parse (self, text_to_parse: str) -> NamedTuple:
		pass


class ProtocolType(enum.Enum):
	HTTPS = 1
	HTTP = 2

class HttpsWithExtentionParser(ILinkParser):


	def __init__(self, extention: str, protocolType: ProtocolType = ProtocolType.HTTPS):
		self._extention = extention
		self._protocolType = protocolType
		self._protocolStr = ''
		self.protocolMissExtentionCount = 0
		self._hasNextLink = True

	def setExtention(self, ext: str):
		self._extention = ext

	def _checkExtention(self) -> bool:
		if (self._extention[0] != '.'):
			print('HttpsWithExtentionParser: extention is must began with \'.\'\n')
			return False

		if (len(self._extention) < 2):
			print('HttpsWithExtentionParser: extention must contain at least one character after \'.\'\n')
			return False
		print('Extention: ', self._extention, '\n')
		return True

	def _checkFileText(self) -> bool:
		if (len(self._fileText) <=0):
			print('HttpsWithExtentionParser: filetext is empty\n')
			return False
		return True

	def setProtocolType(self, pType: ProtocolType):
		self._protocolType = pType

	def _stringFromProtocolType(self) -> str:
		if self._protocolType == ProtocolType.HTTPS:
			return 'https'
		if self._protocolType == ProtocolType.HTTP:
			return 'http'
		print('HttpsWithExtentionParser: _stringFromProtocolType() undefined protocol type')
		return 'UnknownProtocol'

	def findLink(self) -> str:
		protocolLinkStr = self._protocolStr + '://'
		protocolIndex = self._findIndexOf(protocolLinkStr)
		#print ('protocolIndex ', str(protocolIndex), '\n')
		if protocolIndex < 0:
			print('HttpsWithExtentionParser: fail to found protocol index\n')
			self._hasNextLink = False
			return ''

		extentionIndex = self._findIndexOf(self._extention, protocolIndex + len(protocolLinkStr))
		#print ('extentionIndex ', str(extentionIndex), '\n')
		if extentionIndex < 0:
			print('HttpsWithExtentionParser: fail to found extention index\n')
			self._hasNextLink = False
			return ''

		#find next protocol index
		nextProtocolIndex = self._findIndexOf(protocolLinkStr, (protocolIndex + len(protocolLinkStr)))
		#print ('nextProtocolIndex ', str(nextProtocolIndex),'\n')
		if (nextProtocolIndex >=0):
			if (self._isExtentionBelongsToNextHttps(protocolIndex, extentionIndex, nextProtocolIndex)):
				print('Protocol miss extention ', protocolIndex, ' ', extentionIndex, ' ', nextProtocolIndex)
				self.protocolMissExtentionCount += 1
				protocolIndex = nextProtocolIndex
		else:
			self._hasNextLink = False

		link = self._fileText[protocolIndex:extentionIndex + len(self._extention)]

		self._cutFileTextLeft(extentionIndex + len(self._extention))

		return link

	#TODO check how it does
	def _cutFileTextLeft(self, index: int):
		self._fileText = self._fileText[index:]

	def _isExtentionBelongsToNextHttps(self, protocolIndex: int, extentionIndex: int, nextProtocolIndex: int) -> bool:
		return (nextProtocolIndex < extentionIndex and nextProtocolIndex > protocolIndex)

	def _findIndexOf(self, what: str, index = 0) -> int:
		return self._fileText.find(what, index)

	def _loopThroughText(self) -> str:

		if (self._checkExtention() == False or self._checkFileText() == False):
			return ''

		self._protocolStr = self._stringFromProtocolType()
		print('Protocol string: ', self._protocolStr, '\n')
		result: str = ''

		while (self._hasNextLink):
			link = self.findLink()
			if (len(link) > 1):
				result += (link + '\r')

		print('Count of missed extention: ', self.protocolMissExtentionCount)
		return result

	def parse (self, textToParse: str = '') -> str:
		self._fileText = textToParse
		return self._loopThroughText()
	



inputfile1 = open('C:\\Users\\leon2\\source\\repos\\vk link photo parser\\vk link photo parser\\ToBeParsed1.txt')
inputfile2 = open('C:\\Users\\leon2\\source\\repos\\vk link photo parser\\vk link photo parser\\ToBeParsed2.txt')
inputfile3 = open('C:\\Users\\leon2\\source\\repos\\vk link photo parser\\vk link photo parser\\ToBeParsed3.txt')
outputfile = open('C:\\Users\\leon2\\source\\repos\\vk link photo parser\\vk link photo parser\\Parsed.txt', 'w')

print('Parse file 1')
my_text1 = inputfile1.read() #reads to whole text file

parser: ILinkParser = HttpsWithExtentionParser('.jpg', ProtocolType.HTTPS)

result = parser.parse(my_text1)

parser = HttpsWithExtentionParser('.jpg', ProtocolType.HTTP)
result += parser.parse(my_text1)

parser = HttpsWithExtentionParser('.jpeg', ProtocolType.HTTPS)
result += parser.parse(my_text1)

parser = HttpsWithExtentionParser('.jpeg', ProtocolType.HTTP)
result += parser.parse(my_text1)

print('Parse file 2')
my_text2 = inputfile2.read() #reads to whole text file

parser = HttpsWithExtentionParser('.jpg', ProtocolType.HTTPS)

result = parser.parse(my_text2)

parser = HttpsWithExtentionParser('.jpg', ProtocolType.HTTP)
result += parser.parse(my_text2)

parser = HttpsWithExtentionParser('.jpeg', ProtocolType.HTTPS)
result += parser.parse(my_text2)

parser = HttpsWithExtentionParser('.jpeg', ProtocolType.HTTP)
result += parser.parse(my_text2)

print('Parse file 3')
my_text3 = inputfile3.read() #reads to whole text file

parser = HttpsWithExtentionParser('.jpg', ProtocolType.HTTPS)

result = parser.parse(my_text3)

parser = HttpsWithExtentionParser('.jpg', ProtocolType.HTTP)
result += parser.parse(my_text3)

parser = HttpsWithExtentionParser('.jpeg', ProtocolType.HTTPS)
result += parser.parse(my_text3)

parser = HttpsWithExtentionParser('.jpeg', ProtocolType.HTTP)
result += parser.parse(my_text3)

outputfile.write(result)
inputfile1.close()
inputfile2.close()
inputfile3.close()
outputfile.close()
