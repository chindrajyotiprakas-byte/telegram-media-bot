import re
import urllib.parse
import cloudscraper
from bs4 import BeautifulSoup
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedBypasser:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def bypass_url(self, url):
        """
        Main entry point to bypass a URL.
        It identifies the domain and calls the appropriate handler.
        """
        domain = urllib.parse.urlparse(url).netloc
        
        try:
            if "mahitimanch.in" in domain:
                return self.mahitimanch_handler(url)
            else:
                return self.generic_handler(url)
        except Exception as e:
            logger.error(f"Error bypassing {url}: {e}")
            return None

    def generic_handler(self, url):
        """
        Follows standard HTTP redirects and simple JS redirects.
        """
        try:
            response = self.scraper.get(url, allow_redirects=True, timeout=15)
            # Check for window.location.href refresh (often used by google redirects etc)
            match = re.search(r'window\.location\.href\s*=\s*"(.*?)"', response.text)
            if match:
                next_url = match.group(1)
                return self.generic_handler(next_url)
            
            return response.url
        except Exception as e:
            logger.error(f"Generic handler error: {e}")
            return url

    def mahitimanch_handler(self, url):
        """
        Specific handler for mahitimanch.in
        Chain: Landing Page -> JS Redirect (Google) -> Blog Post -> Toolkitspro/Chpadblock Link -> Target
        """
        logger.info(f"Bypassing Mahitimanch: {url}")
        
        # 1. Fetch Landing Page
        response = self.scraper.get(url)
        
        # 2. Find JS Redirect to Google
        match = re.search(r'window\.location\.href\s*=\s*"(.*?)"', response.text)
        if not match:
            logger.warning("No JS redirect found on Mahitimanch landing page.")
            return self.generic_handler(url) # Fallback
            
        google_redirect_url = match.group(1)
        logger.info(f"Found Google Redirect: {google_redirect_url}")
        
        # 3. Extract the Blog Post URL from the Google Redirect
        parsed = urllib.parse.urlparse(google_redirect_url)
        query_params = urllib.parse.parse_qs(parsed.query)
        blog_url = query_params.get('url', [None])[0]
        
        if not blog_url:
            logger.warning("Could not extract blog URL from Google redirect.")
            return google_redirect_url
            
        logger.info(f"Found Blog URL: {blog_url}")
        
        # 4. Fetch the Blog Post
        response_blog = self.scraper.get(blog_url)
        soup = BeautifulSoup(response_blog.text, 'html.parser')
        
        # 5. Look for 'Toolkitspro', 'Chpadblock' or other known wrappers
        # Rule: Find external links that are NOT social media or google
        candidates = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Basic filters
            if not href.startswith('http'): continue
            if 'mahitimanch' in href: continue
            if any(x in href for x in ['google.com', 'facebook.com', 'twitter.com', 'instagram.com', 'whatsapp.com', 'telegram.org', 't.me']):
                 continue
            
            # Specific keywords (add more as discovered)
            if any(x in href for x in ['toolkitspro.com', 'chpadblock.com', 'linksly.co', 'droplink.co']):
                candidates.append(href)
                
        # 6. Check for direct Terabox links first
        terabox_links = re.findall(r'https?://(?:www\.)?(?:terabox\S+|1024terabox\S+)', response_blog.text)
        if terabox_links:
            logger.info(f"Found Direct Terabox link: {terabox_links[0]}")
            return terabox_links[0]
            
        # 7. Follow candidates if found
        if candidates:
            next_link = candidates[0] # Take the first likely candidate
            logger.info(f"Found Wrapper link: {next_link}")
            return self.generic_handler(next_link)

        logger.warning("No known target links found on blog page.")
        return blog_url

# Singleton instance
bypasser = UnifiedBypasser()
