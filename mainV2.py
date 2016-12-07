import copy
import datetime
import random

class HMM:
	
	hmm = None
	observational_probability = None
	dictionary = None
	valid_words = []

	def __init__(self, phonemes_file='phonemes.txt', dictionary_file='dictionary.txt'):
		start = datetime.datetime.now()
		print 'training HMM...please wait...'
		f = open(phonemes_file)
		phonemes = f.read().split('\n')
		f.close()

		f = open(dictionary_file)
		dictionary_words = f.read().split('\n')
		f.close()
		hmm = {}
		observational_probability = {}
		self.dictionary = dictionary_words
		for word_line in dictionary_words:
			line = word_line.split()
			word = line[0]
			self.valid_words.append(word)
			for l_index, letter in enumerate(word):
				if l_index not in observational_probability:
					observational_probability[l_index] = []
				observational_probability[l_index].append(letter)
			word_phonemes = line[1:]
			word_length = len(word)
			joined_word_phonemes_length = len(''.join(word_phonemes))
			for p_index, phoneme in enumerate(word_phonemes):
				found = None
				try:
					found = word_phonemes.index(phoneme)
				except ValueError as e:
					# this is okay, it means the phoneme was not in the
					# list
					pass
				if found >= 0:
					possible_values = [
						word[found:found+1],
						word[found-1:found],
						word[found-1:found+1],
						word[found:found+2]
					]
					if phoneme not in hmm:
						hmm[phoneme] = []
					hmm[phoneme].extend([pv for pv in possible_values if pv not in hmm[phoneme]])
		self.hmm = hmm
		self.observational_probability = observational_probability
		print 'finished training HMM. time elapsed: {}'.format(datetime.datetime.now() - start)

	def match_word(self, phonemes_input):
		test_p = phonemes_input.split()
		markov_model = {}
		transition_map = {}
		for p_i, p in enumerate(test_p):
			for letter in self.hmm[p]:
				compare_letters = ''.join(self.observational_probability[p_i])
				next_compare_letters = ''.join(self.observational_probability[p_i+1])
				total_compare = ''
				for l in range(len(compare_letters)):
					another = ''
					if l < len(next_compare_letters):
						another = next_compare_letters[l]
					total_compare += compare_letters[l] + another
				numerator = max(compare_letters.count(letter), next_compare_letters.count(letter))
				prob = float(numerator)/float(len(self.observational_probability[p_i]))
				if prob > 0:
					if p_i not in markov_model:
						markov_model[p_i] = {}
					markov_model[p_i][letter] = 1
		num_markov_states = len(markov_model)
		paths = []	
		for i in range(num_markov_states):
			if i < num_markov_states - 1:
				for letter_1 in markov_model[i]:
					for letter_2 in markov_model[i+1]:
						prob = self.get_transitional_probability(letter_1, i, letter_2, i+1, markov_model)
						if prob:
							transition_map['{}{}-{}{}'.format(letter_1, i, letter_2, i+1)] = prob
		markov_steps = [markov_model[i] for i in range(num_markov_states)]
		init_state = [key for key in markov_steps[0]]
		for i in range(1, num_markov_states):
			new_states = []
			for state in init_state:
				for key in markov_steps[i]:
					new_states.append('{}-{}'.format(state, key))
			init_state = copy.copy(new_states)

		word_prob = {}
		max_word = None
		for word in init_state:
			prob = 1
			letters = word.split('-')
			for l_index, letter in enumerate(letters):
				prob *= markov_model[l_index][letter]
				if l_index < len(letters) - 1:
					transition = '{}{}-{}{}'.format(letter, l_index, letters[l_index+1], l_index+1)
					if transition in transition_map:
						prob *= transition_map[transition]
			if prob > 0:
				word_prob[word] = prob
				if (max_word is None or prob > word_prob[max_word]) and word.replace('-', '') in self.valid_words:
					max_word = word
		if max_word:
			return max_word.replace('-', '')

	def get_transitional_probability(self, letter_1, letter_1_index, letter_2, letter_2_index, markov_model):
		total_count = 0.0
		found_count = 0.0
		for word_line in self.dictionary:
			word = word_line.split()[0]
			if letter_1_index < len(word) - 1 and (letter_1 in word[letter_1_index:letter_1_index+2]):
				total_count += 1.0
				if letter_2_index < len(word) - 1 and (letter_2 in word[letter_1_index:letter_1_index+2]):
					found_count += 1.0
		output = None
		if not total_count:
			output = 0.0
		else:
			output = found_count/total_count
		return output

if __name__=='__main__':
	hmm = HMM()
	total_count = 0
	success_count = 0
	run_count = 1
	for run in range(run_count):
		random_words = [hmm.dictionary[random.randint(0, len(hmm.dictionary) - 1)] for i in range(10)]
		for line in random_words:
			print '---'
			total_count += 1
			line_items = line.split(' ', 1)
			print 'word: ', line_items[0]
			print 'phonemes: ', line_items[1]
			result = hmm.match_word(line_items[1].strip())
			print 'result: ', result
			if line_items[0] == result:
				success_count += 1
				print 'success'
	print "successful: {}%".format(float(success_count)/float(total_count)*100)
