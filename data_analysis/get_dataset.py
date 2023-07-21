import os
import pathlib
import aiohttp
import asyncio
from datetime import date, timedelta

DATASET = pathlib.Path(__name__).parent / "dataset"

def parse_url(date_from, date_to):
    return f"http://10.0.0.3:8000/verificaciones/resumen?fecha_desde={date_from}&fecha_hasta={date_to}&_export=csv"

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield (start_date + timedelta(n), start_date + timedelta(n+1))

async def get_csv(session, url, date):
    date = date.strftime("%Y-%m-%d")
    print(f"GETTING DATA FOR DATE: {date}")
    filename = DATASET / f"{date}.csv"

    if os.path.exists(filename):
        print("File scrapped!")
        return 0

    try:
        async with session.get(url) as resp:
            stream = resp.content
            while not stream.at_eof():
                data = await stream.read()
                with open(filename, 'w') as file:
                    print(f"WRITING TO FILE {filename}")
                    file.write(data.decode('utf-8'))
            return 0
    except Exception as e:
        print(e)
        return 1

async def main():
    my_timeout = aiohttp.ClientTimeout(
        total=1000, # default value is 5 minutes, set to `None` for unlimited timeout
        sock_connect=1000, # How long to wait before an open socket allowed to connect
        sock_read=1000 # How long to wait with no data being read before timing out
    )

    client_args = dict(
        trust_env=True,
        timeout=my_timeout
    )


    async with aiohttp.ClientSession(**client_args) as session:
        tasks = []
        for year in range(2019, 2023):
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)
            for first, second in daterange(start_date, end_date):
                url = parse_url(first, second)
                tasks.append(asyncio.ensure_future(get_csv(session, url, first)))

        results = await asyncio.gather(*tasks)
        for r in results:
            print(r)

asyncio.run(main())
