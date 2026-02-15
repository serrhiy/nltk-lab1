from datasources import RSSDataSource
import os, asyncio, sys

RESOURCES_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "resources")
)

sources = [
    {
        "url": "https://www.rbc.ua/static/rss/ukrnet.strong.ukr.rss.xml",
        "filename": os.path.join(RESOURCES_DIR, "rbc.csv"),
    },
    {
        "url": "https://www.pravda.com.ua/rss/",
        "filename": os.path.join(RESOURCES_DIR, "ut.csv"),
    },
]


def extract_data(data_source: RSSDataSource):
    data_source.request()
    data_source.write_csv()


async def main():
    data_sources = [RSSDataSource(s["url"], s["filename"]) for s in sources]

    while True:
        try:
            print("Start collecting data")
            tasks = [asyncio.to_thread(lambda: extract_data(s)) for s in data_sources]
            await asyncio.gather(*tasks)
            print("Data collected. Sleep")
            await asyncio.sleep(5 * 60)
        except Exception as ex:
            print(ex, file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())
