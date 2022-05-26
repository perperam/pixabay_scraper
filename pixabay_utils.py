import logging
import itertools
from pathlib import Path
import requests
from time import sleep
from utils import Progressbar

# request timeout
TIMEOUT = 60

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(message)s'
    )

def get_json(url, params):
    try:
        r = requests.get(url, params, allow_redirects=False, timeout=TIMEOUT)
        logging.debug("json url - " +  r.url)
    except requests.exceptions.Timeout as err:
        logger.warning(err)

    try:
        return r
    except Exception as err:
        logger.warning(err)


def download_images(url):
    try:
        r = requests.get(url, allow_redirects=False, timeout=TIMEOUT)
        logging.debug("image url - " +  r.url)
    except requests.exceptions.Timeout as err:
        logger.warning(err)

    try:
        return r
    except Exception as err:
        logger.warning(err)

def get_available_images(API_URL, params, MIN_IMG_PER_PAGE):
    params["page"] = 1
    params["per_page"] = MIN_IMG_PER_PAGE
    j_response = get_json(API_URL, params).json()
    return j_response["total"]

    logger.info(f"There are only ")

def scraper(api_key, img_classes, path="img", images=1):
    logger.debug((api_key, img_classes, path, images))
    # go to https://pixabay.com/api/docs/ to look up these values
    MAX_IMG_PER_PAGE = 200
    MIN_IMG_PER_PAGE = 3
    API_URL = "https://pixabay.com/api/"

    params = {
        "key" : api_key,
        "q" : "None",
        "image_type" : "photo",
        "page" : 1,
        "per_page" : MAX_IMG_PER_PAGE
        }

    path = Path(path)

    logger.info("Starting")

    for img_class in img_classes:
        try:
            params["q"] = img_class

            try:
                class_path = path / img_class
                class_path.mkdir(parents=True, exist_ok=True)
            except:
                logger.warnig("Something went wrong while creating path for {}".format(img_class))

            logger.info("Downloading class: {} to {}".format(img_class, class_path))

            # testing if pixabay can serve the amount of wanted images
            available_images = get_available_images(API_URL, params, MIN_IMG_PER_PAGE)
            if available_images < images:
                logger.info("There are only {} available images... starting download".format(available_images))
                images=available_images-1

            Pbar = Progressbar(images)

            # creating the params list for all pages
            images_downloaded = 0
            run = True

            for page in itertools.count(1):
                try:
                    if not run:
                        break

                    params["page"] = page
                    j_response = get_json(API_URL, params).json()

                    for image in j_response["hits"]:
                        try:
                            if images_downloaded >= images:
                                run = False
                                break

                            image_id = image["id"]
                            image_url = image["largeImageURL"]

                            image_bytes = download_images(image_url).content

                            image_path = class_path / (str(image_id) + ".jpg")
                            with open(image_path, "wb") as file:
                                logger.debug(image_path)
                                file.write(image_bytes)

                            images_downloaded += 1
                            Pbar.set(images_downloaded)

                        except Exception as err:
                            logger.warning(err)
                            logger.warning(f"an error occured proccesing this images {img_url}")

                except Exception as err:
                    logger.warning(err)
                    logger.warning(f"an error occured proccesing page {page}")
                    logger.warning(f"downloaded {images_downloaded} images from {img_class}")
                    break

        except Exception as err:
            logger.warning(err)
            logger.warning(f"an error occured proccesing the class {img_class}")
