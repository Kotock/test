import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import logging
from typing import List, Dict
from config import HEADERS, DELAY, CSV_FILE, JSON_FILE, URLS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebParser:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.data = []
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Загрузка и парсинг HTML страницы"""
        try:
            logger.info(f"Загружаем: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            time.sleep(DELAY)
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Ошибка загрузки {url}: {e}")
            return None
    
    def parse_quotes(self, soup: BeautifulSoup) -> List[Dict]:
        quotes = []
        
        if not soup:
            return quotes
        
        for quote_block in soup.find_all('div', class_='quote'):
            try:
                text = quote_block.find('span', class_='text').text.strip()
                author = quote_block.find('small', class_='author').text.strip()
                tags = [tag.text for tag in quote_block.find_all('a', class_='tag')]
                
                quotes.append({
                    'text': text,
                    'author': author,
                    'tags': ', '.join(tags)
                })
            except AttributeError as e:
                logger.warning(f"Пропущен блок: {e}")
        
        return quotes
    
    def parse_books(self, soup: BeautifulSoup) -> List[Dict]:
        books = []
        
        if not soup:
            return books
        
        for book in soup.find_all('article', class_='product_pod'):
            try:
                title = book.find('h3').find('a')['title']
                price = book.find('p', class_='price_color').text.strip()
                rating = book.find('p', class_='star-rating')['class'][1]
                
                books.append({
                    'title': title,
                    'price': price,
                    'rating': rating
                })
            except (AttributeError, KeyError) as e:
                logger.warning(f"Пропущена книга: {e}")
        
        return books
    
    def run(self, urls: List[str] = None, parse_method: str = 'quotes'):
        if urls is None:
            urls = URLS
        
        parse_func = getattr(self, f'parse_{parse_method}')
        
        for url in urls:
            soup = self.fetch_page(url)
            if soup:
                page_data = parse_func(soup)
                self.data.extend(page_data)
                logger.info(f"Спарсено {len(page_data)} записей с {url}")
        
        logger.info(f"Всего собрано {len(self.data)} записей")
        return self.data
    
    def save_csv(self, filename: str = None):
        if not self.data:
            logger.warning("Нет данных для сохранения")
            return
        
        filename = filename or CSV_FILE
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)
        
        logger.info(f"CSV сохранен: {filename}")
    
    def save_json(self, filename: str = None):
        """Сохранение в JSON"""
        if not self.data:
            logger.warning("Нет данных для сохранения")
            return
        
        filename = filename or JSON_FILE
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"JSON сохранен: {filename}")