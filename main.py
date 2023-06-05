import logging
import logging.handlers
import os
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

# try:
#     SOME_SECRET = os.environ["SOME_SECRET"]
# except KeyError:
#     SOME_SECRET = "Token not available!"
#     #logger.info("Token not available!")
#     #raise

import pandas as pd
from bs4 import BeautifulSoup
import codecs 

def comp_stockName(r):
    id, name = r["id"], r["name"]
    return f"{id},{name}"

def write_LogFile(fileName, write_content):
    os.makedirs(os.path.dirname(fileName), exist_ok=True)
    f = codecs.open(fileName, mode="w", encoding="utf-8", errors="strict")
    f.write(write_content)
    f.close()

if __name__ == "__main__":
    #logger.info(f"Token value: {SOME_SECRET}")

    r = requests.get('https://weather.talkpython.fm/api/weather/?city=Berlin&country=DE')
    if r.status_code == 200:
        data = r.json()
        temperature = data["forecast"]["temp"]
        logger.info(f'Weather in Berlin: {temperature}')

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
    }

    #抓取股票中文名稱
    url = "https://www.wantgoo.com/investrue/all-alive"
    r3 = requests.get(url, headers = headers).content
    soup = BeautifulSoup(r3, "html.parser")
    rr3 = soup.prettify()
    print(rr3)
    write_LogFile(f"paras/股票名稱.csv", rr3)

    # dfn = pd.read_json(rr3)
    # dfn = dfn[(dfn["id"]>="1101") & (dfn["id"]<="9999") & (dfn["id"].str.len() == 4)]
    # dfn = dfn.drop(columns=['type','country','url', 'industries'])
    # dfn["id"] = dfn["id"].astype("string")
    # dfn["comp"] = dfn.apply(comp_stockName, axis = 1)
    # stockNameStr = ""
    # for c in dfn["comp"].tolist():
    #     stockNameStr += f"{c}\n"
    # write_LogFile(f"paras/股票名稱.csv", stockNameStr)

  