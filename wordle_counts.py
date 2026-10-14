import string
from pathlib import Path
import pandas as pd

#--------------------------------------------------------------------------------------------
# Variables
#--------------------------------------------------------------------------------------------
letters = list(string.ascii_uppercase) #because assumption is that answers are in all caps
positions=['first', 'second', 'third', 'fourth', 'fifth']
vowels = ['A', 'E', 'I', 'O', 'U']
month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']
short_month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
directory = directory = Path(__file__).parent / 'data'
partial_file_name = ('*.txt')

#--------------------------------------------------------------------------------------------
# Function to find the answer file
#--------------------------------------------------------------------------------------------
def find_latest_file(dir, partial_file_name):
    files = [f for f in dir.iterdir() if f.is_file()]
    if files:
    # Get the file with the maximum modification time
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
    return latest_file

#--------------------------------------------------------------------------------------------
# Get the data from answer file
#--------------------------------------------------------------------------------------------
text_file_name = find_latest_file(directory, partial_file_name)
df= pd.read_csv(text_file_name)
all_answers = df['Answer'].to_list()

last_date_str = str(df['Year'].iloc[-1]) + '-' + str(df['Month'].iloc[-1]) + '-' + str(df['Date'].iloc[-1])

month_name_num = month_names.index(df['Month'].iloc[-1]) + 1
last_date_val = str(df['Year'].iloc[-1]) + '-' + f"{month_name_num:02}" + '-' + str(df['Date'].iloc[-1])

#--------------------------------------------------------------------------------------------
# Functions to get counts and navigate the df
#--------------------------------------------------------------------------------------------
def get_letter_counts(answers):
    letter_position_counts = [[0 for i in range(0,5)] for letter in letters]
    for word in answers:
        for i, letter in enumerate(word):
            letter_position_counts[letters.index(letter)][i] += 1
    return letter_position_counts

def get_puzzle_num(date_str):
    s = date_str.split('-')
    #print(s)
    year_val = int(s[0])
    date_val = int(s[2])
    month_val = month_names[int(s[1]) - 1]
    num = df.loc[(df['Year'] == year_val) & (df['Month'] == month_val) & (df['Date'] == date_val), 'Puzzle_Number'].values[0]
    return num

def get_answers_between_dates(start_date, end_date):
    num1 = get_puzzle_num(start_date)
    num2 = get_puzzle_num(end_date)
    custom_df = df.loc[(df['Puzzle_Number'] >= num1) & (df['Puzzle_Number'] <= num2), 'Answer']
    custom_answers = custom_df.tolist()
    return custom_answers

def get_answers_for_year(year_val):
    result_df = df.loc[(df['Year'] == year_val), 'Answer']
    answers = result_df.tolist()
    return answers

def get_all_answers():
    answers = df['Answer'].tolist()
    return answers

def get_puzzle_number(answer):
    result_df = df.loc[(df['Answer'] == answer), 'Puzzle_Number']
    puzzle_numbers = result_df.tolist()
    return puzzle_numbers

def get_dates_list(answer):
    date_df = df.loc[(df['Answer'] == answer)]
    date_str_list = []
    for row in date_df.itertuples():
        month_name_num = month_names.index(row.Month)
        date_str = str(row.Year)+f"{month_name_num:02}"+f"{row.Date:02}"
        date_str_list.append(date_str)
    return date_str_list

def get_counts_by_month_for_year(year_val, month_val):
    answers_df = df.loc[(df['Year'] == year_val) & (df['Month'] == month_val), 'Answer']
    answers = answers_df.tolist()
    letter_counts = get_letter_counts(answers)
    
    return letter_counts

def get_years():
    year_list = list(set(df['Year'].tolist()))
    return year_list

#--------------------------------------------------------------------------------------------
# Test the functions
#--------------------------------------------------------------------------------------------
'''
for year_val in [2021, 2022, 2023, 2024, 2025, 2026]:
    result_df = df.loc[(df['Year'] == year_val), 'Puzzle_Number']
    puzzle_nums = result_df.tolist()
    print(year_val, min(puzzle_nums), max(puzzle_nums))


a_list = get_all_answers()
for answer in a_list:
    if answer[0] == 'K':
        p_list = get_puzzle_number(answer)
        y_list = df.loc[(df['Answer'] == answer), 'Year'].tolist()
        print(answer, p_list,y_list)
'''
'''
#letters with no words that started with them
#by year
year_list = list(set(df['Year'].tolist())) #unique values for year
for year in year_list:
    a_list = get_answers_for_year(year)
    yearly_letter_counts = get_letter_counts(a_list)
    for index, letter_counts in enumerate(yearly_letter_counts):
        if letter_counts[0] == 0:
            print(year,letters[index])

'''
'''
#trend of words that start with a given letter
#over months
year_list = list(set(df['Year'].tolist())) #unique values for year
for year_val in year_list:
    year_df = df.loc[(df['Year'] == year_val)]
    for month_val in month_names:
        month_df = year_df.loc[(df['Month'] == month_val)]
        a_list = month_df['Answer'].tolist()
        #s_answers = [word for word in a_list if word[0] == 'S']
        letter_counts = get_letter_counts(a_list)
        print(year_val, month_val, letter_counts[letters.index('S')][0])
'''
'''
sept_2025_df = df.loc[(df['Year'] == 2025) & (df['Month'] == 'September')]
print(sept_2025_df)
'''

'''
print(get_dates_list('CIGAR'))
'''
'''
print(get_counts_by_month_for_year(2023, 'C'))
'''

#print(get_counts_by_month_for_year(2026, 'January'))
