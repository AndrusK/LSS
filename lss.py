import sys
import requests
import time
from alive_progress import alive_bar

def scraper(i):
    summoners = []
    r = requests.get('https://na.op.gg/ranking/level/page='+str(i))
    for line in r.text.splitlines():
        if "userName=" in line:
            if not "%" in line:
                summoner_name = line.split()[6].split('userName=')[1].split("\">")[0]
                summoners.append(summoner_name.replace("+",""))
    return summoners


def scrape_range(x,y):
    summoners = []
    page_count = y - x
    with alive_bar(page_count) as bar:
        for i in range(x,y):
            summoners.extend(scraper(i))
            print(f"scraping page {i}")
            bar()
    return summoners


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("lss.py [start] [end] [filename]")
    else:
        savefile = sys.argv[3]
        summoners = scrape_range(int(sys.argv[1]),int(sys.argv[2]))
        with open(savefile, 'w') as filehandle:
            for summoner in summoners:
                if not summoner == summoners[-1]:
                    filehandle.write('%s\n' % summoner)
                else:
                    filehandle.write('%s' % summoner)
        print("Done!")
