import requests
from bs4 import BeautifulSoup
import re



resp=requests.get("https://geochecki-vpd.nalog.gov.ru/geochecks")
print("cookies:", resp.cookies)
print("time to download:", resp.elapsed)
print("page encoding", resp.encoding)
print("Server response: ", resp.status_code)
print("Is everything ok? ", resp.ok)
print("Page's URL: ", resp.url)

soup = BeautifulSoup(resp.text, "html.parser")