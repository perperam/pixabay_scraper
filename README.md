# pixabay_scraper
 a pixabay api python scraper

 1. create a account on [pixabay](https://pixabay.com)
 2. go to the [pixabay api docs](https://pixabay.com/api/docs/) and kopy your API key from the Parameters
 3. run this script

## Arguments
Argument | Default | Description
-|-|-
--api_key | Must Parse | Your Pixabay API key.
--img_classes | Must Parse | What you are searching for.
--path | ./ |  Your local path where the images get downloaded to.
--pages | 1 | How many pages you want to scrape.
--per_page | 50 | How many images a pages has

## Example

 `python pixabay_scrapper.py --img_class bird horse  --path C:\Users\<name>\Downloads\pix_img --api_key <your_key>`
