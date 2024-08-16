import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

# URL to scrape
url = "https://thehackernews.com/search/label/hacking%20news"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Set the current date and initialize the previous title
current_date = datetime.now().date()
previous_title = "New Mockingjay Process Injection Technique Could Let Malware Evade Detection"

def scrape_news():
    global previous_title
    articles = soup.find_all("div", class_="body-post clear")

    news_list = []

    for article in articles:
        # Extract the date
        date_string = article.find("span", class_="h-datetime").text.split("")[1]
        article_date = datetime.strptime(str(date_string), "%b %d, %Y").date()
        title = article.find("h2", class_="home-title").text.strip()

        if previous_title != title:
            image = article.find("img")['data-src']
            tags_element = article.find("span", class_="h-tags")
            tags = tags_element.text.strip() if tags_element else "No Tags"
            description = article.find("div", class_="home-desc").text.strip()
            
            news_list.append({
                "title": title,
                "image": image,
                "date": date_string,
                "tags": tags,
                "description": description
            })
        else:
            image = article.find("img")['data-src']
            tags_element = article.find("span", class_="h-tags")
            tags = tags_element.text.strip() if tags_element else "No Tags"
            description = article.find("div", class_="home-desc").text.strip()
            
            news_list.append({
                "title": title,
                "image": image,
                "date": date_string,
                "tags": tags,
                "description": description
            })
            previous_title = news_list[0]['title']
            break

    return news_list

def save_to_csv(news_list, output_file="hacker_news.csv"):
    # Check if the output file already exists
    file_exists = os.path.isfile(output_file)
    
    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Title", "Image URL", "Date", "Tags", "Description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()  # Write header only if the file doesn't exist
        
        for news in news_list:
            writer.writerow({
                "Title": news["title"],
                "Image URL": news["image"],
                "Date": news["date"],
                "Tags": news["tags"],
                "Description": news["description"]
            })

if __name__ == "__main__":
    news_list = scrape_news()
    if len(news_list) > 0:
        save_to_csv(news_list)
        print(f"Saved {len(news_list)} articles to 'hacker_news.csv'")
    else:
        print("No new articles found.")
