import aria2p

aria2 = aria2p.API(client=aria2p.Client(secret="12345678"))


downloads = aria2.get_downloads()

for download in downloads:
    print(download.name, download.download_speed / 1024, download.upload_speed / 1024, download.num_seeders, download.is_active, download.is_complete, download.status, download.eta, download.progress, download.has_failed, download.seeder, download.is_waiting, download.connections)

# aria2.purge()
# aria2.remove(downloads)

