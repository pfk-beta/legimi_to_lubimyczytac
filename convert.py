import json
import csv
from datetime import datetime

LEGIMI_TO_LC_RATING_MULTIPLIER = 2
LC_DATE_FORMAT = "%Y/%m/%d"

# legimi.json - jar xvf data.zip; cat data.json| jq > legimi.json

with open('legimi.json') as input_f:
    content = json.load(input_f)

legimi_stats = dict()
for index, top_entry in enumerate(content):
    title = list(top_entry.keys())[0]
    print(title)
    legimi_stats[title] = index

book_stats = content[legimi_stats['book_stats']]['book_stats']
# from ipdb import set_trace; set_trace()

csv_header = [
    "Book Id",
    "Title",
    "Author",
    "Author l-f",
    "Additional Authors",
    "ISBN", # 5
    "ISBN13",
    "My Rating", # 7
    "Average Rating",
    "Publisher",
    "Binding",
    "Number of Pages",
    "Year Published",
    "Original Publication Year",
    "Date Read", # 14
    "Date Added",
    "Bookshelves",
    "Bookshelves with positions",
    "Exclusive Shelf",
    "My Review", # 19
    "Spoiler",
    "Private Notes",
    "Read Count", # 22
    "Owned Copies",
]

def book_to_csv(book):
    INDEX_TITLE = 1
    INDEX_MY_RATING = 7
    INDEX_DATE_ADDED = 15
    INDEX_DATE_READ = 14
    csv_row = len(csv_header) * ['']
    title = book['book']
    csv_row[INDEX_TITLE] = title
    if 'rating' in book:
        csv_row[INDEX_MY_RATING] = book['rating'] * LEGIMI_TO_LC_RATING_MULTIPLIER
    csv_row[INDEX_DATE_ADDED] = datetime.fromisoformat(book['start_date']).date().strftime(LC_DATE_FORMAT)
    if 'end_date' in book:
        csv_row[INDEX_DATE_READ] = datetime.fromisoformat(book['end_date']).date().strftime(LC_DATE_FORMAT);

    return csv_row

with open('import_biblioteczki_do_LC_wzor_pliku.csv', newline='') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read())


ids_to_eksport = [30, 35]

with open('lubimyczytac.csv', 'w') as output:
    print(dialect)
    csv_writer = csv.writer(output, dialect=dialect)
    csv_writer.writerow(csv_header)
    for book_id in ids_to_eksport:
        book = book_stats[book_id]
        print(book)
        csv_writer.writerow(book_to_csv(book))
