# app/utils_geo.py
from math import radians, sin, cos, asin, sqrt


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula distância aproximada em KM usando fórmula de Haversine.
    Coordenadas em graus decimais.
    """
    R = 6371.0  # raio médio da Terra em km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c
