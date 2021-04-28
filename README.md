# World-News-Organizer
> Detailed description can be seen in 0716021_Documentation.pdf.

# Escape your echo chamber! The​ ​World News Organizer

## A. Overview
This is an application that shows international news and headlines from reliable news sources such as BBC, CNN, and Al Jazeera. Other than the news itself, it will also show topics related to the news for the users to broaden their understandings about the issue reported.

## B. Motivation
People nowadays have gradually been considered indifference towards global issues and world topics. There is a term that has become increasingly popular in recent years called "同溫層", resembling the term "echo chamber" in English, which refers to ​an environment in which a person encounters only beliefs or opinions that coincide with their own. The best way for a person to leave his or her echo chamber is to read news about the world. However, local newspapers and media in Taiwan usually cover only little information about the world and are considered biased. Therefore, I came up with the idea to gather international headlines from trusted and reliable sources and display them all at a time, the user could then get a grasp of world issues at a glance. Other than this, adding related topics can also help users to understand what are related to the news.<br><br><br>
# Installation

## Requirements
- Python 3.3+
- Requests, Pandas
- BeautifulSoup4
- NewsAPI
- PyTrends

## Installation
**Requests** <br>
``pip3 install requests``<br>
**Pandas** <br>
``pip3 install pandas``<br>
**BeautifulSoup4** <br>
``pip3 install beautifulsoup4``<br>
**NewsAPI** <br>
``pip3 install newsapi-python``<br>
**PyTrends** <br>
``pip3 install pytrends``<br>

# How to run

## Step 1:
There are two python files in this project, ​main.py​ and ​functions.py respectively. In order to run the project,

**For MacOS:**

Under the same path of the files in terminal, type 
``python3 main.py``

**For Windows:**

In CMD, type ``py main.py`` to run the file.

## Step 2:
After running the file, the program will prompt you to choose 3 news sources from the 8 sources below as shown below:
![prompt1](/resources/img1.png)

Enter your choice and press enter, the program will continue to prompt you.

![prompt2](/resources/img2.png)

After entering three choices, the program will start to request data:
![request](/resources/img3.png)

## Step 3:
After requesting data, the program will generate an HTML file ​pages.html​, ​and automatically open it with the default browser of your system:
![browser](/resources/img4.png)

There will be 3 headlines from each chosen source, 9 articles in total.
![hover](/resources/img5.png)
If you hover your mouse on a keyword, the page will show related topics of the respective keyword.
If you are interested in one article and want to read more, you can click on the **​Read more...** ​and it will lead to the news website.