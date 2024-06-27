import connection
from datetime import datetime
from dateutil.relativedelta import relativedelta

idDeudor = 1
idAcreedor = 1
fecha_corte = datetime.strptime("2024-06-24", "%Y-%m-%d")

total_abonos = None
abonos = None
abono_actual = 0
facturas = {}
total = 0

def obtener_facturas_deudor_acreedor(idAcreedor, idDeudor):
    OBTENER_FACTURAS = """SELECT SUM(subquery.valor) AS suma, subquery.id_facturas, subquery.fecha_vencimiento 
    FROM (SELECT mercancias.id_facturas, ((valor * (iva/100)) + valor) AS valor, facturas.fecha_vencimiento FROM mercancias 
    JOIN facturas ON facturas.id_facturas = mercancias.id_facturas
    WHERE facturas.id_acreedor = %s AND facturas.id_deudor = %s) AS subquery
    GROUP BY subquery.id_facturas ORDER BY subquery.id_facturas;"""

    connection.cursor.execute(OBTENER_FACTURAS, (idAcreedor, idDeudor,))

    return connection.cursor.fetchall()

def obtener_abonos_deudor_acreedor(idAcreedor, idDeudor):
    OBTENER_ABONOS = """SELECT fecha_abono, valor_abono 
    FROM abonos
    where id_acreedor = %s AND id_deudor = %s"""

    connection.cursor.execute(OBTENER_ABONOS, (idAcreedor, idDeudor))

    return connection.cursor.fetchall()

def obtener_diferencia_dias(fecha1, fecha2):

    
    diferencia = relativedelta(fecha1, fecha2)

    hoy = datetime.now()
    
    then = hoy - (hoy - diferencia)

    return then.days


def obtener_porcentaje_tasa_de_interes(mes, anio):
    OBTENER_TASA_DE_INTERES = """SELECT Interes_Bancario_Corriente, fecha_finalizacion
    FROM tasas_de_interes 
    WHERE MONTH(fecha_inicio) = %s AND MONTH(fecha_finalizacion) = %s
    AND YEAR(fecha_inicio) = %s AND YEAR(fecha_finalizacion) = %s
    """

    connection.cursor_2.execute(OBTENER_TASA_DE_INTERES, (mes, mes, anio, anio,))
    
    result = connection.cursor_2.fetchall()

    if len(result) == 0:
        print('Se ingreso una fecha de corte que todavia no se registra en la tasa de intereses, fuera de rango')
        exit()
    return result

def calcular_tasa_usura_mensual(interes_bancario_corriente):
    return float(interes_bancario_corriente)*1.5

def calcular_tasa_diaria(usura):
    return float( 1 + float(usura)) ** (1/30) - 1

def calcular_interes_moratorio(capital, dias_mes, tasa_diaria):
    return capital * dias_mes * tasa_diaria

for valor, id_factura, fecha_vencimiento in obtener_facturas_deudor_acreedor(idAcreedor, idDeudor):

    facturas[id_factura] = []

    dias_finales = obtener_diferencia_dias(fecha_corte, fecha_vencimiento)
    
    fecha_vencimiento_sum = fecha_vencimiento
    valor_sum = valor

    while(dias_finales > 0): 

        if total_abonos == None:
            abonos = obtener_abonos_deudor_acreedor(idAcreedor, idDeudor)
            total_abonos = len(abonos)
            
        if total_abonos > abono_actual:
            fecha_abono = abonos[abono_actual][0]
            valor_abono = abonos[abono_actual][1]

        dias_totales = obtener_diferencia_dias(fecha_abono, fecha_vencimiento_sum)

        if fecha_vencimiento_sum.month <= fecha_corte.month:
            tasa_interes_bancario = obtener_porcentaje_tasa_de_interes(fecha_vencimiento_sum.month, fecha_vencimiento_sum.year)[0]

            porcentaje_tasa_interes = tasa_interes_bancario[0]
            fecha_fin_tasa_interes = tasa_interes_bancario[1]

        if fecha_abono.month <= fecha_fin_tasa_interes.month and fecha_abono.day <= fecha_fin_tasa_interes.day:
            if dias_mensuales > dias_finales:
                dias_mensuales = dias_finales
            else:
                dias_totales = dias_totales + 1
                dias_mensuales = obtener_diferencia_dias(fecha_abono, fecha_vencimiento_sum)+1
        else:
            dias_mensuales = obtener_diferencia_dias(fecha_fin_tasa_interes, fecha_vencimiento_sum)
            if fecha_vencimiento_sum.day == 1:
                dias_mensuales = dias_mensuales + 1


        tasa_usura = calcular_tasa_usura_mensual(porcentaje_tasa_interes)

        tasa_diaria = calcular_tasa_diaria(tasa_usura)

        interes_moratorio = calcular_interes_moratorio(valor_sum, dias_mensuales, tasa_diaria)
        
        dias_totales = dias_totales - dias_mensuales
        if (dias_totales == 0):
            interes_moratorio = interes_moratorio - valor_abono
            dias_faltantes = obtener_diferencia_dias(fecha_fin_tasa_interes, fecha_abono)
            dias_mensuales = dias_mensuales + dias_faltantes
            interes_moratorio = calcular_interes_moratorio(interes_moratorio, dias_faltantes, tasa_diaria)
            abono_actual = abono_actual + 1
        """ print("abono: "+str(abono_actual)) """

        facturas[id_factura].append({
            'mes': fecha_vencimiento_sum.month,
            'valor': interes_moratorio
        })
        
        dias_finales = dias_finales - dias_mensuales
        """ print(dias_mensuales)
        print(dias_finales) """
        
        fecha_vencimiento_sum = fecha_vencimiento_sum + relativedelta(months=1)
        fecha_vencimiento_sum = fecha_vencimiento_sum.replace(day=1)

        valor_sum = interes_moratorio
""" print(facturas) """

for factura in facturas:
    total = total + facturas[factura][fecha_corte.month-factura]["valor"]

print("El valor del dinero adeudado hasta la fecha de corte es: " + str(total) )

# Cerramos la variable encargada de las consultas
connection.cursor.close()
connection.cursor_2.close()
#   cierre de conexion
connection.closeConnection()
connection.closeConnection2()