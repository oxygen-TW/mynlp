import re 

class Dictionary:
    def __init__(self, corpusPath="myfile.utf8"):
        self.__regularExpressionRule = re.compile(r"[^a-zA-Z0-9\u3000\u4e00-\u9fa5]")
        self.__totalTimeInOneGram = 0 ;
        self.__totalTimeInTwoGram = 0 ;
        self.__oneGramDict  = {}
        self.__twoGramData = {}
        self.__setup_dict(corpusPath)

    def __contains__(self, key):
        return (key in self.__oneGramDict)   
    def get_Word_Frequency(self, word):
        frequency = self.__oneGramDict.get(word)
        if frequency is not None:
            return frequency
        return 0  
    def get_TwoGram_Frequency(self,firstWord, secondWord):
        twoGram = firstWord+"#"+secondWord
        frequency = self.__twoGramData.get(twoGram)
        if frequency is not None:
            return frequency
        return 0  

    def get_Corpus_TotalTime(self):
        return self.__totalTimeInOneGram 
    def logger_Print(self):
        for key, value in self.__oneGramDict.items():
            print(key, value)
        for key, value in self.__twoGramData.items():
            print(key, value)    
        return

    """  下面的 Method 為 build-in 
    """
    def __setup_dict(self,corpusPath):
        sentenceList = self.__analyze_Corpus(corpusPath)
        self.__generate_OneGram(sentenceList)
        self.__generate_TwoGram(sentenceList)

    def __remove_puncation(self,word):
        return self.__regularExpressionRule.sub("", word);
    def __analyze_Corpus(self,corpusPath):
        file = open(corpusPath,'r', encoding='UTF-8')
        fileContent = file.read()
        fileContent = fileContent.split("\n")
        sentenceList = []
        for sentence in fileContent:
            sentence = self.__remove_puncation(sentence)
            sentence = sentence.split()
            if len(sentence) >= 1:
                sentenceList.append(sentence)
        self.__oneGramDict.setdefault("BOS", len(sentenceList))
        self.__oneGramDict.setdefault("EOS", len(sentenceList))    
        return sentenceList    

    def __generate_OneGram(self,sentenceList):
        for sentence in sentenceList:
            for word in sentence:
                self.__totalTimeInOneGram = self.__totalTimeInOneGram + 1 
                if word in self.__oneGramDict:
                    self.__oneGramDict[word] = self.__oneGramDict[word]+1
                else:    
                    self.__oneGramDict.setdefault(word, 1)   
    def __generate_TwoGram(self, sentenceList):
        for sentence in sentenceList:
            if(len(sentence)==1):
                twoGram = "BOS#"+sentence[0]
                if twoGram in self.__twoGramData :
                    self.__twoGramData[twoGram]=self.__twoGramData[twoGram]+1
                else :
                    self.__twoGramData.setdefault(twoGram,1)
                twoGram = sentence[0]+"#EOS"
                if twoGram in self.__twoGramData :
                    self.__twoGramData[twoGram]=self.__twoGramData[twoGram]+1
                else :
                    self.__twoGramData.setdefault(twoGram,1)
                self.__totalTimeInTwoGram = self.__totalTimeInTwoGram +1        
            else:
                for i in range(-1,len(sentence)):
                    if(i==-1):
                        firistWord="BOS"
                        secondWord= sentence[i+1]
                    elif(i==len(sentence)-1) :
                        firistWord = sentence[i-1]
                        secondWord = "EOS"
                    else :
                        firistWord = sentence[i]
                        secondWord = sentence[i+1]        
                    twoGram=firistWord+"#"+secondWord
                    if twoGram in self.__twoGramData :
                        self.__twoGramData[twoGram]=self.__twoGramData[twoGram]+1
                    else :
                        self.__twoGramData.setdefault(twoGram,1)
                    self.__totalTimeInTwoGram = self.__totalTimeInTwoGram +1    
        return 