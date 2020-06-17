import requests
import json


class AdaInfo:
    def __init__(self):
        self.__status = ''
        self.__passagens = ''
        pass

    def get_status(self):
        list_status = []
        try:
            for estacao in self.__get_url():
                list_status.append(requests.get(f'{estacao}/status').json())

            return list_status
        except:
            try:
                for estacao in self.__get_url()[1:]:
                    list_status.append(requests.get(
                        f'{estacao}/status').json())
            except:
                pass
        return list_status

    def get_passagens(self):
        list_passagens = []
        try:
            for estacao in self.__get_url():
                list_passagens.append(requests.get(f'{estacao}/passagens').text.replace('"', '').replace(
                    '\n', '').replace('{', '').replace('}', '').replace('Passagens ET-CSS-001:', '').split(','))
            return list_passagens
        except:
            try:
                for estacao in self.__get_url()[1:]:
                    list_passagens.append(requests.get(f'{estacao}/passagens').text.replace('"', '').replace(
                        '\n', '').replace('{', '').replace('}', '').split(','))
            except:
                pass
        return list_passagens

    def __get_url(self):
        lista_url = []
        with open(f'/var/local/ada-urls.txt') as ada_urls:
            for url in ada_urls:
                lista_url.append(url.strip('\n'))
        return lista_url
