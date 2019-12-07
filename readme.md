---
## Concept

This is a command-line utility to organize TODOs and priorities on a day-to-day basis.
The concept is to structure the TODOs in a TODO-DAG (or TODAG), where DAG stands for [Directed Acylic Graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph), instead of following the more common TODO-list format.

You can read more about my TODO frame-work [here.](https://raw.githubusercontent.com/SolbiatiAlessandro/TODAG/master/docs/concept.rst)

---
## Implementation
Every 'TODO' is a card, and every card has parents and children that will form the DAG. A card can be marked as done only when all the parents are also flagged as done. The language choosen for the implementation is Python, and the cards are kept in a dictionary. The dictionary is made persistent using the pickle module, and there are high-level CLI API to create and save cards. The basic use cases are to add cards, add parents cards, and run the 'TODO' routine, that consist in finding all the cards with all the parents already completed (to advance in the todo tree). 

---
## Development
The utility is developed using OOP methodologies, and adhereing to the [Google Python style-guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md), especially regarding the documentation. Is encouraged Test-Drived-Development, as the whole utility will be tested periodically using Continuous Integration practices. Up to now there is no plan in writing a external documentation as the in-code documentation should be enough.

---
## Roadmap
You can read about the roadmap of the project in the [development.md](https://github.com/SolbiatiAlessandro/TODAG/blob/master/docs/development.rst) file.

---
## Usage

If you want to run the TODAG on your local iOS machine you need to do the following.

```
[macOS]
git clone https://github.com/SolbiatiAlessandro/TODAG
cd TODAG
virtualenv venv -p python3
source venv/bin/activate
(venv) pip install -r requirements.txt
``` 

```
[windows]
[macOS]
git clone https://github.com/SolbiatiAlessandro/TODAG
cd TODAG
virtualenv venv -p python3
venv\scripts\activate.bat
(venv) pip install -r requirements.txt
```

Inside the bin folder there are the two scripts to use the TODAG:
- **open.py**: create new todos in the DAG, delete or print the DAG
```
(venv) python bin/open.py
```

- **todo.py**: traverse the DAG and print the todos with highest priority (the roots), and for every todo print the connected components it belongs to
```
(venv) python bin/todo.py
```
For more detail on the usage of bin commands you can check the in-code docs

---
## [REQUIRED] Setup interaction with Google Cloud Storage

To enable interaction with Google Cloud Storage you need to 
1. set up your own bucket on [GCS](https://cloud.google.com/)
2. create a `config.init` file from `config.example`, and modify line `bucketid = your_bucket_id`
3. download your access key and store it in root folder (folder where README.md resides) as gcskey.json, to get your key you need to navigate inside GCP console -> IAM & Admin -> Service Accounts -> Create Key -> Download Key as JSON.

<b>IMPORTANT</b>: save it with the name `gcskey.json` (or modify `.gitignore`) otherwise it will be committed on the public repo and hackerbot will penetrate the cloud account in minutes.

---
## [OPTIONAL] Setup geolocalization for your local machine

To enable geolocalization for your local machine you need to
1. Download the objective-C tool [WhereAmI](https://github.com/robmathers/WhereAmI) from [this link](https://github.com/robmathers/WhereAmI/releases/download/v1.02/whereami-1.02.zip)
2. Create a `config.init` file from like `config.example`, modify line `whereami = your_path_to_whereami_here`


---
## [OPTIONAL] Setup termwdown on your localmachine

`todo.py` will automatically start a [termdown](https://github.com/trehn/termdown) session on your local machine for you to keep track of the time spent on your task. To enable it you need to install it **outside the virutal environment** with:

```
pip install termdown
```


---
## Dashboards

TODAG is plugged in into the Google Cloud Storage environment. There are some dynamic dashboards updated in real time with the metrics coming from TODAG, NOTE: you need to be granted access.
- Dashboard end-point: https://datastudio.google.com/open/1XemSx8qknY35rjlHnehxefj2178omHSn

Here is a preview of the dashboard
![alt text](https://github.com/SolbiatiAlessandro/TODAG/blob/master/dashboard.png?raw=true)
