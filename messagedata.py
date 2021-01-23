# messagedata.py
# This is the main module to get message data for a conversation
# This program gets Facebook Messenger and iMessage data and then
# uses that data to provide some statistics and write those to an
# excel spreadsheet.


import fb_stats
import excel
import calculations
import graph
import printing
import file_handling
import imessage_stats


if __name__ == "__main__":
    conversation, name = file_handling.get_facebook_messages()

    totals_data, dates_data, word_data = fb_stats.convo_totals(conversation)

    imessage_soup = file_handling.get_imessage(name)
    totals_data, dates_data, word_data = imessage_stats.convo_totals(imessage_soup, totals_data, word_data, dates_data)

    #graph.dict_to_graph(totals_data, "Totals", name)
    #graph.dict_to_graph(dates_data, "Date", name)
    #graph.dict_to_graph(word_data, "Word", name)

    excel.write_to_excel(totals_data, "totals", name)
    excel.write_to_excel(dates_data, "dates", name)
    excel.write_to_excel(word_data, "words", name)

    stats = calculations.get_statistics(totals_data, word_data, dates_data)

    printing.print_stats(stats, totals_data, dates_data)
