# imessage_stats.py

from bs4 import BeautifulSoup
from collections import defaultdict
import words

def convo_totals(imessage_soup: BeautifulSoup, totals_data: defaultdict,
                 word_data: defaultdict, dates_data: defaultdict) -> (dict, dict, dict):

    # I am embedding these functions into the larger function here because
    # the alternative would be to pass the data dict each time that I call
    # the function to calculate a certain statistic if they were defined outside
    # this function. For example, each time I would like to call get_dates() to
    # update the dates_data dict, I would need to pass the dates_data dict as an
    # argument since the get_dates() function would not have access to the dict as
    # it is in an entirely separate namespace. The issue is that these are fairly
    # large dictionaries, and passing them several hundred (or several thousand)
    # times can slow down the program. By defining these functions within the
    # convo_totals() function, they are in the convo_totals() namespace and can
    # access and update the data dictionaries without needing them passing through
    # as arguments to the function, thus making the program a bit more efficient.

    def get_number_messages(sender: str) -> None:
        """ Updates the number of messages a person sent"""
        totals_data[name_conversion[sender]] += 1

    def get_number_words(message: str) -> None:
        """ Updates the number of keywords sent """
        if message:
            buffer = ""

            for char in message:
                if char.isalnum():
                    buffer += char.lower()
                else:
                    if buffer in words.words:
                        word_data[buffer] += 1
                    buffer = ""

    def get_dates(date: str) -> None:
        """ Updates the number of messages sent in a certain time """
        # Each date is passed through in the form MM/DD/YYYY HR:MN:SC
        month, year = date[:2], date[6:10]

        # For some reason the iMessage HTML file starts with "-------"
        # and it is tagged as a data, so this if statement deals with
        # that case.
        if not month.startswith('-'):
            formatted = year + "_" + month
            dates_data[formatted] += 1

    # The way the program gives me the iMessage data is very
    # weird. It is an HTML file, but the way they distinguish between whoever sent
    # a message is by giving one the class triangle-isosceles and the other the
    # class triangle-isosceles2, so that is what those represent. However, our
    # totals_data dict doesn't care about that, since it uses actual names to
    # store data. However, one of the keys in the dictionary will ALWAYS be my
    # full name, as it is ran through the Facebook Messenger algorithm first,
    # which stores my name as a dict key. Using this, we can simply use a variable
    # to store the value of the other person's name, and use this variable whenever
    # we need to index/update that person's message count.
    for person in totals_data.keys():
        if person != "Matthew Grosman":
            other_person = person

    # Store this information in a dictionary to make it easy to just index in the
    # get_number_messages() function like we did in the facebook statistics code.
    name_conversion = {'triangle-isosceles': other_person, 'triangle-isosceles2': "Matthew Grosman"}

    # All text messages are stored in a <p> tag, so we search for that, and filter
    # them down to the ones whose class is either date, triangle-isosceles, or
    # triangle-isosceles2. The way the program gives me the iMessage data is very
    # weird. It is an HTML file, but the way they distinguish between whoever sent
    # a message is by giving one the class triangle-isosceles and the other the
    # class triangle-isosceles2, so that is what those represent. The date class
    # is simply the date and time that a message was sent. All other classes were
    # irrelevant to this data collect and need not be considered. The 'message'
    # variable that we are assigning into each iteration is a Tag type from the
    # BeautifulSoup module.
    for message in imessage_soup.find_all('p', attrs={'class': ['date', 'triangle-isosceles', 'triangle-isosceles2']}):
        content = message.string

        # message['class'][0] represents the class. We need to use indexing since
        # message['class'] is technically a list, although it only contains one
        # item, at least in the context of this project and my testing.
        if message['class'][0] == 'date':
            get_dates(content)

        else:
            get_number_messages(message['class'][0])
            get_number_words(content)

    # Sort dates_data so the excel spreadsheet is nicely formatted
    dates_data = {k: v for k, v in sorted(dates_data.items())}
    return totals_data, dates_data, words.sort_dict(word_data)
