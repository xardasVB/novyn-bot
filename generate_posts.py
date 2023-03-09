
import json
import os
import random
from neural import get_novyna

emojiList  = ['‼️', '😁', '⚡️', '⚡️', '⚡️', '⚡️', '❗️', '❗️', '❗️', '💪', '😎', '🤕', '⚔️', '💁🏻‍♂️']

lst = [] 
for i in range(200):
    result = get_novyna()
    result = random.choice(emojiList) + "" + result[:-1].capitalize() + ".\n\n@NovynyarBot";
    lst.append(result)
    print(result)
    print("\n")


with open("neuralDB.txt", "w", encoding="utf-8") as f:
    f.write(json.dumps(lst))
    
#with open("novyny.txt", "w", encoding="utf-8") as f:
    #for m in messages:
    #    if m.message != None:
    #        f.write(m.message)
    #        f.write("\n\n")
        
