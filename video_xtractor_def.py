import os
import sys
import yt_dlp as youtube_dl
import subprocess
import shutil
import re
from colorama import init, Fore, Style

# INITIALISATION DE COLORAMA
init(autoreset=True)

BASE_SITES = (
    "https://www.youtube.com",
    "https://www.tiktok.com",
    "https://www.instagram.com",
    "https://www.twitch.tv",
    "https://www.dailymotion.com"
)

# RÉCUPÉRER L'OUTIL DE TRAITEMENT DES FICHIERS MULTIMEDIA
def get_ffmpeg_path():
    ffmpeg_path = 'ffmpeg/bin/ffmpeg.exe'  # Par défaut, utiliser le ffmpeg local
    if getattr(sys, 'frozen', False):
        # Si l'application est empaquetée, utiliser le ffmpeg inclus avec l'application
        ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg', 'bin', 'ffmpeg.exe')
    if not os.path.exists(ffmpeg_path):
        print(f"{Fore.RED}ERREUR : ffmpeg non trouvé au chemin : {ffmpeg_path}")
    return ffmpeg_path

# EXÉCUTER UNE COMMANDE FFMPEG
def run_ffmpeg_command(command, description, progress_step, total_steps):
    ffmpeg_path = get_ffmpeg_path()
    full_command = [ffmpeg_path] + command
    print(f"{Fore.MAGENTA}Exécution de la commande ({description}) : {Fore.CYAN}{' '.join(full_command)}{Fore.RESET}")
    try:
        result = subprocess.run(full_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        print(result.stderr.decode())
        if 'Extraction' in description:
            print(f"{Fore.GREEN}Extraction de l'audio temporaire terminé {Fore.CYAN}({progress_step}/{total_steps} - {int((progress_step/total_steps)*100)}%)")
        else:
            print(f"{Fore.GREEN}{description} terminé {Fore.CYAN}({progress_step}/{total_steps} - {int((progress_step/total_steps)*100)}%){Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Erreur lors de l'exécution de ffmpeg ({description}) : {e.stderr.decode()}{Style.RESET_ALL}")

# RÉCUPÉRER LES URLS DES VIDÉOS À TÉLÉCHARGER
def get_video_url_from_user():
    urls_input = input(f"{Style.BRIGHT}{Fore.GREEN}Entrez les URL des vidéos à télécharger, séparées par des virgules : {Style.RESET_ALL}")
    urls = [url.strip() for url in urls_input.split(',')]
    
    valid_urls = []
    for url in urls:
        if not any(url.lower().startswith(base) for base in BASE_SITES):
            print(f"{Fore.RED}ERREUR : '{url}' n'est pas une URL valide!{Style.RESET_ALL}")
        else:
            valid_urls.append(url)

    if not valid_urls:
        print(f"{Fore.RED}Aucune URL valide détectée, veuillez réessayer.{Style.RESET_ALL}")
        return get_video_url_from_user()
    
    return valid_urls

# NETTOYER LES NOMS DE FICHIERS
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# SURVEILLER LA PROGRESSION DU TÉLÉCHARGEMENT
def on_download_progress(d):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        print(f"{Fore.CYAN}\rProgression du téléchargement : {percent}{Style.RESET_ALL}", end='')

# TÉLÉCHARGER UNE VIDÉO
def download_video(url):
    with youtube_dl.YoutubeDL({'quiet': True}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        video_title_safe = sanitize_filename(video_title.replace(" ", "_").replace("&", "and").replace("'", "").replace("(", "").replace(")", ""))

    # Créer un répertoire pour les fichiers de cette vidéo
    output_dir = os.path.join(os.getcwd(), video_title_safe)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    original_video_filename = os.path.join(output_dir, f"{video_title_safe}.webm")
    video_temp_filename = os.path.join(output_dir, f"{video_title_safe}_TEMP.webm")
    audio_temp_filename = os.path.join(output_dir, f"{video_title_safe}_TEMP.m4a")
    audio_filename_mp3 = os.path.join(output_dir, f"{video_title_safe}_AUDIO.mp3")
    audio_filename_aac = os.path.join(output_dir, f"{video_title_safe}_AUDIO.aac")
    audio_filename_flac = os.path.join(output_dir, f"{video_title_safe}_AUDIO.flac")
    final_output_filename_mp4 = os.path.join(output_dir, f"{video_title_safe}_VIDEO.mp4")
    final_output_filename_mkv = os.path.join(output_dir, f"{video_title_safe}_VIDEO.mkv")

    # Télécharger la vidéo originale avec son titre d'origine
    ydl_opts_original = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [on_download_progress],
        'ffmpeg_location': get_ffmpeg_path(),
        'quiet': True,
        'noprogress': True,  # Pour masquer la barre de progression de yt-dlp
        'merge_output_format': 'mp4',  # Option pour assurer le bon format de sortie
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # Assure la conversion en MP4
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts_original) as ydl:
        ydl.download([url])
    print()  # Pour passer à la ligne après le téléchargement

    total_steps = 7
    current_step = 1

    # Trouver le fichier téléchargé
    downloaded_files = [f for f in os.listdir(output_dir) if f.endswith(('.webm', '.mp4', '.mkv'))]
    if downloaded_files:
        original_video_filename = os.path.join(output_dir, downloaded_files[0])
        shutil.copyfile(original_video_filename, video_temp_filename)
    else:
        raise FileNotFoundError(f"{Fore.RED}Impossible de trouver le fichier téléchargé pour {video_title}{Style.RESET_ALL}")

    # Masquer les fichiers temporaires
    os.system(f'attrib +h {video_temp_filename}')
    os.system(f'attrib +h {audio_temp_filename}')

    # Extraire l'audio temporaire
    run_ffmpeg_command(['-i', video_temp_filename, '-acodec', 'aac', audio_temp_filename], "Extraction de l'audio temporaire", current_step, total_steps)
    current_step += 1

    # Vérifiez l'existence des fichiers temporaires après leur création
    if not os.path.exists(audio_temp_filename):
        print(f"{Fore.RED}ERREUR : Fichier temporaire audio non trouvé : {audio_temp_filename}{Style.RESET_ALL}")
        return

    # Créer des fichiers audio avec l'audio temporaire dans les formats MP3, AAC et FLAC
    run_ffmpeg_command(['-i', audio_temp_filename, '-acodec', 'mp3', audio_filename_mp3], "Création du fichier MP3", current_step, total_steps)
    current_step += 1
    run_ffmpeg_command(['-i', audio_temp_filename, '-acodec', 'flac', audio_filename_flac], "Création du fichier FLAC", current_step, total_steps)
    current_step += 1
    run_ffmpeg_command(['-i', audio_temp_filename, '-acodec', 'aac', audio_filename_aac], "Création du fichier AAC", current_step, total_steps)
    current_step += 1

    # Créer des fichiers vidéo avec le son dans les formats MP4 et MKV
    run_ffmpeg_command(['-i', video_temp_filename, '-vcodec', 'copy', '-acodec', 'aac', final_output_filename_mp4], "Création du fichier MP4", current_step, total_steps)
    current_step += 1
    run_ffmpeg_command(['-i', video_temp_filename, '-vcodec', 'copy', '-acodec', 'aac', final_output_filename_mkv], "Création du fichier MKV", current_step, total_steps)
    current_step += 1

    print(f"{Fore.MAGENTA}Téléchargement et conversion terminés pour {video_title} ({current_step}/{total_steps} - 100%)")

    # Supprimer les fichiers temporaires
    os.remove(video_temp_filename)
    os.remove(audio_temp_filename)
