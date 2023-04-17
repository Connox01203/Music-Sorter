import os
import ffmpeg
import glob
import subprocess
import sys
import eyed3
import shutil
from zipfile import ZipFile
from mutagen.flac import FLAC
import concurrent.futures
import time 

####################INSERT FOLDERS HERE####################
check_folder = 'C:\\'
save_folder = "C:\\"
####################INSERT FOLDERS HERE####################

path_list = []
ten_list_handoff = []

def convert_flac(a_file):
    out_name = a_file.replace(".flac", ".mp3")
    subprocess.run(f'ffmpeg -i "{a_file}" -codec:a libmp3lame -qscale:a 0 "{out_name}"')
    return(a_file)

def main():
    zip_files = glob.glob(check_folder+"*.zip")

    ##Extract all zip files##
    for z_file in zip_files:
        with ZipFile(z_file) as z:
            z.extractall(check_folder)
        os.remove(z_file)


    ##Find all files##
    flac_files = glob.glob(check_folder + '**\\*.flac', recursive=True)
    mp3_files = glob.glob(check_folder+"**\\*.mp3", recursive=True)
    ab_files = glob.glob(check_folder+"**\\*.jpg", recursive=True)


    while True:
        if len(flac_files) != 0:
            for x in range(10):
                try:
                    ten_list_handoff.append(flac_files[0])
                    flac_files.pop(0)
                except IndexError:
                    break
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = executor.map(convert_flac, ten_list_handoff)
                for a_file in results:
                    print(a_file)
                    out_name = a_file.replace(".flac", ".mp3")

                    audiofile = eyed3.load(out_name)
                    artist = audiofile.tag.artist
                    artist_list = artist.split(';')
                    artist = artist_list[0]
                    

                    album_given = audiofile.tag.album
                    #Check for special characters and remove them#
                    for digit in album_given:
                        if digit == "/" or digit == "\\" or digit == ":" or digit == "*" or digit == "?" or digit == '"' or digit == "<" or digit == ">" or digit == "|":
                            album_given = album_given.replace(digit, "")
                    album = album_given

                    the_name_flac = save_folder + "Flac\\" + album + '-' + artist
                    the_name_mp3 = save_folder + "Mp3\\" + album + '-' + artist
                    the_name_master = save_folder + "Master_Player\\" + album + '-' + artist
                    #Sort flac and mp3#
                    #Sort in master
                    if os.path.isdir(the_name_master): 
                        m_list = glob.glob(the_name_master+"**\\*.mp3")
                        mp3_found = False
                        for mp3_file in m_list:
                            audiofile = eyed3.load(mp3_file)
                            audio_f = FLAC(a_file)
                            audio_ft = audio_f["TITLE"]
                            if audio_ft[0] == audiofile.tag.title:
                                mp3_found = True
                                os.remove(mp3_file)
                                shutil.copy(a_file, the_name_master)
                                break
                        if not mp3_found:
                            shutil.copy(a_file, the_name_master)
                    else:
                        os.mkdir(the_name_master)
                        shutil.copy(a_file, the_name_master)
                    #Sort Flac
                    if os.path.isdir(the_name_flac): 
                        try:
                            shutil.move(a_file, the_name_flac)
                        except shutil.Error:
                            os.remove(a_file)
                    else:
                        os.mkdir(the_name_flac)
                        shutil.move(a_file, the_name_flac)
                    #Sort Mp3
                    if os.path.isdir(the_name_mp3):
                        try:
                            shutil.move(out_name, the_name_mp3)
                        except shutil.Error:
                            os.remove(out_name)
                    else:
                        os.mkdir(the_name_mp3)
                        shutil.move(out_name, the_name_mp3)
                ten_list_handoff.clear()
        else:
            break
    #Sort mp3 files##
    for m_file in mp3_files:
        audiofile = eyed3.load(m_file)

        artist = audiofile.tag.artist
        artist_list = artist.split(';')
        artist = artist_list[0]
        #Check for special characters#
        album_given = audiofile.tag.album
        for digit in album_given:
            if digit == "/" or digit == "\\" or digit == ":" or digit == "*" or digit == "?" or digit == '"' or digit == "<" or digit == ">" or digit == "|":
                album_given = album_given.replace(digit, "")
        album = album_given

        the_name_mp3 = save_folder + "Mp3\\" + album + '-' + artist
        the_name_master = save_folder + "Master_Player\\" + album + '-' + artist

        #Sort mp3#
        #Sort in master
        if os.path.isdir(the_name_master):
            mmusic_list = glob.glob(the_name_master+"**\\*.flac", recursive=True)
            flac_found = False
            for flac_file in mmusic_list:
                audio_f = FLAC(flac_file)
                audio_ft = audio_f["TITLE"]
                if audio_ft[0] == audiofile.tag.title:
                    flac_found = True
                    break
            if not flac_found:
                shutil.copy(m_file, the_name_master)
        else:
            os.mkdir(the_name_master)
            shutil.copy(m_file, the_name_master)
        #Sort in mp3
        if os.path.isdir(the_name_mp3):
            try:
                shutil.move(m_file, the_name_mp3)
            except shutil.Error:
                os.remove(m_file)
        else:
            os.mkdir(the_name_mp3)
            shutil.move(m_file, the_name_mp3)


    ##Sort and rename album covers##
    for ab_file in ab_files:
        ab_file_sep_list = ab_file.split("\\")
        ab_file_sep_list.pop(-1)
        if len(ab_file_sep_list[-1]) > 64:
            new_name = ""
            counter = 0
            for char in ab_file_sep_list[-1]:
                if counter > 63:
                    break
                else:
                    new_name += char
                    counter += 1
            ab_file_sep_list.pop(-1)
            ab_file_sep_list.append(new_name+".jpg")
        else:
            ab_file_sep_list.append(ab_file_sep_list[-1]+".jpg")
        rename_ab = "\\".join(ab_file_sep_list)
        os.rename(ab_file, rename_ab)
        try:
            shutil.move(rename_ab, save_folder + "Album_Covers")
        except shutil.Error:
            os.remove(rename_ab)

    ##Delete all empty remaining folders##
    for root, dirs, f in os.walk(check_folder, topdown = False):
                for name in dirs:
                    path = os.path.join(root, name)
                    if len(os.listdir(path)) == 0:
                        try:
                            os.rmdir(path)
                        except OSError:
                            print(f"{path} was not empty")

    is_exit = input("> ")
    if is_exit.upper() == "EXIT":
        quit()

if __name__ == '__main__':
    main()