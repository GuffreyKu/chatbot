import requests
import urllib.parse
from langchain_core.tools import tool


@tool(parse_docstring=True)
def get_tomorrow_weather(location: str) -> dict:
    """使用中央氣象局 API 查詢明天氣溫並返回相關信息。

    Args:
        location (str): 臺灣縣市，例如:
                        - "臺北市"
                        - "臺南市"
                        - "桃園市"

    Returns:
        str: 氣溫數值
    """
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
    try:
        response = requests.get(full_url)
        
        if response.status_code == 200:
            data = response.json()
            
            tomorrow_weather = data["records"]["location"][0]["weatherElement"][0]["time"][-1]["parameter"]["parameterName"]
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

    return tomorrow_weather

tools = [
    get_tomorrow_weather
]