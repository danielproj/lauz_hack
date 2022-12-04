import json
import openai 
import sys 
import os 
import argparse 

API_KEY = "key here" 
parser = argparse.ArgumentParser(description = "User query")
parser.add_argument("query", type = str, help="An a query inputted by the user.")

if __name__=="__main__":
    openai.api_key = API_KEY
    query = parser.parse_args().query
    print(query)

    vals = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"""
        Which one of the following questions best matches this query: 'Is the meaning of a horse included?'?\n\n
        (A): Point me to a future lecture where I will see this. 
        (B): Summarize previous content I have seen.
        (C): A basic query.
        (D): Summarize future content I will see.
        (E): Point me to the previous lecture where I have seen this content.
        -> C
        Which one of the following questions best matches this query: 'Explain to me previous times I have seen this content?'?\n\n
        (A): Point me to a future lecture where I will see this. 
        (B): Summarize previous content I have seen.
        (C): A basic query.
        (D): Summarize future content I will see.
        (E): Point me to the previous lecture where I have seen this content.
        -> B
        Which one of the following questions best matches this query: '{query}'?\n\n
        (A): Point me to a future lecture where I will see this. 
        (B): Summarize previous content I have seen.
        (C): A basic query.
        (D): Summarize future content I will see.
        (E): Point me to the previous lecture where I have seen this content.
        """,
        max_tokens=30,
        temperature=0
    )   
    print(query, vals["choices"][0]["text"]) # query -> sent in, vals["choices"][0]["text"]: -> B