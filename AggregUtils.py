import pandas as pd
import numpy as np
from CubeZarrUtils import CubeZarr

def NDVI(ligne_mesure, dict_cubes):
    # Récupération du frame satellite associé à la parcelle
    cube = dict_cubes[ligne_mesure['parcel_id']]
    df_cube = cube.dataframe

    # Récupération des informations importantes
    latitude = ligne_mesure['lat']
    longitude = ligne_mesure['lon']
    date_mesure = ligne_mesure['date']

    # Trouver l'image satelitte la plus proche de la date de mesure de moins de 10 jours
    df_date_proche = df_cube[
    (df_cube["date"] <= date_mesure) &
    (df_cube["date"] >= date_mesure - pd.Timedelta(days=30)) &
    (df_cube["B04"].notna()) &
    (df_cube["B08"].notna())
]

    # Si aucune image satelitte ne correspond au critères, information inexploitable à traiter apres
    if df_date_proche.empty:
        return -1

    image_b04 = df_date_proche["B04"].iloc[-1]
    image_b08 = df_date_proche["B08"].iloc[-1]
    pixel_b04 = image_b04.sel(x=latitude, y=longitude, method="nearest") 
    pixel_b08 = image_b08.sel(x=latitude, y=longitude, method="nearest")

    return (pixel_b08.values - pixel_b04.values)/(pixel_b08.values + pixel_b04.values)
    
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
    

    

    