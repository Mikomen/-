import json
import os
import random
import time

import  requests
from bs4 import BeautifulSoup

def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'accept': '*/*'
    }

    post_all_data = []
    iteration_count = 20
    print(f"All iterations: #{iteration_count}")

    for item in range(1,21):

        req = requests.get(url + f"?page={item}", headers)

        folder_name = f"data/data_{item}"

        if os.path.exists(folder_name):
            print("Folder already exists")
        else:
            os.mkdir(folder_name)

        with open(f"{folder_name}/nurkz_{item}.html", "w", encoding="utf-8") as file:
            file.write(req.text)

        with open(f"{folder_name}/nurkz_{item}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "html")
        li_posts = soup.find_all("li", class_="block-infinite__item")
        
        post_url = []
        for item in li_posts:
            posts_url = item.find("article", class_="block-infinite__item-content").find("a").get("href")
            post_url.append(posts_url)

        for i in post_url:
            req = requests.get(i, headers)
            post_name = i.split("/")[-2]

            with open(f"{folder_name}/{post_name}.html", "w", encoding="utf-8") as file:
                file.write(req.text)

            with open(f"{folder_name}/{post_name}.html", encoding="utf-8") as file:
                src = file. read()

            soup = BeautifulSoup(src, "html")
            post_data = soup.find("article", class_="article")
            posts_logo = soup.find("header", class_="header")

            try:
                post_logo = posts_logo.find("a", class_="header__logo").find("img").get("src")
                
            except:
                posts_logo = "No logo"
            try:
                post_title = post_data.find("h1").text
                
            except:
                post_title = "No post Title"
            try:
                post_description = ""
                post_desc = soup.find_all("p", class_="align-left")
                for p in post_desc:
                    post_description += p.text
                
            except:
                post_desc = "No Description"

            post_all_data.append(
                {
                    "Post_url": posts_url,
                    "Post_name": post_name,
                    "Post_logo": post_logo,
                    "Post_title": post_title,
                    "Post_description": post_description.strip()
                }
            )
        iteration_count -= 1
        print(f"Iteration: {item} has done!, has left: {iteration_count} iterations")
        if iteration_count == 0:
            print("Assembling all data has been done")
        time.sleep(random.randrange(2,3))

    with open("data/posts_data.json", "a", encoding="utf-8") as file:
        json.dump(post_all_data, file, indent=4, ensure_ascii=False)

get_data("https://www.nur.kz/society/");
