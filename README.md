# pixabay_scraper
A pixabay api python scraper

 1. create an account on [pixabay](https://pixabay.com)
 2. go to the [pixabay api docs](https://pixabay.com/api/docs/) and kopy your API key from the Parameters
 3. run this script

 You can parse the API key as an argument to the script or create a secrets.py file in the same folder.

```python
# secrets.py
 api_key = "<your_key>"
 ```

## Arguments
Argument | Default | Description
-|-|-
--api_key | Must Parse | Your Pixabay API key.
--img_classes | Must Parse | What you are searching for.
--path | ./ |  Your local path where the images get downloaded to.
--pages | 1 | How many pages you want to scrape.
--per_page | 50 | How many images a page has (3-200)

## Example

 `python pixabay_scraper.py --img_class bird horse --path C:\Users\<name>\Downloads\pix_img --api_key <your_key>`
