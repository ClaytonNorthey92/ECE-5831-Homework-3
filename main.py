import datetime
import numpy
from python_speech_features import mfcc
from os import listdir, remove
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
import speech_recognition

dictionary = {}
single_letter_mapping = {}

if __name__=='__main__':

	# BUILD DICTIONARY FROM TRAINING DATA SET
	f = open('dictionary.txt')
	data = f.read().split('\n')
	f.close()
	for line in data:
		data_items = line.split()
		dictionary[data_items[0]] = data_items[1:]
		if data_items[0].isalpha() and len(data_items[0]) == 1:
			for phone in dictionary[data_items[0]]:
				if phone not in single_letter_mapping:
					single_letter_mapping[phone] = []
				single_letter_mapping[phone].append(data_items[0])
	print single_letter_mapping
	# STEP 1: FEATURE ANALYSIS
	
	

