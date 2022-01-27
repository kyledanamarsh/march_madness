import requests

def send_text(body, number):
    """
    I used textbelt.com for this, but I'm sure you could find another texting
    service if you'd like to.
    """
    requests.post('https://textbelt.com/text', {
    'phone': number,
    'message': body,
    'key': ''
    })
