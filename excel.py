# excel.py
# This module contains the function to write data to an excel spreadsheet


import xlsxwriter
from pathlib import Path
import os


def write_to_excel(d: dict, data: str, name: str):
    """ Writes dictionary data to an excel spreadsheet """
    if not Path(f'/Users/matthew/Documents/Message Data/{name}/excel/').exists():
        os.mkdir(Path(f'/Users/matthew/Documents/Message Data/{name}/excel/'))

    workbook = xlsxwriter.Workbook(f'/Users/matthew/Documents/Message Data/{name}/excel/{name}_{data}.xlsx')
    worksheet = workbook.add_worksheet()

    for i, (key, value) in enumerate(d.items()):
        worksheet.write(0, i, key)
        worksheet.write(1, i, value)

    workbook.close()
