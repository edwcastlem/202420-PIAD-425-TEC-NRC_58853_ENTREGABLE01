import pandas as pd
import numpy as np    

# Generación de datos para los usuarios
def generar_tablas(num_usuarios, num_productos, num_ventas):
    # Lista para generar nombres y aepllidos aleatoriamente
    nombres = ['Luis', 'Adolfo', 'Pedro', 'Carlos', 'Julio', 'Alberto', 'Jorge', 'Felipe']
    apellidos = ['Perez', 'Garcia', 'Martinez', 'Ruiz', 'Lopez', 'Mendoza', 'Gomez', 'Jimenez']

    usuarios = {
        'usuario_id': range(1, num_usuarios + 1), # PAra generar los id de usuarios empezando desde 1
        'nombres': [f"{np.random.choice(nombres)} {np.random.choice(apellidos)}" for _ in range(num_usuarios)], # Genera nobres y apellidos aleatorios
        'edad': np.random.randint(18, 65, num_usuarios), # Edad aleatoria entre 18 y 65
        'genero': np.random.choice(['M', 'F'], num_usuarios), # Genero aleatorio se escoge entre 'M' y 'F'
        'visitas_totales': np.random.randint(5, 100, num_usuarios) # Visitas totales aleatorias entre 5 y 100
    }

    usuarios_df = pd.DataFrame(usuarios) # creamos un DataFrame con los datos de usuarios
    usuarios_df.to_csv("usuarios.csv", index=False) # Generamos un archivo CSV con los datos de usuarios
    print("Archivo de usuarios generado: usuarios.csv")

    # Generación de datos para los productos
    productos = {
        'producto_id': range(1, num_productos + 1), # Generamos los id de productos empezando desde 1
        'categoria': np.random.choice(['Electrónica', 'Hogar', 'Juguetes', 'Ropa', 'Libros'], num_productos), # Generamos una categoría aleatoria desde una lista de categorías
        'precio': np.round(np.random.uniform(10, 500, num_productos), 2) # Generamos un precio aleatorio entre 10 y 500 redondeado a dos decimales
    }

    productos_df = pd.DataFrame(productos)
    productos_df.to_csv("productos.csv", index=False)
    print("Archivo de productos generado: productos.csv")

    # Generación de datos para las ventas
    ventas = {
        'venta_id': range(1, num_ventas + 1),  # Generamos los id de ventas empezando desde 1
        'usuario_id': np.random.choice(usuarios['usuario_id'], num_ventas),  # Se escoge un usuario aleatorio de la lista de usuarios creada anteriormente y se repite num_ventas veces
        'producto_id': np.random.choice(productos['producto_id'], num_ventas), # Se escoge un producto aleatorio de la lista de productos similarmene a lo anterior
        'cantidad': np.random.randint(1, 5, num_ventas), # Se escoge una cantidad aleatoria de productos entre 1 y 5 y se repite num_ventas veces
        'fecha': pd.to_datetime(
            np.random.choice(pd.date_range("2024-01-01", "2024-10-27"), num_ventas) # Se escoge una fecha aleatoria entre los valores dados y se transforma a un formato adecuado para pandas
        )
    }

    # Creamos un dataFrame con los datos de ventas
    ventas_df = pd.DataFrame(ventas)

    # Escribimos el dataFrame final en un archivo CSV
    ventas_df.to_csv("ventas.csv", index=False)
    print("Archivo de ventas generado: ventas.csv")


# Cargar datos al dataframe
def cargar_datos_csv(ruta_archivo):
    try:
        data = pd.read_csv(ruta_archivo)
        print(f"{len(data)} datos cargados correctamente.")
        return data
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None


# Procesamos las ventas (agregamos el precio de cada producto y calculamos el total de la venta)
def procesar_datos_ventas(data_ventas, data_productos):
    # Hacemos un merge con los datos de productos para obtener el precio de cada producto en cada venta
    # Utilizamos el id de producto como llave para hacer el merge de los dataFrames
    data_ventas = data_ventas.merge(data_productos[['producto_id', 'precio']], on='producto_id')

    # Calculamos el total de la venta para cada venta y lo agregamos al dataFrame final
    data_ventas['monto'] = data_ventas['cantidad'] * data_ventas['precio']

    return data_ventas


# Calculamos la cantidad total de ventas por usuario
def total_ventas_por_usuario(data_ventas, data_usuarios):
    total_ventas_por_usuario = data_ventas.groupby("usuario_id")["monto"].sum().reset_index()

    # Unimos los dataframes usuarios_df y total_ventas_por_usuario por el campo comun
    total_ventas = pd.merge(data_usuarios, total_ventas_por_usuario, on="usuario_id")

    # Seleccionamos las columnas que nos interesan mostrar
    usuarios_con_total_ventas = total_ventas[["usuario_id", "nombres", "monto"]]

    # Ordenamos los resultados por el total de ventas en orden descendiente
    total_ventas = usuarios_con_total_ventas.sort_values("monto", ascending=False)
    total_ventas.reset_index(drop=True, inplace=True) # Reseteamos los índices para que comience desde 0

    return total_ventas


# Función para calcular el número de compras por usuario
def total_compras_por_usuario(data_ventas, data_usuarios):
    total_compras_por_usuario = data_ventas.groupby("usuario_id")['monto'].count().reset_index(name="numero de compras")

    # Unimos los dataframes usuarios_df y total_compras_por_usuario por el campo comun
    total_compras = pd.merge(total_compras_por_usuario, data_usuarios[['usuario_id', 'nombres']], on="usuario_id")
    
    # Ordenamos las columnas que nos interesan
    return total_compras[['usuario_id', 'nombres', 'numero de compras']].sort_values("numero de compras", ascending=False).reset_index(drop=True)


# Función para identificar los que compran bastante (compran mas que la cantidad promedio)
def mayores_que_venta_promedio(data_ventas, data_usuarios):
    compradores_frecuentes = data_ventas.groupby('usuario_id')['cantidad'].sum().reset_index(name="productos_comprados")
    nro_promedio_ventas = compradores_frecuentes['productos_comprados'].mean().round(2)

    print(f"Numero de ventas promedio: {nro_promedio_ventas}")

    # Filtramos los usuarios que compraron mas de la cantidad promedio
    compradores_frecuentes = compradores_frecuentes[compradores_frecuentes['productos_comprados'] > nro_promedio_ventas]
    
    # Agregamos el nombre de los usuarios
    compradores_frecuentes = pd.merge(compradores_frecuentes, data_usuarios[['usuario_id', 'nombres']], on="usuario_id")

    return compradores_frecuentes[['usuario_id', 'nombres', 'productos_comprados']].sort_values("productos_comprados", ascending=False).reset_index(drop=True)

# Funcion para generar reportes estadisticos con describe
def generar_estadisticas(data_ventas):
    estadisticos = data_ventas[['cantidad', 'monto']].describe().round(2)
    return estadisticos