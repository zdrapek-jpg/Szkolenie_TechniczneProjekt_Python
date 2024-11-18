import numpy
import re
import math
test_A = "MATEUSZ"
test_B = "wjjcheprzełóż"
def make_dict_from_text(pattern):
    letter_dict = {}

    for char in pattern.lower():
        if char in letter_dict.keys():
            letter_dict[char]+=1
        else:
            letter_dict[char]=1
    return letter_dict
def vectors_Jaccart(vector1,vector2):
    all_keys = set(vector1.keys()).union(set(vector2.keys()))
    vector1_j = [vector1.get(key, 0) for key in all_keys]
    vector2_j = [vector2.get(key, 0) for key in all_keys]
    all_dictAuB = {}
    all_dictAnB = {}
    for key in all_keys:
        all_dictAuB[key] =  vector1.get(key, 0) if vector1.get(key, 0)>vector2.get(key, 0) else vector2.get(key, 0)
    for key in all_keys:
        all_dictAnB[key] =  vector1.get(key, 0) if vector1.get(key, 0)<vector2.get(key, 0) else vector2.get(key, 0)
    return   sum([ 1-(x/y) for x,y in zip(all_dictAnB.values(),all_dictAuB.values())])/len(vector1_j)

print(make_dict_from_text(test_A))
print(make_dict_from_text(test_B))
print("miara niepodobieństwa: ",end=" ")
print(vectors_Jaccart(make_dict_from_text(test_A),make_dict_from_text(test_B)))
