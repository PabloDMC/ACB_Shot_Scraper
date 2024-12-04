import sys
import os
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
src_dir = os.path.join(project_root, 'src')
sys.path.append(src_dir)

from scraper import ScraperACB
# import sqlite3

def main():
    # Crear una instancia de la clase ScraperACB
    scraper = ScraperACB()
    
    # Parámetros de prueba: asegúrate de usar valores válidos de ID para tu prueba
    id_temporada = 2023  # Ajusta el ID de la temporada según tus necesidades
    id_competicion = 2   # 1 para Liga Endesa, 2 para Copa del Rey, 3 para Supercopa Endesa
    id_jornada = 1       # Número de la jornada que deseas probar
    id_partido = 104125  # ID de un partido específico para probar


    # Probar el método `obtener_tiros_partido`
    print("Probando obtener_tiros_partido...")
    datos_tiros_partido = scraper.obtener_tiros_partido(id_partido, id_jornada, id_temporada, id_competicion)
    if datos_tiros_partido:
        print(f"Se obtuvieron {len(datos_tiros_partido)} datos de tiros para el partido {id_partido}.")
    else:
        print(f"No se obtuvieron datos de tiros para el partido {id_partido}.")
    # Cerrar el driver después de la prueba
    scraper.cerrar_driver()


    # Probar el método `obtener_tiros_jornada`
    print("\nProbando obtener_tiros_jornada...")
    datos_tiros_jornada = scraper.obtener_tiros_jornada(id_jornada, id_temporada, id_competicion)
    if datos_tiros_jornada:
        print(f"Se obtuvieron {len(datos_tiros_jornada)} datos de tiros para la jornada {id_jornada}.")
    else:
        print(f"No se obtuvieron datos de tiros para la jornada {id_jornada}.")
    # Cerrar el driver después de la prueba
    scraper.cerrar_driver()


    # Probar el método `obtener_tiros_competicion`
    print("\nProbando obtener_tiros_competicion...")
    datos_tiros_competicion = scraper.obtener_tiros_competicion(id_competicion,id_temporada)
    if datos_tiros_competicion:
        print(f"Se obtuvieron {len(datos_tiros_competicion)} datos de tiros para la competición {id_competicion}.")
    else:
        print(f"No se obtuvieron datos de tiros para la competición {id_competicion}.")
        
        
if __name__ == "__main__":
    main()
