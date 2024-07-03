# Shopmi Dashboard ✨

## Setup Environment - Anaconda
Tahap ini melakukan instalasi setup environment menggunakan Anaconda dengan menginstal pustaka yang ada pada file requirements.txt
```
conda create --base python=3.9
conda activate base
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
Tahap ini melakukan instalasi setup environment menggunakan terminal/Shell dengan menginstal pustaka yang ada pada file requirements.txt
```
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
Setelah melakukan instalasi setup environment, pindah lah ke direktori dashboard untuk membuka file streamlit seperti berikut.
```
cd Dashboard
streamlit run Dashboard.py
```
