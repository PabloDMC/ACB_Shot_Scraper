import time
import pandas as pd
import re

def procesar_tiros(tiros, equipo_local, equipo_visitante, id_partido, id_jornada=None, temporada=None, competicion=None, playoff=None):
    """
    Procesa los datos de los tiros de un partido y devuelve una lista de resultados.

    Args:
        tiros (list): Lista de objetos de tiro que se deben procesar.
        equipo_local (str): Nombre del equipo local.
        equipo_visitante (str): Nombre del equipo visitante.
        id_partido (int): ID del partido.
        id_jornada (int): ID de la jornada.
        temporada (str): Temporada en formato "YYYY-YYYY".
        competicion (str): Nombre de la competición.
        playoff (bool): Indica si el partido es de playoff.

    Returns:
        list: Una lista de datos procesados de los tiros.
    """
    datos = []
    for tiro in tiros:
        try:
            texto = tiro.get_text(separator=' ', strip=True)
            match = re.match(r"(\d{2}:\d{2}) (PR\d|\dC) (\d+)- (\d+) (.+?) (Triple|Tiro de 2|Mate) ?(anotado|fallado)?", texto)
            if match:
                tiempo = match.group(1)
                cuarto = match.group(2)
                resultado_local = match.group(3)
                resultado_visitante = match.group(4)
                nombre = match.group(5)
                descripcion = match.group(6)
                anotado = False if match.group(7)=="fallado" else True

                datos.append([
                    nombre, tiro.get('x', 'No definido'), tiro.get('y', 'No definido'),
                    cuarto, tiempo, equipo_local, resultado_local,
                    resultado_visitante, equipo_visitante, descripcion,
                    anotado, id_partido, id_jornada, temporada,
                    competicion, playoff
                ])
            else:
                print(f"Formato de texto no válido: {texto}")
        except AttributeError as e:
            print(f"Error al procesar el tiro: {e}")
        except Exception as e:
            print(f"Error inesperado al procesar el tiro: {e}")
    return datos

def reintentar(funcion, max_reintentos=3, *args, **kwargs):
    """
    Reintenta ejecutar una función específica hasta `max_reintentos` veces.

    Args:
        funcion (callable): La función que se va a ejecutar.
        max_reintentos (int): Número máximo de reintentos.
        *args: Argumentos posicionales para la función.
        **kwargs: Argumentos con nombre para la función.

    Returns:
        Any: El resultado de la función si tiene éxito, o None si falla.
    """
    for intento in range(max_reintentos):
        try:
            return funcion(*args, **kwargs)
        except Exception as e:
            print(f"Error al ejecutar {funcion.__name__}: {e}. Reintento {intento + 1}/{max_reintentos}")
            time.sleep(2)  # Esperar antes de reintentar
    print(f"Fallaron todos los intentos para {funcion.__name__}.")
    return None

def guardar_datos_csv(data, archivo):
    """
    Guarda los datos en un archivo CSV.

    Args:
        data (list): Datos a guardar.
        archivo (str): Nombre del archivo de salida.
    """
    df = pd.DataFrame(data, columns=[
                    'nombre', 'x', 'y', 'cuarto', 'tiempo', 'equipo_local',
                    'resultado_local', 'resultado_visitante', 'equipo_visitante', 
                    'descripcion', 'anotado', 'id_partido',
                    'id_jornada', 'temporada', 'competicion', 'playoff'
                ])
    df = df.astype({'x':'float', 'y':'float','resultado_local':'int', 'resultado_visitante':'int','anotado':'bool','playoff':'bool'})
    df.to_csv(archivo, index=False)
    print(f"Datos guardados en {archivo}")
