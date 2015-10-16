# from

import itertools

import numpy as np

from scipy.cluster import hierarchy
from scipy.spatial import distance

def leaves(t, t2=None):
    """ Returns the leaves of a ClusterNode """
    if t is not None:
        return t.pre_order()
    elif t2 is not None:
        return t2.pre_order()

    return []

# For an element x, returns the set that x isn't in
other = lambda x, V, W: W if x in V else V


def optimal_scores(v, D, M):
    """ Implementation of Ziv-Bar-Joseph et al.'s leaf order algorithm
    v is a ClusterNode
    D is a distance matrix """

    def score_func(left, right, u, m, w, k):
        return ((M[left, u, m] if u != m else 0)
                + (M[right, w, k] if w != k else 0)
                + D[m, k])

    if v.is_leaf():
        n = v.get_id()
        M[v, n, n] = 0
        return 0,[],[]
    else:
        L = leaves(v.left)
        R = leaves(v.right)

        m_,LL,LR = optimal_scores(v.left, D, M)
        m_,RL,RR = optimal_scores(v.right, D, M)

        for u,w in itertools.product(L, R):
            m_order = sorted(other(u, LL or L, LR or L), key=lambda m: 0 if u == m else M[v.left, u, m])
            k_order = sorted(other(w, RL or R, RR or R), key=lambda k: 0 if w == k else M[v.right, w, k])

            C = D[np.ix_(m_order, k_order)].min()
            Cmin = 1e10
            for m,k in itertools.product(m_order, k_order):
                if M[v.left, u, m] + M[v.right, w, k] + C >= Cmin:
                    break
                C = score_func(v.left, v.right, u, m, w, k)
                if C < Cmin:
                    Cmin = C

            M[v, u, w] = M[v, w, u] = Cmin

        return M[v, L[0], R[0]], L, R


def order_tree(v, M):
    """ Returns an optimally ordered tree """

    L = leaves(v.left)
    R = leaves(v.right)

    if len(L) and len(R):
        u, w = min(((u, w) for u in L for w in R), key=lambda (u,w): M[v, u, w])

        if w in leaves(v.right.left):
            v.right.right, v.right.left = v.right.left, v.right.right

        if u in leaves(v.left.right):
            v.left.left, v.left.right = v.left.right, v.left.left

        v.left = order_tree(v.left, M)
        v.right = order_tree(v.right, M)

    return v


def order_tree2(v, M):
    """ Returns an optimally ordered tree """

    L = leaves(v.left)
    R = leaves(v.right)

    if len(L) and len(R):
        u, w = min(((u, w) for u in L for w in R), key=lambda (u,w): M[v.id, u, w])

        if w in leaves(v.right.left):
            v.right.right, v.right.left = v.right.left, v.right.right

        if u in leaves(v.left.right):
            v.left.left, v.left.right = v.left.right, v.left.left

        v.left = order_tree2(v.left, M)
        v.right = order_tree2(v.right, M)

    return v




def optimal_ordering(linkage, array, metric):
    # take a linkage matrix as input
    # cols 0 and 1 are nodes (including interior nodes)
    # col 2 is distance between two nodes
    # col 3 is count under a node


    tree = hierarchy.to_tree(linkage)
    dists = distance.squareform(distance.pdist(array, metric=metric))

    M = {}

    # Generate scores the first pass
    optimal_scores(tree, dists, M)
    tree = order_tree(tree, M)

    row_reorder = leaves(tree)

    return row_reorder, M



def optimal_scores_g(linkage, array, metric):
    # v: clusterNode
    # D: distance matrix

    def get_lr(n):
        L = n.left.pre_order() if n.left else []
        R = n.right.pre_order() if n.right else []
        return L,R

    n_nodes = array.shape[0]

    M = dict()

    tree,rd = hierarchy.to_tree(linkage, True)
    dists = distance.squareform(distance.pdist(array, metric=metric))

    for i in xrange(linkage.shape[0]):
        v = n_nodes + i
        j,k = int(linkage[i, 0]), int(linkage[i, 1])
        if linkage[i, 3] == 2:
            M[v, j, k] = M[v, k, j] = linkage[i, 2]
        else:
            L = rd[j].pre_order()
            R = rd[k].pre_order()

            LL,LR = get_lr(rd[j])
            RL,RR = get_lr(rd[k])

            for u,w in itertools.product(L, R):
                m_order = sorted(other(u, LL, LR),
                                 key=lambda m: 0 if u == m else M[j, u, m])
                n_order = sorted(other(w, RL, RR),
                                 key=lambda n: 0 if w == n else M[k, w, n])

                if m_order and n_order:
                    C = dists[np.ix_(m_order, n_order)].min()
                else:
                    M[v, u, w] = M[v, w, u] = 0.0
                    continue

                Cmin = 1e10
                for m,n in itertools.product(m_order, n_order):
                    if M[j, u, m] + M[k, w, n] + C >= Cmin:
                        break

                    C = ((M[j, u, m] if u != m else 0)
                         + (M[k, w, n] if w != k else 0)
                         + dists[m, n])

                    if C < Cmin:
                        Cmin = C

                M[v, u, w] = M[v, w, u] = Cmin

    return M