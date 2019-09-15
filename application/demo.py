import analyzer as a
import scraper as s
key = s.get_key()

shops = a.get_shops('1568572639',key,'./tests/')
for shop in shops:
    print(shop)

lcl_string = ['Hello','hello','heLlo','helo','friend','how','are','you','today']
lcl_set = a.get_unique_words(lcl_string)
print(lcl_set)

lcl_gram = [{'word': 'snake', 'count': 849},{'word': 'bird', 'count': 80},{'word': 'lion', 'count': 300},{'word': 'tiger', 'count': 200},{'word': 'cat', 'count': 249},{'word': 'dog', 'count': 149},{'word': 'and', 'count': 549},{'word': 'taco', 'count': 100}]

filtered = a.filter_gram(lcl_gram)
print(filtered)