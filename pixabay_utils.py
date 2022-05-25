import logging
import itertools
from pathlib import Path
import requests
from utils import Progressbar

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s:%(message)s'
    )

def get_json(url, params):
    try:
        r = requests.get(url, params, allow_redirects=False, timeout=15)
        logging.debug("json url - " +  r.url)
    except requests.exceptions.Timeout as err:
        logger.warning(err)

    try:
        return r.json()
    except Exception as err:
        logger.warning(err)


def download_images(url):
    try:
        r = requests.get(url, allow_redirects=False, timeout=15)
        logging.debug("image url - " +  r.url)
    except requests.exceptions.Timeout as err:
        logger.warning(err)

    try:
        return r.content
    except Exception as err:
        logger.warning(err)


def pixabay_scraper(api_key, img_classes, path="img", images=1):
    logger.debug((api_key, img_classes, path, images))
    # go to https://pixabay.com/api/docs/ to look up these values
    MAX_IMG_PER_PAGE = 200
    MIN_IMG_PER_PAGE = 3
    API_URL = "https://pixabay.com/api/"

    params = {
        "key" : api_key,
        "q" : "None",
        "image_type" : "photo",
        "editors_choice" : "true",
        "page" : 1,
        "per_page" : MAX_IMG_PER_PAGE
        }

    path = Path(path)

    logger.info("Starting")

    for img_class in img_classes:
        params["q"] = img_class

        try:
            class_path = path / img_class
            class_path.mkdir(parents=True, exist_ok=True)
        except:
            logger.warnig("Something went wrong while creating path for {}".format(img_class))

        logger.info("Downloading class: {} to {}".format(img_class, class_path))

        Pbar = Progressbar(images)

        # creating the params list for all pages
        images_downloaded = 0
        run = True

        for page in itertools.count(1):
            params["page"] = page
            j_response = get_json(API_URL, params)

            for image in j_response["hits"]:
                if images_downloaded >= images:
                    run = False
                    break

                image_id = image["id"]
                image_url = image["largeImageURL"]

                image_bytes = download_images(image_url)

                image_path = class_path / (str(image_id) + ".jpg")
                with open(image_path, "wb") as file:
                    logger.debug(image_path)
                    file.write(image_bytes)

                images_downloaded += 1
                Pbar.set(images_downloaded)



            if not run:
                break

if __name__ == "__main__":
    from secrets import api_key
    pixabay_scraper(
    api_key,
    ["apple"],
    path="pix_test_img",
    images=201
    )
