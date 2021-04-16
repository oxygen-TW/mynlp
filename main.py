from Dictionary import Dictionary 
from WordNet import WordNet

if __name__ == '__main__':
    word = WordNet(Dictionary())

    while  1 :
        print("=================================")
        string = input("請輸入句子(輸入end結束):")
        if string == "end" :
            exit()   
        word.build_Word_Net(string)  
        word.print_Sentence()
        num=int(input("需要輸出運算的資料嗎(1代表需要):"))
        if num == 1 :
            word.print_Word_Data()
