import requests
from secret import api_key, cheksum
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json


#changing base class to increase limit of articles
class MyElsSearch(ElsSearch):
    def _upper_limit_reached(self):
        if self._cursor_supported:
            return False
        else:
            return self.num_res >= 10000

#create elsclient
client = ElsClient(api_key)
#proceed search
doc_srch = MyElsSearch("('Artificial Intelligence' OR 'Machine Learning' or 'AI' or 'ML') AND date=2020-2025 ",'sciencedirect')
doc_srch.execute(client, get_all = True)
res = doc_srch.results
#writing result into json file
with open('out/raw_data.json', 'w') as f:
    json.dump(res, f)
