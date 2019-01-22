#!/usr/bin/env python

import numpy as np

clip_edge_lower = 1e-15
clip_edge_higher = 1 - clip_edge_lower

def cross_entropy(p, q):
    p = np.clip(p, clip_edge_lower, clip_edge_higher)
    q = np.clip(q, clip_edge_lower, clip_edge_higher)
    h = - np.dot(p, np.log(q))
    return h


def entropy(p):
    S = - np.sum(np.multiply(p, np.log(p)))
    return S


def kl_divergence(p,q):
    kld = - np.sum( np.multiply(p, np.log(np.divide(q,p))))
    return kld
