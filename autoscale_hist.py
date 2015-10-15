# coding: utf-8

import numpy as np

from matplotlib.gridspec import GridSpec
# from matplotlib.patches import Rectangle


def nonzero_intervals(vec, gap=1):
    edges, = np.nonzero(np.diff((vec==0)*1))
    edges += 1

    if vec[0] != 0:
        edge_vec = [[0], edges]
    else:
        edges[0] = 0
        edge_vec = [edges]

    if vec[-1] != 0:
        edge_vec.append([len(vec)])

    edges = np.concatenate(edge_vec)

    if len(edges) > 2 and gap:
        edges0 = [edges[0]]
        edges1 = [edges[1]]

        for i in range(2, len(edges), 2):
            if edges[i] - edges1[-1] <= gap:
                edges1[-1] = edges[i+1] # expand this section
            else:
                edges0.append(edges[i]) # add new section
                edges1.append(edges[i+1])

        return np.array(edges0), np.array(edges1)
    else:
        return edges[::2], edges[1::2]


def get_multiscale(h, scale, gap=1):
    hmax = np.ceil(float(max(h)) / scale) * scale
    sbins = np.arange(0, hmax+1, scale)
    hh = np.histogram(h, sbins)[0]

    nzi0,nzi1 = nonzero_intervals(hh, gap)

    return zip(sbins[nzi0], sbins[nzi1])[::-1], (nzi1 - nzi0)[::-1]


def get_scale(vec):
    scales = np.array([0.1, 0.2, 0.25, 0.5, 0.75, 1.])
    r = max(vec) - min(vec)
    lr = np.ceil(np.log10(r))

    return max(10**(lr - 1) * scales[np.searchsorted(scales, r / 10**lr)], 1.0)


def autoscale_hist(fig, x, bins=10, weights=None, orientation=u'vertical',
                   colors=None, labels=None, scale=None):

    if orientation not in ('vertical', 'horizontal'):
        raise ValueError("Invalid orientation {}".format(orientation))

    if type(x) != np.ndarray:
        x = np.array(x).T

    if np.ndim(x) == 1:
        x = x[:, None]

    if weights is not None:
        if type(weights) != np.ndarray:
            weights = np.array(weights).T

        if np.ndim(weights) == 1:
            weights = weights[:, None]
    else:
        weights = np.ones_like(x)

    bins = np.histogram(x, bins=bins, weights=weights)[1]

    hs = [np.histogram(x[:,i], bins=bins,
                       weights=weights[:,i])[0]
          for i in range(x.shape[1])]

    all_hs = np.concatenate(hs)

    if scale is None:
        scale = get_scale(all_hs)

    ylims,hratios = get_multiscale(all_hs, scale)

    if orientation == 'vertical':
        gs = GridSpec(len(ylims), 1, height_ratios=hratios + 0.2, hspace=0.05)
    else:
        ylims = ylims[::-1]
        gs = GridSpec(1, len(ylims), width_ratios=hratios[::-1] + 0.2, wspace=0.05)


    s10 = scale / 10.
    d = .005 # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(color='k', clip_on=False, linewidth=0.5)

    for i,(y0,y1) in enumerate(ylims):
        ax = fig.add_subplot(gs[i])

        ax.hist(x, bins=bins, weights=weights,
                orientation=orientation, color=colors,
                alpha=0.9, label=labels)

        if i == 0:
            if orientation == 'vertical':
                ax.xaxis.tick_top()
                ax.tick_params(labeltop='off')
            else:
                ax.yaxis.tick_left()
        else:
            if orientation == 'vertical':
                ax.spines['top'].set_visible(False)
                ax.plot((-d, +d), (1 - d, 1 + d), transform=ax.transAxes, **kwargs)
                ax.plot((1 - d, 1 + d), (1- d, 1 + d), transform=ax.transAxes, **kwargs)
            else:
                ax.spines['left'].set_visible(False)
                ax.plot((- d, + d), (-d, +d), transform=ax.transAxes, **kwargs)
                ax.plot((- d, + d), (1 - d, 1 + d), transform=ax.transAxes, **kwargs)

        if orientation == 'vertical':
            ax.set_ylim(max(y0 - s10, 0), y1 + s10)
            ax.set_yticks(np.arange(y0, y1+1, scale))
        else:
            ax.set_xlim(max(y0 - s10, 0), y1 + s10)
            ax.set_xticks(np.arange(y0, y1+1, scale))

        ax.tick_params(direction='out')

        if i == len(ylims) - 1:
            if orientation == 'vertical':
                ax.xaxis.tick_bottom()
            else:
                ax.yaxis.tick_right()
                ax.tick_params(labelright='off')
        else:
            if orientation == 'vertical':
                ax.spines['bottom'].set_visible(False)
                ax.plot((-d, +d), (-d, +d), transform=ax.transAxes, **kwargs)
                ax.plot((1 - d, 1 + d), (-d, +d), transform=ax.transAxes, **kwargs)
            else:
                ax.spines['right'].set_visible(False)
                ax.plot((1 - d, 1 + d), (-d, +d), transform=ax.transAxes, **kwargs)
                ax.plot((1 - d, 1 + d), (1 - d, 1 + d), transform=ax.transAxes, **kwargs)

        if 0 < i < len(ylims) - 1:
            if orientation == 'vertical':
                ax.tick_params(top='off', bottom='off')
            else:
                ax.tick_params(left='off', right='off')

    if labels is not None:
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc=9, ncol=len(labels))

    return fig

