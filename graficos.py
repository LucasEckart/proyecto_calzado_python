import matplotlib.pylab as plt
import main

def grafico_ventas_por_pais(datos):
    paises = list(datos.keys())
    ventas = list(datos.values())

    plt.figure(figsize=(10, 6))
    plt.bar(paises, ventas)
    plt.xlabel('País')
    plt.ylabel('Ventas ($)')
    plt.title('Ventas de calzados por país')
    plt.xticks(rotation=45)
    plt.show()


def grafico_ventas_por_genero(generos):
    genero = list(generos.keys())
    ventas = list(generos.values())

    plt.figure(figsize=(6, 6))
    plt.pie(ventas, labels=genero, autopct='%1.1f%%')
    plt.title('Distribución de ventas por género seleccionado')
    plt.show()


if __name__ == "__main__":

    db = main.read_db()

    country = db[0]
    gender = db[1]
    size = db[2]
    price = db[3]
    countries = main.paises_unicos(country)

    genero = str(input('Seleccionar genero del calzado (hombre = H, mujer = M, unisex = U): ')).lower()

    if genero == "h":
        gender_target = "Male"
    elif genero == "m":
        gender_target = "Female"
    elif genero == "u":
        gender_target = "Unix"    



    datos_genero = main.ventas_genero_pais(countries, gender_target, country, gender)
    grafico_ventas_por_genero(datos_genero)


    datos_ventas = main.ventas_pais(countries, country, price)
    grafico_ventas_por_pais(datos_ventas)