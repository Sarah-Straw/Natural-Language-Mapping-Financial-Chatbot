# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 16:47:12 2026

@author: Sarah Straw

"""


#==============================================================================
# Imports

import pandas as pd

#==============================================================================
# Organising data

file_path = 'GenAI/DataFile.xlsx'
df = pd.read_excel(file_path)

df['Total Revenue'] = df['Total Revenue'].replace({',': ''}, regex=True).astype(float)
df['Net Income'] = df['Net Income'].replace({',': ''}, regex=True).astype(float)

# data file had years in reverse order to how 'pct_change' interprets them, so must sort them
df = df.sort_values(['Company Name', 'Year']).reset_index(drop=True)
df.fillna(0, inplace=True)

# calculating revenue growth and net income growth
df['Revenue Growth (%)'] = df.groupby('Company Name')['Total Revenue'].pct_change() * 100
df['Net Income Growth (%)'] = df.groupby('Company Name')['Net Income'].pct_change() * 100

# making each compary have one index, within which is all their data

company_groups = {}
for i, (name, group) in enumerate(df.groupby('Company Name')):
# df.groupby('Company Name') collates the rows of each company
# enumerate produces a touple of the index and object, 
# then assigning i to index and assigning (name, group) to the name of 
# each group in df.groupby and the group itself which in this case is 
# the data frame for each company
    company_groups[i] = group.reset_index(drop=True)
    company_groups[i].fillna(0, inplace=True)

    
#==============================================================================
# Scanning functions

companies =  df['Company Name'].unique().tolist()

def company_scan(user_question):
    """
    Scans the prompt for what company is being asked about
    
    Parameters
    ----------
    user_question : prompt

    Returns
    -------
    company_i : index of company in 'companies' list
    None: if no company is in prompt,will trigger responce asking to
        specify which company
    """
    user_question = user_question.lower()
    for company_i, company in enumerate(companies):
        if company.lower() in user_question:
            return company_i
    else:
        return None

key_words = [ ' '.join(column.split()[:2]) for column in df.columns]
key_words[8] = 'Income Growth'
    
def key_word_scan(user_question):
    """
    Scans the prompt for the key word of what the user is looking for
    eg. revenue, growth, net income

    Parameters
    ----------
    user_question : users prompt

    Returns
    -------
    key_i: index of found key word in 'key_words' list

    """
    user_question = user_question.lower()
    for key_i, key_word in enumerate(key_words):
        if key_word.lower() in user_question:
            return key_i
    else:
        return None

# matches index of years in each 'company_groups' dataframe
years = df['Year'].unique() 

def year_scan(user_question):
    """
    Scans the prompt for the specified year they're asking about

    Parameters
    ----------
    user_question : users prompt

    Returns
    -------
    year_i: index of found year in 'years' list

    """
    user_question = user_question.lower()
    for year_i, year in enumerate(years):
        if str(year) in user_question:
            return year_i
    else:
        return None

def response(company_i, key_i, year_i):
    """
    Generates a responce to the user questions.

    Parameters
    ----------
    company_i : index of company being asked about
    key_i : index of key word being asked about
    year_i : index of year being asked about

    Returns
    -------
    responces dependent on which and what indexes are asked for
    
    """
    
    print("")
    print("--------------------------------------------------------")
    
    # None None None
    if company_i is None and key_i is None and year_i is None:
        print("")
        print("I can't provide any information about that.")

    # -- -- --
    if company_i is not None and key_i is not None and year_i is not None:
        print("")
        print(f"Great question! The {key_words[key_i].lower()} of {companies[company_i]} in {years[year_i]} was ${company_groups[company_i].iloc[year_i, key_i]} million dollars!")

    # -- -- None
    if company_i is not None and key_i is not None and year_i is None:
        print("")
        print(f"Great question! The {key_words[key_i].lower()} of {companies[company_i]} varies across the years:")
        print("")
        print("(in millions)")
        print("")
        for year_i in range(len(years)):
            
            # the column label in the df is 'Revenue Growth (%)'
            # instead of using the strings in the key_words list use the index 
            if key_i < 2:
                continue
            
            if company_groups[company_i].iloc[year_i, key_i] == 0:
                print(f"{years[year_i]}: (Not enough data)")
                print("")
                
            elif key_i > 6:
                print(f"{years[year_i]}: {round(company_groups[company_i].iloc[year_i, key_i], 2)} %")
                print("")    
                
            else:
                print(f"{years[year_i]}: ${company_groups[company_i].iloc[year_i,key_i]}")
                print("")
            
    # -- None --
    if company_i is not None and key_i is None and year_i is not None:
        print("")
        print(f"Great question! Here's the data on {companies[company_i]} in {years[year_i]}:")
        print("")
        print("(in millions)")
        print("")
        for key_i in range(len(key_words)):
            if key_i < 2:
                continue
            
            if (company_groups[company_i].iloc[year_i, key_i]) == 0:
                print(f"{key_words[key_i]}: Not enough data.")
                print("")
            
            elif key_i > 6:
                print(f"{key_words[key_i]}: {round(company_groups[company_i].iloc[year_i, key_i], 2)} %")
                print("")
        
                
            else:
                print(f"{key_words[key_i]}: ${company_groups[company_i].iloc[year_i, key_i]}")
                print("")

    # None -- --
    if company_i is None and key_i is not None and year_i is not None:
        print("")
        print(f"Great question! Here's the data on {key_words[key_i]} in {years[year_i]}:")
        print("")
        print("(in millions)")
        print("")
        for company_i in range(len(companies)):
            print(f"{companies[company_i]}:")
            print("")
            # the column label in the df is 'Revenue Growth (%)'
            # instead of using the strings in the key_words list use the index 
            if key_i < 2:
                continue
            
            if company_groups[company_i].iloc[year_i, key_i] == 0:
                print(f"{years[year_i]}: (Not enough data)")
                print("")
                
            elif key_i > 6:
                print(f"{round(company_groups[company_i].iloc[year_i, key_i], 2)} %")
                print("")    
                
            else:
                print(f"${company_groups[company_i].iloc[year_i,key_i]}")
                print("")
           

    # None None --
    if company_i is None and key_i is None and year_i is not None:
        print("")
        print(f"Great question! Here's the data from {years[year_i]}:")
        print("")
        print("(in millions)")
        print("")
        for company_i in range(len(companies)):
            print(f"{companies[company_i]}:")
            print("")
            for key_i in range(len(key_words)):
                if key_i < 2:
                    continue
                
                if (company_groups[company_i].iloc[year_i, key_i]) == 0:
                    print(f"{key_words[key_i]}: Not enough data.")
                    print("")
                
                elif key_i > 6:
                    print(f"{key_words[key_i]}: {round(company_groups[company_i].iloc[year_i, key_i], 2)} %")
                    print("")
            
                    
                else:
                    print(f"{key_words[key_i]}: ${company_groups[company_i].iloc[year_i, key_i]}")
                    print("")

    # None -- None
    if company_i is None and key_i is not None and year_i is None:
        print("")
        print(f"Great question! Here's the data on {key_words[key_i]}:")
        print("")
        print("(in millions)")
        print("")
        for company_i in range(len(companies)):
            print(f"{companies[company_i]}:")
            print("")
            for year_i in range(len(years)):
                
                if key_i < 2:
                    continue
                
                if company_groups[company_i].iloc[year_i, key_i] == 0:
                    print(f"{years[year_i]}: (Not enough data)")
                    print("")
                    
                elif key_i > 6:
                    print(f"{years[year_i]}: {round(company_groups[company_i].iloc[year_i, key_i], 2)} %")
                    print("")    
                    
                else:
                    print(f"{years[year_i]}: ${company_groups[company_i].iloc[year_i,key_i]}")
                    print("")
              
                
    # -- None None
    if company_i is not None and key_i is None and year_i is None:
        print("")
        print(f"Great question! Here's the data on {companies[company_i]}:")
        print("")
        print("(in millions)")
        print("")
        
        for year_i in range(len(years)):
            print(f"{years[year_i]}:")
            print("")
            for key_i in range(len(key_words)):
                if key_i < 2:
                    continue
                
                if (company_groups[company_i].iloc[year_i, key_i]) == 0:
                    print(f"{key_words[key_i]}: Not enough data.")
                    print("")
                
                elif key_i > 6:
                    print(f"{key_words[key_i]}: {round(company_groups[company_i].iloc[year_i, key_i], 2)} %")
                    print("")
            
                    
                else:
                    print(f"{key_words[key_i]}: ${company_groups[company_i].iloc[year_i, key_i]}")
                    print("")

    
#==============================================================================
# Prompt section

while True:
    
    print("")
    print("===========================================================")
    print("")
    print("Welcome to Sarah's financial chatbot!")
    print("")
    print("Ask a question about Apple, Tesla or Microsoft.")
    print(f"We can provide data on {', '.join(key_words[2:])} from years 2022, 2023 and 2024!")
    print("")
    print("To quit simply type 'quit'.")
    print("")
    
    user_question = input("Ask your question: ")

    # exit
    if user_question.lower() == "quit":
        break
    
    # scanning question
    company_i = company_scan(user_question)
    key_i = key_word_scan(user_question)
    year_i = year_scan(user_question)
    
    # responce generated
    response(company_i, key_i, year_i)



