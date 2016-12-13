#! /usr/bin/python
''' Implements the OCR controller using Tesseract (tesserocr)
'''

# STANDARD PYTHON IMPORTS

# PYTHON LIBRARIES
import tesserocr
from tesserocr import PSM
from PIL import Image

# USER LIBRARIES

# GLOBAL VARIABLES
PSM_MODE = 3
LANG = u'eng'

# CLASSES
class OCRController():
	""" Exposes an interface for performing common OCR tasks on an image.
	"""
	def __init__(self, lang=LANG, psm=PSM_MODE, state_machine=None):
		''' Initialises the language and page segmentation modes of the OCR.

			'state_machine' is a reference to the state_machine that contains a
				function 'handler_extracted_text(string)' to handle the end of
				text extractions
		'''
		self._lang = lang
		self._psm = psm
		self._state_machine = state_machine
		self.extracted_text = ""
		self.is_extracting = False

	def queue_extract_text(self, image_path):
		''' Queues a text extraction routine on a background thread. When the 
		extraction is complete, self.is_extracting will be deasserted and the 
		result of the extraction will be in self.extracted_text.

		Furthermore, the state_machine's handler_extracted_text() function will
		be invoked, with the extracted text as the sole parameter.	

		TODO: BACKGROUND THREAD
		'''
		self.extracted_text = self.extract_text(image_path)
		self._state_machine.handler_extracted_text(self.extracted_text)

	def extract_text(self, image_path):
		''' Returns the OCR-d text from an image 
		'''
		self.is_extracting = True
		image = Image.open(image_path)
		text = tesserocr.image_to_text(image, lang=self._lang, psm=self._psm)
		self.is_extracting = False
		return text


# FUNCTIONS

# CODE
if __name__ == '__main__':
	print "Do not run ocr.py from __main__."

# END OF FILE