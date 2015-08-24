# whatsapp chat parser

This repo is for a script I wrote for generating some stats about a whatsapp chat history file.
It works with chats between two people or group chats.
It will display the results in terminal as well as write it to a file (stats.txt).

It generates stats per individual in the chat, including:
* Total messages sent
* Average message length (characters)
* Average message length (words)
* Maximum message length (words)
* Minimum message length (words)
* Images sent
* Videos sent
* Positive messages & percentage of total
* Neutral messages & percentage of total
* Negative messages & percentage of total
* Most common word
* Second most common word
* Third most common word

It will also generate stats for the chat, including:
* Total messages in chat
* Who sent the most messages, the count and percentage of total
* Who sent the least messages, the count and percentage of total
* Most negative message sent, who sent it and the polarity
* Most positive message sent, who sent it and the polarity
* Longest message sent, who sent it and its' length (characters)
* Shortest message sent, who sent it and it's length (characters)

## Dependecies

This script requires the [TextBlob](https://github.com/sloria/TextBlob) package to be installed.

## whatsapp_stats.py

The main script. This script does all the processing of the history file.

### Usage

`python whatsapp_stats.py <filename> [<stopwords_filename>]`

e.g. `python whatsapp_stats.py "WhatsApp Chat Alice.txt"

Where `<filename>` is the whatsapp chat history file e.g. WhatsApp Chat Alice.txt

You do not have to specify the stopwords file, it will then just use the default file stopwords.txt.

## stopwords.txt

Contains a list of words that you wish to exclude from the most common words count. Contains words like a, an, the, I etc.

## Known Issues

Chat history files exported from different Operating Systems have different formats. Currently this script only works for files exported from WhatsApp running on an OSX device or an Android device. The script will output "This line could not be parsed: " followed by the line if that line in the chat history file does not follow a recognized format. This output will not be included in the stats.txt output.

Multi-line messages. The script sees each line as a complete message so if a message runs over multiple lines it only parses the first line of the multi-line message.

## Sources 

For the sentiment analysis I'm using [TextBlob](https://github.com/sloria/TextBlob).

For the stopwords list I extended the English Google stopwords list found at [https://code.google.com/p/stop-words/](https://code.google.com/p/stop-words/).

I consulted the following StackOverflow posts:
* https://stackoverflow.com/questions/3277503/python-read-file-line-by-line-into-array
* https://stackoverflow.com/questions/8689795/how-can-i-remove-non-ascii-characters-but-leave-periods-and-spaces-using-python
* https://stackoverflow.com/questions/17507876/trying-to-count-words-in-a-string-python
* https://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
* https://stackoverflow.com/questions/5214578/python-print-string-to-text-file

## Disclaimer

This script may break for whatever reason. I did not do extensive testing on it.
It will also probably take a long time to generate stats for long group chats with many people part of the group.