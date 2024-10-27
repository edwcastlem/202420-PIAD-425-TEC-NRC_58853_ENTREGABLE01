import funciones as fn
import pandas as pd


print("GENERANDO DATA...")
# Generamos data aleatoriamente (se crean archivos CSV con los datos generados)
fn.generar_tablas(20, 100, 500)

# Cargamos la data generadada anteriormente
print("CARGANDO DATA...")
usuarios_df = fn.cargar_datos_csv("usuarios.csv")
productos_df = fn.cargar_datos_csv("productos.csv")
ventas_df = fn.cargar_datos_csv("ventas.csv")

print("PROCESANDO VENTAS...")
# Procesamos las ventas (agregamos el precio del producto en las ventas y calculamos el precio total)
ventas_df = fn.procesar_datos_ventas(ventas_df, productos_df)
print(ventas_df)

print("VENTAS POR USUARIO...")
ventas_usuario = fn.total_ventas_por_usuario(ventas_df, usuarios_df)
print(ventas_usuario)

# Compras por usuario
print("COMPRAS POR USUARIO...")
compras_usuario = fn.total_compras_por_usuario(ventas_df, usuarios_df)
print(compras_usuario)

print("COMPRADORES FRECUENTES...")
c_frecuentes = fn.mayores_que_venta_promedio(ventas_df, usuarios_df)
print(c_frecuentes)

print("OTRAS ESTADÍSTICAS...")
estadisticas = fn.generar_estadisticas(ventas_df)
print(estadisticas)