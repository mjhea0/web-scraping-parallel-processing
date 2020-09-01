import asyncio
import datetime
from concurrent.futures import ProcessPoolExecutor
from time import sleep, time
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


async def run_blocking_tasks(executor):
    loop = asyncio.get_event_loop()
    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{output_timestamp}.csv'
    blocking_tasks = [
        loop.run_in_executor(executor, run_process, i, output_filename)
        for i in range(1, 21)
    ]
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]


if __name__ == '__main__':
    start_time = time()
    executor = ProcessPoolExecutor()
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            run_blocking_tasks(executor)
        )
    finally:
        event_loop.close()
    end_time = time()
    elapsed_time = end_time - start_time
    print(f'Elapsed run time: {elapsed_time} seconds')
