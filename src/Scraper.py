from utils import procesar_tiros, reintentar
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup

class ScraperACB:
    def __init__(self):
        self.driver = None

    def iniciar_driver(self):
        if self.driver is None:  # Solo inicializa si no está ya iniciado
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Ejecuta sin interfaz gráfica
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            self.driver = webdriver.Chrome(options=options)
        
    def cerrar_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def obtener_id_partidos_jornada(self,id_jornada,id_temporada,id_competicion):
        """
        Obtiene los IDs de los partidos de una jornada específica.

        Args:
            id_jornada (int): ID de la jornada.
            id_temporada (int): ID de la temporada.
            id_competicion (int): ID de la competición.

        Returns:
            list: Una lista de IDs de los partidos de la jornada.
        """
        try:
            self.iniciar_driver()
            url_jornada = f'https://www.acb.com/resultados-clasificacion/ver/temporada_id/{id_temporada}/competicion_id/{id_competicion}/jornada_numero/{id_jornada}'
            self.driver.get(url_jornada)
            
            partidos=self.driver.find_elements(By.XPATH,'//a[@title="Estadísticas"]')
            if not partidos:
                    print(f"No se encontraron partidos para la jornada {id_jornada} de la temporada {id_temporada}.")
                    return []
            
            id_partidos=[]
            for i in partidos:
                id_partidos.append(i.get_attribute('href').split('/id/')[1])
            return id_partidos
        except Exception as e:
            print(f"Error al obtener los IDs de los partidos para la jornada {id_jornada}: {e}")
            return []
    
    def obtener_id_partidos_jugador(self,id_jugador,temporada):
        """
        Obtiene los IDs de los partidos de un jugador específico para una temporada.

        Args:
            id_jugador (int): ID del jugador.
            id_temporada (int): ID de la temporada.

        Returns:
            list: Una lista de IDs de los partidos del jugador en esa temporada.
        """
        self.iniciar_driver()
        url_jugador = f'https://www.acb.com/jugador/todos-sus-partidos/id/{id_jugador}/temporada_id/{temporada}/casa_fuera_id/0/victorias_derrotas_id/0/mes_id/0#cuerpo'
        self.driver.get(url_jugador)
        id_partidos = []
        partidos = self.driver.find_elements(By.XPATH,'//td[@class="partido"]/a')
        for i in partidos:
            j = i.get_attribute('href').split('/id/')[1]
            if j not in id_partidos:
                id_partidos.append(j)
        self.cerrar_driver()
        return id_partidos
    
    def obtener_tiros_jugador(self,nombre_jugador,id_partido):
        """
            Obtiene los datos de los tiros de un jugador en un partido.

            Args:
                nombre_jugador (str): Nombre del jugador ('N. Apellido').
                id_partido (int): ID del partido.

            Returns:
                list: Datos de los tiros del jugador en el partido.
        """
        try:
            self.iniciar_driver()
            url = f'https://jv.acb.com/es/{id_partido}/cartadetiro'
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'sm-table--local')))
                WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'foreignObject')))
            except TimeoutException:
                print(f"No se cargaron los elementos dinámicos en el tiempo esperado para el partido {id_partido}.")
                return []
            
            self.driver.find_element(By.XPATH,'.//div[@class="sm-table sm-table--local"]/div[2]').click()
            self.driver.find_element(By.XPATH,'.//div[@class="sm-table sm-table--visitor"]/div[2]').click()
            jugador = self.driver.find_element(By.XPATH,f'//tr[@id="{nombre_jugador}"]')
            jugador.click()
            time.sleep(1)
            html = self.driver.page_source
            soup = BeautifulSoup(html,features="html.parser")

            equipo_local = soup.find('div', class_='sm-table sm-table--local').find('span').get_text(strip=True)
            equipo_visitante = soup.find('div', class_='sm-table sm-table--visitor').find('span').get_text(strip=True)
            tiros = soup.find_all('foreignobject')
            datos = procesar_tiros(tiros, equipo_local, equipo_visitante, id_partido)
            return datos
        except NoSuchElementException:
            print("No se pudieron extraer los tiros.")
            return []

    def obtener_tiros_partido(self,id_partido,id_jornada=None,id_temporada=None,id_competicion=None):
        """
        Obtiene los datos de los tiros de un partido específico.

        Args:
            id_partido (int): ID del partido.
            id_jornada (int, optional): ID de la jornada. Por defecto es None.
            id_temporada (int, optional): ID de la temporada. Por defecto es None.
            id_competicion (int, optional): ID de la competición. Por defecto es None.

        Returns:
            list: Una lista de datos procesados de los tiros del partido.
        """
        try:
            self.iniciar_driver()
            url = f'https://jv.acb.com/es/{id_partido}/cartadetiro'
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'sm-table--local')))
                WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'foreignObject')))
            except TimeoutException:
                print(f"No se cargaron los elementos dinámicos en el tiempo esperado para el partido {id_partido}.")
                return []
            
            html = self.driver.page_source
            soup = BeautifulSoup(html,features='html.parser')
            
            equipo_local = soup.find('div', class_='sm-table sm-table--local').find('span').get_text(strip=True)
            equipo_visitante = soup.find('div', class_='sm-table sm-table--visitor').find('span').get_text(strip=True)
            temporada = f"{id_temporada}-{int(id_temporada)+1}" if id_temporada else None
            competicion = "Liga Endesa" if id_competicion == 1 else "Copa del Rey" if id_competicion == 2 else "Supercopa Endesa" if id_competicion == 3 else None
            playoff = None if id_jornada is None or id_competicion is None else int(id_competicion == 1 and id_jornada > 34)
            tiros = soup.find_all('foreignobject')
            datos = procesar_tiros(tiros,equipo_local,equipo_visitante,id_partido,id_jornada,temporada,competicion,playoff)
            return datos
        except NoSuchElementException:
            print("No se pudieron extraer los tiros.")
            return []
    
    def obtener_tiros_jornada(self, id_jornada, id_temporada, id_competicion):
        """
            Obtiene los datos de todos los partidos de una jornada específica.
            Usa reintentos para manejar errores en partidos individuales.

            Args:
                id_jornada (int): Número de la jornada.
                id_temporada (int): Año de la temporada.
                id_competicion (int): Tipo de competición.

            Returns:
                list: Datos de los tiros de todos los partidos de la jornada.
        """
        id_partidos = self.obtener_id_partidos_jornada(id_jornada, id_temporada, id_competicion)

        if not id_partidos:
            print(f"No se encontraron partidos para la jornada {id_jornada}.")
            return []

        datos_jornada = []
        for id_partido in id_partidos:
            print(f"Procesando partido {id_partido} de la jornada {id_jornada}...")
            datos_partido = reintentar(self.obtener_tiros_partido, 3, id_partido, id_jornada, id_temporada, id_competicion)
            if datos_partido:
                datos_jornada.extend(datos_partido)
            else:
                print(f"No se pudieron obtener datos para el partido {id_partido} después de 3 intentos.")

        return datos_jornada

    def obtener_tiros_competicion(self, id_competicion, id_temporada):
        """
        Obtiene los datos de todos los partidos de una competición específica por una temporada.

        Args:
            id_temporada (int): ID de la temporada.
            id_competicion (int): ID de la competición.

        Returns:
            list: Una lista de datos de tiros de todos los partidos de la competición durante la temporada.
        """
        try:
            datos_competicion = []
            id_jornada = 1

            while True:
                print(f"Obteniendo datos de la jornada {id_jornada}...")
                datos_jornada = self.obtener_tiros_jornada(id_jornada, id_temporada, id_competicion)

                if not datos_jornada:
                    print(f"No se encontraron datos para la jornada {id_jornada}. Finalizando la obtención de datos.")
                    break

                datos_competicion.extend(datos_jornada)
                id_jornada += 1

            self.cerrar_driver()
            return datos_competicion
        except Exception as e:
            print(f"Error al obtener los datos de la competición: {e}")
            return []
        finally:
            self.cerrar_driver()
        
"""
# Obtener los tiros de los partidos de una jornada
    def obtener_tiros_jornada(self, id_jornada, id_temporada, id_competicion):
        # Obtener los IDs de los partidos de la jornada
        id_partidos = self.obtener_id_partidos_jornada(id_jornada, id_temporada, id_competicion)
        
        if not id_partidos: # Si id_partidos está vacío
            return []
    
        # Número máximo de reintentos para cada partido
        max_reintentos = 3
        datos_jornada = []

        for id_partido in id_partidos:
            reintento = 0
            while reintento < max_reintentos:
                try:
                    if reintento > 0:
                        print(f"Reintentando la carga de la página para el partido {id_partido} ({reintento}/{max_reintentos})...")
                        self.driver.refresh()
                        time.sleep(1)  # Esperar un poco para que la página recargue

                    # Llamar al método para obtener los tiros del partido
                    datos_partido = self.obtener_tiros_partido(id_partido, id_jornada, id_temporada, id_competicion)
                    
                    # Si los datos se obtuvieron con éxito, se sale del bucle
                    if datos_partido:
                        break

                except (NoSuchElementException, TimeoutException) as e:
                    print(f"Error al intentar scrapear el partido {id_partido}: {e}")
                    reintento += 1
                    if reintento < max_reintentos:
                        print("Esperando antes del siguiente intento...")
                        time.sleep(1)
                    else:
                        print(f"Fallo al scrapear el partido {id_partido} después de {max_reintentos} reintentos.")
                        datos_partido = []  # Si después de 3 reintentos no se obtiene información, se establece como lista vacía

            # Agregar los datos del partido a la lista de datos de la jornada
            datos_jornada.extend(datos_partido)

        return datos_jornada"""