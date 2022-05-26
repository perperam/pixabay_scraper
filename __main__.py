from pathlib import Path
import logging
import argparse
from pixabay_utils import scraper
try:
    from secrets import api_key
except:
    api_key = None

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(message)s'
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", nargs="?", default=None)
    parser.add_argument("--img-classes", nargs="+")
    parser.add_argument("--path", nargs="?", default=None)
    parser.add_argument("--images", nargs="?", default=1, type=int)

    args = parser.parse_args()

    if not api_key:
        if args.api_key:
            api_key = args.api_key
        else:
            logger.warning("Could not find a Pixabay API KEY. Please prase one with --api_key <your-key> or with a secrets.py file")
            raise Exception("MISSING API KEY")

    if args.path:
        path = Path(args.path)
    else:
        path = Path(".")

    scraper(api_key, args.img_classes, path, args.images)
