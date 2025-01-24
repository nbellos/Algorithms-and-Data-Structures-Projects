import sys
import argparse
import random
from collections import deque, defaultdict

def maxepirroi(G, p, k, mc):
    S = set()
    e = []

    for i in range(k):
        me = -999
        b = None

        for komvos in list(G.keys()): 
            if komvos not in S:
                n = S.copy()
                n.add(komvos)
                avg = ektimhsh(G, n, p, mc)
                if avg > me:
                    me = avg
                    b = komvos

        if b is None:
            break
        else:
            S.add(b)
            e.append(me)
    
    return list(S), e

def ektimhsh(G, sporoi, p, mc):
    se = 0
    for i in range(mc):
        energoi = set(sporoi)
        oura = deque(sporoi)
        epeksergasia = set()

        while len(oura) > 0:
            u = oura.popleft()
            for v in G[u]:
                if (u, v) not in epeksergasia and v not in energoi:
                    epeksergasia.add((u, v))
                    if random.random() < p:
                        energoi.add(v)
                        oura.append(v)
        
        se += len(energoi)

    avg = se / mc
    return avg

def bm(data):
    graph = defaultdict(list)
    with open(data, 'r') as file_data:
        for line in file_data:
            if line.strip():
                u, v = map(int, line.split())
                graph[u].append(v)
    return graph


def maxsporoi(g, k):
    b = {}
    for akmh, n in g.items():
        b[akmh] = len(n)
    ss = sorted(b, key=b.get, reverse=True)
    ks= []
    for i in range(k):
        if i < len(ss):  
            ks.append(ss[i])
        else:
            break  
    return ks


def w(G, sporoi, p, mc):
    epirroes = []
    se = set()
    
    for sporos in sporoi:
        se.add(sporos)
        epirroi = ektimhsh(G, se, p, mc)
        epirroes.append(epirroi)
    return epirroes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Εντοπισμός κόμβων για μεγιστοποίηση επιρροής")
    parser.add_argument("graph", type=str, help="αρχείο με τους συνδέσμους του γράφου.")
    parser.add_argument("k", type=int, help="αριθμός των κόμβων που θέλουμε να επιλέξουμε ως σπόρους.")
    parser.add_argument("strategy", type=str, choices=["greedy", "max_degree"], help="Μέθοδος επιλογής σπόρων.")
    parser.add_argument("probability", type=float, help="η πιθανότητα με την οποία επηρεάζεται ένας κόμβος από έναν γείτονά του.")
    parser.add_argument("mc", type=int, help="αριθμός επαναλήψεων στη μέθοδο Monte Carlo.")
    parser.add_argument("-r", "--random_seed", type=int, help="Τιμή σπόρου για γεννήτρια ψευδοτυχαίων αριθμών.", default=None)
    args = parser.parse_args()

    G = bm(args.graph)
    k = args.k
    p = args.probability
    mc = args.mc

    if args.strategy == "greedy":
        sporoi, e = maxepirroi(G, p, k, mc)
    else:
        sporoi = maxsporoi(G, k)

        e = w(G, sporoi, p, mc)
    
    print("Seeds:", sporoi)
    print("Influences:", e)
