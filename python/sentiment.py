import pickle


sentiment = pickle.load(open('sentiment.pkl','rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

review = input()
def sentimental(review):
    vec = vectorizer.transform(review)
    return sentiment.predict(vec)

print(sentimental(['good']))