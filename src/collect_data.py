from datasources import RSSDataSource
import os, sys, time

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


def main():
    data_sources = list([RSSDataSource(s["url"], s["filename"]) for s in sources])

    while True:
        try:
            print("Start collecting data")
            for data_source in data_sources:
                print(f"Collect data for {data_source.url}")
                data_source.request()
                data_source.write_csv()
            print("Finish, sleep")
            time.sleep(5 * 60)
        except Exception as ex:
            print(ex, file=sys.stderr)


if __name__ == "__main__":
    main()
