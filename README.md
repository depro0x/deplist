# deplist

**deplist** is a Python tool for domain enumeration, generating customizable wordlists and subdomains. It supports input files, subdomain permutations, and output saving, making it ideal for security researchers and penetration testers.

## Installation

Clone this repository to your local machine:
```bash
git clone https://github.com/depro0x/deplist.git
cd deplist
chmod +x deplist.py
./deplist.pu -h
```
Alternatively, you can download the `deplist.py` script and run it directly.

## Usage

Run the script from the command line with the following options:

python3 deplist.py -h

### Arguments

- `-d`, `--domain`: Specify the target domain (e.g., `domain.com`).
- `-l`, `--list`: Provide a file containing a list of subdomains.
- `-w`, `--wordlist`: Specify a wordlist for subdomain permutations.
- `-o`, `--output`: Specify an output file to save the results.
- `-dp`, `--depth`: Set the depth for subdomain permutations (1-5).
- `-m`, `--mode`: Choose between `wordlist` (to generate a wordlist) or `subdomains` (to generate subdomains).
- `-v`, `--verbose`: Enable verbose output to see the generated subdomains/wordlist on the screen.

### Example Commands

1. **Generate a wordlist:**
python deplist.py -d domain.com -l subdomains.txt -m wordlist -o wordlist.txt

2. **Generate subdomain permutations:**
python deplist.py -d domain.com -w wordlist.txt -m subdomains -o subdomains.txt

3. **Verbose output:**
python deplist.py -d domain.com -l subdomains.txt -m wordlist -v

## Contributing

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to your fork (`git push origin feature-name`).
5. Create a pull request.

## Acknowledgments

- Python’s `argparse` library for argument parsing.
- All contributors to this repository.
