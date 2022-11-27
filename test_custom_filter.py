
text='Команды Формулы-1 сказать «Здорово, что сезон-2022 заканчивается на пару недель раньш…'



# запиликивает бранное слово
def replace_bad_word(word):
   BAD_WORDS = [
      'формулы',
      'сказать',
      'здорово',
      'автомашины',
   ]
   #print(f'{word}')
   if word.lower() in BAD_WORDS:
      print(f'{word}')
      if word.isalpha():
         stars='*'*(len(word)-1)
         return word[0]+stars
      else:
         raise ValueError(f'{word} is not valid word')

   return word


def censor(text):
   """
   #text: текст, в котором ищем слова для замены
   """
   #return text
   return ' '.join(list(map(replace_bad_word,text.split())))

res=censor(text)
print(res)
