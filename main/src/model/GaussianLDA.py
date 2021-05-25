import random
import scipy as sp
import scipy.special
import gensim
from collections import defaultdict

import numpy as np

class Wishart(object):
    def __init__(self, word_vecs):
        self.nu = None
        self.kappa = None
        self.psi = None

        self.set_params(word_vecs)

    def set_params(self, word_vecs):
        #turn dict of word vecs into a matrix
        word_vecs = np.vstack(word_vecs.values())

        self.nu = word_vecs.shape[1] #len of columns
        self.kappa = 0.01
        # should this be np.sum(x.dot(x.T)))??? also changed this to x.T.dot(x)
        self.psi = np.sum(word_vecs.T.dot(word_vecs), axis=0) 
        self.mu = np.mean(word_vecs, axis=0)

class GaussianLDA:
    def __init__(self, num_topics, corpus, word_vector_filepath = None):
        self.doc_topic_CT = None
        self.word_topics = {}
        self.corpus = corpus
        self.vocab = None
        self.priors = None
        self.word_vecs = {}
        self.num_topics = num_topics
        self.vocab = set([])
        self.topic_params = defaultdict(dict)
        self.word_vector_filepath = word_vector_filepath
        self.word_index = {}
        self.word_vec_size = 300
        self.alpha = 50./self.num_topics
    def process_corpus(self, documents):
        """
        Takes a list of documents, and processes them
        sets vocab
        [doc_id,documents]
        returns: None
        """
        temp_corpus = {}
        for index, doc in enumerate(documents):
            doc_id = doc[0]
            words = doc[1]
            temp_corpus[doc_id] = doc[1]
            for word in words:
                self.vocab.add(word)
        self.corpus = temp_corpus
        print("Done processing corpus with {} documents".format(len(documents)))
    def process_wordvectors(self, filepath = None):
        print("Processing word-vectors, this takes a moment")
        if filepath is None:
            for word in self.vocab:
                self.word_vecs[word] = np.random.uniform(0,1,size=(self.word_vec_size,))
        else:
            vectors = gensim.models.KeyedVectors.load_word2vec_format(fname=filepath, binary=False)
            useable_vocab = 0
            unusable_vocab = 0
            index = 0
            self.word_vec_size = vectors.vector_size

            for word in self.vocab:
                try:
                    self.word_vecs[word] = vectors[word]
                    useable_vocab += 1
                    index += 1
                except KeyError:
                    self.word_vecs[word] = np.random.random(size=(self.word_vec_size,1))
                    unusable_vocab += 1
            print ("There are {0} words that could be convereted to word vectors in your corpus \n" \
              "There are {1} words that could NOT be converted to word vectors".format(useable_vocab, unusable_vocab))
        print("Word-vectors for the corpus are created")
    def init(self):
        self.process_corpus(self.corpus)
        self.process_wordvectors(self.word_vector_filepath)
        # setting wishhart priors
        self.priors = Wishart(self.word_vecs)
        self.doc_topic_CT = np.zeros((len(self.corpus.keys()), self.num_topics))

        self.word_topics = {word: random.choice(range(self.num_topics)) for word in self.vocab}
        # get Doc-Topic Counts
        for docID in self.corpus:
            doc = self.corpus
            for word in doc:
                topicID = self.word_topics[word]
                self.doc_topic_CT[docID,topicID] += 1
    def recalculate_topic_params(self, topic_id):

        topic_count = np.sum(self.doc_topic_CT[:, topic_id], axis=0) # N_k

        kappa_k = self.priors.kappa + topic_count # K_k
        nu_k = self.priors.nu + topic_count # V_k

        scaled_topic_mean_K, scaled_topic_cov_K  = self.get_scaled_topic_mean_cov(topic_id) # V-Bar_k and C_k

        vk_mu = scaled_topic_mean_K - self.priors.mu #V-bar_k - Mu
        # print self.priors.psi
        psi_k = self.priors.psi + scaled_topic_cov_K + ((self.priors.kappa * topic_count) / kappa_k) * (vk_mu.T.dot(vk_mu)) # Psi_k

        topic_mean = (self.priors.kappa * self.priors.mu + topic_count * scaled_topic_mean_K) / kappa_k # Mu_k
        topic_cov = psi_k / (nu_k - self.word_vec_size + 1) # Sigma_k

        self.topic_params[topic_id]["Topic Count"] = topic_count
        self.topic_params[topic_id]["Topic Kappa"] = kappa_k
        self.topic_params[topic_id]["Topic Nu"] = nu_k
        self.topic_params[topic_id]["Topic Mean"], self.topic_params[topic_id]["Topic Covariance"] = topic_mean, topic_cov
        self.topic_params[topic_id]["Inverse Covariance"] = np.linalg.inv(topic_cov)
        self.topic_params[topic_id]["Covariance Determinant"] = np.linalg.det(topic_cov)
        self.topic_params[topic_id]["Liklihood Componant"] = None


        return topic_mean, topic_cov
    def get_scaled_topic_mean_cov(self, topic_id):
        'mean of word vecs in a topic'
        # get words assigned to topic_id
        word_vecs = []
        for word, topic in self.word_topics:
            topic = self.word_topics[word]
            if topic == topic_id:
                word_vecs.append(self.word_vecs[word])
        word_vecs = np.vstack(word_vecs)
        # added a small number here to stop overflow
        mean = np.sum(word_vecs, axis=0) / (np.sum(self.doc_topic_CT[:, topic_id], axis=0) + 2)
        mean_centered = word_vecs - mean
        cov = mean_centered.T.dot(mean_centered)
        return mean, cov
    def sample(self, init=True):

        print("sampling started")
        # Randomly assign word to topics
        if init == False:
            self.word_topics = {word: random.choice(range(self.num_topics)) for word in self.vocab}
        for docID, doc in self.corpus:
            doc = self.corpus[docID]
            for word in doc:
                # subtracting info about current word-topic assignment from doc-topic count table
                topic_id = self.word_topics[word]
                self.doc_topic_CT[docID, topic_id] - doc.count(word)

                self.recalculate_topic_params(topic_id)
                posterior = []
                max = 0
                for k in range(self.num_topics):  # start getting the pdf's for each word-topic assignment
                    log_prob = self.draw_new_wt_assgns(word, k)
                    # Count of topic in doc
                    Nkd = self.doc_topic_CT[docID, k]
                    log_posterior = np.log(Nkd + self.alpha) * log_prob
                    posterior.append(log_posterior)
                    # doing this for some normalization scheme
                    if log_posterior > max: max = log_posterior

                normalized_posterior = [np.exp(i - max) for i in posterior]
                ## need to copy the normalization scheme from Util.sample
        init = False
    def draw_new_wt_assgns(self, word, topic_id):

        # Getting params for calculating PDF of T-Dist for a word
        wordvec = self.word_vecs[word]
        inv_cov = self.topic_params[topic_id]["Inverse Covariance"]
        cov_det = self.topic_params[topic_id]["Covariance Determinant"]
        Nk = self.topic_params[topic_id]["Topic Count"]
        KappaK = self.topic_params[topic_id]["Topic Kappa"]
        centered = self.word_vecs[word] - self.priors.mu
        topic_cov = self.topic_params[topic_id]["Topic Covariance"]


        # Precalculating some terms (V_di - Mu)^T * Cov^-1 * (V_di - Mu)
        LLcomp = centered.T.dot(inv_cov).dot(centered)
        d = self.word_vec_size
        nu = self.priors.nu + Nk - d + 1

        log_prop = scipy.special.gammaln(nu + d / 2) - \
                   (scipy.special.gammaln(nu / 2) + d/2 * (np.log(nu) + np.log(np.pi)) +0.5 * np.log(cov_det) +
                    (nu + d) / 2 * np.log(1 + LLcomp / nu))

        return log_prop
    def fit(self,iterations=1, init=True):
        if init:
            self.init()
            init = False
        print("Starting fit")
        for i in range(iterations):
            self.sample()
            print("{} iterations complete".format(i))

