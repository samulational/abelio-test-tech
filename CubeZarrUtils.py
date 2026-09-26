import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

class CubeZarr:
    """Classe dédiée à l'exploitation d'un cube satellite Zarr v3 unique (parcelle)."""
    def __init__(self, chemin_zarr, bandes):
        self.chemin_zarr = chemin_zarr
        self.ds = xr.open_zarr(chemin_zarr)
        self.x = self.ds["x"]
        self.y = self.ds["y"]
        self.spatial_ref = self.ds["spatial_ref"]
        self.raster = self.ds["raster"]
        self.bandes = self.ds["band"].values.tolist()
        self.dates = self.ds["time"].values
        self.dataframe = self.df(bandes)

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
    
    def df(self, bandes):
        """Retourne un dataframe contenant les dates ré-ordonnées et les bandes choisies"""
        donnees = []
        for index_jour in range(len(self.dates) - 1, -1, -1):
            ligne = {
                "date": self.date(index_jour)
            }
            for bande in bandes:                
                image = self.bande(index_jour, bande)
                # Image invalide si elle contient un NaN ou est vide
                if np.isnan(image).any() or np.sum(image) == 0:
                    continue
                ligne[bande] = image
            donnees.append(ligne)
        return pd.DataFrame(donnees)

