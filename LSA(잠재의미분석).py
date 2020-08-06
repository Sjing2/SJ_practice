class  LSA() :
    def __init__(self) :
        pass

    def _make_dtm(self) :#언더바를 쓴것은 외부에서 호출하지 않겠다는 뜻
        from sklearn.feature_extraction.text import CountVectorizer
        
        def tokenize(x):
            return x.split()
        
        cv = CountVectorizer(tokenizer = tokenize)
        self.DTM = cv.fit_transform(self.docs).toarray()
        self.feature_names = cv.get_feature_names()
        self.word2id = cv.vocabulary_
    
    def _truncatedSVD(self) :
        from sklearn.decomposition import randomized_svd
        self.U, s, self.VT = randomized_svd(self.DTM, n_components=self.k, n_iter = 10) #특이값분해

    def print_topics(self) :#언더바를 쓰지 않은 것은 외부에서도 호출하겠다는 뜻
        for topic in self.VT :
            print([self.feature_names[i] for i in topic.argsort()[::-1][:self.n_words]])

    def get_word_vec(self, keyword) :
        v = self.VT.T[self.word2id[keyword]]
        print("단어 {} : {}".format(keyword, v))
        return v

    def get_doc_vec(self, idx_doc) :
        print("문서 {} : {}".format(idx_doc, self.U[idx_doc]))
        return self.U[idx_doc]

    def calc_similarity(self, x, y) :
        import numpy as np
            # x와 y, 두 벡터의 코사인 유사도를 계산하는 함수
        nominator = np.dot(x, y)    # 분자
        denominator = np.linalg.norm(x)*np.linalg.norm(y)  # 분모
        print('유사도 : {}'.format(nominator/denominator))
        return nominator/denominator

    def train(self, docs, k, n_words = 3) :
        self.docs = docs
        self.k = k
        self.n_words = n_words

        self._make_dtm()
        self._truncatedSVD()
        self.print_topics()


if __name__ == '__main__' :#시작점 확인
    doc_ls = ['바나나 사과 포도 포도 짜장면',
         '사과 포도',
         '포도 바나나',
         '짜장면 짬뽕 탕수육',
         '볶음밥 탕수육',
         '짜장면 짬뽕',
         '라면 스시',
         '스시 짜장면',
         '가츠동 스시 소바',
         '된장찌개 김치찌개 김치',
         '김치 된장 짜장면',
         '비빔밥 김치'
         ]

    lsa = LSA()
    lsa.train(doc_ls, k=4, n_words=3)

    lsa.get_doc_vec(1)
    lsa.get_word_vec("라면")
    lsa.calc_similarity(lsa.get_doc_vec(1), lsa.get_word_vec("라면"))
    lsa.calc_similarity(lsa.get_word_vec("포도"), lsa.get_word_vec("사과"))