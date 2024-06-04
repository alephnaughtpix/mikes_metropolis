import os
import os.path
import re
from bs4 import BeautifulSoup, Comment
import data_url

SOURCE_DIR = '../source/'
DEST_DIR = '../dest/'
EXTERNAL_FILES = {}
file_match = r'\/web\/\w+\/http:\/\/grelb\.src\.gla\.ac\.uk:8000\/~mjames\/'

def add_external_file(element, data, original_url):
    
    if original_url not in EXTERNAL_FILES:
        file_name = re.sub(file_match, '', original_url)
        if file_name.startswith('http') or file_name.startswith('/web'):
            return
        EXTERNAL_FILES[original_url] = file_name
        file_path = os.path.join(DEST_DIR, os.path.dirname(file_name))
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        full_file_path = os.path.join(DEST_DIR, file_name)
        full_url = '{{ "/' + file_name + '" | relative_url }}'
        try:
            img = data_url.DataURL.from_url(data)
            with open(full_file_path, 'wb') as f:
                f.write(img.data)
        except Exception as e:
            print('ERROR:', e)
    else:
        full_file_path = EXTERNAL_FILES[original_url]
        full_url = '{{ "/' + full_file_path + '" | relative_url }}'
    if element.name == 'img':
        element['src'] = full_url
        del element['data-savepage-src']
    if element.name == 'body':
        element['background'] = full_url
        del element['data-savepage-background']
        
        
        
# EXTRACT IMAGES
def extract_images(body):
    if body.has_attr('background'):
        add_external_file(body, body['background'], body['data-savepage-background'])
    all_images = body.find_all('img')
    for image in all_images:
        if image.has_attr('src'):
            add_external_file(image, image['src'], image['data-savepage-src'])
    return body

# REMOVE WAYBACK MACHINE CONTENT
def remove_wayback(body):
    # REMOVE TOOLBAR AND COMMENTS
    for comment in body.findAll(text=lambda str:isinstance(str, Comment)):
        if comment in [' BEGIN WAYBACK TOOLBAR INSERT ', ' END WAYBACK TOOLBAR INSERT ']:
            remove_elements = []
            # If the comment is the end of the wayback toolbar insert, remove all elements until the BODY tag
            if comment == ' END WAYBACK TOOLBAR INSERT ':
                element = comment.previous_element
                while element is not None:
                    remove_elements.append(element)
                    element = element.previous_element
                    if element.name is not None:
                        if element.name == 'body':
                            comment.extract()
                            break
            # If the comment is the beginning of the wayback toolbar insert, remove all elements until the end comment
            else:
                element = comment.next_element
                while element is not None:
                    remove_elements.append(element)
                    element = element.next_element
                    if isinstance(element, Comment):
                        if element == ' END WAYBACK TOOLBAR INSERT ':
                            element.extract()
                            comment.extract()
                            break
            for element in remove_elements:
                if element.name is not None:
                    element.decompose()
        # Remove comments at the end of the page
        if 'FILE ARCHIVED ON' in comment:
            comment.extract()  
        if 'playback timings' in comment:
            comment.extract()
            
    # ALTER LOCAL LINKS
    all_links = body.find_all('a')
    for link in all_links:
        if link.has_attr('data-savepage-href'):             # The original local link is stored in this attribute
            link_href = link['data-savepage-href']
            if not link_href.startswith('http'):
                link['href'] = link_href                    # Replace the href with the original local link
                del link['data-savepage-href']              # Remove the data-savepage-href attribute
                 
    return body

def process_file(file_source_dir, file_dest_dir, file):
    if file.endswith('.html'):
        source_file_path = os.path.join(file_source_dir, file)
        dest_file_path = os.path.join(file_dest_dir, file)
        with open(source_file_path, 'r') as f:
            content = f.read()
            html_parser = BeautifulSoup(content, 'html.parser')
            iframes = html_parser.find_all('iframe')
            if len(iframes) == 2:
                iframe = iframes[1]['srcdoc']
                iframe_parser = BeautifulSoup(iframe, 'html.parser')
                title = iframe_parser.title.string
                meta_tags = iframe_parser.find_all('meta')
                body = iframe_parser.body
                #print('meta_tags', meta_tags)
            else:
                #print('NOPE!')
                iframe = None
                title = html_parser.title.string
                meta_tags = []
                body = html_parser.body
            print('file:', source_file_path, '-> dest:', dest_file_path)
            body = remove_wayback(body)
            body = extract_images(body)
            body = remove_data(body)
            all_meta_tags = ''
            for meta_tag in meta_tags:
                meta_tag_string = meta_tag.string
                if meta_tag_string:
                    all_meta_tags = meta_tag_string + '\n'
            if not os.path.exists(file_dest_dir):
                os.makedirs(file_dest_dir)
            with open(dest_file_path, 'w') as f:
                output_file= f'''---
---
<html>
<head>
<title>{title}</title>
{all_meta_tags}</head>
{body}</html>
'''
                f.write(output_file)

 # REMOVE ALL DATA ATTRIBUTES              
def remove_data(body):
    tags = body.parent.find_all(True)
    for tag in tags:
        attrs = dict(tag.attrs)
        for attribute in attrs:
            if attribute.startswith('data-'):
                del tag[attribute]
    return body

# MAIN
if not os.path.exists(DEST_DIR):
    os.makedirs(DEST_DIR)
for root, dirs, files in os.walk(SOURCE_DIR):
    file_dest_dir = root.replace(SOURCE_DIR, DEST_DIR)
    for file in files:
        process_file(root, file_dest_dir, file)
