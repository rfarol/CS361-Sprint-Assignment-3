from tkinter import *
import csv
import os.path
import pandas as pd

root = Tk()
root.title("Top Toys Searcher")
root.geometry("800x800")

category_paragraph_search = ["Hobbies", "Characters", "Fancy", "Dress", "Arts", "Crafts", "Bags", "Games", "Figures", "Playsets",
        "Home", "Accessories", "Sports", "Outdoor", "Die-Cast", "Vehicles", "Baby", "Toddler",
        "Electronic", "Robots", "Educational", "Puppets", "Theatres", "Jigsaws", "Puzzles", "Party",
        "Supplies", "Dolls", "Novelty", "Special Use"]

amazon_csv_headers = ["uniq_id", "output_item_name", "manufacturer", "price", "number_available_in_stock",
          "output_item_num_reviews", "number_of_answered_questions",
          "output_item_rating", "input_item_category", "customers_who_bought_this_item_also_bought",
          "description", "product_information", "product_description",
          "items_customers_buy_after_viewing_this_item",
          "customer_questions_and_answers", "customer_reviews", "sellers"]

GUI_dropdown_category = ["Hobbies", "Characters & Brands", "Fancy Dress", "Arts & Crafts", "Bags", "Games", "Figures & Playsets",
           "Home Accessories", "Sports Toys & Outdoor", "Die-Cast & Toy Vehicles", "Baby & Toddler Toys",
           "Electronic Toys > Robots", "Educational Toys", "Puppets & Puppet Theatres", "Jigsaws & Puzzles",
           "Party Supplies", "Sports Toys & Outdoor", "Dolls & Accessories",
           "Novelty & Special Use"]  # list of the categories


def create_list():
    with open('contentGenoutput.csv', 'r') as csv_file:
        local_data = csv.reader(csv_file)

        for i in range(2):  # move to the column and row with the paragraph
            next(local_data)

        for row in local_data:
            paragraph = row[1]

        paragraph_words = (paragraph.replace(',', '').split(" "))  # take out the commas in the paragraph
        category_LC, paragraph_LC = [], []

        for i in paragraph_words:  # make the paragraph and category list all lower case so we can compare them
            category_LC.append(i.lower())

        for i in category_paragraph_search:
            paragraph_LC.append(i.lower())

    return paragraph_LC, category_LC


def get_input():
    if os.path.exists('contentGenoutput.csv'):  # condition to check if there's a Content Generator output csv file
        generate = 10
        create_list()
        count = 0
        paragraph_LC, category_LC = create_list()

        for i in paragraph_LC:
            count += 1

            for j in category_LC:
                if i == j:  # if category term exist in the paragraph then set it as category
                    category = category_paragraph_search[count - 1]
                    break

    else:
        category = clicked.get()  # else we get our values from tkinter
        generate = int(num.get())

    return category, generate


def get_data():
    category, generate = get_input()
    with open('amazon_co-ecommerce_sample.csv', 'r', encoding="utf8") as csv_file:
        local_data = csv.reader(csv_file)
        category_match = []

        for line in local_data:
            if category in line[8]:  # add the rows that match the category
                if any(line[5]):
                    category_match.append(line)

        for line in category_match:
            if "," in line[5]:  # delete the comma in the for the numbers in amount of reviews
                new_num = (line[5].replace(',', ''))
                line[5] = new_num

        range_list = len(category_match)

    return range_list, category_match, generate


def bubble_sort_helper(column_num, range_list, list_new, int_boolean):
    for i in range(0, range_list):
        for j in range(0, range_list - i - 1):

            if int_boolean == 1:
                curr_str = list_new[j][column_num]
                next_str = list_new[j + 1][column_num]

            elif int_boolean == 0:
                curr_str = int(list_new[j][column_num])  # turn all the string in amount of reviews to integers
                next_str = int(list_new[j + 1][column_num])

            if curr_str < next_str:
                temp = list_new[j]
                list_new[j] = list_new[j + 1]
                list_new[j + 1] = temp

    return list_new


def start_sort(range_list, category_match_list, generate):
    category_match_list = bubble_sort_helper(0, range_list, category_match_list, 1)
    category_match_list = bubble_sort_helper(5, range_list, category_match_list, 0)

    if range_list < generate:  # when user select a input a number greater than actual toys on the list
        # print out how many there is on the list
        generate = range_list

    double_list = generate * 10
    new_list, final_list = [], []

    for i in category_match_list[0:double_list]:
        new_list.append(i)

    new_range = len(new_list)

    new_list = bubble_sort_helper(0, new_range, new_list, 1)
    new_list = bubble_sort_helper(7, new_range, new_list, 1)

    for i in new_list[0:generate]:     # final list is the list with the sorted elements and with the number generated
        final_list.append(i)

    return final_list


def output_CSV(generate, final_list):
    toy_col = []
    generate_col = []

    for i in range(generate):
        toy_col.append("toys")         # create the type column and number to generate
        generate_col.append(generate)

    df = pd.DataFrame(final_list, columns=amazon_csv_headers)  # add new columns to df
    df["input_item_type"] = toy_col
    df["input_number_to_generate"] = generate_col
    df.to_csv("output.csv", columns=["input_item_type", "input_item_category", "input_number_to_generate",
                                     "output_item_name", "output_item_rating",
                                     "output_item_num_reviews"])  # outputs to csv


def create_row_helper(row_info, row, col_slice_1, col_slice_2):
    for info in row[col_slice_1:col_slice_2]:
        row_info.append(str(info))

    return row_info


def print_GUI(generate, final_list):
    header_titles = ["input_item_type", "input_item_category", "input_number_to_generate", "output_item_name",
                     "output_item_rating", "output_item_num_reviews"]  # list of headers that is at the top
    header = [str(i) for i in header_titles]
    myLabel = Label(root, text=header)  # this outputs the headers to the GUI
    myLabel.pack()

    for row in final_list:  # this loop creates the rows with information to the GUI
        row_info = []

        row_info.append(str("Toys"))

        create_row_helper(row_info, row, 8, 9)

        row_info.append(str(generate))

        create_row_helper(row_info, row, 1, 2)

        create_row_helper(row_info, row, 7, 8)

        create_row_helper(row_info, row, 5, 6)

        myLabel = Label(root, text=row_info)
        myLabel.pack()       # outputs the row into the GUI


def main_generator():
    range_list, category_match_list, generate = get_data()
    final_list = start_sort(range_list, category_match_list, generate)

    output_CSV(generate, final_list)            # call our functions to output csv and to GUI

    if os.path.exists('content-generator.py'):
        from subprocess import call
        call(["python", "content-generator.py"])

    if os.path.exists('contentGenoutput.csv'):  # if we have an input csv then we skip building the GUI
        exit()

    print_GUI(generate, final_list)


if os.path.exists('contentGenoutput.csv'):
    main_generator()

else:
    Ask_Num = Label(root, text="Please enter the size of the list: inside the box: ")
    Ask_Type = Label(root, text="Please select a category from the dropbox: ")
    Ask_Type.pack()

    clicked = StringVar()   # create our drop down menu
    clicked.set(GUI_dropdown_category[0])
    drop = OptionMenu(root, clicked, *GUI_dropdown_category)
    drop.pack(pady=10)

    Ask_Num.pack()          # create our input box
    num = Entry(root, width=10)
    num.pack(pady=10)

    myButton = Button(root, text="Click to show list and output CSV", command=main_generator).pack(
        pady=10)            # set the button to start the function to output csv and print to GUI
    root.mainloop()
