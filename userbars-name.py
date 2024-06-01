import warnings
import requests
import bs4
import html
import dateutil.parser as parser
import ssl
import urllib.request
import os
import json

warnings.filterwarnings("ignore")

ssl._create_default_https_context = ssl._create_unverified_context

base_url = "http://www.userbars.name/"

userbars_dict = dict(userbars = [])
download_url = ""

def main():
    if not os.path.exists("userbars-name/data"):
        os.makedirs("userbars-name/data")
    save_userbars()


def save_userbars():

    userbars_urls = []

    for i in range(1,21):
        category_url = base_url + f"cat{str(i)}.html"
        res = requests.get(category_url, allow_redirects=False, verify=False)
        soup = bs4.BeautifulSoup(res.text, "lxml", from_encoding="utf-8")
        category = soup.select("span.title")[0].getText()
        print(f"Downloading category {category} ({str(i)}/20) ...")
        last_page_element = soup.select("a.paging")[-1]
        num_pages = int(last_page_element.attrs["href"].split("?page=")[-1])
        
        for n in range(1, num_pages + 1):
            print(f"Downloading page {n}/{num_pages} of category {category} ({str(i)}/20) ...")
            page_urls = get_page_urls(category_url + f"?page={n}")
            userbars_urls.extend(page_urls)
    download_userbars(userbars_urls)


def get_page_urls(url):
    res = requests.get(url, allow_redirects=False, verify=False)
    soup = bs4.BeautifulSoup(res.text, "lxml", from_encoding="utf-8")
    anchor_elements = soup.select("a")
    page_urls = []

    for anchor_element in anchor_elements:
        href = anchor_element.attrs["href"]
        if href.startswith("./ub"):
            userbar_url = base_url + href[2:]
            page_urls.append(userbar_url)

    return page_urls


def download_userbars(urls):
    counter = 1
    total = len(urls)
    for url in urls:
        print(f"Getting data (Userbar {counter}/{total}) ...")
        res = requests.get(url, allow_redirects=False, verify=False)
        soup = bs4.BeautifulSoup(res.text, "lxml", from_encoding="utf-8")

        id = url.split(".name/")[-1].split(".html")[0]

        title = soup.select("b.title")[0].getText()
        
        image_path = soup.select("img[src*='./data/']")[0].attrs["src"][2:]
        image_url = base_url + image_path
        image_share_url = base_url + f"sendpic_en.php?url=/{image_path}"

        res_share = requests.get(image_share_url, allow_redirects=False, verify=False)
        soup_share = bs4.BeautifulSoup(res_share.text)

        image_imgur_url = soup_share.select("img")[0].attrs["src"]
        
        category = html.unescape(soup.select("a.clickstream")[-1].getText())
        date = parser.parse(soup.select("td.row1[valign='top']")[3].getText()).isoformat()
        uploader = soup.select("td.row2[valign='top'] a")[-1].getText()

        data = {
            "id": id,
            "title": title,
            "url": image_url,
            "imgur_url": image_imgur_url,
            "category": category,
            "date": date,
            "uploader": uploader
        }

        userbars_dict["userbars"].append(data)

        write_data()
        
        counter = counter + 1


def write_data():
    with open("userbars-name/data/userbars-name.json", "w", encoding="utf-8") as outfile:
        json.dump(userbars_dict, outfile, indent=4, ensure_ascii=False)

    # downloading images from Imgur is not easy, so we save the URLs to a text file and use other tools, like gallery-dl, to save them
    with open("userbars-name/data/imgur-urls.txt", "w") as f:
        for userbar in userbars_dict["userbars"]:
            f.write(userbar["imgur_url"] + "\n")


if __name__ == "__main__":
    main()
