import re
from bs4 import BeautifulSoup
import requests
import sys, os, time

def get_chaps():
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    };

    url = "https://w3.mangaonepunch.com/"
    req = requests.get(url, headers);
    soup = BeautifulSoup(req.content, "html.parser");

    # containers of all chapter's link
    container = soup.find("li", {"id": "ceo_latest_comics_widget-3"});

    # List of all a tag within container
    ls_a_tags = container.find_all("a");

    for a in ls_a_tags:
        yield a.contents[0], a["href"];


def get_chap_imgs(url):
    # sample
    url = "https://w3.mangaonepunch.com/manga/one-punch-man-chapter-177/"
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    };
    
    req = requests.get(url, headers);
    soup = BeautifulSoup(req.content, "html.parser");
    entry_inner = soup.find(
            "div",
            {"class":"entry-inner"});

    ls_pictures = entry_inner.find_all("picture");

    for pic in ls_pictures:
        img = pic.find("img");
        yield img["src"];


def save_img(url, fn):
    with open(fn, "wb") as f:
        f.write(requests.get(url).content);

def parse_name(fn:str)->str:
    out = re.sub(r'\s', '_', fn);
    return out.lower();

def get_fn_name(url):
    return url.split("/")[-1];


def crawl():
    chaps = get_chaps();

    for (chap_name, url) in chaps:
        print(f"[+] Downloading chap {chap_name}");

        fn_chap = parse_name(chap_name);
        os.mkdir(f"data/{fn_chap}");

        imgs = get_chap_imgs(url);

        for img_url in imgs:
            fn_name = get_fn_name(img_url);
            fn_pth = f"data/{fn_chap}/{fn_name}"

            print(f"[+] Saving {fn_pth}");
            with open(fn_pth, "wb") as f:
                f.write(requests.get(img_url).content);
            time.sleep(2);
