from themoviedb import TMDb
from dotenv import load_dotenv
import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel
import aria2p
import os
import sys

load_dotenv()
ARIA2_HOST = os.getenv("ARIA2_HOST", "http://localhost")
ARIA2_PORT = int(os.getenv("ARIA2_PORT", 6800))
ARIA2_SECRET = os.getenv("ARIA2_SECRET", "")

aria2 = aria2p.API(
    client=aria2p.Client(host=ARIA2_HOST, port=ARIA2_PORT, secret=ARIA2_SECRET)
)


class Media(BaseModel):
    name: str
    source: str
    size: float
    resolution: str
    download_link: str


def get_media_fullname(keyword: str) -> str:
    tmdb = TMDb()
    movies = tmdb.search().movies(keyword)
    sorted_movies = sorted(movies, key=lambda x: x.popularity, reverse=True)
    movie_id = sorted_movies[0].id
    movie = tmdb.movie(movie_id).details()
    fullname = f"{movie.title} ({movie.year})"
    return fullname


def convert_size(size_string: str) -> float:
    size = float(size_string[:-2])
    match size_string[-2:]:
        case "GB":
            pass
        case "MB":
            size /= 1024
        case _:
            raise ValueError("Unrecognized specifier")

    return size


def get_available_medium(fullname: str) -> list[Media]:
    medium: list[Media] = []

    r = httpx.get(f"https://en.kickass-official.blue/movies?keyword={fullname}")
    text = r.text
    soup = BeautifulSoup(text, "html.parser")
    element = soup.find("a", class_="browse-movie-link")
    link = element["href"]

    r = httpx.get(link)
    text = r.text
    soup = BeautifulSoup(text, "html.parser")
    element = soup.find("tbody")

    rows = element.find_all("tr")
    for row in rows:
        elements = row.find_all("td")
        download_link = elements[3].find("a")["href"]
        source = elements[1].string
        size = convert_size(elements[2].string)
        resolution = elements[0].string
        media = Media(
            name=fullname,
            size=size,
            resolution=resolution,
            download_link=download_link,
            source=source,
        )
        medium.append(media)

    return medium


def calculate_media_priority(media: Media) -> tuple[int, int, float]:
    match media.resolution:
        case "2160p":
            score1 = 1
        case "1080p":
            score1 = 2
        case _:
            score1 = 3

    match media.source:
        case "BLURAY":
            score2 = 1
        case "WEB":
            score2 = 2
        case _:
            score2 = 3

    return (score1, score2, media.size)


def select_best_media(medium: list[Media]) -> Media:
    medium.sort(key=calculate_media_priority)
    return medium[0]


def get_download_link(keyword: str) -> str:
    fullname = get_media_fullname(keyword)
    medium = get_available_medium(fullname)
    best_media = select_best_media(medium=medium)
    print(f"准备下载 {best_media.name} ({best_media.resolution})")
    print(f"文件大小：{best_media.size:.2f}GB")
    print(f"文件来源：{best_media.source}")
    print(f"下载链接：{best_media.download_link}")
    print()
    return best_media.download_link


def download_media(download_link: str):
    _download = aria2.add_magnet(download_link)


def main():
    keywords = sys.argv[1:]
    if len(keywords) == 0:
        print("没有想搜寻的关键词")

    for keyword in keywords:
        print(f"搜寻 `{keyword}` ...")
        download_link = get_download_link(keyword)
        download_media(download_link)


if __name__ == "__main__":
    main()
