import io
import requests
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
img_data = io.BytesIO()
plt.savefig(img_data, format='png')
img_data.seek(0)

response = requests.request(
    "POST",
    "https://api.imgur.com/3/image",
    headers={ 'Authorization': 'Client-ID <TOKEN HERE>' },
    data=img_data,
)

response_json = response.json()
return response_json['data']['link']