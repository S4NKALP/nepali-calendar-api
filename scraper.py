import argparse
import asyncio
import json
import os

import aiohttp
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

BASE_URL = "https://nepalicalendar.rat32.com/index_nep.php"
DATA_DIR = "./data"


# Helper: wait between requests
async def delay(ms):
    await asyncio.sleep(ms / 1000)


async def fetch_month(session, year, month, save_dir=True, attempt=1):
    month_log = f"[{year}/{month}]"
    file_path = f"{DATA_DIR}/{year}/{month}.json"

    print(Fore.CYAN + f"\nFetching data for {month_log} (Attempt {attempt})")

    if os.path.exists(file_path):
        print(Fore.LIGHTBLACK_EX + "Skipped: File already exists.")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    try:
        print(Fore.BLUE + "Sending request...")
        payload = {
            "selYear": year,
            "selMonth": month,
            "viewCalander": "View Calander",
        }

        async with session.post(BASE_URL, data=payload, timeout=15) as resp:
            if resp.status != 200:
                raise Exception(f"HTTP {resp.status}")
            html = await resp.text()

        print(Fore.GREEN + "Page fetched successfully. Parsing HTML...")
        soup = BeautifulSoup(html, "html.parser")

        # Metadata
        metadata = {
            "en": soup.select_one("#entarikYr").get_text(strip=True)
            if soup.select_one("#entarikYr")
            else "",
            "np": soup.select_one("#yren").get_text(strip=True)
            if soup.select_one("#yren")
            else "",
        }
        print(Fore.LIGHTBLACK_EX + f"Metadata: {metadata['np']} ({metadata['en']})")

        # Helper to extract lists
        def extract_list(selector, remove_tags=None):
            el = soup.select_one(selector)
            if not el:
                return []
            remove_tags = remove_tags or []
            for tag in remove_tags:
                t = el.select_one(tag)
                if t:
                    t.decompose()
            return [line.strip() for line in el.get_text().split("\n") if line.strip()]

        holi_fest = extract_list("#holi", ["b", "a"])
        marriage = extract_list("#bibah", ["b"])
        bratabandha = extract_list("#bratabandha", ["b"])

        print(Fore.MAGENTA + f"Holidays/Festivals: {len(holi_fest)}")
        print(Fore.MAGENTA + f"Marriage Dates: {len(marriage)}")
        print(Fore.MAGENTA + f"Bratabandha Dates: {len(bratabandha)}")

        # Extract days
        days = []
        cells = soup.select(".cells")
        for i, cell in enumerate(cells):
            cell_soup = BeautifulSoup(cell.decode_contents(), "html.parser")

            n = (
                cell_soup.select_one("#nday").get_text(strip=True)
                if cell_soup.select_one("#nday")
                else ""
            )
            e = (
                cell_soup.select_one("#eday").get_text(strip=True)
                if cell_soup.select_one("#eday")
                else ""
            )
            t = (
                cell_soup.select_one("#dashi").get_text(strip=True)
                if cell_soup.select_one("#dashi")
                else ""
            )
            f = (
                cell_soup.select_one("#fest").get_text(strip=True)
                if cell_soup.select_one("#fest")
                else ""
            )
            color = ""
            font_tag = cell_soup.select_one("#nday font")
            if font_tag and font_tag.has_attr("color"):
                color = font_tag["color"].lower()
            h = color == "red"

            days.append({"d": (i % 7) + 1, "n": n, "e": e, "t": t, "f": f, "h": h})

        print(Fore.GREEN + f"Parsed {len(days)} days successfully.")

        data = {
            "metadata": metadata,
            "days": days,
            "holiFest": holi_fest,
            "marriage": marriage,
            "bratabandha": bratabandha,
        }

        if save_dir:
            os.makedirs(f"{DATA_DIR}/{year}", exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    data,
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
            print(Fore.LIGHTBLACK_EX + f"Saved individual month: {file_path}")

        return data

    except Exception as err:
        print(Fore.RED + f"Error fetching {month_log}: {err}")
        if attempt < 3:
            wait_time = 3000 * attempt
            print(Fore.YELLOW + f"Retrying in {wait_time / 1000}s...")
            await delay(wait_time)
            return await fetch_month(session, year, month, save_dir, attempt + 1)
        else:
            print(Fore.RED + f"Failed after 3 attempts for {month_log}")
            return None


async def scrape_year(session, year, save_single=True, save_dir=True):
    print(Style.BRIGHT + f"\nStarting scrape for year: {Fore.CYAN}{year}")
    print(
        f"   Mode: {'Single JSON' if save_single else ''} {'Directory' if save_dir else ''}\n"
    )
    year_data = {}
    success_count = 0

    for month in range(1, 13):
        data = await fetch_month(session, year, month, save_dir=save_dir)
        if data:
            year_data[str(month)] = data
            success_count += 1
        else:
            print(Fore.RED + f"Failed to gather data for month {month}")

        await delay(2000)  # delay between months

    if success_count == 12 and save_single:
        os.makedirs(DATA_DIR, exist_ok=True)
        year_file_path = f"{DATA_DIR}/{year}.json"
        with open(year_file_path, "w", encoding="utf-8") as f:
            json.dump(year_data, f, indent=2, ensure_ascii=False)
        print(Style.BRIGHT + Fore.GREEN + f"\nSaved aggregated file: {year_file_path}")

    fail_count = 12 - success_count
    print(Fore.LIGHTBLACK_EX + f"Success: {success_count}  Failed: {fail_count}\n")


async def scrape_years(start_year, end_year, save_single=True, save_dir=True):
    async with aiohttp.ClientSession() as session:
        for year in range(start_year, end_year + 1):
            await scrape_year(session, year, save_single, save_dir)
            if year < end_year:
                print(Fore.YELLOW + "Waiting 5 seconds before next year...")
                await delay(5000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nepali Calendar Scraper")
    parser.add_argument(
        "years", nargs="+", type=int, help="Year or year range (start end)"
    )
    parser.add_argument(
        "--single",
        nargs="?",
        const="json",
        help="Generate single JSON (e.g. --single json)",
    )
    parser.add_argument(
        "--dir",
        nargs="?",
        const="format",
        help="Generate directory format (e.g. --dir format)",
    )

    args = parser.parse_args()

    # Determine output mode
    save_single = False
    save_dir = False

    if not args.single and not args.dir:
        # Default behavior: both
        save_single = True
        save_dir = True
    else:
        if args.single:
            save_single = True
        if args.dir:
            save_dir = True

    if len(args.years) == 1:
        start_year = end_year = args.years[0]
    else:
        start_year, end_year = args.years[0], args.years[1]

    asyncio.run(scrape_years(start_year, end_year, save_single, save_dir))
