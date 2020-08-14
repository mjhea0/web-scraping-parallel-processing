import datetime
from itertools import repeat
from time import sleep, time
from multiprocessing import Pool, cpu_count
import concurrent.futures
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapers.scraper import get_driver, connect_to_base, \
    parse_html, write_to_file


def run_process(page_number, filename):
    browser = get_driver()
    if connect_to_base(browser, page_number):
        sleep(2)
        html = browser.page_source
        output_list = parse_html(html)
        write_to_file(output_list, filename)
        browser.quit()
    else:
        print('Error connecting to hackernews')
        browser.quit()


if __name__ == '__main__':
    start_time = time()
    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f"output_{output_timestamp}.csv"
    
    futures = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for page in range(1, 21):
                futures.append(
                    executor.submit(run_process, page_number=page, filename=output_filename)
                )
    for future in concurrent.futures.as_completed(futures):
        try:
            print(future.result())
        except requests.ConnectTimeout:
            print("ConnectTimeout.")
    
    end_time = time()
    elapsed_time = end_time - start_time
    print(f'Elapsed run time: {elapsed_time} seconds')