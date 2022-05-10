import requests
import argparse
from pathlib import Path
try:
    from secrets import api_key
    api_key = api_key
except:
    api_key = None


def scraper(api_key, img_classes, path, pages=1, per_page=50):
    path = Path(path)
    print("WORKING")
    print(api_key, img_classes, path, pages, per_page)
    url = "https://pixabay.com/api/?key={api_key}&q={img_class}&image_type=photo&editors_choice=true&page={page}&per_page={per_page}"

    for img_class in img_classes:
        print("[DOWNLOADING CLASS]: {}".format(img_class))
        class_path = path / img_class
        class_path.mkdir(parents=True, exist_ok=True)


        for page in range(1, pages+1):
            furl = url.format(api_key=api_key, img_class=img_class, page=page, per_page=per_page)

            print("[DOWNLOADING PAGE]: {}".format(page))
            r = requests.get(furl)
            json_data = r.json()
            for image in json_data["hits"]:
                name = image["id"]
                img_url = image["largeImageURL"]
                r = requests.get(img_url, stream=True)
                img_path = class_path / (str(name) + ".jpg")
                with open(img_path, "wb") as f:
                    f.write(r.content)

    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key", nargs="?", default=None)
    parser.add_argument("--img_classes", nargs="+")
    parser.add_argument("--path", nargs="?", default=None)
    parser.add_argument("--pages", nargs="?", default=1, type=int)
    parser.add_argument("--per_page", nargs="?", default=50, type=int)

    args = parser.parse_args()

    if not api_key:
        if args.api_key:
            api_key = args.api_key
        else:
            raise Exception("PLEASE PARSE A PIXABAY API KEY WITH --api_key <your_key> OR WITH A secrets.py FILE")

    if args.path:
        path = Path(args.path)
    else:
        path = Path(".")

    scraper(api_key, args.img_classes, path, args.pages, args.per_page)
