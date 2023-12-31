from colorama import Fore, init
import os
import argparse
import requests
from bs4 import BeautifulSoup

# Initialize colorama
init()

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('directory')
args = parser.parse_args()

# Create the directory if it doesn't exist
os.makedirs(args.directory, exist_ok=True)

visited_files = []


def print_and_save(url, file_name):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    content = ''

    for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']:
        elements = soup.find_all(tag)
        for element in elements:
            if tag == 'a':
                text = Fore.BLUE + element.get_text(strip=True) + Fore.RESET
            else:
                # Preserve the spaces around each word
                text = element.get_text()

            content += text + '\n'
    print(content)

    # Save content to file
    with open(f'{args.directory}/{file_name}', 'w') as file:
        visited_files.append(file_name)
        file.write(content)


def get_url():
    global visited_files
    while True:
        user_input = input()

        if user_input in visited_files:
            with open(f'{args.directory}/{user_input}', 'r') as file:
                print(file.read())
        elif '.' in user_input:
            file_name, xtra = user_input.split('.', 1)
            if 'https://' not in user_input:
                user_input = 'https://' + user_input
            r = requests.get(user_input)
            if r.status_code == 200:
                print_and_save(user_input, file_name)
            continue
        elif user_input == 'exit':
            break
        elif user_input == 'back':
            if len(visited_files) != 0:
                visited_files.pop()
                with open(f'{args.directory}/{visited_files[-1]}', 'r') as file:
                    print(file.read())
                continue
            else:
                continue
        else:
            print('Invalid URL')


get_url()
