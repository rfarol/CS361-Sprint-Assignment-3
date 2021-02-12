import wikipedia
import csv

def search_wiki(primary, secondary):
    """search_wiki function takes a primary and secondary argument and uses the primary argument to search a Wikipedia
     page with the the primary argument as the title. It then takes the secondary argument, and searches a paragraph
     containing both primary and secondary arguments and outputs it. Uses the Wikipedia API to gather the web page"""
    page = wikipedia.page(primary) # finds the primary web page
    page = page.content # stores the entire webpage
    temp = page.split("==") # separates each section of the page to make search easier
    for section in temp: # iterate through each section
        if primary and secondary in section: # find both arguments
            return section.strip() # return paragraph


if __name__ == '__main__':
    file = "input.csv" # read csv file
    headers = [] # empty list for headers
    final = [] # final output for rows
    with open(file, "r", newline= "") as csvfile:
        csv_read = csv.reader(csvfile) # read csv file
        headers = next(csv_read) # input headers to the empty list
        headers.append("output_content")
        for row in csv_read: # iterate through each list
            for words in row: # iterate through each element of the list
                separate = words.split(";") # split the two words
                result = search_wiki(separate[0], separate[1]) # perform search on 1st and 2nd word of each list
                output = list(result.split(" ")) # combine results and turn output into a list
                output = [" ".join(output)] # format list
                combine = row + output # add the output to each row
                final.append(combine) # append each row to final output list
        outfile = "output.csv"
        with open(outfile, "w") as csvfile: # output a csv file containing new output
            csv_write = csv.writer(csvfile)
            csv_write.writerow(headers) # output header
            csv_write.writerows(final) # output row