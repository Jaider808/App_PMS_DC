import app
url = 'https://api-inventario-gv.herokuapp.com/stock'
data = requests.get(url).json()
