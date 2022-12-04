import json
import openai 
import sys 
import os 
import argparse 

API_KEY = "key here" 
parser = argparse.ArgumentParser(description = "User query")
parser.add_argument("query", type = str, help="An a query inputted by the user.")
parser.add_argument("option", type = str, help="""
        (A): Point me to a future lecture where I will see this. 
        (B): Summarize previous content I have seen.
        (C): A basic query.
        (D): Summarize future content I will see.
        (E): Point me to the previous lecture where I have seen this content.""")


class HistoricalData:
    def __init__(self, initial_prompt):
        self.historical_context = initial_prompt

    def update_history(self, new_context):
        self.historical_context = new_context

def get_answer_step_1(query: str):
    openai.api_key = API_KEY
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
    return str(vals["choices"][0]["text"]).replace("->", "").strip()

def elasticsearch_output():
    return "WORD", "CONTEXT", "OBJECT_TYPE" # search term, context windown around the term, video lecture or lecture ? 

# get_answer_step_2
def process_option(query, option, previous_history, term, context, title) -> str:
    if option == "A":
        return "You saw this content in {}".format(title)
    if option == "B":
        prompt = f"Given this context: {context}, explain the use of the term: {term}."
        return process_GPT(prompt, "") # no history
    if option == "C":
        return process_GPT(query, previous_history)
    if option == "D":
        prompt = f"Given this context: {context}, explain the use of the term: {term}."
        return process_GPT(prompt, "") # no history 
    if option == "E":
        return "You saw this content in {}".format(title)
    return process_GPT(query, previous_history)

def process_GPT(prompt: str, previous_history: str):
    openai.api_key = API_KEY
    vals=openai.Completion.create(model = "text-davinci-002",
        prompt=previous_history + "\n\n" + prompt,
        max_tokens=100,
        temperature=0
    )   
    return vals["choices"][0]["text"]

# explanation
def initial_gpt(term, context):
    openai.api_key = API_KEY
    vals=openai.Completion.create(model = "text-davinci-002",
        prompt=f"Given the context: {context}, what is the meaning of the term {term}",
        max_tokens=100,
        temperature=0
    )   
    return vals["choices"][0]["text"]

if __name__=="__main__":
    history = HistoricalData("")

    openai.api_key = API_KEY
    args = parser.parse_args()
    option = args.option 
    query = args.query
    print(process_option(query,option,""))