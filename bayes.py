import pdb
import math

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
        mapped_words = map(count, word_list)
        mapped_word_type = reduce(self.tally_words, mapped_words)
        return mapped_word_type, total_word_count


class Folder:
    
    def __init__(self, directory):
        self.directory = directory
        self.total_word_count = 0
    
    def reduce_files(self, prev, nxt):
       reader = DocumentReader()
       nxt_words_map, doc_word_count = reader.load(nxt)
       self.total_word_count = self.total_word_count + 1
       for key in nxt_words_map.keys():
           match = prev.get(key)
           if match:
               if match['file_name'] != nxt:
                   count = count + 1
                   prev.update({current_key:{'file_name':nxt, 'count':count}})
           else:
               prev[current_key] = {'file_name':nxt, 'count':1}
       return prev

    def load(self):
        ''' return word_map, total_words, total_docs '''
        file_names = listdir(self.directory)        
        word_maps = reduce(self.reduce_files, file_names)
        return word_maps, self.total_word_count, len(word_maps.keys()), len(file_names)


class ProbabilityTable:

    def __init__(self, word_map, total_word_count, total_word_types, total_docs_from_type, total_docs):
        self.word_map = word_map
        self.total_word_count = total_word_count
        self.total_word_types = total_word_types
        self.total_docs_from_type = total_docs_from_type
        self.total_docs = total_docs
        self.lambda_value = 1

    def prob_map_words(self, words):
        new_word_map = {}
        for word in words:
            word_count = word_map_item['count']
            word['value'] = self.lambda_smooth(word_count)
            new_word_map[word.keys()[0]] = word

    def get(self, key):
        value = new_word_map[key]
        if not value:
            return self.lambda_smooth(0)
        return value
    
    def probability(self):
        return total_docs_from_type/total_docs 

    def lambda_smooth(self, word_count):
        return (word_count + self.lambda_value) / (self.total_word_count + self.total_word_types * self.lambda_value)


class Trainer:

    def __init__(self, parent_folder):
        self.parent_folder = parent_folder

    def train(self):
        spam_word_map, spam_total_word_count, spam_total_word_types, spam_total_docs = folder.load()
        ham_word_map, ham_total_word_count, ham_total_word_types, ham_total_docs = folder.load()
        total_docs = spam_total_docs + ham_total_docs
        spam_prob_table = prob_table = ProbabilityTable(word_map=spam_word_map, total_word_count=spam_total_word_count,
                                                          total_word_types=spam_total_word_types, total_docs_from_type=spam_total_docs,
                                                          total_docs=total_docs)
        ham_prob_table = prob_table = ProbabilityTable(word_map=ham_word_map, total_word_count=ham_total_word_count,
                                                          total_word_types=ham_total_word_types, total_docs_from_type=ham_total_docs,
                                                          total_docs=total_docs)
        return ham_prob_table, spam_prob_table


class BayesClassifier:

    def __init__(self, ham_prob_table, spam_prob_table):
        self.ham_prob_table = ham_prob_table    
        self.spam_prob_table = spam_prob_table    

    def classify(self, document):
        ''' return spam or ham '''
        self.prob_spam(document)

    def prob_spam(self, document):
        reader = DocumentReader()
        word_map = reader.load(document)
        sum_spam = self._sum_spam(word_map.keys()) 
        sum_ham = self._sum_ham(word_map.keys())
        return math.log(self.spam_prob_table.probability) + self._sum_spam() - math.log(self.ham_prob_table.probability()) - self.sum_ham()
    
    def prob_ham(self, document):
        reader = DocumentReader()
        word_map = reader.load(document)
        sum_spam = self._sum_spam(word_map.keys()) 
        sum_ham = self._sum_ham(word_map.keys())
        return math.log(self.spam_prob_table.probability) + self._sum_spam() - math.log(self.ham_prob_table.probability()) - self.sum_ham()
        
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

    def refine_value(self, value):
        math.log(value) #natural logarithm 
        math.exp(value) #euler exponent
        

class Runner:

    def __init__(self):
        self.trainer = None
        self.classifier = None

    def train(self):
        trainer = Trainer('dataset/training')
        self.classifier = BayesClassifier(trainer.train())

    def classify(self, document):
        if not self.trainer:
            print "Please train me first"
            return
        return self.classifier.classify(document)

runner = Runner()
runner.train()
runner.classify('document')
pdb.set_trace()
