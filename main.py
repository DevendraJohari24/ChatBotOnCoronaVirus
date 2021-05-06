import random
from newspaper import Article
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# download the punkt package
nltk.download('punkt', quiet=True)

#get the article
article = Article('https://en.wikipedia.org/wiki/Coronavirus')
article.download()
article.parse()
article.nlp()  #natural language processesing
corpus1 = article.text
article = Article('https://www.mayoclinic.org/diseases-conditions/coronavirus/symptoms-causes/syc-20479963')
article.download()
article.parse()
article.nlp()
corpus2 = article.text
corpus = corpus1 + corpus2
#print(corpus)

#tokenisation
test = corpus
sentence_list = nltk.sent_tokenize(test)
#print(sentence_list)

#Function to return a random greeting message to a user
def greet_res(text):
    text = text.lower()
    #bots greeting response
    bot_greetings = ['hello', 'hi', 'hey', 'wassup']
    #user greeting response
    user_greetings = ['hello','hi', 'hii', 'wassup','helloooo']

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


#Function to sort the index
def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0,length))
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                #swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index

#Function for create bot response
def bot_res(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_res = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    s_score = cosine_similarity(cm[-1],cm)
    s_score_list = s_score.flatten()  #convert to list
    #print(s_score_list)
    #sorting score with respect to index
    index = index_sort(s_score_list)
    index = index[1:]
    res_flag = 0
    j=0
    for i in range(len(index)):
        if s_score_list[index[i]] > 0.0:
            bot_res = bot_res + ' ' + sentence_list[index[i]]
            res_flag = 1
            j = j+1
        if j>2:
            break

    if res_flag == 0:
        bot_res = bot_res + 'I apologise that i have not understood your meaning . please be specific'

    sentence_list.remove(user_input)
    return bot_res
""" 
cosine_similarity response
0.0 -> 0% Match
1.0 -> 100% Match
"""

#start the chat
print('Covid Helpline: I am here to help you with the information regarding corona virus...If you want to exit type bye or exit')

exit_list = ['bye', 'exit', 'quit', 'byeee']
while(True):
    user_input = input()
    if user_input.lower() in exit_list:
        print('Bot: Thanks for your queries!. Stay Home Use Mask')
        break
    else:
        if greet_res(user_input) != None:
            print('Bot: ' + greet_res(user_input))
        else:
            print('Bot: '+ bot_res(user_input))