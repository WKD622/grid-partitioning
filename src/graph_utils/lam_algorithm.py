import random


def is_free(M, v):
    pass


def match(M, a, b):
    pass


def to_remove(R, a, b):
    R.add((a, b))


def try_match(a, b, R, U, M):
    C_a = set()
    C_b = set()
    while is_free(M, a) and is_free(M, b):
        pass


def lam_algorithm(G):
    M = {}
    U = set(G.edges)
    R = set()
    while len(U) != 0:
        index = random.randint(0, len(G.edges) - 1)
        a, b = list(G.edges)[index]
        try_match(a, b, R, U, M)
