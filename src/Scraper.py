import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class ScraperACB:
    def __init__(self):
        self.driver = None

    def iniciar_driver(self):
        if self.driver is None:  # Solo inicializa si no está ya iniciado
            self.driver = webdriver.Chrome()
        
    def cerrar_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    # Obtener los ids de los partidos de un jugador en una temporada
    def obtener_id_partidos_jugador(self,id_jugador,temporada):
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

    # Obtener los ids de los partidos de una jornada
    def obtener_id_partidos_jornada(self,jornada,temporada):
        self.iniciar_driver()
        url_jornada = f'https://www.acb.com/resultados-clasificacion/ver/temporada_id/{temporada}/competicion_id/1/jornada_numero/{jornada}'
        self.driver.get(url_jornada)
        
        id_partidos=[]
        partidos=self.driver.find_elements(By.XPATH,'//a[@title="Estadísticas"]')
        for i in partidos:
            id_partidos.append(i.get_attribute('href').split('/id/')[1])
        return id_partidos
    
    # Obtiene los tiros de un jugador en un partido
    def obtener_tiros_jugador(self,nombre_jugador,id_partido):
        try:
            self.iniciar_driver()
            url = f'https://jv.acb.com/es/{id_partido}/cartadetiro'
            self.driver.get(url)
            WebDriverWait(self.driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'use')))
            
            loc_x, loc_y, nombres, result = [], [], [], []

            self.driver.find_element(By.XPATH,'.//div[@class="sm-table sm-table--local"]/div[2]').click()
            self.driver.find_element(By.XPATH,'.//div[@class="sm-table sm-table--visitor"]/div[2]').click()
            jugador = self.driver.find_element(By.XPATH,f'//tr[@id="{nombre_jugador}"]')
            jugador.click()
            time.sleep(1)
            tiros = self.driver.find_elements(By.CSS_SELECTOR, 'use')
            for tiro in tiros:
                x = tiro.get_attribute('x')
                y = tiro.get_attribute('y')
                href = tiro.get_attribute('xlink:href')
                if x and y:
                    nombres.append(nombre_jugador)
                    loc_x.append(x)
                    loc_y.append(y)
                    result.append(1 if href != "#local-out" and href != "#visitor-out" else 0)
            return list(zip(nombres, result, loc_x, loc_y))
        except NoSuchElementException:
            print("No se pudieron extraer los tiros.")
            return []

    # Obtiene los tiros de un partido
    def obtener_tiros_partido(self,id_partido):
        try:
            self.iniciar_driver()
            url = f'https://jv.acb.com/es/{id_partido}/cartadetiro'
            self.driver.get(url)
            
            jugadores = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH,'//tr[@id]'))
            )
            loc_x, loc_y, nombres, result = [], [], [], []
            
            self.driver.find_element(By.XPATH,'.//div[@class="sm-table sm-table--visitor"]/div[2]').click()
            for jugador in jugadores:
                nombre_jugador = jugador.get_attribute("id")
                jugador.click()
                time.sleep(1)
                tiros = self.driver.find_elements(By.CSS_SELECTOR, 'use')
                for tiro in tiros:
                    x = tiro.get_attribute('x')
                    y = tiro.get_attribute('y')
                    href = tiro.get_attribute('xlink:href')
                    if x and y:
                        nombres.append(nombre_jugador)
                        loc_x.append(x)
                        loc_y.append(y)
                        result.append(1 if href != "#local-out" and href != "#visitor-out" else 0)
                jugador.click()
            return list(zip(nombres, result, loc_x, loc_y))
        except NoSuchElementException:
            print("No se pudieron encontrar los extraer los tiros.")
            return []

    # Guardar los datos en CSV
    def guardar_datos_csv(data, archivo):
        df = pd.DataFrame(data, columns=['name', 'shot_made', 'x', 'y'])
        df['x'] = pd.to_numeric(df['x'], errors='coerce')
        df['y'] = pd.to_numeric(df['y'], errors='coerce')
        df.to_csv(archivo, index=False)
        print(f"Datos guardados en {archivo}")