import sys
import argparse

parser = argparse.ArgumentParser(description='Process an integer input.')
parser.add_argument('n', type=int, help='an integer input')
args = parser.parse_args()

def printbox(table):
    for row in table:
        print(" ".join(row))

def splitquarters(table):
    size = len(table)
    mid = size // 2
    q2 = [row[:mid] for row in table[:mid]]
    q1 = [row[mid:] for row in table[:mid]]
    q3 = [row[:mid] for row in table[mid:]]
    q4= [row[mid:] for row in table[mid:]]
    return q2, q1, q3, q4

#def switchcolors(table):
    g = len(table)
    s = len(table[0])
    newbox = [["X"] * g for _ in range(s)]
    
    for x in range(g):
        for y in range(s):
            if newbox[x][y] == "B": newbox[x][y] = "R"
            elif newbox[x][y] == "R": newbox[x][y] = "B"
            
    return newbox

def trominobox(table,n):
   size=n**2
   if n == 1:
        table = [
            ['G', 'X'],
            ['G', 'G']
        ]

        return table
   
   elif n == 2:
        #συνθήκες έτσι ώστε στην αναδρομή να γεμίσει ο πίνακας για n=3.
        #λέγχει ποιο τεταρτημόριο έχει 'G' σε συγκεκριμένη θέση,πχ στο 1ο τεταρτημόριο το 'G' υπαρχει κατω αριστερα
        #2ο τεταρτημόριο ακουμπάει το Χ στο κεντρο,3ο τεταρτημοριο ακουμπαει πανω δεξια το 'G' του κεντρου
        if table[size-1][size-1] == "G": # υπάρχει "G" κάτω δεξιά
            table = [
                ['B', 'B', 'R', 'R'], 
                ['B', 'G', 'G', 'R'],  
                ['R', 'G', 'B', 'B'],  
                ['R', 'R', 'B', 'X']   
            ]
        elif table[size-1][0] == "G":  # υπάρχει "G" κάτω αριστερά
            table = [
                ['B', 'B', 'R', 'R'], 
                ['B', 'G', 'G', 'R'],  
                ['R', 'R', 'G', 'B'],  
                ['G', 'R', 'B', 'B']   
            ]
        elif table[0][size-1] == "G":  # υπάρχει "G" πάνω δεξιά
            table = [
                ['B', 'B', 'R', 'G'], 
                ['B', 'G', 'R', 'R'],  
                ['R', 'G', 'G', 'B'],  
                ['R', 'R', 'B', 'B']   
            ]
        elif table[0][0] == "G":  # υπάρχει "G" πάνω αριστερά
            table = [
                ['G', 'B', 'R', 'R'], 
                ['B', 'B', 'G', 'R'],  
                ['R', 'G', 'G', 'B'],  
                ['R', 'R', 'B', 'B']   
            ]
        elif table[size-1][size-1] == "X":  #δε βρέθηκε "G" αλλά Χ κατω δεξιά
            table = [
                ['B', 'B', 'R', 'R'], 
                ['B', 'G', 'G', 'R'],  
                ['R', 'G', 'B', 'B'],  
                ['R', 'R', 'B', 'X']
            ]
        return table
   
   elif n >2:
        size=2**n
        midpoint = size// 2
        #τοποθέτηση 'G' τρόμινο στο κέντρο του πίνακα
        table[midpoint - 1][midpoint] = 'G'  
        table[midpoint][midpoint - 1] = 'G' 
        table[midpoint][midpoint] = 'G' 
        
        #χωρισμός του αρχικού πίνακα σε 4 υποπινακες (Τεταρτημόρια)
         
        q2,q1,q3,q4= splitquarters(table)
        
        #ενδεχομένως σε αυτο το κομμάτι κωδικα θα μπορούσε να υπαρξει καποιος αντιστοιχος έλεγχος συνθήκης όπως και στην περίπτωση για n=2 
        #για να εμφανιστεί το επιθυμητό αποτέλεσμα και να μην υπάρχουνε πάνω απο 1 Χ στο output για n>=4
        
        #αναδρομή trominobox για κάθε τεταρτημόριο μεγέθους 2^n-1*2^n-1
        q2=trominobox(q2,n-1)
        q1=trominobox(q1,n-1)
        q3=trominobox(q3,n-1)
        q4=trominobox(q4,n-1)
        
        #ένωση των τεσσάρων υποπινάκων στον τελικό
        finalbox = [[None] * size for _ in range(size)]
        mid = len(q1)
        for i in range(mid):
            for j in range(mid):
                finalbox[i][j] = q2[i][j]
                finalbox[i][j + mid] = q1[i][j]
                finalbox[i + mid][j] = q3[i][j]
                finalbox[i + mid][j + mid] = q4[i][j]
        return finalbox
        
   
size = 2 ** args.n
table = [['X' for _ in range(size)] for _ in range(size)]

table = trominobox(table, args.n)
printbox(table)







