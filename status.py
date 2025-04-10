import aria2p
from dotenv import load_dotenv
import os

load_dotenv()
RPC_SECRET = os.getenv("RPC_SECRET", "")

aria2 = aria2p.API(client=aria2p.Client(secret=RPC_SECRET))
downloads = aria2.get_downloads()


def convert_speed(speed: float) -> str:
    level = 0
    while speed > 1000:
        speed /= 1000
        level += 1

    unit = "B/s"
    match level:
        case 0:
            unit = "B/s"
        case 1:
            unit = "KB/s"
        case 2:
            unit = "MB/s"
        case _:
            unit = "GB/s"

    return f"{speed:.2f}{unit}"


for download in downloads:
    print(f"文件名：{download.name}")
    print(f"下载速度：{convert_speed(download.download_speed)}")
    print(f"上传速度：{convert_speed(download.upload_speed)}")
    print(f"做种数：{download.num_seeders}")
    print(f"状态：{download.status}")
    print(f"下载进度：{(download.progress):.2f}%")
    print(f"预计剩余时间：{download.eta}")
    print()
