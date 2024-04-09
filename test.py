import requests

BASE_URL = "http://127.0.0.1:5000/"

data = [{"name":"Visahl","views":2345,"likes":234554},
        {"name":"Anu","views":6543,"likes":9876},
        {"name":"Guru","views":54340,"likes":7643}]

# for i in range(len(data)):
#     response = requests.put(BASE_URL+"/video/"+str(i), data[i])
#     print(response.json())
# input()
# # responce = requests.delete(BASE_URL+"/video/0")
# # print(responce)
# # input()
# response = requests.get(BASE_URL+"/video/6")
# print(response.json())

# response = requests.get(BASE_URL+"/video/1234")
# print(response.json())

responce = requests.patch(BASE_URL+"/video/0",{"views":2345654321})
print(responce.json())