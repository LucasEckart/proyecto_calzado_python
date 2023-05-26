import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, not_
import numpy as np


# Crear el motor de la base de datos
engine = sqlalchemy.create_engine("sqlite:///ventas_calzados.db")
base = declarative_base()

# Consumir la base de datos
class VentasCalzados(base):
    
    __tablename__ = "venta"

    id = Column(Integer, primary_key=True)
    date = Column(String)
    product_id = Column(Integer)
    country = Column(String)
    gender =  Column(String)
    size =  Column(String)
    price =  Column(String)

    def __repr__(self):
        return f'Producto: {self.product_id}'


def read_db():
    '''lee la base de datos, elimina valores faltantes, almacena las columnas requeridas en arrays'''
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(VentasCalzados).filter(
        not_(VentasCalzados.date == ''),
        not_(VentasCalzados.product_id == ''),
        not_(VentasCalzados.country == ''),
        not_(VentasCalzados.gender == ''),
        not_(VentasCalzados.size == ''),
        not_(VentasCalzados.price == '')
    )

    pais = [i.country for i in query]
    genero = [i.gender for i in query]
    talle = [i.size for i in query]
    precio = [float(i.price.replace('$', '').replace(' ', '')) for i in query]

    country = np.array(pais)
    gender = np.array(genero)
    size = np.array(talle)
    price = np.array(precio)

    return country, gender, size, price


def paises_unicos(country):
    '''lista de paises que realizaron ventas'''
    return np.unique(country)
    

def ventas_pais(countries, country, price):
    '''diccionario con datos de dinero recaudado por cada pais'''
    datos = {}
    for p in countries:
        paises = country == p
        ventas = price[paises]
        suma_total = np.sum(ventas)
        datos[p] = suma_total
    return datos


def calzado_pais(countries, country, size):
    '''diccionario con talles mas vendidos por cada pais'''
    talles_mas_vendidos = {}
    for p in countries:
        paises = country == p
        talles = size[paises]
        talle, recuento = np.unique(talles, return_counts=True)
        mas_vendidos = talle[np.argmax(recuento)]
        talles_mas_vendidos[p] = mas_vendidos
    return talles_mas_vendidos
        

def ventas_genero_pais(countries, gender_target, country, gender):
    '''diccionario con genero de zapatillas mas vendidas por pais'''
    generos = {}
    for p in countries:
        pais = country == p
        genero = gender == gender_target
        pais_genero = pais & genero
        ventas_totales = len(country[pais_genero])
        generos[p] = ventas_totales
    return generos




if __name__ == "__main__":
    
    db = read_db()

    country = db[0]
    gender = db[1]
    size = db[2]
    price = db[3]

    countries = paises_unicos(country)
    plata = ventas_pais(countries, country, price)
    talles = calzado_pais(countries, country, size)

    genero = str(input('Seleccionar genero del calzado (hombre = H, mujer = M, unisex = U): ')).lower()

    if genero == "h":
        gender_target = "Male"
    elif genero == "m":
        gender_target = "Female"
    elif genero == "u":
        gender_target = "Unix"   


    ventas_genero = ventas_genero_pais(countries, gender_target, country, gender)


    headers = ('Pais', 'Dinero recuadado', 'Talle mas vendidos', 'Ventas totales del genero seleccionado')
    print(f"{headers[0]:<20s} {headers[1]:<25s} {headers[2]:<25s} {headers[3]:<25s}")
    print("-"*100)
    for country in countries:
        recaudo = plata[country]
        talle = talles[country]
        ventas = ventas_genero[country]
        print(f'{country:<20} {recaudo:<25} {talle:<25} {ventas:<10}')

