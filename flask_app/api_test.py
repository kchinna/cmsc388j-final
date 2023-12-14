# import requests

# model = 'honda'
# api_url = 'https://api.api-ninjas.com/v1/cars?make={}'.format(model)
# CAR_API_KEY = 'U0RJI5E43DWeM7WUWTMYWw==3PsCdTC8WtPglv7o'
# sess = requests.Session()
# response = sess.get(api_url, headers={'X-Api-Key': CAR_API_KEY})
# if response.status_code == requests.codes.ok:
#     print(response.text)
# else:
#     print("Error:", response.status_code, response.text)


import requests, json
url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/honda?format=json'
r = requests.get(url)
data = r.json()["Results"]
print(r.json()["fdsf"])
print(json.dumps(data[0], indent=2))