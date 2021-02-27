import wikipediaapi
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter.filedialog import askopenfile



root = tk.Tk()
def search_wiki(primary, secondary):
    """search_wiki function takes a primary and secondary argument and uses the primary argument to search a Wikipedia
       page with the the primary argument as the title. It then takes the secondary argument, and searches a paragraph
       containing both primary and secondary arguments and outputs it. Uses the Wikipedia API to gather the web page html
       page. After, Beautiful Soup is used to parse through the html to separate the paragraphs. Then, the primary
       and secondary searches are implemented. Paragraph is outputted into a text box. Contains inner function:
       def OutputCSV()"""
    find_html = wikipediaapi.Wikipedia(
            language="en",
            extract_format=wikipediaapi.ExtractFormat.HTML
    )
    page_html = find_html.page(primary) # find HTML page with the primary word
    raw = page_html.text # store raw HTML
    soup = BeautifulSoup(raw, 'html.parser') # parse through HTML with Beautiful Soup
    paragraph_list = [] # intialize empty list
    for paragraph in soup.find_all('p'): # separate paragrpahs and add to list
        paragraph_list.append(paragraph)
    prim_lower = primary.lower()
    sec_lower = secondary.lower()
    for search in paragraph_list: # search for paragraph with primary and secondary word
        if prim_lower and sec_lower in search.text.lower():
            result = search.text # if both found, return output
            text_box = tk.Text(root, height=10, width=50, padx=15, pady=15)
            text_box.insert(1.0, result)
            text_box.grid(column=1, row=7)
            # download file button
            download_button = tk.Button(root, text="Download CSV", command=lambda:outputCSV(), font="Arial", bg="orange", height=1, width=12)
            download_button.grid(column=1, row=8)
            def outputCSV():
                """This function outputs the result into a csv file if the download button is pressed"""
                headers = []
                headers.append("input_keywords")
                headers.append("output_content")
                row = []
                row.append(primary + ";" + secondary)
                row.append(result)
                outfile = "contentGenoutput.csv"
                with open(outfile, "w") as csvfile:  # output a csv file containing new output
                    csv_write = csv.writer(csvfile)
                    csv_write.writerow(headers)  # output header
                    csv_write.writerow(row)  # output row

def getCSV():
    """getCSV function reads a CSV file that is uploaded from the user and calls search_wiki function once the primary
    and secondary words are found"""
    file = askopenfile(parent=root, mode="r", title="Choose a file", filetype=[("Csv file", "*.csv")])
    if file is not None:
        headers = []  # empty list for headers
        csv_read = csv.reader(file)  # read csv file
        headers = next(csv_read)  # input headers to the empty list
        if len(headers) > 2:
            temp_1 = []
            temp_2 = []
            primary_list = []
            secondary_list = []
            for columns in csv_read:
                temp_1.append(columns[2])
                temp_2.append(columns[4])
            for item in temp_1:
                separate = item.split(" > ")
                primary = separate[1]
                primary_list.append(primary)
            for item in temp_2:
                secondary = item.split()
                secondary_list.append(secondary)
            secondary_revised = [item for sublist in secondary_list for item in sublist]
            prim_counter = 0
            sec_counter = 0
            while prim_counter <= len(primary_list)-1:
                result = search_wiki(primary_list[prim_counter], secondary_revised[sec_counter])
                sec_counter += 1
                if sec_counter <= len(secondary_revised):
                    prim_counter += 1
                    sec_counter = 0
                if result != None:
                    break
        for row in csv_read:  # iterate through each list
            for words in row:  # iterate through each element of the list
                separate = words.split(";")  # split the two words
                result = search_wiki(separate[0], separate[1])  # perform search on 1st and 2nd word of each list"""

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=8)

# instructions 1
instructions_1 = tk.Label(root, text="Look Me Up!", font="Arial")
instructions_1.grid(column=1, row=0)

# instructions 2
instructions_2 = tk.Label(root, text="Please enter a primary and secondary search word below!", font="Arial")
instructions_2.grid(column=1, row=1)

# primary entry
p_entry = tk.Entry(root, font=40)
p_entry.grid(column=1, row=2)

# secondary entry
s_entry = tk.Entry(root, font=40)
s_entry.grid(column=1, row=3)

# generate button
generate_button = tk.Button(root, text="Generate Search", font=50, bg="orange", command=lambda: search_wiki(str(p_entry.get()), str(s_entry.get())))
generate_button.grid(column=1, row=4)

#instructions 3
instructions_3 = tk.Label(root, text="OR you can input your own CSV file!", font="Arial")
instructions_3.grid(column=1, row=5)

# search file button
select_button = tk.Button(root, text="Search File", command=lambda:getCSV(), font="Arial", bg="orange", height=1, width=10)
select_button.grid(column=1, row=6)

root.mainloop()