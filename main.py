import requests
from secret import api_key, cheksum
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json

class MyElsSearch(ElsSearch):
    def _upper_limit_reached(self):
        """Determines if the upper limit for retrieving results from of the
            search index is reached. Returns True if so, else False. Upper 
            limit is 5,000 for indexes that don't support cursor-based 
            pagination."""
        if self._cursor_supported:
            return False
        else:
            return self.num_res >= 10000


client = ElsClient(api_key)
import json

doc_srch = MyElsSearch("('Artificial Intelligence' OR 'Machine Learning' or 'AI' or 'ML') AND date=2020-2025 ",'sciencedirect')
doc_srch.execute(client, get_all = True)
res = doc_srch.results
#print(len(res))
#print(doc_srch._tot_num_res)
with open('data.json', 'w') as f:
    json.dump(res, f)
#for doc in res[:4]:
#    print(doc)






print()
