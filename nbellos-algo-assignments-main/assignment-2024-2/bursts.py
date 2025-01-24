import sys
import argparse
import math
import collections
#παράμετροι που θα δοθούν απο τον χρήστη
parser = argparse.ArgumentParser(description='Εντοπισμός εξάρσεων.')
parser.add_argument('-s', type=float, default=2, help='Τιμή παραμέτρου s ')
parser.add_argument('-g', type=float, default=1, help='Τιμή παραμέτρου γ ')
parser.add_argument('-d', action='store_true', help='Εκτυπώνει προαιρετικά μηνύματα')
parser.add_argument('algorithm', choices=['viterbi', 'trellis'], help='επιλογή μεθόδου εκτέλεσης')
parser.add_argument('offsets_file', type=str, help='Αρχεία txt με χρονικές στιγμές εξάρσεων')
args = parser.parse_args()

#υπολογισμός παραμέτρων λi των καταστάσεων qi
def l(T, times, s):
    x = [times[i] - times[i - 1] for i in range(1, len(times))]
    min_x = min(x)
    n = len(times)
    g = T / n
    k = math.ceil(1 + math.log(T, s) + math.log(1 / min_x, s))
    l = [(s ** i) / g for i in range(k)]
    return l

#υπολογισμός συνάρτησης f που ακολουθεί την εκθετική κατανομή για τη κάθε κατάσταση qi
def q(l, x):
    n = len(x)
    f_table = [[l[j] * math.exp(-l[j] * x[i]) for i in range(n)] for j in range(len(l))]
    return f_table

#υπολογισμός κόστους μετάβασης απο μια κατάσταση σε άλλη
def t(n, GAMMA):
    taf = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if j > i:
                taf[i][j] = GAMMA * (j - i) * math.log(n)
            else:
                taf[i][j] = 0
    return taf

#υπολογισμός του βέλτιστου κόστους για την ακολουθία των εξάρσεων
def viterbi(x, l_table, taf, p=False):
    k = len(l_table)
    n = len(x)
    C = [[float('inf') for _ in range(k)] for _ in range(n + 1)]
    C[0][0] = 0
    P = [[0 for _ in range(n + 1)] for _ in range(k)]

    if p:
        formatted_C = ["{:.2f}".format(c) for c in C[0]]

    for t in range(1, n + 1):
        for s in range(k):
            l_min = 0
            c_min = C[t - 1][0] + taf[0][s]
            for l in range(1, k):
                c = C[t - 1][l] + taf[l][s]
                if c < c_min:
                    c_min = c
                    l_min = l
            C[t][s] = c_min + neglnf(x, l_table, t - 1, s)
            P[s][:t] = P[l_min][:t]
            P[s][t] = s

        if p:
            formatted_C = ["{:.2f}".format(c) for c in C[t]]

    c_min = C[n][0]
    s_min = 0
    for s in range(1, k):
        if C[n][s] < c_min:
            c_min = C[n][s]
            s_min = s

    S = P[s_min]
    return S, C

#υπολογισμός αρνητικού λογαρίθμου(πιθανότητες)
def neglnf(x, l, t, j):
    return -math.log(l[j] * math.exp(-l[j] * x[t]) + 1e-8 )

def neglnf_table(f_table, x):
    n = len(x)
    k = len(f_table)
    neglnf_table = [[0] * n for _ in range(k)]

    for j in range(k):
        for c in range(n):
            neglnf_table[j][c] = -math.log(f_table[j][c] + 1e-8 )

    return neglnf_table

#εκτύπωση των περιόδων των εξάρσεων
def print_bursts(road, times):
    trends = []
    nowtrend = road[0]
    begintrend = times[0]
    o = len(road)

    for a in range(1, o):
        if road[a] != nowtrend:
            trends.append((nowtrend, begintrend, times[a - 1]))
            nowtrend = road[a]
            begintrend = times[a - 1]
    trends.append((nowtrend, begintrend, times[-1]))

    for trend, start, end in trends:
        print(f"{trend} [{start} {end})")


MAX_INT = sys.maxsize

#αλγόριθμος εύρεσης συντομότερου μονοπατιού στον γράφο
def bellman_ford(graph, bnode, akmes, x, l_table, p=False):
    dist = {akmh: MAX_INT for akmh in akmes}
    dist[bnode] = 0
    pred = {akmh: None for akmh in akmes}

    q = collections.deque([bnode])
    in_queue = {akmh: False for akmh in akmes}
    in_queue[bnode] = True

    xal = []

    while q:
        u = q.popleft()
        in_queue[u] = False

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist0 = dist[v]
                dist[v] = dist[u] + w
                pred[v] = u
                xal.append((v, dist0, dist[v], u, dist[u], w))
                if not in_queue[v]:
                    q.append(v)
                    in_queue[v] = True
    if p:
        for b, (v, dist0, dist1, u, rotu, w) in enumerate(xal):
            move = w + neglnf(x, l_table, u[0], v[1])
            print(f"({v[0]}, {v[1]}) {dist0:.2f} -> {dist1:.2f} from ({u[0]}, {u[1]}) {rotu:.2f} + {move:.2f} + {neglnf(x, l_table, u[0], v[1]):.2f}")

    return pred, dist

#χτίσιμο γράφου και των ακμών του για τον bellman-ford μόνο
def structure(x, l_table, taf, f_table):
    n = len(x)
    k = len(l_table)
    grafos = collections.defaultdict(list)
    akmes = set()
    neg_lnf = neglnf_table(f_table, x)

    for j in range(k):
        grafos[(0, 0)] = grafos.get((0, 0), []) + [((1, j), taf[0][j] + neg_lnf[j][0])]
        akmes.add((0, 0))
        akmes.add((1, j))

    for c in range(1, len(x)):
        for i in range(k):
            for j in range(k):
                grafos[(c, i)] = grafos.get((c, i), []) + [((c + 1, j), taf[i][j] + neg_lnf[j][c])]
                akmes.add((c, i))
                akmes.add((c + 1, j))

    return grafos, akmes

#Σκοπός της main μεθόδου είναι η εύρεση της ακολουθίας των καταστάσεων του συστήματος και των περιόδων που το σύστημα βρίσκεται σε κάθε
#επίπεδο δραστηριότητας,χρησιμοποιώντας τους δύο διαφορετικούς τρόπους-> αλγόριθμο Viterbi και αλγόριθμο Bellman-Ford.
def main():
    with open(args.offsets_file, 'r') as file:
        times = list(map(float, file.read().strip().split()))

    x = [times[i] - times[i - 1] for i in range(1, len(times))]
    T = times[-1]
    l_table = l(T, times, args.s)
    f_table = q(l_table, x)
    taf = t(len(l_table), args.g)

    if args.algorithm == 'viterbi':
        road, C = viterbi(x, l_table, taf, p=args.d)

        if args.d:
            for row in C:
                formatted_C = ["{:.2f}".format(c) for c in row]
                print(f"[{', '.join(formatted_C)}]")
            print(f"{len(road)} {road}")

        print_bursts(road, times)

    elif args.algorithm == 'trellis':
        def key_func(kp):
            return dist[kp]

        way = []
        grafos, akmes = structure(x, l_table, taf, f_table)
        bnode = (0, 0)
        pred, dist = bellman_ford(grafos, bnode, akmes, x, l_table, p=args.d)
        lakmes = [(len(x), j) for j in range(len(l_table))]
        lakmh = min(lakmes, key=key_func)

        while lakmh is not None:
            way.append(lakmh)
            lakmh = pred[lakmh]
        way.reverse()

        if args.d:
            n = len(way)
            
            loc = [w[1] for w in way]
            print(f"{len(way)} {loc}")

        else:
            loc = [w[1] for w in way]

        print_bursts(loc, times)

if __name__ == "__main__":
    main()
