import sys
import requests
from alive_progress import alive_bar, styles

def scraper(current_page):
    summoners = []
    r = requests.get('https://na.op.gg/ranking/level/page='+str(current_page))
    for line in r.text.splitlines():
        if "userName=" in line:
            if not "%" in line:
                summoner_name = line.split()[6].split('userName=')[1].split("\">")[0]
                summoners.append(summoner_name.replace("+",""))
    return summoners


def scrape_range(start,end):
    summoners = []
    page_count = start - end
    with alive_bar(page_count, enrich_print=False, monitor=True) as bar:
        for i in range(start,end):
            print(f"Currently scraping page: {i}")
            summoners.extend(scraper(i))
            bar()
    return summoners


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        savefile = sys.argv[3]
        summoners = scrape_range(int(sys.argv[1]),int(sys.argv[2]))
        with open(savefile, 'w') as filehandle:
            for summoner in summoners:
                if not summoner == summoners[-1]:
                    filehandle.write('%s\n' % summoner)
                else:
                    filehandle.write('%s' % summoner)
        print("Done!")
    else:
        print("lss.py [start] [end] [filename]")
