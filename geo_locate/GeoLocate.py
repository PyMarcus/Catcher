import json
import platform
import httpx
from os import getenv
import requests
from dotenv import load_dotenv


load_dotenv(".env")


class GeoLocate:
    """
    Geo localizacao é um recurso tecnologico
    que permite a localizacao de uma pessoa
    ou recurso com base em suas coordenadas
    geográficas
    """
    def __init__(self, whatsmyip: str) -> None:
        self.__whatsmyip = whatsmyip  # atributo privado

    def __whats_my_ip_address(self) -> str:
        """
        Método [PRIVADO] que retorna o endereço ip
        público da pessoa
        :return: string
        """
        response = httpx.get(self.__whatsmyip)
        if response.status_code == 200:
            return response.text

    @staticmethod
    def __device_info() -> dict:
        """
        Método [PRIVADO] que retorna informações
        do dispositivo
        :return: dict
        """
        response = json.loads(httpx.get(getenv("DEVICE_INFO")).text)
        return response

    @staticmethod
    def __get_geo_location() -> dict:
        """
        Método [PRIVADO] que retorna a localizacao
        com base no endereço ip passado
        :return: dict
        """
        result = dict()
        ip_address: str = httpx.get(getenv("WMIP")).text
        find_loc = getenv("LOC") + ip_address
        response = requests.get(find_loc).text.split(',')
        city = response[2]  # para fins de legibilidade, criei variáveis
        postal_code = response[3]
        lat = response[4]
        long = response[5]
        state = response[7].replace("}", '').replace(")", '')
        result[state.split(':')[0].replace('\"', '')] = state.split(':')[1].replace('\"', '')
        result[city.split(':')[0].replace('\"', '')] = city.split(':')[1].replace('\"', '')
        result[postal_code.split(':')[0].replace('\"', '')] = postal_code.split(':')[1].replace('\"', '')
        result[lat.split(':')[0].replace('\"', '')] = lat.split(':')[1].replace('\"', '')
        result[long.split(':')[0].replace('\"', '')] = long.split(':')[1].replace('\"', '')
        return result

    def __hardware_info(self) -> dict:
        """
        Método [PRIVATE] que obtem informações do hardware, no
        momento, como temperatura, ram utilizada,
        processamento, escrita no disco
        :return: dict
        """
        ...

    def run(self) -> dict:
        """
        Inicializa busca de informações básicas
        do dispositivo e da geolocalizacao
        retornando generator com dados de um dicionario
        desse modo, há economia de memória e aumento
        do desempenho
        :return: dict
        """
        total_result = self.__device_info()
        total_result.update(self.__get_geo_location())
        total_result["operational_system"] = platform.system()
        for key, value in total_result.items():
            yield {key: value}


if __name__ == '__main__':
    locate = GeoLocate(getenv("WMIP"))
    for x in locate.run():  # debug
        print(x)
