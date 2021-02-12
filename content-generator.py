import wikipedia
import csv

def search_wiki(primary, secondary):
    page = wikipedia.page(primary)
    page = page.content
    temp = page.split("==")
    for section in temp:
        if primary and secondary in section:
            return section.strip()


if __name__ == '__main__':
    file = "input.csv"
    fields = []
    rows = []
    with open(file, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)


