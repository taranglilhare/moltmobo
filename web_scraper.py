"""
Web Scraping Module - Free Data Extraction
Uses BeautifulSoup and Selenium for web automation
"""

from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
import json

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

from utils.logger import logger


class WebScraper:
    """Web scraping using BeautifulSoup"""
    
    def __init__(self):
        """Initialize web scraper"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Android 11; Mobile) MoltMobo/1.0'
        })
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch webpage content
        
        Args:
            url: URL to fetch
        
        Returns:
            HTML content or None
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            logger.info(f"✓ Fetched: {url}")
            return response.text
        
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML with BeautifulSoup"""
        return BeautifulSoup(html, 'html.parser')
    
    def extract_text(self, url: str) -> str:
        """Extract all text from webpage"""
        html = self.fetch_page(url)
        if not html:
            return ""
        
        soup = self.parse_html(html)
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def extract_links(self, url: str) -> List[Dict]:
        """Extract all links from webpage"""
        html = self.fetch_page(url)
        if not html:
            return []
        
        soup = self.parse_html(html)
        links = []
        
        for a_tag in soup.find_all('a', href=True):
            links.append({
                'text': a_tag.get_text(strip=True),
                'url': a_tag['href']
            })
        
        return links
    
    def extract_images(self, url: str) -> List[Dict]:
        """Extract all images from webpage"""
        html = self.fetch_page(url)
        if not html:
            return []
        
        soup = self.parse_html(html)
        images = []
        
        for img_tag in soup.find_all('img', src=True):
            images.append({
                'src': img_tag['src'],
                'alt': img_tag.get('alt', ''),
                'title': img_tag.get('title', '')
            })
        
        return images
    
    def find_by_selector(self, url: str, selector: str) -> List:
        """Find elements by CSS selector"""
        html = self.fetch_page(url)
        if not html:
            return []
        
        soup = self.parse_html(html)
        return soup.select(selector)
    
    def extract_table(self, url: str, table_index: int = 0) -> List[List[str]]:
        """Extract table data"""
        html = self.fetch_page(url)
        if not html:
            return []
        
        soup = self.parse_html(html)
        tables = soup.find_all('table')
        
        if table_index >= len(tables):
            return []
        
        table = tables[table_index]
        data = []
        
        for row in table.find_all('tr'):
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
            data.append(row_data)
        
        return data
    
    def monitor_price(self, url: str, selector: str) -> Optional[str]:
        """
        Monitor price on webpage
        
        Args:
            url: Product page URL
            selector: CSS selector for price element
        
        Returns:
            Price string or None
        """
        elements = self.find_by_selector(url, selector)
        
        if elements:
            return elements[0].get_text(strip=True)
        
        return None


class BrowserAutomation:
    """Browser automation using Selenium"""
    
    def __init__(self):
        """Initialize browser automation"""
        self.driver = None
        self.enabled = SELENIUM_AVAILABLE
        
        if not self.enabled:
            logger.warning("⚠️  Selenium not installed")
            logger.info("Install: pip install selenium")
    
    def start_browser(self, headless: bool = True):
        """Start browser"""
        if not self.enabled:
            return False
        
        try:
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            self.driver = webdriver.Chrome(options=options)
            logger.info("✓ Browser started")
            return True
        
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            return False
    
    def navigate(self, url: str):
        """Navigate to URL"""
        if not self.driver:
            return False
        
        try:
            self.driver.get(url)
            logger.info(f"✓ Navigated to: {url}")
            return True
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return False
    
    def click_element(self, selector: str, by: str = "css"):
        """Click element"""
        if not self.driver:
            return False
        
        try:
            by_type = By.CSS_SELECTOR if by == "css" else By.XPATH
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((by_type, selector))
            )
            element.click()
            logger.info(f"✓ Clicked: {selector}")
            return True
        except Exception as e:
            logger.error(f"Click failed: {e}")
            return False
    
    def fill_form(self, selector: str, text: str, by: str = "css"):
        """Fill form field"""
        if not self.driver:
            return False
        
        try:
            by_type = By.CSS_SELECTOR if by == "css" else By.XPATH
            element = self.driver.find_element(by_type, selector)
            element.clear()
            element.send_keys(text)
            logger.info(f"✓ Filled: {selector}")
            return True
        except Exception as e:
            logger.error(f"Fill failed: {e}")
            return False
    
    def get_page_source(self) -> str:
        """Get page HTML"""
        if not self.driver:
            return ""
        
        return self.driver.page_source
    
    def screenshot(self, filename: str):
        """Take screenshot"""
        if not self.driver:
            return False
        
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"✓ Screenshot saved: {filename}")
            return True
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return False
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")


# Free APIs Integration
class FreeAPIs:
    """Integration with free public APIs"""
    
    @staticmethod
    def get_weather(city: str) -> Optional[Dict]:
        """Get weather using free API"""
        try:
            # Using wttr.in (completely free, no API key)
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            current = data['current_condition'][0]
            return {
                'temperature': current['temp_C'],
                'description': current['weatherDesc'][0]['value'],
                'humidity': current['humidity'],
                'wind_speed': current['windspeedKmph']
            }
        except Exception as e:
            logger.error(f"Weather API failed: {e}")
            return None
    
    @staticmethod
    def get_news(category: str = "general") -> Optional[List[Dict]]:
        """Get news headlines (requires API key for NewsAPI)"""
        # Using free tier of NewsAPI
        # User needs to add API key in .env
        api_key = os.getenv("NEWS_API_KEY")
        
        if not api_key:
            logger.warning("NEWS_API_KEY not set")
            return None
        
        try:
            url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={api_key}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            articles = []
            for article in data.get('articles', [])[:5]:
                articles.append({
                    'title': article['title'],
                    'description': article['description'],
                    'url': article['url']
                })
            
            return articles
        except Exception as e:
            logger.error(f"News API failed: {e}")
            return None
    
    @staticmethod
    def get_joke() -> Optional[str]:
        """Get random joke"""
        try:
            url = "https://official-joke-api.appspot.com/random_joke"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            return f"{data['setup']} - {data['punchline']}"
        except Exception as e:
            logger.error(f"Joke API failed: {e}")
            return None
