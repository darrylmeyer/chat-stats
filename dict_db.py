"""
Orignial code - Darryl Meyer
Functionality - Pieter van der Westhuizen
20 August 2015
Parser for WhatsApp chat history.
Outputs list of words, word count and word polarity into a CSV file, ordered by most used.
"""

import re
import sys
import collections
from collections import defaultdict
from textblob import TextBlob
import string
import time

# Global stats variables
stopwords = []
message_count = 0
chat_os = "" 
global_dict = {} 
ascii_check = 0 
stopwords_filename = "stopwords.txt"
num_records = 0

def chat_parser(filename, records):
	global stopwords
	global chat_os
	global num_records

	num_records = int(records)

	chat = readfile(filename)
	setup_stopwords(stopwords_filename)

	# Set global OS flag
	first_line = chat[0]
	first_line = first_line.strip()
	first_line = first_line.lstrip("\xef\xbb\xbf") # Beginning of line chars
	chat_os = os_check(first_line)

	main_loop(chat)

	write_file()

# Checks which operating system the chat history file is from.
def os_check(line):
	osx_pattern = re.compile(r'\d\d\d\d/\d\d/\d\d')
	android_pattern = re.compile(r'\d\d/\d\d/\d\d\d\d')
	
	osx_match = osx_pattern.match(line)
	android_match  = android_pattern.match(line)

	if osx_match:
	    return "osx"
	elif android_match:
		return "android"
	else:
		return "no match"

# Reads the stopwords file and removes end of lines from the list
def setup_stopwords(stopwords_filename):
	global stopwords
	
	stopwords = readfile(stopwords_filename)

	# Remove end of lines from the stopwords
	for stopword in stopwords:
		stopwords[stopwords.index(stopword)] = stopword.strip()


# Reads the contents of a file to an array
def readfile(filename):
	with open(filename) as f:
		content = f.readlines()

	return content

# Writes the stats to a file
def write_file():
	global num_records

	ordered_global_dict = collections.OrderedDict(sorted(global_dict.items(), key=lambda t: t[1], reverse=True)) #Orders the global dict by word count
	
	dictlen = len(ordered_global_dict)
	print "Total number of words - " + str(dictlen)

	#Verify that the the number specified by user is not bigger than the maximum number of words found
	if dictlen > num_records:
		print "Only processing the top "+ str(num_records)+" words"
	elif dictlen < num_records:
		num_records = dictlen
		print "Processing all "+ str(num_records)+" words"

	start_time = time.time()

	content ="Word,Count,Polarity\n" #First Row
	
	#Get Polarity for each of the words as they are added to the next row
	#for i in range(0,dictlen):
	for i in range(num_records):
		thepolarity = get_polarity(str(ordered_global_dict.items()[i][0]))
		content += str(ordered_global_dict.items()[i][0])+","
		content += str(ordered_global_dict.items()[i][1])+","
		content += str(thepolarity)+"\n"
	
	#Write all rows to file	
	with open("Chat_DB_"+filename+".csv", "w") as output_file: 
		output_file.write(content)
		end_time = time.time() - start_time
		print "Process took "+ str(end_time) + " seconds"

# Spits the line into an array with form: [date, name, message]
def get_line_array(line):

	if not all(char.isspace() for char in line):
		os = os_check(line)
			
		if os == "osx":
			return line.split(": ")
		elif os == "android":
			line_array = []
			temp_line_array = line.split(" - ")

			if len(temp_line_array) >= 2:
				line_array.append(temp_line_array[0])
				temp_line_array = temp_line_array[1].split(": ")

				if len(temp_line_array) >= 2:
					line_array.append(temp_line_array[0])
					line_array.append(temp_line_array[1])	

					return line_array
		else:
			print("This line could not be parsed: " + line)

# Iterates through each line in the chat to determine stats
def main_loop(chat):
	for line in chat:
		line = line.strip()
		line = line.lstrip("\xef\xbb\xbf") # Beginning of line chars

		line_arr = get_line_array(line)

		if line_arr and len(line_arr) >= 3:
			name = line_arr[1]
			message = line_arr[2]

			media = False # flag for when the message is a media item
			
			if chat_os == "osx":
				if is_image(message):
					media = True
					
				elif is_video(message):
					media = True
				
			elif chat_os == "android":
				#PVDW - Added Media for Android Support
				if is_media(message):
					media = True
			
                             
			if not media:
				# Add to common words
				update_common_words(message)

# Update the common words dictionary 
def update_common_words(message):
	global stopwords

	words = re.split(r'[^0-9A-Za-z]+', message)

	#PVDW Add to Global dictionary to find most commonly used words in chat
	for word in words:
		if not word.isspace() and len(word) > 2:
			if word.lower() not in stopwords:
				if word.lower() in global_dict:
					global_dict[word.lower()] += 1
				else:
					global_dict[word.lower()] = 1

# PVDW - Return true is message was Media - Android compatibility
def is_media(message):
	if message.rstrip() == "<Media omitted>":
		return True
	else:
		return False
	
# Return true is message was an image
def is_image(message):
	if message.rstrip() == "<image omitted>":
		return True
	else:
		return False

# Return true is message was a video
def is_video(message):
	if message.rstrip() == "<video omitted>":
		return True
	else:
		return False
# Returns the count of the words in the message
def get_word_count(message):
	words = re.split(r'[^0-9A-Za-z]+', message)

	return len(words)

def get_polarity(message):
	# Remove non-printable chars from the message
	message_printable_only = filter(lambda x: x in string.printable, message)
			
	blob_message = TextBlob(message_printable_only)
		
	return blob_message.sentiment.polarity

# Run the parser if the number of words is supplied
if len(sys.argv) == 2:
	filename = sys.argv[1]
	records = 500
	chat_parser(filename, records)

elif len(sys.argv) == 3:
	filename = sys.argv[1]
	records = sys.argv[2]
	chat_parser(filename, records)
	
else:
	print("Usage: python whatsapp_stats.py <filename> [<number of records to process>]\nDefault records to process:500")