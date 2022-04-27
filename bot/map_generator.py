import os

class MapGenerator:
    def __init__(self, longitud, latitud, geolist, zoomlevel=16):

        self.longitud = longitud
        self.latitud = latitud
        self.geolist = geolist
        self.zoomlevel = zoomlevel

    def get_longitud(self):
        return self.longitud

    def get_latitud(self):
        return self.latitud

    def get_geolist(self):
        return self.geolist    
    
    def get_zoomlevel(self):
        return self.zoomlevel    


    def get_image_url(self):
        api_key = os.getenv("MAPS_KEY")
    
        url = 'https://maps.googleapis.com/maps/api/staticmap?center='
        url += f'{self.latitud},{self.longitud}'
        url += f'&zoom={self.zoomlevel}&size=500x500'
        url += f'&markers=size:tiny%7Ccolor:red%7C{self.latitud},{self.longitud}'
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for lat, long in self.geolist:
            pos = self.geolist.index((lat, long))
            url += f'&markers=color:red%7Clabel:{labels[pos]}%7C{lat},{long}'

        url += f'&key={api_key}'
        url += f'&map_id=51ed0b0105645e4e'

        return url

    


