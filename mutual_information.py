# code adopted from Pedro Alcocer,
# https://github.com/pealco/python-mutual-information/blob/master/entropy.py

# not actually sure if this is correct, should probably check that


import numpy as np
import scipy.stats as st


def entropy(counts):
    '''Compute entropy.'''
    ps = counts / float(counts.sum())  # coerce to float and normalize
    ps = ps[np.nonzero(ps)]            # toss out zeros
    H = - (ps * np.log2(ps)).sum()   # compute entropy

    return H


def mi(x, y, bins, normalized=False):
    '''Compute mutual information'''
    counts_xy = np.histogram2d(x, y, bins=bins)[0]
    counts_x  = np.histogram(x, bins=bins)[0]
    counts_y  = np.histogram(y, bins=bins)[0]

    H_xy = entropy(counts_xy)
    H_x  = entropy(counts_x)
    H_y  = entropy(counts_y)

    if normalized:
        return (H_x + H_y - H_xy) / np.sqrt(H_x * H_y)
    else:
        return H_x + H_y - H_xy


def nmi(x, y, bins):
    return mi(x, y, bins, True)


def get_part(x, y, c):
    return ((c[0] <= x) & (x < c[1]) & (c[2] <= y) & (y < c[3]))

def mutinA(x, y):
    assert x.shape[0] > 2 and y.shape[0] > 2

    x0,x1 = np.min(x), np.max(x) + 1e-6
    y0,y1 = np.min(y), np.max(y) + 1e-6

    def calc_t(N):
        return ((N - N.mean())**2).sum() / N.mean() > 7.81

    cells = [(x0,x1,y0,y1)]
    m = []

    if get_part(x, y, cells[0]).sum() <= 2:
        return cells

    while cells:
        c = cells.pop()
        x0,x1,y0,y1 = c
        i = get_part(x, y, c)

        xm = np.median(x[i])
        ym = np.median(y[i])

        new_cells = [(x0, xm, y0, ym),
                     (xm, x1, y0, ym),
                     (x0, xm, ym, y1),
                     (xm, x1, ym, y1)]

        cell_i = [get_part(x, y, mc) for mc in new_cells]

        if calc_t(np.array([i.sum() for i in cell_i])):
            for i,mc in zip(cell_i, new_cells):
                if i.sum() <= 2:
                    m.append(mc)
                else:
                    cells.append(mc)
        else:
            m.append(c)

    return m


def mutin_mI(x, y, cells=None):
    mi = 0.0
    N = x.shape[0]
    logN = np.log(N)

    if cells is None:
        cells = mutinA(x, y)

    for k,c in enumerate(cells):
        N_k = get_part(x, y, c).sum()
        if N_k:
            N_xk = ((c[0] <= x) & (x < c[1])).sum()
            N_yk = ((c[2] <= y) & (y < c[3])).sum()
            mi += N_k * (np.log(N_k) - np.log(N_xk) - np.log(N_yk) + logN)

    return mi / N


def mi_dist(x, y, bins):
    '''Compute the MI-based distance metric'''
    counts_xy = np.histogram2d(x, y, bins=bins)[0]
    counts_x  = np.histogram(x, bins=bins)[0]
    counts_y  = np.histogram(y, bins=bins)[0]

    H_xy = entropy(counts_xy)
    H_x  = entropy(counts_x)
    H_y  = entropy(counts_y)

    return 2 - (H_x + H_y) / H_xy


# if __name__ == '__main__':
    # for s in (1.0, 2.0, 5.0):
    #     print s
    #     for n in (10, 100, 1000, 10000):
    #         x = np.random.randint(0, n, n)
    #         y = x + np.random.normal(scale=s, size=n)
    #
    #         print 'mutual information n=%d (x,y): %g\t%g' % (n, mi(x, y, np.floor(np.sqrt(n))),
    #                                                          nmi(x, y, np.floor(np.sqrt(n))))
    #
    # for n in (10, 100, 1000, 10000):
    #     x = np.random.normal(size=n)
    #     y = np.random.normal(size=n)
    #
    #     print 'mutual information n=%d (x,y): %g\t%g' % (n, mi(x, y, np.floor(np.sqrt(n))),
    #                                                      nmi(x, y, np.floor(np.sqrt(n))))
