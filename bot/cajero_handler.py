
import logging
import csv
from scipy import spatial
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from cajero_schema import Cajero

logger = logging.getLogger(__name__)


class CajeroHandler:
    """
    El almacenamiento se realiza en la base de datos basada en documentos TinyDB. Para el dataset en uso 
    resulta suficiente, ya que se accede a los elementos en forma directa, por ser relativa a la lista de 
    puntos de busqueda. (con datasets mas grandes probablemente se utilizaria otro tipo de base de datos)
    """

    def __init__(self) -> None:
        self.db = TinyDB('../files/db.json', storage=CachingMiddleware(JSONStorage))
        self.banelco_table = TinyDB.table(self.db, 'banelco')
        self.link_table = TinyDB.table(self.db, 'link')
        self.init()

    def init(self):
        geo_banelco, geo_link = self.parse_csv('../files/cajeros-automaticos.csv')
        logger.info("Generando arboles..")
        self.link_tree = self.build_kdtree(geo_link)
        self.banelco_tree = self.build_kdtree(geo_banelco)

    def build_kdtree(self, lista: list):
        """
        Los arboles KD proporcionan un tiempo de busqueda promedio de orden O(log n) 
        por lo cual la busqueda es muy eficiente. El arbol contiene los puntos geograficos
        y residen en memoria, con ids relativos a la BD almacenada.
        """
        tree = spatial.KDTree(lista)
        return tree

    def query_tree(self, tree: list, geopoint: list, distance_max: float, amount: int):
        """
        Resulta ideal esta estructira de datos ya que se requiere una busqueda en 2 dimensiones sobre tuplas numericas.
        Se utiliza un algoritmo de tipo 'nearest neighbor search' para lograr la busqueda.
        """
        return tree.query(geopoint, amount, distance_upper_bound=distance_max)

    def get_banelco(self, user_location):
        banelco_points, banelco_data = self.get_cajero_data(
            self.banelco_tree, self.banelco_table, user_location)
        return banelco_points, banelco_data

    def get_link(self, user_location):
        link_points, link_data = self.get_cajero_data(
            self.link_tree, self.link_table, user_location)
        return link_points, link_data

    def db_reload(self):
        self.db.storage.flush()

    def get_cajero_data(self, kdtree, table, geo_tuple, distance=0.00500, amount=3, extrMax=100):
        cajero_ids = self.query_tree(kdtree, geo_tuple, distance, amount)
        table_long = len(table)
        points_raw = cajero_ids[1]
        points = list(filter(lambda x: x < table_long, points_raw))
        freepoints = []
        data = []
        geopoints = []
        for p in points:
            el = table.get(doc_id=p+1)
            if(el['extracciones'] < extrMax):
                data.append(el)
                geopoints.append((float(el['lat']), float(el['long'])))
                freepoints.append(p)
                logger.info(
                    f"{el['ubicacion']} extracciones: {el['extracciones']} {el['lat']} {el['long']}")
            else:
                logger.warning(
                    f" Cajero superó limite de extracciones: {el['ubicacion']} extracciones: {el['extracciones']}")
        self.add_extraction(table, freepoints)
        return geopoints, data

    def parse_csv(self, filename):
        extracciones = 0
        banelco_points = []
        link_points = []
        insert = True
        logger.info('Parseando csv...')
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            if(len(self.banelco_table) > 0 or len(self.link_table) > 0):
                insert = False
            for row in reader:
                if(row[4] == 'LINK'):
                    link_points.append((float(row[1]), float(row[2])))
                    if(insert):
                        self.insert_cajero_db(
                            self.link_table, row, extracciones)
                else:
                    banelco_points.append((float(row[1]), float(row[2])))
                    if(insert):
                        self.insert_cajero_db(
                            self.banelco_table, row, extracciones)
        self.db_reload()
        return banelco_points, link_points

    def add_extraction(self, table, points_raw):

        def add(amount, idx):
            el = table.get(doc_id=idx+1)
            numExt = el['extracciones']
            table.update({'extracciones': numExt+amount}, doc_ids=[idx+1])

        table_long = len(table)
        points = list(filter(lambda x: x < table_long, points_raw))
        cant = len(points)
        if(cant == 3):
            add(0.7, points[0])
            add(0.2, points[1])
            add(0.1, points[2])
        elif(cant == 2):
            add(0.7, points[0])
            add(0.3, points[1])
        elif(cant == 1):
            add(1, points[0])
        else:
            return False
        self.db_reload()
        return True

    def insert_cajero_db(self, table, cajero, extractions):
        newCajero = Cajero(*cajero, extractions)
        table.insert(newCajero.__dict__)

    def reset_cronjob(self):
        logger.info('Reseteando cajeros')
        ids = [x+1 for x in range(len(self.banelco_table))]
        self.banelco_table.update({'extracciones': 0}, doc_ids=ids)
        ids2 = [x+1 for x in range(len(self.link_table))]
        self.link_table.update({'extracciones': 0}, doc_ids=ids2)
        self.db_reload()



