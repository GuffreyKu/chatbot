import requests
import urllib.parse



def url_compose(location):
    authorization = "CWA-2E34BEE5-9808-4840-B526-913CF162503C"
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"

    headers = {
        "Authorization": f"{authorization}",
        "locationName":location,
        "elementName":"MaxT",
        "sort":"time"
    }

    encoded_params = urllib.parse.urlencode(headers, encoding='utf-8')
    full_url = f"{url}?{encoded_params}"
    return full_url

if __name__ == '__main__':
    try:
        full_url = url_compose("臺北市")
        response = requests.get(full_url)
        
        if response.status_code == 200:
            data = response.json()
            tomorrow_weather = data["records"]["location"][0]["weatherElement"][0]["time"][-1]["parameter"]["parameterName"]
            print(tomorrow_weather)
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)