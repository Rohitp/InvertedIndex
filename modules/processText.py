from nltk import FreqDist
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from pathlib import Path
from collections import defaultdict
import pickle, json

# Saving as dat file. Habit from C days
FILE_PATH = "savedata.dat"
INDEX_PATH = "index.dat"

def process(data):
        
    hashKey = storeData(data)
    returnedIndex = createIndex(data, hashKey)
    return returnedIndex
    # return stemmedTaggedWords


# TODO: Remove punctuation
def procesText(textstring):
    wordlist = textstring.strip().lower().split()

    # Stem the words 
    # Then use a part of speech tagger
    # Then lemmatize the verbs
    # Calculate the final frequency

    wordNetLemmatizer = WordNetLemmatizer()
    porterStemmer = PorterStemmer()
    stemmedTaggedWords = FreqDist([porterStemmer.stem(word) for word in wordlist if word not in stopwords.words('english')])
    return stemmedTaggedWords

def createIndex(data, hashkey):
    
    indexData = readDataFromFile(INDEX_PATH)
    if(not bool(indexData)):
        print("no data")
        indexData = defaultdict(lambda: defaultdict(dict))
    
    for k, v in data.items():
        if(isinstance(v, str)):
            stemmedTaggedWords = procesText(v)
            for key, value in stemmedTaggedWords.items():
                indexData[key][k][hashkey] = value

    
    with open(INDEX_PATH, "wb+") as indexFile:
        pickle.dump(indexData, indexFile)


    return indexData 
    # return stemmedTaggedWords

def readDataFromFile(path):
    storageFile = Path(path)
    dataFromFile = {}
    if storageFile.is_file():
        with open(path, 'rb') as file:
            try:
                dataFromFile = pickle.load(file)
            except:
                dataFromFile = {}
            
        file.close()

    else:
        dataFromFile = {}

    return dataFromFile;            
    

def storeData(data):
    dataFromFile = readDataFromFile(FILE_PATH)
    hashKey = id(data)
    dataFromFile[hashKey] = data
    # print(dataFromFile)
    with open(FILE_PATH, 'wb+') as file:
        pickle.dump(dataFromFile, file)

    file.close()

    return hashKey;
    
