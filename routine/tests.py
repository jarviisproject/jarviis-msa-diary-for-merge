# 문장 벡터화 하기(사전 만들기)
from sklearn.feature_extraction.text import TfidfVectorizer
### 코사인 유사도 ###
from sklearn.metrics.pairwise import cosine_similarity
### 유클리디언 유사도 (두 점 사이의 거리 구하기) ###
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
### 맨하탄 유사도(격자로 된 거리에서의 최단거리) ###
from sklearn.metrics.pairwise import manhattan_distances

def ngram(s, num):  #num : 몇글자씩 끊을 건지
    res=[]
    slen=len(s)-num+1 # slen : 끊었을 때 나오는 개수
    for i in range (slen):
        ss=s[i:i+num] #num만큼 s문자열에서 단어 자르기
        res.append(ss) #자른 단어는 res배열에 저장
    return res


def diff_ngram(sa,sb,num):
    a=ngram(sa,num)    #a문자열을 num단어씩 자른 배열
    b=ngram(sb,num) #b문자열을 num단어씩 자른 배열
    r=[]
    cnt=0
    for i in a:
        for j in b:
            if i==j:    #a에서 자른 단어가 b에도 있다면
                cnt+=1   #cnt++
                r.append(i) #중복되는 단어i를 r배열에 추가한다.
    return cnt/len(a), r #cnt/len=(중복되는 횟수/a의 길이), r=중복되는 단어


if __name__ == '__main__':
    #테스트할 문장 입력
    a="자바 개발"
    b="파이썬 개발"

    #2-gram
    r2,word2=diff_ngram(a,b,2)
    print("2-gram : ", r2,word2)

    #3-gram
    r3,word3 =diff_ngram(a,b,3)
    print("3-gram : ", r3, word3)


    sentences = (a,b)
    tfidf_vectorizer = TfidfVectorizer()
    # 문장 벡터화 하기(사전 만들기)
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

    ### 코사인 유사도 ###
    # 첫 번째와 두 번째 문장 비교
    cos_similar = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    print("코사인 유사도 측정")
    print(cos_similar)

    ### 유클리디언 유사도 (두 점 사이의 거리 구하기) ###
    ## 정규화 ##
    tfidf_normalized = tfidf_matrix / np.sum(tfidf_matrix)

    ##유클리디언 유사도##
    euc_d_norm = euclidean_distances(tfidf_normalized[0:1], tfidf_normalized[1:2])
    # print("유클리디언 유사도 측정")
    # print(euc_d_norm)

    ### 맨하탄 유사도(격자로 된 거리에서의 최단거리) ###
    manhattan_d = manhattan_distances(tfidf_normalized[0:1], tfidf_normalized[1:2])
    print("맨하탄 유사도 측정")
    print(manhattan_d)
    if (manhattan_d > 0.7 or cos_similar > 0.7) and manhattan_d != 1:
        print("맞음")
    else:
        print("틀림")

    # print(f"**** tfidf_matrix :: {tfidf_matrix}")
    # print(f"**** tfidf_normalized :: {tfidf_normalized}")
