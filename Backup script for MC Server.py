import psutil
import shutil
import time
import pyuac
import os
from datetime import datetime

#wyszukanie procesu poprzez iterowanie po wszystkich aktywnych procesach i dopasowanie po nazwie
def findProcess(process):
    for item in psutil.pids():
        p = psutil.Process(item)
        if p.name() == process:
            return True
    return False

#Tworzy kopię pliku i usuwa poprzednią
def makeBackUp(source, destination):
    try: os.chmod(destination, 0o777) #nadanie uprawnień do modyfikacji
    except Exception as e:
        shutil.copytree(source, destination)
    shutil.rmtree(destination) #usunięcie istniejącego backupu
    shutil.copytree(source, destination)

#Pokazuje obecną godzinę
def currentDate():
    c = datetime.now()
    current_time = c.strftime('%H:%M')
    return current_time

#czeka 15 minut = 900 sekund
def czekanie(t):
        time.sleep(t)

def pauseProcesses(PID):
    for item in PID:
        psutil.Process(item).suspend()

def resumeProcesses(PID):
    for item in PID:
        psutil.Process(item).resume()

def getPIDs(processes):
    pids = []
    for item in processes:
        for proc in psutil.process_iter():
            if item in proc.name():
                pids.append(proc.pid)
    return pids

def main():
    processes = ['minecraft', 'javaw.exe', 'Curse.Agent']
    McPID = []
    t = 900
    process = 'minecraft.exe'
    source = r"C:\Users\wojte\curseforge\minecraft\Instances\Chosen's Modded Adventure\saves\Eryk i Wojtek turbo przygoda"
    destination1 = r"D:\Minecraft Backups\Backup 1 Eryk i Wojtek"
    destination2 = r"D:\Minecraft Backups\Backup 2 Eryk i Wojtek"

    McPID = getPIDs(processes)
    os.chmod(r"D:\Minecraft Backups", 0o777)
    if findProcess(process): 
        print ('Process found.')
        while findProcess(process):
            print('Initiating backup...')
            pauseProcesses(McPID)
            try: 
                makeBackUp(source, destination1)
                print ('Backup complete.')
            except Exception as e:
                resumeProcesses(McPID)
                print(f'Backup failed at {currentDate()}. Resumed processes.\nError: {e}')
                break
            resumeProcesses(McPID)
            print (f'Processes resumed. Sequence completed at {currentDate()}.')
            czekanie(t)
            print('Initiating backup...')
            pauseProcesses(McPID)
            try: 
                makeBackUp(source, destination2)
                print ('Backup complete.')
            except Exception as e:
                resumeProcesses(McPID)
                print(f'Backup failed at {currentDate()}. Resumed processes.\nError: {e}')
                break
            resumeProcesses(McPID)
            print (f'Processes resumed. Sequence completed at {currentDate()}.')
            czekanie(t)
        else: 
            makeBackUp(source, destination1)
            print (f'Exit backup made at {currentDate()}.\nProcess exited. Shutting down...')
    else: print ('Process not found :(')

main()
