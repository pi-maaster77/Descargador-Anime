from animeflv import AnimeFLV
import subprocess
import os

# Configuración del directorio de destino
DEST_DIR = '/mnt/sec/anime'

def parse_episode_selection(selection, max_episode):
    episodes = set()
    parts = selection.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            if start > end or start < 1 or end > max_episode:
                raise ValueError("Rango de episodios inválido")
            episodes.update(range(start, end + 1))
        else:
            episode = int(part)
            if episode < 1 or episode > max_episode:
                raise ValueError("Número de episodio inválido")
            episodes.add(episode)
    return sorted(episodes)

def main():
    with AnimeFLV() as api:
        search_term = input("Escribe la serie: ")
        elements = api.search(search_term)
        for i, element in enumerate(elements):
            print(f"{i}, {element.title}")
        try:
            selection = int(input("Seleccionar Opción: "))
            selected_anime = elements[selection]
            info = api.get_anime_info(selected_anime.id)
            info.episodes.reverse()

            max_episode = len(info.episodes)
            episode_selection = input(f"Seleccionar episodios (1-{max_episode}): ")
            episodes_to_download = parse_episode_selection(episode_selection, max_episode)

            for j in episodes_to_download:
                procesar_episodio(j - 1, info.episodes[j - 1], selected_anime, api, DEST_DIR)
        except Exception as e:
            print(e)

def procesar_episodio(k, myepisode, selected_anime, api, dest_dir):
    #print(f"{k+1} | Episode - {myepisode.id}")
    serie = selected_anime.id
    capitulo = myepisode.id
    
    # Obtener los enlaces del API
    results = api.get_links(serie, capitulo)
    mega_url = results[0].url
    print(mega_url)
    
    # Definir el directorio de destino
    episode_dest_dir = os.path.join(dest_dir, serie)
    
    # Crear el directorio si no existe
    os.makedirs(episode_dest_dir, exist_ok=True)
    
    # Comando para descargar el archivo desde MEGA
    download_command = f'mega-get {mega_url} {episode_dest_dir}'
    subprocess.run(download_command, shell=True, check=True)
    
    # Buscar el archivo descargado en el directorio de destino
    downloaded_files = os.listdir(episode_dest_dir)
    downloaded_files_paths = [os.path.join(episode_dest_dir, f) for f in downloaded_files]
    downloaded_files_paths.sort(key=os.path.getctime, reverse=True)  # Ordenar por tiempo de creación

    if downloaded_files_paths:
        original_file_path = downloaded_files_paths[0]
        # Definir el nuevo nombre para el archivo
        new_file_name = f'{serie}-{capitulo}.mp4'  # Ajusta la extensión según el tipo de archivo
        new_file_path = os.path.join(episode_dest_dir, new_file_name)
        # Renombrar el archivo
        os.rename(original_file_path, new_file_path)
        print(f"Archivo descargado y renombrado a: {new_file_path}")
    else:
        pass
        print("Error: no se encontró ningún archivo descargado.")

if __name__ == "__main__":
    main()
