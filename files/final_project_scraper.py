import time
import csv
import requests
from multiprocessing.pool import ThreadPool
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# webdriver options
options = Options()
options.add_argument('--headless') # runs chrome instance without gui
options.add_argument('--disable-gpu') # runs chrome instance without gpu

# gets data from a player page
def get_data(url_container):
    user_data = []
    
    # creates chrome instance
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
    driver.implicitly_wait(1000)
    
    # gets page contents
    driver.get(url_container['href'])
    player_page = driver.page_source
    
    driver.quit()
    
    player_soup = BeautifulSoup(player_page, 'html.parser')
    
    if player_soup.find("h1", {"class":"profile-info__name"}) is not None:
        user_data.append(next(player_soup.find("h1", {"class":"profile-info__name"}).children).text) # username
        
        ranks_and_pp = player_soup.find_all("div", {"class":"value-display__value"})
        user_data.append(next(ranks_and_pp[0].children).text.replace(',', '').replace('#', '')) # global rank
        user_data.append(next(ranks_and_pp[1].children).text.replace(',', '').replace('#', '')) # country rank
        user_data.append(next(ranks_and_pp[4].children).text.replace(',', '')) # pp
        
        # playtime
        playtime_unformatted = player_soup.find("span", {"data-tooltip-position":"bottom center"}).text
        playtime_list = playtime_unformatted.split(' ')
        days_in_minutes = int(playtime_list[0].replace('d', '')) * 1440
        hours_in_minutes = int(playtime_list[1].replace('h', '')) * 60
        minutes = int(playtime_list[2].replace('m', ''))
        user_data.append(str(days_in_minutes + hours_in_minutes + minutes))
        
        stats = player_soup.find_all("dd", {"class":"profile-stats__value"})
        user_data.append(stats[0].text.replace(',', '')) # ranked score
        user_data.append(stats[1].text.replace('%', '')) # hit accuracy
        user_data.append(stats[2].text.replace(',', '')) # play count
        user_data.append(stats[3].text.replace(',', '')) # total score
        user_data.append(stats[4].text.replace(',', '')) # total hits
        user_data.append(stats[5].text.replace(',', '')) # maximum combo
        csv_writer.writerow(user_data)

for i in range(1000):
    leaderboard_page = requests.get('https://osu.ppy.sh/rankings/osu/performance?page=' + str(i + 43) + '#scores')
    leaderboard_soup = BeautifulSoup(leaderboard_page.content, 'html.parser')
    link_containers = leaderboard_soup.find_all(class_ = 'ranking-page-table__user-link-text js-usercard')
    with open('osu_data.csv', 'a') as osu_csv:
        time.sleep(10)
        csv_writer = csv.writer(osu_csv, delimiter = ',', lineterminator = '\n')
        ThreadPool(10).map(get_data, link_containers[0:10])
        time.sleep(10)
        ThreadPool(10).map(get_data, link_containers[10:20])
        time.sleep(10)
        ThreadPool(10).map(get_data, link_containers[20:30])
        time.sleep(10)
        ThreadPool(10).map(get_data, link_containers[30:40])
        time.sleep(10)
        ThreadPool(10).map(get_data, link_containers[40:50])
        time.sleep(10)