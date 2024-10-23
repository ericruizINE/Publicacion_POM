import pandas as pd
import numpy as np
import re
import pytest
import allure

file_path = '/var/jenkins_home/workspace/Publicacion_POM/tests/data/PRES_2024.csv'
df = pd.read_csv(file_path, skiprows=4, delimiter=',', low_memory=False)  # Cambia ';' por el delimitador correcto
df1 = pd.read_csv(file_path, skiprows=3, nrows=1, header=None, names=["ACTAS_ESPERADAS","ACTAS_REGISTRADAS","ACTAS_FUERA_CATALOGO","ACTAS_CAPTURADAS","PORCENTAJE_ACTAS_CAPTURADAS","ACTAS_CONTABILIZADAS","PORCENTAJE_ACTAS_CONTABILIZADAS","PORCENTAJE_ACTAS_INCONSISTENCIAS","ACTAS_NO_CONTABILIZADAS","LISTA_NOMINAL_ACTAS_CONTABILIZADAS","TOTAL_VOTOS_C_CS","TOTAL_VOTOS_S_CS","PORCENTAJE_PARTICIPACION_CIUDADANA"])

# Mapeo de las columnas datos
CONTABILIZADA = 'CONTABILIZADA'
OBSERVACIONES = 'OBSERVACIONES'
LISTA_NOMINAL = 'LISTA_NOMINAL'
TOTAL_VOTOS_CALCULADO = 'TOTAL_VOTOS_CALCULADO'
TIPO_CASILLA = 'TIPO_CASILLA'

# Mapeo de las columnas conteos
ACTAS_ESPERADAS = 'ACTAS_ESPERADAS'
ACTAS_REGISTRADAS = 'ACTAS_REGISTRADAS'
ACTAS_FUERA_CATALOGO = 'ACTAS_FUERA_CATALOGO'
ACTAS_CAPTURADAS = 'ACTAS_CAPTURADAS'
PORCENTAJE_ACTAS_CAPTURADAS = 'PORCENTAJE_ACTAS_CAPTURADAS'
ACTAS_CONTABILIZADAS = 'ACTAS_CONTABILIZADAS'
PORCENTAJE_ACTAS_CONTABILIZADAS = 'PORCENTAJE_ACTAS_CONTABILIZADAS'
PORCENTAJE_ACTAS_INCONSISTENCIAS = 'PORCENTAJE_ACTAS_INCONSISTENCIAS'
ACTAS_NO_CONTABILIZADAS = 'ACTAS_NO_CONTABILIZADAS'
LISTA_NOMINAL_ACTAS_CONTABILIZADAS = 'LISTA_NOMINAL_ACTAS_CONTABILIZADAS'
TOTAL_VOTOS_C_CS = 'TOTAL_VOTOS_C_CS'
TOTAL_VOTOS_S_CS = 'TOTAL_VOTOS_S_CS'
PORCENTAJE_PARTICIPACION_CIUDADANA = 'PORCENTAJE_PARTICIPACION_CIUDADANA'

# Función para limpiar los valores
def limpiar_valor(valor):
    # Usar regex para extraer solo el contenido entre corchetes y comillas simples
    if isinstance(valor, str):
        # Extrae el contenido entre comillas simples
        return ', '.join(re.findall(r"'([^']*)'", valor))
    return valor
# Aplicar la limpieza a la columna
df[OBSERVACIONES] = df[OBSERVACIONES].apply(limpiar_valor)

# Filtros para realizar conteos y enviarlos como parametros
valores_especificos = ['1']
valores_especificos2 = ['2']
valores_especificos3 = ['0']
valores_especificos4 = ['0','1','2']
valores_especificos5 = ['0','1']
valores_especificos6 = [
    'Todos los campos ilegibles',
    'Sin dato',
    'Ilegible',
    'Todos los campos vacíos',
    'Ilegible, Sin dato',
    'Excede Lista Nominal',
    'Excede Lista Nominal, Sin dato',
    'Excede Lista Nominal, Ilegible',
    'Excede Lista Nominal, Ilegible, Sin dato'
]

if CONTABILIZADA in df.columns:
    filtro = df[CONTABILIZADA].isin(valores_especificos)
    df_filtrado = df[filtro]

if CONTABILIZADA in df.columns:
    filtro2 = df[CONTABILIZADA].isin(valores_especificos2)
    df_filtrado2 = df[filtro2]

if CONTABILIZADA in df.columns:
    filtro3 = df[CONTABILIZADA].isin(valores_especificos3)
    df_filtrado3 = df[filtro3]

if CONTABILIZADA in df.columns:
    filtro4 = df[CONTABILIZADA].isin(valores_especificos4)
    df_filtrado4 = df[filtro4]

if CONTABILIZADA in df.columns:
    filtro5 = df[CONTABILIZADA].isin(valores_especificos5)
    df_filtrado5 = df[filtro5]

if OBSERVACIONES in df.columns:
    filtro6 = df[OBSERVACIONES].isin(valores_especificos6)
    df_filtrado6 = df[filtro6]

if CONTABILIZADA in df.columns and LISTA_NOMINAL in df.columns:
    df_filtrado7 = df[df[CONTABILIZADA] == 1].copy()
    # Convertir los datos a numéricos si es necesario
    df_filtrado7[LISTA_NOMINAL] = pd.to_numeric(df_filtrado[LISTA_NOMINAL], errors='coerce')
    
if CONTABILIZADA in df.columns and TOTAL_VOTOS_CALCULADO in df.columns:
    df_filtrado8 = df[df[CONTABILIZADA] == 1].copy()
    # Convertir los datos a numéricos si es necesario
    df_filtrado8[TOTAL_VOTOS_CALCULADO] = pd.to_numeric(df_filtrado[TOTAL_VOTOS_CALCULADO], errors='coerce')

if TOTAL_VOTOS_CALCULADO in df.columns and TIPO_CASILLA in df.columns:
    #df_filtrado9 = df[df[TIPO_CASILLA] != 'S'].copy()
    df_filtrado9 = df[(df[CONTABILIZADA].isin(['1','2'])) & (df[TIPO_CASILLA] != 'S')].copy()
    # Convertir los datos a numéricos si es necesario
    df_filtrado9[TOTAL_VOTOS_CALCULADO] = pd.to_numeric(df_filtrado9[TOTAL_VOTOS_CALCULADO], errors='coerce')

    value_counts = df_filtrado[CONTABILIZADA].value_counts()
    value_counts1 = df_filtrado2[CONTABILIZADA].value_counts()
    value_counts2 = df_filtrado3[CONTABILIZADA].value_counts()
    value_counts3 = df_filtrado4[CONTABILIZADA].astype(int).value_counts().sum() 
    value_counts3 = [value_counts3]
    value_counts4 = df_filtrado5[CONTABILIZADA].astype(int).value_counts().sum() 
    value_counts4 = [value_counts4]
    value_counts5 = (df_filtrado5[CONTABILIZADA].astype(int).value_counts().sum() * 100) / df1[ACTAS_ESPERADAS].astype(int).values 
    value_counts5 = pd.Series(value_counts5)
    value_counts5 = value_counts5.apply(lambda x: int(x * 10000) / 10000)
    value_counts6 = (df_filtrado[CONTABILIZADA].value_counts() * 100) / df1[ACTAS_ESPERADAS].astype(int).values 
    value_counts6 = pd.Series(value_counts6)
    value_counts6 = value_counts6.apply(lambda x: int(x * 10000) / 10000)
    value_counts7 = (df_filtrado6[OBSERVACIONES].value_counts().sum() * 100) / df1[ACTAS_ESPERADAS].astype(int).values 
    value_counts7 = pd.Series(value_counts7)
    value_counts7 = value_counts7.apply(lambda x: int(x * 10000) / 10000)
    value_counts8 = df_filtrado7[LISTA_NOMINAL].sum()
    value_counts8 = [value_counts8]
    value_counts9 = (df_filtrado8[TOTAL_VOTOS_CALCULADO].sum() * 100) / value_counts8
    value_counts9 = pd.Series(value_counts9)
    value_counts9 = value_counts9.apply(lambda x: int(x * 10000) / 10000)
    value_counts10 = df_filtrado8[TOTAL_VOTOS_CALCULADO].sum()
    value_counts10 = [value_counts10]
    value_counts11 = df_filtrado9[TOTAL_VOTOS_CALCULADO].sum()
    value_counts11 = [value_counts11]
    actas_regis = df1[ACTAS_REGISTRADAS].values
    actas_fuera = df1[ACTAS_FUERA_CATALOGO].values
    actas_cap = df1[ACTAS_CAPTURADAS].values
    actas_cap_por = df1[PORCENTAJE_ACTAS_CAPTURADAS].values
    actas_con = df1[ACTAS_CONTABILIZADAS].values
    actas_con_por = df1[PORCENTAJE_ACTAS_CONTABILIZADAS].values
    actas_incon_por = df1[PORCENTAJE_ACTAS_INCONSISTENCIAS].values
    actas_nocon = df1[ACTAS_NO_CONTABILIZADAS].values
    lnactascon = df1[LISTA_NOMINAL_ACTAS_CONTABILIZADAS].values
    totalvotosc = df1[TOTAL_VOTOS_C_CS].values
    totalvotoss = df1[TOTAL_VOTOS_S_CS].values
    participacionciu = df1[PORCENTAJE_PARTICIPACION_CIUDADANA].values
    #print(value_counts11)

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('Validación de Actas Registradas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_registradas_coinciden():
    """
    Prueba que los valores de ACTAS_REGISTRADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de ACTAS_REGISTRADAS con los esperados"):
        if np.array_equal(value_counts3, actas_regis):
            allure.attach(
                f"Los valores de ACTAS_REGISTRADAS coinciden: Conteo CSV: {value_counts3} Encabezado CSV: {actas_regis}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"Los valores de ACTAS_REGISTRADAS no coinciden. Conteo CSV: {value_counts3} Encabezado CSV: {actas_regis}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        try:
            assert np.array_equal(value_counts3, actas_regis)
        except AssertionError:
            pytest.fail(f"Los valores no coinciden. Conteo CSV: {value_counts3} Encabezado CSV: {actas_regis}")

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('Validación de Actas Fuera de Catálogo')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_fuera_catalogo_coinciden():
    """
    Prueba que los valores de ACTAS_FUERA_CATALOGO coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de ACTAS_FUERA_CATALOGO con los esperados"):
        if np.array_equal(value_counts1, actas_fuera):
            allure.attach(
                f"Los valores de ACTAS_FUERA_CATALOGO coinciden: Conteo CSV: {value_counts1} Encabezado CSV: {actas_fuera}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"Los valores de ACTAS_FUERA_CATALOGO no coinciden. Conteo CSV: {value_counts1} Encabezado CSV: {actas_fuera}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        try:
            assert np.array_equal(value_counts1, actas_fuera)
        except AssertionError:
            pytest.fail(f"Los valores no coinciden. Conteo CSV: {value_counts1} Encabezado CSV: {actas_fuera}")

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('4.- Validación de Actas Capturadas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_capturadas_coinciden():
    """
    Prueba que los valores de ACTAS_CAPTURADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de ACTAS_CAPTURADAS con los esperados"):
        if np.array_equal(value_counts4, actas_cap):
            allure.attach(
                f"4.- Los valores de ACTAS_CAPTURADAS coinciden: Conteo CSV: {value_counts4} Encabezado CSV: {actas_cap}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"4.- Los valores de ACTAS_CAPTURADAS no coinciden. Conteo CSV: {value_counts4} Encabezado CSV: {actas_cap}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        try:
            assert np.array_equal(value_counts4, actas_cap)
        except AssertionError:
            pytest.fail(f"Los valores no coinciden. Conteo CSV: {value_counts4} Encabezado CSV: {actas_cap}")

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('Validación de Porcentaje de Actas Capturadas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_porcentaje_capturadas_coinciden():
    """
    Prueba que los valores de PORCENTAJE_ACTAS_CAPTURADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de PORCENTAJE_ACTAS_CAPTURADAS con los esperados"):
        if np.array_equal(value_counts5, actas_cap_por):
            allure.attach(
                f"Los valores de PORCENTAJE_ACTAS_CAPTURADAS coinciden: Conteo CSV: {value_counts5} Encabezado CSV: {actas_cap_por}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"Los valores de PORCENTAJE_ACTAS_CAPTURADAS no coinciden. Conteo CSV: {value_counts5} Encabezado CSV: {actas_cap_por}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        try:
            assert np.array_equal(value_counts5, actas_cap_por)
        except AssertionError:
            pytest.fail(f"Los valores no coinciden. Conteo CSV: {value_counts5} Encabezado CSV: {actas_cap_por}")

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('Validación de Actas Contabilizadas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_contabilizadas_coinciden():
    """
    Prueba que los valores de ACTAS_CONTABILIZADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de ACTAS_CONTABILIZADAS con los esperados"):
        if np.array_equal(value_counts, actas_con):
            allure.attach(
                f"Los valores de ACTAS_CONTABILIZADAS coinciden: {actas_con}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"Los valores de ACTAS_CONTABILIZADAS no coinciden. {actas_con} vs {value_counts}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        try:
            assert np.array_equal(value_counts, actas_con)
        except AssertionError:
            pytest.fail(f"Los valores no coinciden. Conteo CSV: {value_counts} Encabezado CSV: {actas_con}")

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('Validación de Porcentaje de Actas Contabilizadas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_porcentaje_contabilizadas_coinciden():
    """
    Prueba que los valores de PORCENTAJE_ACTAS_CONTABILIZADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de PORCENTAJE_ACTAS_CONTABILIZADAS con los esperados"):
        if np.array_equal(value_counts6, actas_con_por):
            allure.attach(
                f"Los valores de PORCENTAJE_ACTAS_CONTABILIZADAS coinciden: Conteo CSV: {value_counts6} Encabezado CSV: {actas_con_por}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"Los valores de PORCENTAJE_ACTAS_CONTABILIZADAS no coinciden. Conteo CSV: {value_counts6} Encabezado CSV: {actas_con_por}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        try:
            assert np.array_equal(value_counts6, actas_con_por)
        except AssertionError:
            pytest.fail(f"Los valores no coinciden. Conteo CSV: {value_counts6} Encabezado CSV: {actas_con_por}")

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('Validación de Porcentaje de Actas con Inconcistencias')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_porcentaje_inconsistencias_coinciden():
    """
    Prueba que los valores de PORCENTAJE_ACTAS_INCONSISTENCIAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de PORCENTAJE_ACTAS_INCONSISTENCIAS con los esperados"):
        if np.array_equal(value_counts7, actas_incon_por):
            allure.attach(
                f"Los valores de PORCENTAJE_ACTAS_INCONSISTENCIAS coinciden: Conteo CSV: {value_counts7} Encabezado CSV: {actas_incon_por}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"Los valores de PORCENTAJE_ACTAS_INCONSISTENCIAS no coinciden. Conteo CSV: {value_counts7} Encabezado CSV: {actas_incon_por}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        try:
            assert np.array_equal(value_counts7, actas_incon_por)
        except AssertionError:
            pytest.fail(f"Los valores no coinciden. Conteo CSV: {value_counts7} Encabezado CSV: {actas_incon_por}")

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('Validación de Actas No Contabilizadas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_actas_no_contabilizadas_coinciden():
    """
    Prueba que los valores de ACTAS_NO_CONTABILIZADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de ACTAS_NO_CONTABILIZADAS con los esperados"):
        if np.array_equal(value_counts2, actas_nocon):
            allure.attach(
                f"Los valores de ACTAS_NO_CONTABILIZADAS coinciden: Conteo CSV: {value_counts2} Encabezado CSV: {actas_nocon}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"Los valores de ACTAS_NO_CONTABILIZADAS no coinciden. Conteo CSV: {value_counts2} Encabezado CSV: {actas_nocon}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        try:
            assert np.array_equal(value_counts2, actas_nocon)
        except AssertionError:
            pytest.fail(f"Los valores no coinciden. Conteo CSV: {value_counts2} Encabezado CSV: {actas_nocon}")

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('Validación de Lista Nominal de Actas Contabilizadas')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_lista_nominal_actas_contabilizadas_coinciden():
    """
    Prueba que los valores de LISTA_NOMINAL_ACTAS_CONTABILIZADAS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de LISTA_NOMINAL_ACTAS_CONTABILIZADAS con los esperados"):
        if np.array_equal(value_counts8, lnactascon):
            allure.attach(
                f"Los valores de LISTA_NOMINAL_ACTAS_CONTABILIZADAS coinciden: Conteo CSV: {value_counts8} Encabezado CSV: {lnactascon}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"Los valores de LISTA_NOMINAL_ACTAS_CONTABILIZADAS no coinciden. Conteo CSV: {value_counts8} Encabezado CSV: {lnactascon}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        try:
            assert np.array_equal(value_counts8, lnactascon)
        except AssertionError:
            pytest.fail(f"Los valores no coinciden. Conteo CSV: {value_counts8} Encabezado CSV: {lnactascon}")

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('Validación de Total Votos C_CS')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_total_votos_c_cs_coinciden():
    """
    Prueba que los valores de TOTAL_VOTOS_C_CS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de TOTAL_VOTOS_C_CS con los esperados"):
        if np.array_equal(value_counts10, totalvotosc):
            allure.attach(
                f"Los valores de TOTAL_VOTOS_C_CS coinciden: Conteo CSV: {value_counts10} Encabezado CSV: {totalvotosc}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"Los valores de TOTAL_VOTOS_C_CS no coinciden. Conteo CSV: {value_counts10} Encabezado CSV: {totalvotosc}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        try:
            assert np.array_equal(value_counts10, totalvotosc)
        except AssertionError:
            pytest.fail(f"Los valores no coinciden. Conteo CSV: {value_counts10} Encabezado CSV: {totalvotosc}")

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('Validación de Total de Votos S_CS')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_total_votos_s_cs_coinciden():
    """
    Prueba que los valores de TOTAL_VOTOS_S_CS coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de TOTAL_VOTOS_S_CS con los esperados"):
        if np.array_equal(value_counts11, totalvotoss):
            allure.attach(
                f"Los valores de TOTAL_VOTOS_S_CS coinciden: Conteo CSV: {value_counts11} Encabezado CSV: {totalvotoss}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"Los valores de TOTAL_VOTOS_S_CS no coinciden. Conteo CSV: {value_counts11} Encabezado CSV: {totalvotoss}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        try:
            assert np.array_equal(value_counts11, totalvotoss)
        except AssertionError:
            pytest.fail(f"Los valores no coinciden. Conteo CSV: {value_counts11} Encabezado CSV: {totalvotoss}")

@allure.feature('Validación de datos CSV Publicación')  # Usa etiquetas estándar de Allure
@allure.story('13.- Validación de Porcentaje de Participación Ciudadana')  # Usa etiquetas estándar de Allure
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_porcentaje_participacion_ciudadana_coinciden():
    """
    Prueba que los valores de PORCENTAJE_PARTICIPACION_CIUDADANA coincidan con los valores esperados.
    """
    with allure.step("Comparando los valores de PORCENTAJE_PARTICIPACION_CIUDADANA con los esperados"):
        if np.array_equal(value_counts9, participacionciu):
            allure.attach(
                f"13.- Los valores de PORCENTAJE_PARTICIPACION_CIUDADANA coinciden: Conteo CSV: {value_counts9} Encabezado CSV: {participacionciu}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                f"13.- Los valores de PORCENTAJE_PARTICIPACION_CIUDADANA no coinciden. Conteo CSV: {value_counts9} Encabezado CSV: {participacionciu}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
        try:
            assert np.array_equal(value_counts9, participacionciu)
        except AssertionError:
            pytest.fail(f"Los valores no coinciden. Conteo CSV: {value_counts9} Encabezado CSV: {participacionciu}")