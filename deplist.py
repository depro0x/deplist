#!/usr/bin/env python3
import argparse
from urllib.parse import urlparse, parse_qs
import requests
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="deplist - A tool to generate wordlist.",
        epilog="For more information, visit https://github.com/depro0x/deplist"
    )
    parser.add_argument(
        "-d", "--domain",
        type=str,
        metavar="domain.com",
        help="Specify the target domain.",
        required=False
    )
    parser.add_argument(
        "-l", "--list",
        type=argparse.FileType('r'),
        metavar="file.txt",
        help="Specify an input file to read.",
        required=False
    )
    parser.add_argument(
        "-w", "--wordlist",
        type=argparse.FileType('r'),
        metavar="wordlist.txt",
        help="Specify the wordlist for subdomain permutation.",
        required=False
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        metavar="output.txt",
        help="Specify the output file to save the results.",
        required=False
    )
    parser.add_argument(
        "-dp", "--depth",
        type=int,
        help="Choose the level (1-5).",
        required=False
    )
    parser.add_argument(
        "-m", "--mode",
        type=str,
        choices=["wordlist", "subdomains"],
        help="Choose the mode of operation (wordlist, subdomains).",
        required=False
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )
    parser.add_argument(
        "-dw", "--downloadwordlist",
        type=str,
        help="Download a wordlist like all.txt",
        required=False
    )
    parser.add_argument(
        "-sw", "--showwordlists",
        action="store_true",
        help="List available wordlists."
    )

    return parser.parse_args()

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    return lines    

def save_output(output, file_path):
    try:
        with open(file_path, "w") as file:
            for item in output:
                file.write(f"{item}\n")
        print(f"Output successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the output: {e}")

def verbose_output(output):
    for item in output:
        print(f"{item}")

def subdomain_to_wordlist(input_data):
    wordlist = set()

    def extract_words(data):
        if "://" in data:
            parsed_url = urlparse(data)
            domain_parts = parsed_url.netloc.split(".")
            path_parts = parsed_url.path.strip("/").split("/")

            query_parts = []
            if parsed_url.query:
                query_parts = [k for k in parse_qs(parsed_url.query).keys()]

            return domain_parts + path_parts + query_parts
        else:
            return data.split(".")
    for item in input_data:
        wordlist.update(extract_words(item))

    return list(set(wordlist))

def generate_subdomain_permutations(wordlist, domain, depth=3):
    permutations = []
    
    for word in wordlist:
        subdomain = f"{word}.{domain}"
        permutations.append(subdomain)
    
    for _ in range(depth - 1):
        new_permutations = []
        for word in wordlist:
            for perm in permutations:
                subdomain = f"{word}.{perm}"
                new_permutations.append(subdomain)
        permutations.extend(new_permutations)

    return permutations

def show_wordlists():
    print("Available wordlists:")
    for wordlist_name in wordlists_dict:
        print(f"- {wordlist_name}")

def download_wordlist(wordlist_name):
    if wordlist_name in wordlists_dict:
        url = wordlists_dict[wordlist_name]
        try:
            with requests.get(url, stream=True) as response:
                if response.status_code == 200:
                    total_size = int(response.headers.get('Content-Length', 0))
                    wordlist = []
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading {wordlist_name}") as pbar:
                        for chunk in response.iter_content(chunk_size=1024):
                            wordlist.extend(chunk.decode().splitlines())
                            pbar.update(len(chunk))
                    return wordlist
                else:
                    print(f"Failed to download the wordlist '{wordlist_name}'. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occured: {e}")
    else:
        print(f"Wordlist '{wordlist_name}' not found.")
    return []

wordlists_dict = {
    "all.txt": "https://gist.githubusercontent.com/jhaddix/86a06c5dc309d08580a018c66354a056/raw/96f4e51d96b2203f19f6381c8c545b278eaa0837/all.txt",
    "common.txt": "https://raw.githubusercontent.com/v0re/dirb/refs/heads/master/wordlists/common.txt",
    "raft-large-words.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/raft-large-words.txt",
    "big.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/big.txt",
}

if __name__ == "__main__":
    args = parse_arguments()

    if args.mode == "wordlist":
        lines = read_file(args.list.name) if args.list else []
        wordlist = subdomain_to_wordlist(lines)
        print(f"Generated {len(wordlist)} words from subdomains.")

        if args.output:
            save_output(wordlist, args.output)
        if args.verbose:
            verbose_output(wordlist)

    elif args.mode == "subdomains":
        if not args.domain:
            print("Error: Domain is required.")
            exit(1)

        if args.list:
            lines = read_file(args.list.name)
            wordlist = subdomain_to_wordlist(lines)
        elif args.wordlist:
            wordlist = read_file(args.wordlist.name)
        else:
            print("Error: Please specify an input file for subdomain generation.")
            exit(1)
        
        depth = args.depth if args.depth else 3
        permutated_subdomains = generate_subdomain_permutations(wordlist, args.domain, depth)

        if args.output:
            save_output(permutated_subdomains, args.output)
        elif args.verbose:
            verbose_output(permutated_subdomains)
        else:
            print("Please specify an output file or enable verbose mode.")

    elif args.downloadwordlist:
        wordlist_content = download_wordlist(args.downloadwordlist)
        if args.output:
            save_output(wordlist_content, args.output)
        elif args.verbose:
            verbose_output(wordlist_content)
        else:
            print("Please specify an output file or enable verbose mode.")

    elif args.showwordlists:
        show_wordlists()
        exit(0)#!/usr/bin/env python3
import argparse
from urllib.parse import urlparse, parse_qs
import requests
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="deplist - A tool to generate wordlist.",
        epilog="For more information, visit https://github.com/depro0x/deplist"
    )
    parser.add_argument(
        "-d", "--domain",
        type=str,
        metavar="domain.com",
        help="Specify the target domain.",
        required=False
    )
    parser.add_argument(
        "-l", "--list",
        type=argparse.FileType('r'),
        metavar="file.txt",
        help="Specify an input file to read.",
        required=False
    )
    parser.add_argument(
        "-w", "--wordlist",
        type=argparse.FileType('r'),
        metavar="wordlist.txt",
        help="Specify the wordlist for subdomain permutation.",
        required=False
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        metavar="output.txt",
        help="Specify the output file to save the results.",
        required=False
    )
    parser.add_argument(
        "-dp", "--depth",
        type=int,
        help="Choose the level (1-5).",
        required=False
    )
    parser.add_argument(
        "-m", "--mode",
        type=str,
        choices=["wordlist", "subdomains"],
        help="Choose the mode of operation (wordlist, subdomains).",
        required=False
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )
    parser.add_argument(
        "-dw", "--downloadwordlist",
        type=str,
        help="Download a wordlist like all.txt",
        required=False
    )
    parser.add_argument(
        "-sw", "--showwordlists",
        action="store_true",
        help="List available wordlists."
    )

    return parser.parse_args()

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    return lines    

def save_output(output, file_path):
    try:
        with open(file_path, "w") as file:
            for item in output:
                file.write(f"{item}\n")
        print(f"Output successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the output: {e}")

def verbose_output(output):
    for item in output:
        print(f"{item}")

def subdomain_to_wordlist(input_data):
    wordlist = set()

    def extract_words(data):
        if "://" in data:
            parsed_url = urlparse(data)
            domain_parts = parsed_url.netloc.split(".")
            path_parts = parsed_url.path.strip("/").split("/")

            query_parts = []
            if parsed_url.query:
                query_parts = [k for k in parse_qs(parsed_url.query).keys()]

            return domain_parts + path_parts + query_parts
        else:
            return data.split(".")
    for item in input_data:
        wordlist.update(extract_words(item))

    return list(set(wordlist))

def generate_subdomain_permutations(wordlist, domain, depth=3):
    permutations = []
    
    for word in wordlist:
        subdomain = f"{word}.{domain}"
        permutations.append(subdomain)
    
    for _ in range(depth - 1):
        new_permutations = []
        for word in wordlist:
            for perm in permutations:
                subdomain = f"{word}.{perm}"
                new_permutations.append(subdomain)
        permutations.extend(new_permutations)

    return permutations

def show_wordlists():
    print("Available wordlists:")
    for wordlist_name in wordlists_dict:
        print(f"- {wordlist_name}")

def download_wordlist(wordlist_name):
    if wordlist_name in wordlists_dict:
        url = wordlists_dict[wordlist_name]
        try:
            with requests.get(url, stream=True) as response:
                if response.status_code == 200:
                    total_size = int(response.headers.get('Content-Length', 0))
                    wordlist = []
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading {wordlist_name}") as pbar:
                        for chunk in response.iter_content(chunk_size=1024):
                            wordlist.extend(chunk.decode().splitlines())
                            pbar.update(len(chunk))
                    return wordlist
                else:
                    print(f"Failed to download the wordlist '{wordlist_name}'. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occured: {e}")
    else:
        print(f"Wordlist '{wordlist_name}' not found.")
    return []

wordlists_dict = {
    "all.txt": "https://gist.githubusercontent.com/jhaddix/86a06c5dc309d08580a018c66354a056/raw/96f4e51d96b2203f19f6381c8c545b278eaa0837/all.txt",
    "common.txt": "https://raw.githubusercontent.com/v0re/dirb/refs/heads/master/wordlists/common.txt",
    "raft-large-words.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/raft-large-words.txt",
    "big.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/big.txt",
}

if __name__ == "__main__":
    args = parse_arguments()

    if args.mode == "wordlist":
        lines = read_file(args.list.name) if args.list else []
        wordlist = subdomain_to_wordlist(lines)
        print(f"Generated {len(wordlist)} words from subdomains.")

        if args.output:
            save_output(wordlist, args.output)
        if args.verbose:
            verbose_output(wordlist)

    elif args.mode == "subdomains":
        if not args.domain:
            print("Error: Domain is required.")
            exit(1)

        if args.list:
            lines = read_file(args.list.name)
            wordlist = subdomain_to_wordlist(lines)
        elif args.wordlist:
            wordlist = read_file(args.wordlist.name)
        else:
            print("Error: Please specify an input file for subdomain generation.")
            exit(1)
        
        depth = args.depth if args.depth else 3
        permutated_subdomains = generate_subdomain_permutations(wordlist, args.domain, depth)

        if args.output:
            save_output(permutated_subdomains, args.output)
        elif args.verbose:
            verbose_output(permutated_subdomains)
        else:
            print("Please specify an output file or enable verbose mode.")

    elif args.downloadwordlist:
        wordlist_content = download_wordlist(args.downloadwordlist)
        if args.output:
            save_output(wordlist_content, args.output)
        elif args.verbose:
            verbose_output(wordlist_content)
        else:
            print("Please specify an output file or enable verbose mode.")

    elif args.showwordlists:
        show_wordlists()
        exit(0)