"""
main.py

Mustafa Branch

Thursday, May 18, 2023

"""
from dotenv import load_dotenv
from classes import EntryMaker, LoopScraper
import openai, os, transform
import datetime

def main():
    
    load_dotenv('.env')
    
    loop_html = LoopScraper() # Can pass username and password as params, otherwise will use .env file to source
    entrymaker = EntryMaker(loop_html.get_source()) # Creates an EntryMaker object from html of passed loop page
    entries = entrymaker.make_entries() # Creates a list of Entry objects from the loop
    
    openai.organization = os.getenv("ORG_ID")
    openai.api_key = os.getenv("API_KEY")
    
    weekly_summary = transform.create_summary(entries) # Creates a weekly summary from the list of Entry objects
    
    #Write to file and save
    with open(f"./documents/Weekly summary {datetime.date.today()}.txt", "x") as file:
        file.write(weekly_summary)
        
    print("Summary written to file.")
            
if __name__ == "__main__":
    main()