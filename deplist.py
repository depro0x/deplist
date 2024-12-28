#!/usr/bin/env python3
import argparse

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
        required=True
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
        required=True
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
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

def subdomain_to_wordlist(subdomains, domain):
    wordlist = []
    for subdomain in subdomains:
        if domain and subdomain.endswith(f".{domain}"):
            stripped = subdomain.replace(f".{domain}", "")
            words = stripped.split(".")
            wordlist.extend(words)
        else:
            wordlist.append(subdomain)
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

if __name__ == "__main__":
    args = parse_arguments()

    if args.mode == "wordlist":
        if not args.domain:
            print("Error: Domain is required for wordlist generation.")
            exit(1)
        lines = read_file(args.list.name) if args.list else []
        wordlist = subdomain_to_wordlist(lines, args.domain)
        print(f"Generated {len(wordlist)} words from subdomains.")

        if args.output:
            save_output(wordlist, args.output)
        elif args.verbose:
            verbose_output(wordlist)

    elif args.mode == "subdomains":
        if not args.domain:
            print("Error: Domain is required.")
            exit(1)

        if args.list:
            lines = read_file(args.list.name)
            wordlist = subdomain_to_wordlist(lines, args.domain)
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
