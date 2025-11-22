import requests

class SMS:
    def text(self,phone,message,key):
        resp = requests.post('https://textbelt.com/text', {
        'phone': phone,
        'message': message+' -- Hasan Imanli.',
        'key': key,
        })
        print(resp.json())