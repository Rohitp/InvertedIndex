from nltk import FreqDist
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from pathlib import Path
from collections import defaultdict
import pickle, json

FILE_PATH = "savedata.json"
INDEX_PATH = "index.json"

def process(data):
    hashKey = storeData(data)
    returnedIndex = createIndex(data, hashKey)
    return returnedIndex


#  Handles the stemming and cleaning
def procesText(textstring):
    strippedString = "".join(c for c in textstring if c not in ('!','.',',','?'))
    wordlist = strippedString.strip().lower().split()

    # Stem the words 
    # Then use a part of speech tagger
    # Then lemmatize the verbs
    # Calculate the final frequency

    wordNetLemmatizer = WordNetLemmatizer()
    porterStemmer = PorterStemmer()
    stemmedTaggedWords = FreqDist([porterStemmer.stem(word) for word in wordlist if word not in stopwords.words('english')])
    return stemmedTaggedWords

# creates the inverted index
def createIndex(data, hashkey):
    
    # indexData = defaultdict(lambda: defaultdict(dict))didn't work. Must find out why
    indexData = readDataFromFile(INDEX_PATH)
    
    
    for k, v in data.items():
        if(isinstance(v, str)):
            stemmedTaggedWords = procesText(v)
            for key, value in stemmedTaggedWords.items():
                if key in indexData:
                    if k in indexData[key]:
                        indexData[key][k][hashkey] = value
                    else:
                        indexData[key][k] = {}
                        indexData[key][k][hashkey] = value
                else:
                    indexData[key] = {}
                    indexData[key][k] = {}
                    indexData[key][k][hashkey] = value

    
    with open(INDEX_PATH, "w") as indexFile:
        json.dump(indexData, indexFile)


    return indexData 
    # return stemmedTaggedWords

def readDataFromFile(path):
    storageFile = Path(path)
    dataFromFile = {}
    if storageFile.is_file():
        with open(path, 'r') as file:
            try:
                dataFromFile = json.load(file)
            except:
                dataFromFile = {}
            
        file.close()

    else:
        dataFromFile = {}

    return dataFromFile;            
    

def storeData(data):
    dataFromFile = readDataFromFile(FILE_PATH)
    hashKey = str(id(data))
    dataFromFile[hashKey] = data
    with open(FILE_PATH, 'w') as file:
        json.dump(dataFromFile, file)

    file.close()

    return hashKey;


def processSearch(searchString):
    indexDataFromFile = readDataFromFile(INDEX_PATH)
    searchString = searchString.strip().lower().split()
    searchOn = ""
    avoid = ""
    for i in searchString:
        if i.startswith("on:"):
            searchOn = i[3:]
            searchString.remove(i)
        if i.startswith("not:"):
            avoid = i[4:]
            searchString.remove(i)
        
    porterStemmer = PorterStemmer()
    stemmedWords = [porterStemmer.stem(word) for word in searchString if word not in stopwords.words('english')]
    files = {}
    result = []
    for i in stemmedWords:
        if i in indexDataFromFile:
            length = 0;
            for metaTitle, metaDict in indexDataFromFile[i].items():
                if searchOn != "" and metaTitle != searchOn:
                    continue
                if avoid != "" and metaTitle == avoid:
                    continue
                for hashval, num in indexDataFromFile[i][metaTitle].items():
                    if hashval in files:
                        files[hashval] += num
                    else:
                        files[hashval] = num

    
    if (bool(files)):
        dataFromFile = readDataFromFile(FILE_PATH)
        for hashval, num in files.items():
            dataFromFile[hashval]["weight"] = num
            result.append(dataFromFile[hashval]) 

        result = sorted(result, key=lambda k: k['weight'], reverse=True)
        print(result)
        return result

    return {"code": -1, "message": "NO_RESULTS_FOUND"}


# incomplete. unused
#  formula from here
#  http://www.tfidf.com/
def inverseDocmentfrequency(data):
    # Not using lexical diversity 
    # a very useful parameter to look into to determine text corpus importance
    lexicalDiversity = len(set(data)) / len(data)
    result = {}
    totalCount = len(data)
    words = list(set([word for item in contents for word in contents[item].split()]))

    for i, word in enumerate(words):
        cnt = sum([1 for item in contents if word in contents[item]])
        idf = math.log(totalCount / cnt)
        result[word] = idf

    print result
                
            
    
