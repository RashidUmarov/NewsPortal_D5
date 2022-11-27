from django import template

register = template.Library()

BAD_WORDS = [
    'формулы',
    'сказать',
    'здорово',
    'автомашины',
    'АвтоВАЗ',
    'Впервые',
    'ввести',
    'перечислила',
    'ядру',
    'уточнил',
    'генеральный',
    'прервал',
    'обыграл',
    'певица',
    'члены',
]

# проверяет, что слово в блеклисте
def is_bad(word):
    for w in BAD_WORDS:
        # print(f'{w}  vs {word}')
        if w.lower() == word.lower().replace(',', '').replace('«', '').replace('»', ''):
            return True
    return False

# заменим символы в плохом слове
def change_bad_word(word: str):
    for b in BAD_WORDS:
        start = word.lower().find(b.lower())
        if start>=0:
            #print(f'{word} start={start}')
            size=(len(b) - 1)
            stars = '*' * size
            replacement = word[:start+1] + stars+word[start+size+1:]
            return replacement
    return word

# запиликивает плохие слова
@register.filter()
def censor(text):
    """
    #text: текст, в котором ищем слова для замены
    """
    # return text
    # print(f'{BAD_WORDS}')
    word_list = text.split()
    # print(f'{word_list}')
    return ' '.join(list(map(change_bad_word, word_list)))
