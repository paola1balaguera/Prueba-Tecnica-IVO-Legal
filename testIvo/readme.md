# Cálculo de Interés Moratorio para Facturas Vencidas

### DESCRIPCION:

Este proyecto calcula el interés de deudas atrasados que debe un deudor a un acreedor sobre facturas vencidas. El cálculo se hace tomando en cuenta las tasas de interés aplicables, los pagos realizados y el período de interés hasta una fecha específica. El objetivo es determinar los intereses totales sobre las deudas.

## Modulos necesarios
    . pip install python-dateutil 
    . pip install python-dotenv



# Incersiones adicionales en la BD

Para cumplir con los requerimientos de la prueba tecnica fue necesario adicionar estos insert en la base de datos de "tasas_de_intereses", puesto que a la fecha de corte no se encontraban esos registros:

URL: https://www.superfinanciera.gov.co/publicaciones/10829/sala-de-prensacomunicados-de-prensa-interes-bancario-corriente-10829/

```
     INSERT INTO `tasas_de_interes` (`fecha_inicio`, `fecha_finalizacion`, `Interes_Bancario_Corriente`) VALUES ('2024-05-01', '2024-05-31', 21.00);
```

```
        INSERT INTO `tasas_de_interes` (`fecha_inicio`, `fecha_finalizacion`, `Interes_Bancario_Corriente`) VALUES ('2024-06-01', '2024-06-30', 20.00);
```

### Definición de Variables

El código comienza definiendo variables globales que se utilizarán a lo largo del script:

- idDeudor: ID del deudor.
- idAcreedor: ID del acreedor.
- fecha_corte: Fecha de corte para el cálculo del interés moratorio.


idDeudor = 1

idAcreedor = 1

fecha_corte = datetime.strptime("2024-06-24", "%Y-%m-%d")


### Obtención de Datos

Se definen funciones para obtener las facturas y los abonos desde la base de datos:

- obtener_facturas_deudor_acreedor(idAcreedor, idDeudor): Obtiene las facturas vencidas entre un deudor y un acreedor.
- obtener_abonos_deudor_acreedor(idAcreedor, idDeudor): Obtiene los abonos realizados por el deudor al acreedor.

### Consulta SQL para obtener las facturas

```
def obtener_facturas_deudor_acreedor(idAcreedor, idDeudor):
    # Consulta SQL para obtener las facturas
    OBTENER_FACTURAS = """SELECT ..."""
    connection.cursor.execute(OBTENER_FACTURAS, (idAcreedor, idDeudor,))
    return connection.cursor.fetchall()

```

### Consulta SQL para obtener los abonos
```
def obtener_abonos_deudor_acreedor(idAcreedor, idDeudor):
   
    OBTENER_ABONOS = """SELECT ..."""
    connection.cursor.execute(OBTENER_ABONOS, (idAcreedor, idDeudor,))
    return connection.cursor.fetchall()
```
