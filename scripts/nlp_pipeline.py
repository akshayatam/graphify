# nlp_pipeline.py 
# This script processes the content of a Wikipedia page using a natural language processing (NLP) pipeline. 
import spacy 
import coreferee 
from pathlib import Path 

def load_pipeline(mode: str = "en_core_web_lg") -> spacy.Language:
    """
    Load the spaCy NLP pipeline.
    Args:
        mode (str): The name of the spaCy model to load.
    Returns:
        spacy.Language: The loaded spaCy NLP pipeline.
    """
    nlp = spacy.load(mode) 
    
    if not nlp.has_pipe("coreferee"):
        nlp.add_pipe("coreferee")
    return nlp 

def resolve_coreferences(doc: spacy.tokens.Doc) -> str:
    """
    Resolve coreferences in the document.
    Args:
        doc (spacy.tokens.Doc): The spaCy document to process.
    Returns:
        str: The processed text with resolved coreferences.
    """
    resolved_text = "" 

    for token in doc: 
        resolved_coref = doc._.coref_chains.resolve(token)
        if token._.coref_chains:
            resolved_text += " " + " and ".join(r.text for r in resolved_coref) 
        else:
            rresolved_text += " " + token.text 

    return resolved_text.strip() 

def process_text_file(input_path: Path) -> str:
    """
    Process a text file using the NLP pipeline.
    Args:
        input_path (Path): The path to the input text file.
    Returns:
        str: The processed text with resolved coreferences.
    """
    with open(input_path, 'r', encoding='utf-8') as f: 
        return f.read() 
    
def save_resolved_text(output_path: Path, resolved_text: str): 
    """
    Save the resolved text to a file.
    Args:
        output_path (Path): The path to the output text file.
        resolved_text (str): The resolved text to save.
    """ 
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f: 
        f.write(resolved_text) 

if __name__ == "__main__": 
    # Example usage 
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to cleaned input .txt file")
    parser.add_argument("--output", required=True, help="Path to save resolved text")
    args = parser.parse_args()

    nlp = load_pipeline()
    raw_text = process_text_file(Path(args.input))
    doc = nlp(raw_text)
    resolved = resolve_coreferences(doc)
    save_resolved_text(resolved, Path(args.output))

    print(f"Resolved coreference text saved to {args.output}")