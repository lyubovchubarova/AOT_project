from nltk import word_tokenize, sent_tokenize, ngrams
import re
import sqlite3
import pymorphy2
import string

morph = pymorphy2.MorphAnalyzer()

class ExactFormPattern:
    def __init__(self, pattern):
        self.word = pattern.replace('"', '')

    def check(self, word, **kwargs):
        return word == self.word

    def __repr__(self):
        return f"ExactFormPattern({self.word})"


class AnyFormPattern:
    def __init__(self, pattern):
        self.word = pattern

    def check(self, word, **kwargs):
        return morph.parse(self.word)[0].normal_form == morph.parse(word)[0].normal_form

    def __repr__(self):
        return f"AnyFormPattern({self.word})"


class ExactPosPattern:
    def __init__(self, pattern):
        self.word, self.pos = pattern.split('+')

    def check(self, word, pos):
        return self.word == word and self.pos == pos

    def __repr__(self):
        return f"ExactPosPattern({self.word}, {self.pos})"


class PosPattern:
    def __init__(self, pattern):
        self.pos = pattern

    def check(self, pos, **kwargs):
        return self.pos == pos

    def __repr__(self):
        return f"PosPattern({self.pos})"

exact_form = re.compile('\"[a-яёА-ЯЁ]+\"')
all_forms = re.compile('[a-яёА-ЯЁ]+')
word_pos = re.compile('[a-яёА-ЯЁ]+\+[A-Z]+')
pos = re.compile('^[A-Z]+')

def parse_requests(request):
  request = request.split()
  patterns = []

  for elem in request:
    if bool(exact_form.fullmatch(elem)):
      patterns.append(ExactFormPattern(elem))
    elif bool(word_pos.fullmatch(elem)):
      patterns.append(ExactPosPattern(elem))
    elif bool(all_forms.fullmatch(elem)):
      patterns.append(AnyFormPattern(elem))
    elif bool(pos.fullmatch(elem)):
      patterns.append(PosPattern(elem))
    else:
      raise ValueError("Incorrect pattern") # TODO

  return patterns

def check_matching(ngram, patterns, pos_tokens):

  for (idx, word), pattern in zip(ngram, patterns):
    if not pattern.check(word=word, pos=pos_tokens[idx]):
        return False

  return True

def find_in_db(request, cursor):
  patterns = parse_requests(request)
  ans = []
  n = len(patterns)

  cnt = 0

  for row in cursor.execute("SELECT * FROM post_data"):
    poses = row[2].split()
    cnt += 1
    if len(poses) < 2:
      continue

    if cnt % 300 == 0:
        print(f"Обработано {cnt} предложений")
    for ngram in ngrams(enumerate(row[1].split()), n):
        # проверить матчится ли нграмма с patterns
      if check_matching(ngram, patterns, poses):
        ans.append((row[0], row[3]))
        break

  return ans