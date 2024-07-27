from colorama import init, Fore, Style
from video_xtractor_def import get_video_url_from_user, download_video


# INITIALISATION DE COLORAMA
init(autoreset=True)

if __name__ == "__main__":
    urls = get_video_url_from_user()
    for url in urls:
        try:
            download_video(url)
        except Exception as e:
            print(f"{Fore.RED}Erreur lors du téléchargement de la vidéo : {e}{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{Fore.MAGENTA}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
