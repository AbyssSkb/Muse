import aria2p
from dotenv import load_dotenv
import os

load_dotenv()
ARIA2_HOST = os.getenv("ARIA2_HOST", "http://localhost")
ARIA2_PORT = int(os.getenv("ARIA2_PORT", 6800))
ARIA2_SECRET = os.getenv("ARIA2_SECRET", "")

aria2 = aria2p.API(
    client=aria2p.Client(host=ARIA2_HOST, port=ARIA2_PORT, secret=ARIA2_SECRET)
)
downloads = aria2.get_downloads()


for download in downloads:
    print(f"文件名：{download.name}")
    print(f"文件大小：{download.total_length_string()}")
    print(f"下载速度：{download.download_speed_string()}")
    print(f"上传速度：{download.upload_speed_string()}")
    print(f"连接数：{download.connections}")
    print(f"做种数：{download.num_seeders}")
    print(f"状态：{download.status}")
    print(f"已下载大小：{download.completed_length_string()}")
    print(f"下载进度：{(download.progress):.2f}%")
    print(f"预计剩余时间：{download.eta}")
    print()

aria2.purge()
