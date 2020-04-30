# Importing modules
import re
from nltk.corpus import wordnet
import json

# Building a list of Keywords
list_words=['joining']
list_syn={}
for word in list_words:
    synonyms=[]
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():
            # Remove any special characters from synonym strings
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
            synonyms.append(lem_name)
    list_syn[word]=set(synonyms)
 
#print (list_syn)

# Building dictionary of Intents & Keywords
keywords={}
keywords_dict={}

# Defining a new key in the keywords dictionary
keywords['joining_date']=[]

# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['joining']):
    keywords['joining_date'].append('.*\\b'+synonym+'\\b.*')

for intent, keys in keywords.items():
    # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
    keywords_dict[intent]=re.compile('|'.join(keys))

#print (keywords_dict)

def user_data(user_response):
    with open('dataset/{id}.json'.format(id = user_response)) as f:
        responses = json.load(f)
        return responses

# Generating response
def bot_response(user_response, valid_user, user_id):
    if user_response == 'quit':
        bot_response = {"message":"Thank you for visiting.", "user_id": None}

    if  valid_user == "false" and type(int(user_response)) == int:
        try:
            responses = user_data(user_response)
            bot_response =  {"message":"Hi " + responses['name'] + ". How can I help you?", "user_id": user_id}
        except:
            bot_response =  {"message":"Sorry, details not found!", "user_id": None}
    else:
        try:
            responses = user_data(user_id)
        except:
            bot_response =  {"message":"Sorry, details not found!", "user_id": None}
        matched_intent = None
        for intent, pattern in keywords_dict.items():
            # Using the regular expression search function to look for keywords in user input
            if re.search(pattern, user_response):
                # if a keyword matches, select the corresponding intent from the keywords_dict dictionary
                matched_intent=intent
        # The fallback intent is selected by default
        key='fallback'
        if matched_intent in responses:
            # If a keyword matches, the fallback intent is replaced by the matched intent as the key for the responses dictionary
            key = matched_intent
        # The chatbot prints the response that matches the selected intent
        bot_response = {"message":responses[key], "user_id": user_id}

    return bot_response