from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Any
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    @abstractmethod
    def search_jobs(self, query: str, location: str = None) -> List[Dict[str, Any]]:
        pass
    
    def _make_request(self, url: str, params: Dict = None) -> requests.Response:
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"Error making request to {url}: {str(e)}")
            raise

class InfoJobsScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.infojobs.net/jobsearch/search-results/list.xhtml"
    
    def search_jobs(self, query: str, location: str = None) -> List[Dict[str, Any]]:
        params = {
            'keyword': query,
            'location': location or '',
            'page': 1,
            'sortBy': 'PUBLICATION_DATE'
        }
        
        try:
            response = self._make_request(self.base_url, params)
            return self._parse_jobs(response.text)
        except Exception as e:
            logger.error(f"Error searching jobs on InfoJobs: {str(e)}")
            return []
    
    def _parse_jobs(self, html: str) -> List[Dict[str, Any]]:
        jobs = []
        soup = BeautifulSoup(html, 'html.parser')
        
        for job in soup.find_all('div', class_='ij-OfferCard'):
            try:
                jobs.append({
                    'title': job.find('h2', class_='ij-OfferCard-title').text.strip(),
                    'company': job.find('span', class_='ij-OfferCard-companyName').text.strip(),
                    'location': job.find('span', class_='ij-OfferCard-location').text.strip(),
                    'description': job.find('div', class_='ij-OfferCard-description').text.strip(),
                    'url': job.find('a', class_='ij-OfferCard-link')['href'],
                    'source': 'InfoJobs'
                })
            except Exception as e:
                logger.error(f"Error parsing job from InfoJobs: {str(e)}")
                continue
        
        return jobs

class TecnoempleoScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.tecnoempleo.com/busqueda-empleo.php"
    
    def search_jobs(self, query: str, location: str = None) -> List[Dict[str, Any]]:
        params = {
            'te': query,
            'pr': location or '',
            'ordenar': 'fecha'
        }
        
        try:
            response = self._make_request(self.base_url, params)
            return self._parse_jobs(response.text)
        except Exception as e:
            logger.error(f"Error searching jobs on Tecnoempleo: {str(e)}")
            return []
    
    def _parse_jobs(self, html: str) -> List[Dict[str, Any]]:
        jobs = []
        soup = BeautifulSoup(html, 'html.parser')
        
        for job in soup.find_all('div', class_='job-item'):
            try:
                jobs.append({
                    'title': job.find('h2').text.strip(),
                    'company': job.find('span', class_='company').text.strip(),
                    'location': job.find('span', class_='location').text.strip(),
                    'description': job.find('div', class_='description').text.strip(),
                    'url': job.find('a')['href'],
                    'source': 'Tecnoempleo'
                })
            except Exception as e:
                logger.error(f"Error parsing job from Tecnoempleo: {str(e)}")
                continue
        
        return jobs

class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.linkedin.com/jobs/search"
    
    def search_jobs(self, query: str, location: str = None) -> List[Dict[str, Any]]:
        params = {
            'keywords': query,
            'location': location or '',
            'sortBy': 'DD'
        }
        
        try:
            response = self._make_request(self.base_url, params)
            return self._parse_jobs(response.text)
        except Exception as e:
            logger.error(f"Error searching jobs on LinkedIn: {str(e)}")
            return []
    
    def _parse_jobs(self, html: str) -> List[Dict[str, Any]]:
        jobs = []
        soup = BeautifulSoup(html, 'html.parser')
        
        for job in soup.find_all('div', class_='base-card'):
            try:
                jobs.append({
                    'title': job.find('h3', class_='base-search-card__title').text.strip(),
                    'company': job.find('h4', class_='base-search-card__subtitle').text.strip(),
                    'location': job.find('span', class_='job-search-card__location').text.strip(),
                    'description': job.find('p', class_='base-search-card__metadata').text.strip(),
                    'url': job.find('a', class_='base-card__full-link')['href'],
                    'source': 'LinkedIn'
                })
            except Exception as e:
                logger.error(f"Error parsing job from LinkedIn: {str(e)}")
                continue
        
        return jobs 