import math

class Vertex :
    def __init__(self, word, index):
        self.word  = word 
        self.index = index

class Edge :
    def __init__(self ,word, index, weight):
        self.word  = word
        self.index  = index
        self.weight = weight

class WordNet:
    def __init__(self, dic,word=None):
        self.__dic  = dic
        self.__word = None
        self.__sentence    = None
        self.__vertexTable = None
        self.__edgeTable   = None
        self.__DPTable     = None 
        if word is not None:
            self.build_Word_Net(word)

    def print_Net_Data(self):
        print("Vertex Table : ")
        for  i in range(len(self.__vertexTable)):
            print("Start at Index",i," : ",end="")
            for vertex in self.__vertexTable[i]:
                print(vertex.word, vertex.index ,end=",")
            print("")
        print("Edge Table :")    
        for i in range(len(self.__edgeTable)):
            print("Start at Index",i, " : ",end="")
            for edge in self.__edgeTable[i]:
                print(edge.word, edge.index, edge.weight, end=",")
            print("")    
                
    def build_Word_Net(self, word):
        ## reset the reference word
        self.__word = word 
        ## clear the Vertex Table and Init it 
        self.__vertexTable = [ []for i in range(len(word)+2)]
        self.__vertexTable[0].append(Vertex("BOS",0))
        self.__vertexTable[-1].append(Vertex("EOS",len(word)+1))
        self.__build_Vertex_Table()
        # clear the Edge Table and Init it 
        self.__edgeTable = [ [] for i in range(len(word)+2)]
        self.__build_Edge_Table()
        # clear the dp table and Init it 
        self.__DPTable = [] 

    def __atomic_Segment(self, index=1):
        if len(self.__vertexTable[index]) == 0:
            word = self.__word[index-1:index]
            self.__vertexTable[index].append(Vertex(word, index))
        if self.__vertexTable[index][0].word == "EOS":
            return 
        for vertex in self.__vertexTable[index] :
            toIndex = index + len(vertex.word)
            self.__atomic_Segment(toIndex)
                    
    def __build_Vertex_Table(self):
        for index in range(1, len(self.__word)+1):
            start = index-1 
            for end in range(start+1, len(self.__word)+1):
                word = self.__word[start:end]
                if word in self.__dic:
                    self.__vertexTable[index].append(Vertex(word,index))
        self.__atomic_Segment()  

    def __calcul_Weight(self, beginWord, endWord):
        totalTime = self.__dic.get_Corpus_TotalTime()
        frequency =  self.__dic.get_Word_Frequency(beginWord)
        frequency = frequency if frequency >0 else 1
        twoGramFrequency = self.__dic.get_TwoGram_Frequency(beginWord, endWord)
        sConst  = 0.9
        uConst  = 1-(1/ totalTime + 0.00001)
        return - math.log( sConst*(uConst*(twoGramFrequency/frequency)+(1-uConst)) + (1-uConst)*((frequency+1)/totalTime) )

    def __build_Edge_Table(self, index=1, record=set()):       
        for beginVertex in self.__vertexTable[index]:
            if beginVertex.word == "EOS" :
                record.add(beginVertex.word)
                return
            if beginVertex.word not in record :  
                record.add(beginVertex.word)    
                for toVertex in self.__vertexTable[index+len(beginVertex.word)] :
                    weight = self.__calcul_Weight(beginVertex.word, toVertex.word)
                    self.__edgeTable[beginVertex.index].append(Edge(beginVertex.word+"#"+toVertex.word, beginVertex.index, weight))
                    self.__build_Edge_Table(toVertex.index, record)   