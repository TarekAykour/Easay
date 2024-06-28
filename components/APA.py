import requests
from bs4 import BeautifulSoup

def url_to_apa(url):
    try:
        # Send a request to the URL
        response = requests.get(url)
        response.raise_for_status()  
        
        # Parse  HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get the title of the webpage
        title = soup.find('title').text if soup.find('title') else 'No Title Found'
        
        # Get meta tags for author and publication date if available
        author = None
        pub_date = None
        for meta in soup.find_all('meta'):
            if 'name' in meta.attrs:
                if meta.attrs['name'].lower() == 'author':
                    author = meta.attrs['content']
                elif meta.attrs['name'].lower() == 'pubdate' or meta.attrs['name'].lower() == 'date':
                    pub_date = meta.attrs['content']
        
        
        author = author if author else 'No Author Found'
        pub_date = pub_date if pub_date else 'n.d.'
        
        #  website name
        website_name = soup.find('meta', property='og:site_name')
        if website_name:
            website_name = website_name['content']
        else:
            # Extract domain as website name if og:site_name is not available
            website_name = url.split('/')[2]  
        
        # APA citation
        apa_citation = f"{author}. ({pub_date}). {title}. Retrieved from {url}"
        
        return apa_citation
    
    except requests.exceptions.RequestException as e:
        return url


