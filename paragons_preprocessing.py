import random
import re
from  Functions import dict_from_text, vectorization, cos_similarity

# reading paragons and finding information
class paragon_transoformations:
    count = 0
    Bills = []
    sims = [{'p': 1, 't': 1, 'u': 1, 'b': 1},
                {'s': 1, 'u': 2, 'm': 1, 'a': 1, 'p': 1, 't': 1},
                {'s': 1, 'u': 1, 'm': 1, 'a': 1, 'p': 1, 'l': 1, 'n': 1,',': 1},
                {'s': 1, 'p': 2, 'r': 1, 'z': 1, 'e': 1, 'd': 2, 'a': 5, 'ż': 1, 'o': 3, 't': 1,
                 'k': 1, 'w': 1, 'n': 1},
                {'s': 1, 'p': 3, 'r': 1, 'z': 1, 'e': 1, 'd': 2, '.': 1, 'o': 2, 't': 1, 'u': 1, 'a': 1}
                ]
    def __init__(self,text):
        self.text= text
        paragon_transoformations.count+=1
        paragon_transoformations.Bills.append(text)

    def read_from_file(self):
        sections = []
        with open("Paragons/tesseract_paragons_recognization.txt", "r",encoding='utf-8') as file_read:
            file  = file_read.read()
        sections = file.split("\n\n\n\n\n")
        sections2 = file.split('\n\n\n')
        if len(sections)>=len(sections2):
            return sections2
        return sections
    def split_paragon(texts):
        tekst=[]
        for i in range(len(texts)):
            teksts = texts.split('\n')
            tekst = [tekst  for tekst in teksts]
        return tekst

    def find_similarity(self, line: str, sims: list[dict]) -> list[int]:
        dict_from_line = dict_from_text(line)
        return [cos_similarity(vectorization(dict_from_line, sim)) for sim in sims]

    def patterns_finding(text):
        owner = []
        products = []
        kod_pocztowy = []
        other_items = []
        # zamknięcie real items "suma ptu" ipt
        # paragon fiskalny
        looking_for_similarity_to ={'p': 1, 'a': 3, 'r': 1, 'g': 1, 'o': 1, 'n': 2, 'f': 1, 'i': 1, 's': 1, 'k': 1, 'l': 1, 'y': 1}
        for  line in text:

            vectors =vectorization(dict_from_text(line),looking_for_similarity_to)
            cosine_similarity = cos_similarity(vectors)
            # if cosinus similarity find "paragon fiskalny"
            if  cosine_similarity > 0.7:
                indexx= 0
                print(f"{line} is found with  {cosine_similarity} plausibility")
                print("similarity from line:")
                for counter in range(text.index(line)+1,len(text)-1):
                    # function looking for ending element of paragon
                    similarities = paragon_transoformations.find_similarity(paragon_transoformations,text[counter], paragon_transoformations.sims)
                    # if similarity i greater than 80% with texts  it will cut text else all lines are set in owner info
                    if max(similarities) > 0.80:
                        print(similarities)
                        print(max(similarities))
                        indexx = counter
                        break
                    # append products after line
                    products.append(text[counter])
                # all lines before product are from owner informations
                owner = (list(owners for owners in text[:text.index(line)]))
                del text[:indexx+1]

        # in owner we will look for poczta and  ragion
        kod_pocztowy = [poczta_line  for poczta_line  in  owner if re.search(r"\d{2}-\d{3} .*$",poczta_line)]
        # others contins suma ptu, suma price and tail of recipe
        other_items = text
        print(kod_pocztowy)
        print(owner)
        print(products)
        print(other_items)
        return owner,kod_pocztowy,products,other_items


# usage demands text file or string to process
print(paragon_transoformations.patterns_finding(paragon_transoformations.split_paragon("sdd")))
