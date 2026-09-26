import numpy as np

def Maizy(ligne_mesure):
    
    #Instanciation des facteurs Maizy
    A = [0.040108, 0.040146, 0.040172]
    A.append(np.mean(A))
    B = [-26.240, -29.108, -31.951]
    B.append(np.mean(B))

    # calcul des facteurs a et b
    a = A[ligne_mesure['precocite']]
    b = B[ligne_mesure['precocite']]

    # Retourner le Maizy pour la ligne_mesure donnée
    return a*ligne_mesure['djc']+b