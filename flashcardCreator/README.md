# About the project

This tool will help you learn Bulgarian more efficiently saving you time and effort. It only generates flashcards for the irregular forms of the words.

## Goals and Motivation

- To provide a tool to learn the complexity of the Bulgarian verbs focussing on the irregular ones
- To allow any person to learn Bulgarian with their own handpicked vocabulary

## Advantages

You can study your own vocabulary with your own English translations using [Ankiweb](https://ankiweb.net/). You can focus on only learning the irregular forms of the nouns, adjectives, adverbs and verbs.

## Features

* Generates flashcards for your own vocabulary. You can choose what words are important for you
* It generates additional flashcards for the irregular forms of the word
* Searches for the translation in English on [DeepL](https://www.deepl.com/translator) and [PONS's online dictionary](https://en.pons.com/translate/bulgarian-english/) and you can modify and extend those translations
* Stores the flashcards in a database which you can modify manually using the [SQLite Database Browser](https://sqlitebrowser.org/)

## Limitations

* Only irregular forms which are in the [grammar dictionary](https://rechnik.chitanka.info/w) are identified
* You have to enter your own vocabulary. If you want to spare time by using my flashcards, you can use [Ankiweb's decks with Bulgarian vocabulary](https://ankiweb.net/shared/decks?search=bulgarian)

# Getting stated

## Installation

On the terminal window, create a virtual environment and install the dependencies:

```bash
cd flashcardCreator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Please run the script installDictionary.py to create a local copy of the grammatical classification of the words:

```bash
python installDictionary.py
```

## Configuration

Create a new configuration file based on the template. You need to enter your DeepL API key to be able to search for translations in English.
```
cp apiKeys.ini.template apiKeys.ini
```

## Usage

Now you are ready to create your own flashcards. 

### Add one work at the type

```
python start.py -v -a
```

TODO Add use cases using a list of words from a file, a single word from the command line, and adding multiple words interactively

```
cp apiKeys.ini.template apiKeys.ini
```

# Help

## FAQ

* Is is possible to use other translation services or online dictionaries?

Yes, please create a feature request explaining what are the advantages over DeepL and PONS. If I have time, I will do the connection

* What is imported if a verb has a participle with multiple derivative forms like 'завалял'?

When having something like:
```
{'мин.деят.св.прич. м.р.': 'завалял', 
    'мин.деят.св.прич. мн.ч.': 'завалели', 
    'мин.деят.несв.прич. м.р.': 'завалял'}
```
The duplicated participles are combined and imported like this:
![particles With Multiple Derivate Forms Combination.jpg](docs/img/particlesWithMultipleDerivateFormsCombination.jpg)

## Troubleshooting

TODO To complete this section

## How to report a bug

TODO To complete this section

# Get involved

TODO To complete this section

# How to contribute

TODO To complete this section

# How to regerate the dependencies file

If you add new dependencies to the project, please regenerate the requirements.txt file using pip freeze:

```bash
pip freeze > requirements.txt
```