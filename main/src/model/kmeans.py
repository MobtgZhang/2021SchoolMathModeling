import numpy as np
from tqdm import tqdm
def cos_sim(a, b):
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    cos = np.dot(a,b)/(a_norm * b_norm)
    return cos
class KMeans:
    def __init__(self,dataset,k_numbers,max_iter):
        '''
        Given `data_set`, which is an array of arrays,
        find the minimum and maximum for each coordinate, a range.
        Generate `k` random points between the ranges.
        Return an array of the random points within the ranges.
        :param k_numbers: 聚类中心个数
        :param num_iters: 迭代次数
        '''
        self.max_iter = max_iter
        self.k_numbers = k_numbers
        # 准备好训练语料，整理成BM25HF模型需要的输入格式
        self.dataset = dataset
        # 1.选取K个点做为初始聚集的簇心（也可选择非样本点）;
        self.dimensions = len(self.dataset)
        self.centers = np.random.randint(0, self.dimensions, size=(self.k_numbers,))  # 注意这里是指的是文档的索引
    @staticmethod
    def _find_max(params):
        index,dataset,centers = params
        max_sim = 0  # positive infinity
        max_index = 0
        for i in range(len(centers)):
            centdocs = dataset[centers[i]]
            documents = dataset[index]
            val = cos_sim(centdocs, documents)
            if val > max_sim:
                max_sim = val
                max_index = centers[i]
        return max_index
    def assign_points(self,epoch):
        """
        Given a data set and a list of points betweeen other points,
        assign each point to an index that corresponds to the index
        of the center point on it's proximity to that point.
        Return a an array of indexes of centers that correspond to
        an index in the data set; that is, if there are N points
        in `data_set` the list we return will have N elements. Also
        If there are Y points in `centers` there will be Y unique
        possible values within the returned list.
        2.分别计算每个样本点到 K个簇核心的距离（这里的距离一般取欧氏距离或余弦距离），找到离该点最近的簇核心，将它归属到对应的簇；
        """
        # point 指的是文档中的每个文章
        centers = self.dataset[self.centers]
        ab = np.matmul(self.dataset,centers.T)
        a = np.linalg.norm(centers, axis=1).reshape(self.k_numbers, 1)
        b = np.linalg.norm(self.dataset, axis=1).reshape(self.dimensions, 1)
        c = np.matmul(b,a.T)
        value = np.divide(ab, c)
        assignments = [np.where(vec == np.max(vec))[0][0].tolist() for vec in value]
        return assignments
    def update_centers(self,assignments,epoch):
        """
        Accepts a dataset and a list of assignments; the indexes
        of both lists correspond to each other.
        Compute the center for each of the assigned groups.
        Return `k` centers where `k` is the number of unique assignments.
        3.所有点都归属到簇之后， M个点就分为了 K个簇。之后重新计算每个簇的重心（平均距离中心），将其定为新的“簇核心”；
        """
        new_means = {}
        centers = []
        for point in range(self.dimensions):
            cluster = assignments[point]
            if cluster not in new_means:
                new_means[cluster] = []
                new_means[cluster].append(point)
            else:
                new_means[cluster].append(point)
        for points in new_means:
            params = [self.dataset,new_means[points]]
            max_index = KMeans.point_avg(params)
            centers.append(max_index)
        self.centers = centers
    @staticmethod
    def point_avg(params):
        """
        Accepts a list of points, each with the same number of dimensions.
        NB. points can have more dimensions than 2
        Returns a new point which is the center of all the points.
        """
        dataset, points = params
        length = len(points)
        doc_vec = dataset[points]
        ab = np.matmul(doc_vec, doc_vec.T)
        a = np.linalg.norm(doc_vec, axis=1).reshape(length, 1)
        b = np.linalg.norm(doc_vec, axis=1).reshape(length, 1)
        c = np.matmul(a, b.T)
        value = np.divide(ab, c)
        d = np.sum(value, axis=1)
        final = np.where(d == np.max(d))
        return points[final[0][0]]
    def run(self):
        for epoch in tqdm(range(self.max_iter),desc='KMeans process'):
            old_assignments = self.assign_points(epoch)
            self.update_centers(old_assignments,epoch+1)
            new_assignments = self.assign_points(epoch + 1)
            self.assignments = new_assignments
    def get_centers(self):
        return self.centers
    def get_assignments(self):
        return self.assignments
    def get_dataset(self):
        return self.dataset

