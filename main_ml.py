import numpy as np
import wikipedia as wiki
import nltk
nltk.download('punkt')
from nltk import tokenize
import datetime
import gensim 

from nlp_parser import temporal

def date_key(a):
    """
    a: date as string
    """
    if a:
        a = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S').date()
        return a
    else: 
        return None
        
import re #Regex (Regualar Expr Operations)
import gensim

########Function to remove All the punctuations from the text
def strippunc(data):
    p = re.compile(r'[?|!|\'|"|#|.|,|)|(|\|/|~|%|*|;|_|:|–|\[|\]]')
    return p.sub('',data)

def word_embed(results):
    final_string=[]
    for sent in tokenize.sent_tokenize(results):
        filtered_sentence=[]
        sent=strippunc(sent)# remove Punctuation Symbols
        sent = sent.lower()
        sentence=[]
        for word in sent.split():
            sentence.append(word)
        final_string.append(sentence)
    # print(final_string)
        
    #Training own Word2Vec model using your own text corpus
    w2v_model=gensim.models.Word2Vec(final_string,min_count=1,size=10, workers=-1)
    #min-count: Ignoring the words which occurs less than 1 times
    #size:Creating vectors of size 10 for each word
    #workers: Use these many worker threads to train the model (faster training with multicore machines)
    
    w2v_model.save('w2vmodel')#Persist/Saving the model to a file in the disk


def timeline_sentences(query,n=10):
    #Getting the first result from Wikipedia
    article = wiki.search(query, results=1, suggestion=False)
    
    #If Article exists
    if article:
        results = wiki.summary(article[0], sentences=0, chars=0, auto_suggest=True, redirect=True)
        
        #Creating Word Embeddings
        word_embed(results)
        #Loading Word Embedding from file
        
        w2v_model = gensim.models.Word2Vec.load('w2vmodel')

        sortable_articles =[]
        unsortable_articles =[]
        for index,result in enumerate(tokenize.sent_tokenize(results)):
            dates = sorted(temporal(result), key=date_key)
            if dates:
                final = dates[0]
                sortable_articles.append({"sent":result,"dates":dates,"final":final})
            else:
                unsortable_articles.append({"sent":result})

        sortable_articles = sorted(sortable_articles,key= lambda k:date_key(k["final"]))
        articles = sortable_articles + unsortable_articles
        
        final_array =[]
        for index,article in enumerate(articles[:n],1): 
            # if "dates" in article:
                # print(article["dates"])
                # print(article["final"])
            # else:
                # print("None")
                

            # print("Sentence",index,":",article["sent"])
            
            sent_vec = np.zeros(10)
            #If there is only single word in sentence
            if " " not in result:
                try:
                    sent_vec = w2v_model.wv[result]
                except:
                    pass
            #If result is sentence
            else:    
                for word in result.split():
                    try:
                        vec = w2v_model.wv[word]
                        sent_vec += vec
                    except:
                        continue
#                     print(word)
            # print("Embedding:",sent_vec,"\n")
            final_dict = {"date":article["final"],
                        "dates":str(article["dates"]),
                        "word_embed":str(sent_vec),
                         "sent":article["sent"]}
            final_array.append(final_dict)
        # final_value = {"data":final_array}
        # w2v_vocub = w2v_model.wv.vocab
        # print(len(w2v_vocub))
        # print(final_array)
        # final_array = np.array(final_array)
        # .tolist()
        return final_array
    else:
        return {"data":[]}
        #If there is no article
        # print("No results found!")

# timeline_sentences("Gandhi",5)
# w2v_vocub = w2v_model.wv.vocab
# len(w2v_vocub)