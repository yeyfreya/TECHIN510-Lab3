# TECHIN 510 Lab 3
Freya Yu 2372732

Data storage and retrieval using Python.

To Do List App Link: https://yeyfreya-techin510-lab3.azurewebsites.net/ 

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## Lessions Learned

1. SQLite language and commands
2. Streamlit App coding and debugging
3. When tried to add new functions, encountered the following errors:
- sqlite3.ProgrammingError: You can only execute one statement at a time.
- sqlite3.OperationalError: table tasks already exists
- sqlite3.OperationalError: no such column: state
- sqlite3.OperationalError: table tasks has no column named state
- sqlite3.OperationalError: table tasks has no column named created_at
- sqlite3.OperationalError: table tasks has no column named created_by
- sqlite3.OperationalError: table tasks has no column named category
- ValueError: 'state' is not in list
- No instant display after applying filter function

## Questions

Even though I completed the lab and made the Todo App functioning, I still feel like chaotic and not sure what is the problem (like the filter display). Is there any way that I can have a more systematic knowledge structure along with this lab practice?   
