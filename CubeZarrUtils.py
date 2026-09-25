import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

class CubeZarr:
    """Classe dédiée à l'exploitation d'un cube satellite Zarr v3 unique (parcelle)."""
    def __init__(self, chemin_zarr):
        self.chemin_zarr = chemin_zarr
        self.ds = xr.open_zarr(chemin_zarr)
        self.x = self.ds["x"]
        self.y = self.ds["y"]
        self.spatial_ref = self.ds["spatial_ref"]
        self.raster = self.ds["raster"]
        self.bandes = self.ds["band"].values.tolist()
        self.dates = self.ds["time"].values

    def date(self, index_jour):
        """Retourne la date exacte correspondant à l'index du jour demandé."""
        return pd.to_datetime(self.dates[index_jour]).normalize()

    def list_of_dates(self):
        return pd.to_datetime(self.dates).normalize().tolist()[::-1]

    def bande(self, index_jour, nom_ou_index_bande):
        """Retourne le DataArray Xarray d'une bande pour un jour précis."""
        if isinstance(nom_ou_index_bande, str):
            return self.raster.sel(time=self.dates[index_jour], band=nom_ou_index_bande)
        return self.raster.isel(time=index_jour, band=nom_ou_index_bande)
        
    def nombre_jours(self):
        """Retourne le nombre total de jours (images temporelles) disponibles."""
        return len(self.dates)

    def dimension_image(self):
        """Retourne la dimension spatiale de l'image sous forme de tuple (Hauteur, Largeur)."""
        hauteur = len(self.y)
        largeur = len(self.x)
        return (hauteur, largeur)
        
    def toDict(self, nom_ou_index_bande):
        "Retourne un dictionnaire date du jour:image de la bande nettoyé des aquisitions nulles"
        dictionnaire = {}
        for index_jour in range(len(self.dates) - 1, -1, -1):
            image = self.bande(index_jour, nom_ou_index_bande) 
            # 1. On rejette l'image s'il y a au moins un NaN (n'importe où)
            if np.isnan(image.any()):
                continue  # Contient un NaN -> acquisition rejetée
            
            # 2. On rejette l'image si elle est entièrement vide (uniquement des 0)
            if np.sum(image) == 0:
                continue  # Uniquement des zéros -> acquisition rejetée
            
            # Si l'image passe les deux tests, elle est valide
            dictionnaire[self.date(index_jour)] = image
        return dictionnaire

    '''
    def ndvi (self, date, latitude, longitude):
        "Retourne l'indice de végétation au point donné (lat, long)"
        dict_b04 = self.toDict('B04')
        dict_b08 = self.toDict('B08')
        image_b04 = dict_b04[date]
        image_b08 = dict_b08[date]
        pixel_b04 = image_b04.sel(x=latitude, y=longitude, method="nearest") 
        pixel_b08 = image_b08.sel(x=latitude, y=longitude, method="nearest") 
    
        return (pixel_b08.values - pixel_b04.values)/(pixel_b08.values + pixel_b04.values)
    '''