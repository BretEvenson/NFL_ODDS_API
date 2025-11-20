import requests
from abc import ABC, abstractmethod

class APIBase(ABC):
    def __init__(self, base_url, params, timeout):
        self.__base_url = base_url
        self.__params = params
        self.__timeout = timeout

        self.__message = None
        self.__status = -1

    def get_api(self):
        try:
            resp = requests.get(self.__base_url, 
                            params = self.__params, 
                            timeout= self.__timeout)
        
            resp.raise_for_status()
            data = resp.json()
            if not data:
                raise LookupError("No Data")
        except requests.exceptions.RequestException as e:
            self.__message = f"A Network/HTTP error occured {e}"
        except ValueError as e:
            self.__message = e
        except LookupError as e:
            self.__message = "The server response was not valid JSON"
        except Exception as e:
            self.__message = f"An unexpected error occured {e}"
        else:
            self.__status = 0
            return data
        
    @property
    def status(self):
        return self.__status
    
    @property
    def message(self):
        return self.__message
    
    @abstractmethod
    def call_api(self):
        pass

    @abstractmethod
    def __str__(self):
        pass