import aria2p
from dotenv import load_dotenv
import os

load_dotenv()
RPC_SECRET = os.getenv("RPC_SECRET", "")

aria2 = aria2p.API(client=aria2p.Client(secret=RPC_SECRET))
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
