import numpy
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint

def sample(preds, temperature=1.0):
    preds = numpy.asarray(preds).astype('float64')
    preds = numpy.log(preds) / temperature
    exp_preds = numpy.exp(preds)
    preds = exp_preds / numpy.sum(exp_preds)
    probas = numpy.random.multinomial(1, preds, 1)
    return numpy.argmax(probas)

def tokenize_words(input):
    # lowercase everything to standardize it
    input = input.lower()

    # instantiate the tokenizer
    tokenizer = RegexpTokenizer(r'[А-яґєіїҐЄІЇ\']+')#(r'[\S+]+')#(r'\w+')#
    tokens = tokenizer.tokenize(input)

    # if the created token isn't in the stop words, make it part of "filtered"
    filtered = tokens#filter(lambda token: token not in stopwords.words('ukrainian'), tokens)
    return " ".join(filtered)

with open("novyny.txt", "r", encoding="utf-8") as f:
    processed_inputs = tokenize_words(f.read())

chars = sorted(list(set(processed_inputs)))
char_to_num = dict((c, i) for i, c in enumerate(chars))

input_len = len(processed_inputs)
vocab_len = len(chars)
print ("Total number of characters:", input_len)
print ("Total vocab:", vocab_len)

seq_length = 80
x_data = []
y_data = []

# loop through inputs, start at the beginning and go until we hit
# the final character we can create a sequence out of
for i in range(0, input_len - seq_length, 1):
    # Define input and output sequences
    # Input is the current character plus desired sequence length
    in_seq = processed_inputs[i:i + seq_length]

    # Out sequence is the initial character plus total sequence length
    out_seq = processed_inputs[i + seq_length]

    # We now convert list of characters to integers based on
    # previously and add the values to our lists
    x_data.append([char_to_num[char] for char in in_seq])
    y_data.append(char_to_num[out_seq])
    
n_patterns = len(x_data)
print ("Total Patterns:", n_patterns)

X = numpy.reshape(x_data, (n_patterns, seq_length, 1))
X = X/float(vocab_len)

y = np_utils.to_categorical(y_data)

model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(128))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))

#model.compile(loss='categorical_crossentropy', optimizer='adam')
#filepath = "model_weights_saved.hdf5"
#checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
#desired_callbacks = [checkpoint]
#model.fit(X, y, epochs=20, batch_size=256, callbacks=desired_callbacks)

filename = "100epochs.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

num_to_char = dict((i, c) for i, c in enumerate(chars))

def get_novyna():
    start = numpy.random.randint(0, len(x_data) - 1)
    pattern = x_data[start]
    index = char_to_num[' ']
    pattern.append(index)
    pattern = pattern[1:len(pattern)]
    #print('--- Generating with seed: "' + ''.join([num_to_char[value] for value in pattern]) + '"')
    #print("\n")

    num_of_chars = numpy.random.randint(70, 200)

    #for temperature in [0.2, 0.5, 0.7, 0.9]:
    #print('------ temperature:', temperature)
    #sys.stdout.write(''.join([num_to_char[value] for value in pattern]))

    #for i in range(seq_length):
    i = 0
    result = ""
    while i < num_of_chars or num_to_char[index] != ' ':
        temperature = numpy.random.choice([0.2, 0.5, 0.5, 0.5, 0.7, 0.7, 0.7, 0.9, 0.9])
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / float(vocab_len)
        prediction = model.predict(x, verbose=0)[0]
        index = sample(prediction, temperature)#numpy.argmax(prediction)#

        result += num_to_char[index]
        #sys.stdout.write(num_to_char[index])
        #sys.stdout.flush()

        pattern.append(index)
        pattern = pattern[1:len(pattern)]
        i += 1
    return result

#while True:
#    print(get_novyna())
#    print("\n")
#    input('Enter \n')
