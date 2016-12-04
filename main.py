import datetime
import numpy
from python_speech_features import mfcc
from os import listdir, remove
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
import speech_recognition
from config import dictionary, training_data_dir

if __name__=='__main__':

	# GATHER FEATURES FROM KNOWN WORDS, USE MFCCS
	training_files = listdir(training_data_dir)
	word_features = {}
	for word in dictionary:
		filtered_word_files = [training_data_dir + '/' + this_file for this_file in training_files if word in this_file]
		word_features[word] = []
		word_count = 0
		for my_file in filtered_word_files:
			word_count += 1
			(rate, sig) = wav.read(my_file)
			mfccs = mfcc(sig, rate, numcep=26)
			word_features[word].append(numpy.average(mfccs, axis=0))
		word_features[word] = sum(word_features[word])/word_count


	# STEP 1: FEATURE ANALYSIS
	r = speech_recognition.Recognizer()
	with speech_recognition.Microphone() as source:
		print 'listening'
		audio = r.listen(source)
	now = str(datetime.datetime.now()).replace(' ', '_')
	file_name = '{}.wav'.format(now)
	with open(file_name, 'wb') as output_file:
		output_file.write(audio.get_wav_data())
	(rate, sig) = wav.read(my_file)
	remove(file_name)
	sentence_mfccs = mfcc(sig, rate, numcep=26)
	for word in sentence_mfccs:
		print word



