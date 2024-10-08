import re
import requests
from bs4 import BeautifulSoup
import spacy
import PyPDF2

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")
api_key = "39183a2b66049fba96e3be46519e9218"  # Replace with your actual ScraperAPI key


def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    text = ""
    for page_num in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page_num).extractText()
    return text


def extract_keywords_from_query(query):
    doc = nlp(query)
    skills = []
    job_roles = []

    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            if "development" in token.text.lower() or "developer" in token.text.lower():
                job_roles.append(token.text)
            else:
                skills.append(token.text)

    return {"job_roles": job_roles, "skills": skills}


import time


def scrape_jobss(search_term, location="", company=""):
    # ScraperAPI URL and API key

    # params = {"q": search_term, "l": location, "rbc": company}  # Filter by company name
    base_url = f"https://www.indeed.com/jobs/?{search_term}"
    api_url = f"https://api.scraperapi.com?api_key={api_key}&url=https://www.indeed.com/jobs?q={search_term}&l="

    # Send the request to ScraperAPI
    response = requests.get(api_url)

    # Check if the response was successful
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []

    # Parse the HTML response with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []
    # Adjust according to the actual structure of the Indeed page you want to scrape
    for job_card in soup.find_all("li", class_="css-5lfssm"):
        title_div = job_card.find("a", class_="jcs-JobTitle")
        print(title_div)
        if title_div:
            title = title_div.find("span").text.strip()
            company_div = job_card.find("div", class_="company_location")
            location = company_div.find(
                "div", attrs={"data-testid": "text-location"}
            ).text.strip()
            company = company_div.find("span").text.strip()
            link = "https://www.indeed.com" + title_div["href"]

            jobs.append(
                {"title": title, "company": company, "location": location, "link": link}
            )

    return jobs


def scrape_jobs(search_term, location="", company=""):
    url = f"https://www.monster.com/jobs/search/?q={search_term.replace(' ', '-')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []
    for job_card in soup.find_all('section', class_='card-content'):
        title = job_card.find('h2', class_='title').text.strip()
        company = job_card.find('div', class_='company').text.strip()
        location = job_card.find('div', class_='location').text.strip()
        link = job_card.find('a')['href']

        jobs.append({"title": title, "company": company, "location": location, "link": link})

    return jobs

def extract_skills_from_text(text, skills_db):
    skills = []
    for skill in skills_db:
        if re.search(skill, text, re.IGNORECASE):
            skills.append(skill)
    return skills


def parse_resume(file):
    text = extract_text_from_pdf(file)
    skills_db = [
        "Python",
        "Java",
        "Django",
        "React",
        "JavaScript",
        "AWS",
        "Machine Learning",
        "SQL",
    ]
    skills = extract_skills_from_text(text, skills_db)

    # Here, you can further extract entities such as education, etc.
    return {"skills": skills}
