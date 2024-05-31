import requests
import bs4
import os
import json

base_url = "https://www.userbars.be/"
download_base_url = "https://www.userbars.be/download/"
userbars_dict = dict(userbars = [])
download_url = ""

def main():
    n = get_userbars_number()
    save_userbars(n)


def get_userbars_number():
    print("Getting number of userbars...")
    res = requests.get(base_url)
    soup = bs4.BeautifulSoup(res.text, "lxml")
    tags = soup.select("[id^='ub_box_top_']")
    n = int(tags[0].attrs["id"][11:])
    return n

def save_userbars(n):
    for i in range(1, n + 1):
        print(f"Downloading userbar number {i}...")
        page_url = base_url + "userbar/" + str(i)
        try:
            res_page = requests.get(page_url)
        except:
            f = open("errors.txt", "a")
            f.write(str(i) + "\n")
            f.close()
            continue
        if res_page.history:    # if page does not exist and redirects to homepage
            not_found(i)
            continue
        get_data(i, res_page)
        try:
            res_download = requests.get(download_url)
        except:
            f = open("errors.txt", "a")
            f.write(str(i) + "\n")
            f.close()
            continue
        download(i, res_download)
    write_data()
    print("Done.")


def not_found(i):

    data = {
        'number': i,
        'download_url': 'not found',
        'title': 'not found',
        'uploader': 'not found',
        'date': 'not found',
        'category': 'not found'
    }

    userbars_dict["userbars"].append(data)

def get_data(i, res):

    soup = bs4.BeautifulSoup(res.text, "lxml")
    global download_url
    download_url = download_base_url + str(i)
    title = soup.select(".keywords")[0].getText()
    uploader = soup.select("[align='left'] a")[0].getText()
    date = soup.select("span.nice_date")[0].attrs["title"]
    category = soup.select("[align='right'] a")[0].getText()

    data = {
        'number': i,
        'download_url': download_url,
        'title': title,
        'uploader': uploader,
        'date': date,
        'category': category
    }

    userbars_dict["userbars"].append(data)

def download(i, res):
    if not os.path.exists("userbars-be/data"):
        os.makedirs("userbars-be/data")
    ext = res.headers['content-type'].split("/")[-1]  # gets file extension
    if ext == 'x-ms-bmp':   # clean .bmp extension
        ext = 'bmp'
    save_path = "userbars-be/" + str(i) + "." + ext
    open(save_path, 'wb').write(res.content)

def write_data():
    with open('userbars-be/userbars-be.json', 'w') as outfile:
        json.dump(userbars_dict, outfile, indent=4)

if __name__ == "__main__":
    main()
