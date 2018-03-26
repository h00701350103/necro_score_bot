from nsb_config import options
import nsb_steam
import nsb_database

class index:
    def __init__(self, saveToFile = True):
        self.path = options['data'] + 'leaderboards.xml'
        self.data = None
    
    def fetch(self):
        url = nsb_steam.leaderboardUrl()
        response = nsb_steam.fetchUrl(url)
        self.data = nsb_database.xml_to_list(response=response, responseType='index')

    def read_pickle(self):
        self.data = nsb_database.unpickle(self.path)
    
    def read_xml(self):
        self.data = nsb_database.xml_to_list(self.path, responseType='index')

    def write(self):
        nsb_database.pickle_file(data=self.data, path=self.path)

    def entries(self):
        if self.data == None:
            raise Exception('Read or fetch data first')
        return self.data

