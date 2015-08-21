"""
Darryl Meyer
20 August 2015
Person class used in WhatsApp chat parser.
"""
import collections
from collections import defaultdict

class Person:

   def __init__(self, name):
      self.name = name
      self.message_count = 0
      self.positive_count = 0
      self.neutral_count = 0
      self.negative_count = 0
      self.character_count = 0
      self.word_count = 0
      self.image_count = 0
      self.video_count = 0
      self.max_message_length = 0 # Count of words
      self.min_message_length = 100 # Count of words
      self.common_words = {}

   def to_string(self):
      string = "Name: " + self.name
      string += "\n\tTotal messages: " + str(self.message_count)
      string += "\n\tAverage message length (characters): " + str(round(self.character_count / float(self.message_count) ,2))
      string += "\n\tAverage message length (words): " + str(round(self.word_count / float(self.message_count) ,2))
      string += "\n\tMaximum message length (words): " + str(self.max_message_length)
      string += "\n\tMinimum message length (words): " + str(self.min_message_length)
      string += "\n\tImages sent: " + str(self.image_count)
      string += "\n\tVideos sent: " + str(self.video_count)
      string += "\n\tPositive messages: " + str(self.positive_count) + " Percentage of total: " + str(round((self.positive_count/float(self.message_count))*100, 2)) + "%"
      string += "\n\tNeutral messages: " + str(self.neutral_count) + " Percentage of total: " + str(round((self.neutral_count/float(self.message_count))*100, 2)) + "%"
      string += "\n\tNegative messages: " + str(self.negative_count) + " Percentage of total: " + str(round((self.negative_count/float(self.message_count))*100, 2)) + "%"
      string += Person.get_common_words(self)

      return string

   def get_common_words(self):
      ordered_dict = collections.OrderedDict(sorted(self.common_words.items(), key=lambda t: t[1], reverse=True))
      string = "\n\tMost common word: " + str(ordered_dict.items()[0][0])
      string += "\n\t\tSaid " + str(ordered_dict.items()[0][1]) + " times"
      string += "\n\tSecond most common word: " + str(ordered_dict.items()[1][0])
      string += "\n\t\tSaid " + str(ordered_dict.items()[1][1]) + " times"
      string += "\n\tThird most common word: " + str(ordered_dict.items()[2][0])
      string += "\n\t\tSaid " + str(ordered_dict.items()[2][1]) + " times"

      return string
