import re
import binascii
from PIL import Image
from docx import Document



def is_image(file_path):
    try:
        with Image.open(file_path) as img:
            print(img.format, img.size, img.mode)
            return True
    except IOError:
        return False

"""
Read .rtf file and return its content, title, and URLs
Using regex to extract title, paragraphs, and URLs
"""
def read_rtf(path):
    title = None
    paragraphs = []
    urls = []
    image_filenames = []

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

        
        # Extract Image
        image_matches = re.findall(r'\\pard\\sa200\\sl240\\slmult1{\\pict{\\*\\picprop}.*?\\wmetafile8.*?[\r\n]+(.*?)\s*}', content, re.DOTALL)
        print('images', image_matches)
        for i, image_match in enumerate(image_matches, 1):
            cleaned_image_data = re.sub(r'[^a-fA-F0-9]', '', image_match)
            if cleaned_image_data:
                try:
                    image_data = binascii.unhexlify(cleaned_image_data)
                    image_filename = f'extracted_image_{i}.png'  # Assuming WMF format as per \wmetafile8
                    with open(image_filename, 'wb') as img_file:
                        img_file.write(image_data)
                    paragraphs.append(f'[IMAGE: {image_filename}]')
                    image_filenames.append(image_filename)
                except binascii.Error:
                    print('Error: Invalid image data')
        # Extract title
        title_match = re.search(r'\\fs(2[6-9]|3[0-9]|4[0-8]|5[0-6])\\lang19 (.+?)\\par', content)
        if title_match:
            title = re.sub(r'\\[a-z]+\d*', '', title_match.group(2)).strip()
        
        # Extract all non-empty paragraphs
        raw_paragraphs = re.findall(r'\\par\s*(.+?)(?=\\par)', content)
        for match in raw_paragraphs:
            cleaned_match = match.replace('}}}', '')
            cleaned_match = re.sub(r'\\pard\\sa200\\sl276\\slmult1\\par', '', cleaned_match)
            text = re.sub(r'\\[a-z]+\d*|{\*\[^}]+}|{[^}]+}', '', cleaned_match).strip()
            if text:
                to_replace = ['}', 'URL', 'Links', 'url', 'Url', 'links', 'URLS', 'urls', 'Urls', 'URLs', 'URls', 'urlS', r'd\{title\}']
                pattern = '|'.join(re.escape(sub) for sub in to_replace)
                cleaned_text = re.sub(pattern, ' ', text)
                url_in_paragraphs = any("URL" in paragraph for paragraph in paragraphs)
                links_in_paragraphs = any("Links" in paragraph for paragraph in paragraphs)
                if "URL" in cleaned_text and not url_in_paragraphs:
                    paragraphs.append(cleaned_text)
                elif "Links" in cleaned_text and not links_in_paragraphs:
                    paragraphs.append(cleaned_text)
                else:
                    paragraphs.append(cleaned_text)
        
        # Extract URLs
        url_matches = re.findall(r'\\fldinst{HYPERLINK\s+([^}]+)}', content)
        for match in url_matches:
            url = match.strip().strip('"')
            urls.append(url)
    
    return title, paragraphs, urls, image_filenames


"""
reading docx file and return its content, title, and URLs
"""
def read_doc(path):
    doc = Document(path)
    title = doc.core_properties.title
    
    paragraphs = [p.text for p in doc.paragraphs]
    
    urls = []
    for rel in doc.part.rels.values():
        if "hyperlink" in rel.reltype:
            urls.append(rel.target_ref)
    
    return title, paragraphs, urls
