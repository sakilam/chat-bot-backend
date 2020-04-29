#import libraries
from newspaper import Article
import random
import string 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt', quiet=True) # Download the punkt package
nltk.download('wordnet', quiet=True) # Download the wordnet package

#Get the article URL
article = Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
article.download() #Download the article
article.parse() #Parse the article
article.nlp() #Apply Natural Language Processing (NLP)
corpus = article.text #Store the article text into corpus

#Tokenization
text = corpus
sent_tokens = nltk.sent_tokenize(text)# txt to a list of sentences 

# Keyword Matching#Greeting input from the user
GREETING_INPUTS = ["hi", "hello",  "hola", "greetings",  "wassup","hey"] #Greeting responses back to the user
GREETING_RESPONSES = ["howdy","hi", "hey", "what's good",  "hello","hey there"]#Function to return a random greeting response to a users greeting
def greeting(sentence):
   #If user's input is a greeting, return a randomly chosen greeting response
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

#Create a dictionary (key:value pair) to remove punctuations  
remove_punct_dict = dict(  (ord(punct), None) for punct in string.punctuation)

#Create a function to return a list of lemmatized lower case words after removing punctuations 
def LemNormalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punct_dict))

# Generating response
def response(user_response):
    robo_response='' #Create an empty response for the bot
    sent_tokens.append(user_response) #Append the users response to the list of sentence tokens
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english') 
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    score = flat[-2]
    if(score==0):
        robo_response=robo_response+"I apologize, I don't understand."
    else:
        robo_response = robo_response+sent_tokens[idx]    
    
    sent_tokens.remove(user_response) 
       
    return robo_response
