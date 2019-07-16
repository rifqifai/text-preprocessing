import re
import nltk
import pandas as pd

String = "Buku ini selalu di rekomendasi,... *sebagai salah satu novel terbaik, #BukuBagus" \
         "@rifqifai Woaaahh.. udah habiissss.. n penasaran lanjutannya " \
         " huuu,,, huu,,, HuuuuSudah lama nggak menangis sambil tertawa karena membaca buku. ==a" \
         "Saya terkagum-kagum dengan pribadi Nyai Ontosoroh, yaitu Sunikem" \
         " persahabatan yang mereka jalin sungguh manis sekali... :)" \
         " 'Kenapa baru baca sekarang!?!?!?!?' Memang buku yang sungguh luar biasa. \^_^/" \
         "Bintang 5 dech. Bukuu yang benar-benar membuat saya termotivasi, Membuat saya hangat *etcieh." \
         "Wow.. Cuma itu yang bisa aku ucapkan setelah menamatkan novel ini." \
         " Ngilu baca bukunya, hiks hiks hiks."

def casefolding(review):
    review = review.lower()
    return review

def tokenize(review):
    token = nltk.word_tokenize(review)
    return token

def filtering(review):
    # Remove angka termasuk angka yang berada dalam string
    # Remove non ASCII chars
    review = re.sub(r'[^\x00-\x7f]', r'', review)
    review = re.sub(r'(\\u[0-9A-Fa-f]+)', r'', review)
    review = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", review)
    review = re.sub(r'\\u\w\w\w\w', '', review)
    # Remove link web
    review = re.sub(r'http\S+', '', review)
    # Remove @username
    review = re.sub('@[^\s]+', '', review)
    # Remove #tagger
    review = re.sub(r'#([^\s]+)', '', review)
    # Remove simbol, angka dan karakter aneh
    review = re.sub(r"[.,:;+!\-_<^/=?\"'\(\)\d\*]", " ", review)
    return review

def replaceThreeOrMore(review):
    # Pattern to look for three or more repetitions of any character, including newlines (contoh goool -> gol).
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1", review)

def convertToSlangword(review):
    kamus_slangword = eval(open("slangwords.txt").read()) # Membuka dictionary slangword
    pattern = re.compile(r'\b( ' + '|'.join (kamus_slangword.keys())+r')\b') # Search pola kata (contoh kpn -> kapan)
    content = []
    for kata in review:
        filteredSlang = pattern.sub(lambda x: kamus_slangword[x.group()],kata) # Replace slangword berdasarkan pola review yg telah ditentukan
        content.append(filteredSlang.lower())
    review = content
    return review

def removeStopword(review):
    stopwords = open('stopword-tala.txt', 'r').read().split()
    content = []
    filteredtext = [word for word in review.split() if word not in stopwords]
    content.append(" ".join(filteredtext))
    review = content
    return review

# stringData = casefolding(String)
# print (stringData)

data = pd.read_csv('data-label.csv', encoding='latin-1')
# Keeping only the neccessary columns
datasets = [data]
   
for teks in datasets:
    label = teks['sentimen']
    teks = teks['ulasan'].apply(casefolding)
    teks = teks.apply(filtering)
    teks = teks.apply(replaceThreeOrMore)
    teks = teks.apply(tokenize)
    teks = teks.apply(convertToSlangword)
    teks = teks.apply(" ".join)
    teks = teks.apply(removeStopword)
    teks = teks.apply(" ".join)
    print(teks)

review_dict = {'ulasan': teks, 'sentimen' : label}
df = pd.DataFrame(review_dict, columns = ['ulasan', 'sentimen'])
print(df.info())
df.to_csv('data-bersih.csv', sep= ',' , encoding='utf-8')