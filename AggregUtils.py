import pandas as pd
import numpy as np
from CubeZarrUtils import CubeZarr

def DJc(ligne_mesure, dict_meteo):
    
    #Récupération du frame météo associé à la parcelle
    df_meteo = dict_meteo[ligne_mesure['parcel_id']]

    # Filtrer sur la plage de dates [sowing_date, date]
    mask = (df_meteo['time'] >= ligne_mesure['sowing_date']) & (df_meteo['time'] <= ligne_mesure['date'])
    df_meteo_periode = df_meteo.loc[mask]

    # Calculer DJ : max( 0, (temp_min + temp_max) / 2 - 6 )
    # Calcul de la moyenne journalière diminuée de 6°C
    moyenne_moins_base = (df_meteo_periode['temperature_min'] + df_meteo_periode['temperature_max']) / 2 - 6
    # Application du max(0, valeur)
    dj = moyenne_moins_base.clip(lower=0)

    return dj.sum()

def RGc(ligne_mesure, dict_meteo):
    df_meteo = dict_meteo[ligne_mesure['parcel_id']]
    mask = (df_meteo['time'] >= ligne_mesure['sowing_date']) & (df_meteo['time'] <= ligne_mesure['date'])
    df_meteo_periode = df_meteo.loc[mask]
    return df_meteo_periode['shortwave_radiation_sum'].sum()
    
def Pc(ligne_mesure, dict_meteo):
    df_meteo = dict_meteo[ligne_mesure['parcel_id']]
    mask = (df_meteo['time'] >= ligne_mesure['sowing_date']) & (df_meteo['time'] <= ligne_mesure['date'])
    df_meteo_periode = df_meteo.loc[mask]
    return df_meteo_periode['precipitation'].sum()
    
def ETPc(ligne_mesure, dict_meteo):
    df_meteo = dict_meteo[ligne_mesure['parcel_id']]
    mask = (df_meteo['time'] >= ligne_mesure['sowing_date']) & (df_meteo['time'] <= ligne_mesure['date'])
    df_meteo_periode = df_meteo.loc[mask]
    return df_meteo_periode['et0_fao_evapotranspiration'].sum()
    
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

'''
def NDVI (ligne_mesure, dict_cubesZarrs):
    
    #Récupération du cube zarr associé à la parcelle
    parcel_id = ligne_mesure['parcel_id']
    cube = dict_cubesZarrs[parcel_id]
    print(parcel_id)

    lat_mesure = ligne_mesure['lat'] 
    long_mesure = ligne_mesure['lon']

    date_cible = ligne_mesure['date']
    dates_dispo = cube.list_of_dates()

    print(date_cible)

    date_A   # La plus proche avant
    date_B   # La plus proche après
    
    # calcul des ndvi aux bornes
    ndvi_A = cube.ndvi(date_A, lat_mesure, long_mesure)
    ndvi_B = cube.ndvi(date_B, lat_mesure, long_mesure)

    if date_A == date_B:
        ndvi_interpole = ndvi_A
    else:
        # Interpolation linéaire pondérée par le temps calendaire
        jours_ecart_cible = (date_cible - date_A).days
        jours_totaux_intervalle = (date_B - date_A).days
        ndvi_interpole = ndvi_A + jours_ecart_cible * (ndvi_B - ndvi_A) / (jours_totaux_intervalle)
    
    return ndvi_interpole
'''

    

    