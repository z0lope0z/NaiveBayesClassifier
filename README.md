NaiveBayesClassifier
====================

This is a Python implementation of the [Naive Bayes Classifier].

This is a solution for the 2nd Machine Problem in CS-180 Artificial Intelligence

#### Quick Implementation Details
- Uses in-built map and reduce python functions to count number of spam and ham words
- Probability table is generated and cached in-memory to improve speed (~3 seconds on given data sets)
- Probability table is represented as a dictionary to improve speed, O(1) average case, O(n) amortized worst case
- Uses decimal.Decimal for high precision computations
- Uses a derived formula to generate the probability table [Credits to instructor]

### Configuration

**Training Data Set**
```
dataset/training/ham/[file].txt
dataset/training/spam/[file].txt
```

**Testing Data Set**
```
dataset/test/[file].txt
```

Sample file:
```
recent title syntax morphology oxford acquisition secondlanguage syntax susan braidus west virginium university issue syntactic development one most central both linguistics apply linguistics assume detail background knowledge lingui    stics book introduction acquisition syntax second language text build coherent picture second language grammatical development show interaction between syntactic process functional discourse approach why different approach different     result arnold publication december pp linecut paper x cloth oxford university press understanding syntax maggie tallerman university durham understand language text provide complete introduction syntax human language assume prior kno    wledge linguistics book discuss illustrate
```

### Running
```
python bayes.py
```

### Output
Sample **output.txt** derived from classifying the files in dataset/test/[file].txt:
```
1.txt, ham
10.txt, ham
100.txt, ham
101.txt, ham
102.txt, spam
103.txt, ham
104.txt, ham
105.txt, spam
106.txt, ham
107.txt, spam
108.txt, ham
109.txt, ham
```

Sources:

[Naive Bayes Classifier]: http://en.wikipedia.org/wiki/Naive_Bayes_classifier
[Python Time Complexity](https://wiki.python.org/moin/TimeComplexity)

Instructor:

Kristofer E. delas Penas
