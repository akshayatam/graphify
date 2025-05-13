# wiki_fetch.py 
# This script fetches the content of a Wikipedia page and saves it to a file. 
import os 
import argparse 
import re 
import wikipedia as wiki 

RAW_DIR = "pages/raw" 
CLEAN_DIR = "pages/clean" 

os.makedirs(RAW_DIR, exist_ok=True) 
os.makedirs(CLEAN_DIR, exist_ok=True) 

def fetch_wikipedia_page(title: str) -> str: 
    """
    Fetches the content of a Wikipedia page by its title.
    Args:
        title (str): The title of the Wikipedia page to fetch.
    Returns:
        str: The content of the Wikipedia page.
    """
    wiki.set_lang("en") 

    try: 
        page = wiki.page(title) 
        return page.content 
    except wiki.exceptions.DisambiguationError as e: 
        print(f"Disambiguation error: {e}. Please specify a more specific title.") 
    except wiki.exceptions.PageError as e: 
        print(f"Page error: {e}. The page does not exist.") 
    return "" 

def clean_wikipedia_page(text: str) -> str: 
    """
    Cleans the content of a Wikipedia page by removing references and formatting.
    Args:
        text (str): The raw content of the Wikipedia page.
    Returns:
        str: The cleaned content of the Wikipedia page.
    """
    text = text.lower().replace('\n', ' ')
    text = re.sub(r'== see also ==.*|[@#:&\"]|===.*?===|==.*?==|\(.*?\)', '', text)
    return text.strip() 

def save_to_file(filename: str, content: str): 
    """
    Saves the content to a file.
    Args:
        filename (str): The name of the file to save the content to.
        content (str): The content to save.
    """
    with open(filename, 'w', encoding='utf-8') as f: 
        f.write(content)

def main(): 
    parser = argparse.ArgumentParser(description="Fetch and clean Wikipedia pages.") 
    parser.add_argument("title", type=str, help="The title of the Wikipedia page to fetch.") 
    args = parser.parse_args() 

    raw_text = fetch_wikipedia_page(args.title) 
    if not raw_text: 
        print("Failed to fetch the page.") 
        return 
    
    clean_text = clean_wikipedia_page(raw_text) 

    raw_path = os.path.join(RAW_DIR, f"{args.title.replace(' ', '_')}.txt") 
    clean_path = os.path.join(CLEAN_DIR, f"{args.title.replace(' ', '_')}.txt") 

    save_to_file(raw_path, raw_text) 
    save_to_file(clean_path, clean_text) 

    print(f"Raw content saved to {raw_path}") 
    print(f"Clean content saved to {clean_path}") 

if __name__ == "__main__": 
    main() 