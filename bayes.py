import pdb
import math
import os

from decimal import Decimal
from os import listdir


class DocumentReader:

    def count(self, word):
        return {word:1}

    def tally_words(self, prev, nxt):
        current_key = nxt.keys()[0]
        count = prev.get(nxt.keys()[0])
        if count:
            count = count + 1
            prev.update({current_key:count})
        else:
            prev[current_key] = 1 
        return prev

    def load(self, filename):
        words = ''
        with open(filename, 'r') as file_object:
            for line in file_object:
                words = words + line
        word_list = words.split()
        total_word_count = len(word_list)
        mapped_words = map(self.count, word_list)
        mapped_word_type = reduce(self.tally_words, mapped_words)
        return mapped_word_type, total_word_count


class Folder:
    
    def __init__(self, directory):
        self.directory = directory

    def gen_word_map(self, files):
        word_map = {}
        total_word_count = 0
        for file_name in files:
            reader = DocumentReader()
            file_words_map, doc_word_count = reader.load(os.path.join(self.directory, file_name))
            total_word_count = total_word_count + doc_word_count 
            for key in file_words_map.keys():
                match = word_map.get(key)
                if match:
                   if match['last_file_name'] != file_name:
                       count = match['count']
                       count = count + 1
                       word_map.update({key:{'last_file_name':file_name, 'count':count}})
                   else:
                       pass
                else:
                   word_map[key] = {'last_file_name':file_name, 'count':1}
        return word_map, total_word_count

    def load(self):
        ''' return word_map, total_words, total_docs '''
        file_names = listdir(self.directory)        
        word_maps, total_word_count = self.gen_word_map(files=file_names)
        return word_maps, total_word_count, len(word_maps.keys()), len(file_names)


class ProbabilityTable:

    def __init__(self, word_map, total_word_count, total_word_types, total_docs_from_type, total_docs):
        self.word_map = word_map
        self.total_word_count = total_word_count
        self.total_word_types = total_word_types
        self.total_docs_from_type = total_docs_from_type
        self.total_docs = total_docs
        self.lambda_value = 1
        self.word_prob_dict = self.gen_word_map()

    def gen_word_map(self):
        prob_dict = {}
        for word in self.word_map.keys():
            prob_dict[word] = self.lambda_smooth(self.word_map[word]['count'])
        return prob_dict 

    def get(self, key):
        value = self.word_prob_dict.get(key, False)
        if not value:
            return self.lambda_smooth(0)
        return value
    
    def probability(self):
        return float(Decimal(self.total_docs_from_type) / Decimal(self.total_docs)) 

    def lambda_smooth(self, word_count):
        return float(Decimal(word_count + self.lambda_value) / Decimal(self.total_word_count + self.total_word_types * self.lambda_value))


class Trainer:

    def __init__(self, parent_folder):
        self.parent_folder = parent_folder

    def train(self):
        spam_folder = Folder('%s/spam' % self.parent_folder)
        ham_folder = Folder('%s/ham' % self.parent_folder)
        spam_word_map, spam_total_word_count, spam_total_word_types, spam_total_docs = spam_folder.load()
        ham_word_map, ham_total_word_count, ham_total_word_types, ham_total_docs = ham_folder.load()
        total_docs = spam_total_docs + ham_total_docs
        spam_prob_table = ProbabilityTable(word_map=spam_word_map, total_word_count=spam_total_word_count,
                                                          total_word_types=spam_total_word_types, total_docs_from_type=spam_total_docs,
                                                          total_docs=total_docs)
        ham_prob_table = ProbabilityTable(word_map=ham_word_map, total_word_count=ham_total_word_count,
                                                          total_word_types=ham_total_word_types, total_docs_from_type=ham_total_docs,
                                                          total_docs=total_docs)
        return ham_prob_table, spam_prob_table


class BayesClassifier:

    def __init__(self, ham_prob_table, spam_prob_table):
        self.ham_prob_table = ham_prob_table    
        self.spam_prob_table = spam_prob_table    

    def classify(self, document):
        ''' return spam or ham '''
        return 'spam' if self.prob_spam(document) > self.prob_ham(document) else 'ham'

    def prob_spam(self, document):
        reader = DocumentReader()
        word_map, doc_word_count = reader.load(document)
        sum_spam = self._sum_spam(word_map.keys()) 
        sum_ham = self._sum_ham(word_map.keys())
        z = math.log(self.ham_prob_table.probability()) + sum_ham - math.log(self.spam_prob_table.probability()) - sum_spam
        return 1 / (math.exp(z) + 1)
    
    def prob_ham(self, document):
        reader = DocumentReader()
        word_map, doc_word_count = reader.load(document)
        sum_spam = self._sum_spam(word_map.keys()) 
        sum_ham = self._sum_ham(word_map.keys())
        z = math.log(self.spam_prob_table.probability()) + sum_spam - math.log(self.ham_prob_table.probability()) - sum_ham
        return 1 / (math.exp(z) + 1)
        
    def _sum_spam(self, words):
        total = 0
        for word in words:
            lambda_prob = self.spam_prob_table.get(word)
            total = total + math.log(lambda_prob)
        return total

    def _sum_ham(self, words):
        total = 0
        for word in words:
            lambda_prob = self.ham_prob_table.get(word)
            total = total + math.log(lambda_prob)
        return total


class Runner:

    def __init__(self):
        self.trainer = None
        self.classifier = None

    def train(self):
        self.trainer = Trainer('dataset/training')
        prob_ham, prob_spam = self.trainer.train()
        self.classifier = BayesClassifier(prob_ham, prob_spam)

    def classify(self):
        if not self.trainer:
            print "Please train me first"
            return
        result_dict = {}
        reader = DocumentReader()
        for file_name in os.listdir('dataset/test'):
            result_dict[file_name] = self.classifier.classify(document=os.path.join('dataset/test', file_name))
        pdb.set_trace()
        return result_dict


runner = Runner()
runner.train()
runner.classify()
pdb.set_trace()
