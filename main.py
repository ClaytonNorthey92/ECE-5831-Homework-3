import datetime
import numpy
from python_speech_features import mfcc
from os import listdir, remove
from matplotlib import pyplot as plt
import random
import scipy.io.wavfile as wav
import speech_recognition

dictionary = {}
single_letter_mapping = {}
transitional_numbers = {}
valid_test_words = []

extra_dictionary_lines = [
	'C C',
	'C CH',
	'Q QUA',
	'E EH1',
	'A EH1',
	'S Z',
	'IE IY1',
	'T DT',
	'ER ER0'
]

def get_observational_proabability(value, time, dictionary):
	total_states = 0.0
	found_states = 0.0
	for word in dictionary:
		word_length = len(word)
		if time < word_length and word[time:time+len(word)] == value:
			found_states += 1.0
		total_states += 1.0
	return found_states/total_states

if __name__=='__main__':

	# BUILD DICTIONARY FROM TRAINING DATA SET
	f = open('dictionary.txt')
	data = f.read().split('\n')
	f.close()
	data.extend(extra_dictionary_lines)
	for line in data:
		data_items = line.split()
		this_word = data_items[0]
		dictionary[this_word] = data_items[1:]
		for index, phone in enumerate(dictionary[this_word]):
			if len(data_items[1:]) == 1 or (this_word.isalpha() and len(this_word) < 3):
				if phone not in single_letter_mapping:
					single_letter_mapping[phone] = []
				single_letter_mapping[phone].append(this_word)
		for index, letter in enumerate(this_word):
			if index != len(this_word) - 1:
				key = '{}-{}'.format(letter, this_word[index+1])
				if key not in transitional_numbers:
					transitional_numbers[key] = 0
				transitional_numbers[key]+= 1
	
	valid_phones = [phone for phone in single_letter_mapping]
	for word in dictionary:
		valid_word = 1
		for phone in dictionary[word]:
			if phone not in valid_phones:
				valid_word = 0
		if valid_word:
			valid_test_words.append(word)

	# GET RANDOM TEST PHONEMES
	test_word = valid_test_words[random.randint(0, len(valid_test_words))]
	test_phones = dictionary[test_word]

	print 'The test word is: ', test_word, " --- THE PROGRAM DOES NOT KNOW THIS!"
	print 'the phonemes are: ', test_phones, " --- THE PROGRAM DOES KNOW THIS!"

	output_results_map = {}
	for time_index, phone in enumerate(test_phones):
		possible_letters = single_letter_mapping[phone]
		print phone, possible_letters
		output_results_map[time_index] = {}
		for index, letter in enumerate(possible_letters):
			probability = 1
			probability *= get_observational_proabability(letter, time_index, dictionary)
			output_results_map[time_index][letter] = probability
			if index != len(possible_letters) -1:
				transistion = '{}-{}'.format(letter, possible_letters[index+1])
				if transistion in transitional_numbers:
					print transitional_numbers[transistion]

			
