import os
import codecs

dict_pair_score={}
dict_pair_cont={}

size_sim_scale = 4.0
with codecs.open("rg65_spanish.txt", "r", "utf-8") as f1:
    dataset_1 = f1.readlines()
with codecs.open("rg65_farsi.txt", "r", "utf-8") as f2:
    dataset_2 = f2.readlines()
  
len_dataset_1=len(dataset_1)
len_dataset_2=len(dataset_2)

if len_dataset_1!=len_dataset_2:  print ("ERROR: files have different number of lines")
for i in range(len_dataset_1):
    linesplit_1=dataset_1[i].split("\t")
    word_1_1=linesplit_1[0]
    word_1_2=linesplit_1[1]
    score_1=float(linesplit_1[2])
    
    linesplit_2=dataset_2[i].split("\t")
    word_2_1=linesplit_2[0]
    word_2_2=linesplit_2[1]
    score_2=float(linesplit_2[2])
    
    pair_1=(word_1_1,word_2_2)
    pair_2=(word_1_2,word_2_1)
    
    if score_1>score_2:
        max_score=score_1
        min_score=score_2
    else:
        max_score=score_2
        min_score=score_1
    
    if max_score-min_score<=(size_sim_scale/4.0):
        average_score=(score_1+score_2)/2
        if pair_1 not in dict_pair_score:
            dict_pair_score[pair_1]=average_score
            dict_pair_cont[pair_1]=1
        else:
            dict_pair_score[pair_1]=((dict_pair_score[pair_1]*dict_pair_cont[pair_1])+average_score)/(dict_pair_cont[pair_1]+1)
            dict_pair_cont[pair_1]+=1
                    
        if pair_2 not in dict_pair_score:
            dict_pair_score[pair_2]=average_score
            dict_pair_cont[pair_2]=1
        else:
            dict_pair_score[pair_2]=((dict_pair_score[pair_2]*dict_pair_cont[pair_2])+average_score)/(dict_pair_cont[pair_2]+1)
            dict_pair_cont[pair_2]+=1

with codecs.open("cross-lingual.txt",'w',encoding='utf-8') as txtfile:  
    number_of_pairs=len(dict_pair_score)
    cont_pair=0
    for pair in dict_pair_score:
        cont_pair+=1
        txtfile.write(pair[0]+"\t"+pair[1]+"\t"+str(dict_pair_score[pair]))
        if cont_pair!=number_of_pairs: txtfile.write("\n")
    txtfile.close()
    print ("Creation of the cross-lingual dataset finished")
