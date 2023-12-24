import requests, os, time, pdfkit
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from colorama import Fore


class Scraper:


    def __init__(self):

        ua = UserAgent()
        
        self.headers = {}
   
        self.cookies = {}


    # Function to scrape all of the main links 
    def getLinks(self):

        url = ''

        try:
            
            response = requests.get(link, headers=self.headers, cookies=self.cookies) 
            
            soup = BeautifulSoup(response.text, 'html.parser')
        
        except Exception as e:
            
            print(f"Error occurred while requesting data: {e}")

        containerDiv = soup.find('div', class_='') # Div containing all element data
        
        targetDivs = containerDiv.find_all('') # Target element that contains data

        links = []

        for aTag in targetDivs: # Iterate through each element searching for data (in this case, a link)

            link = aTag.find('a')
            
            href = link.get('href')

            links.append(href)

            print('.', end='', flush=True) # Using '.' flush print as a metric tool in the terminal

        return links # Return list of links to iterate through in main function
    

    # Function to scrape sub links (if necessary) from each main link
    def getSubLinks(self, link):

        # Same process as getLinks function except we are scraping through a list of links 
        # and adding a baseURL to search for more data (for this case, links)

        baseUrl = ''

        try:
            
            response = requests.get(baseUrl + link, headers=self.headers, cookies=self.cookies) 
            
            soup = BeautifulSoup(response.text, 'html.parser')
        
        except Exception as e:
            
            print(f"Error occurred while requesting data: {e}")

        containerDiv = soup.find('div', class_='')

        targetDivs = containerDiv.find_all('', class_='')

        links = []

        for aTag in targetDivs:

            link = aTag.find('a')
            
            href = link.get('href')
            
            href = baseUrl + href

            links.append(href)

            print('.', end='', flush=True)

        return links
    

    # Helper function
    def sanitize_filename(self, filename):
        
        illegal_chars = r'\/:*?"<>|' # The OS will not allow these types of characters in the filename so we must remove them
        
        for char in illegal_chars:
            filename = filename.replace(char, '_')
        
        return filename


    # Function to scrape data from each sub link
    def fetch(self, link):
        
        if not os.path.exists('./output'):
            os.makedirs('./output')

        title = link.split('/')[-1]
        
        sanitizedTitle = self.sanitize_filename(title)

        try: 
            pdfkit.from_url(link, os.path.join('./output/' + sanitizedTitle + '.pdf'))
        
            print(f"\n{Fore.GREEN}Downloaded {link} {Fore.RESET}", end='', flush=True)
        
        except Exception as e:
            
            print(f"\n{Fore.RED}Error when scraping {link}: {e}{Fore.RESET}", end='', flush=True)


    # Main function
    def main(self):
        
        startTime = time.time()

        # --------------------

        links = self.getLinks()

        subLinks = []
        
        for link in links:
            subLinks.extend(self.getSubLinks(link)) # Can add threading support here

        # Multi-processing support
        with Pool(processes=20) as p:
            p.map(self.fetch, subLinks)

        # --------------------

        # Measuring time taken in order to account for optimization issues
        print('\n\tTotal time taken:', time.time() - startTime)
    

if __name__ == "__main__":
    
    scraper = Scraper()   
    
    scraper.main()

