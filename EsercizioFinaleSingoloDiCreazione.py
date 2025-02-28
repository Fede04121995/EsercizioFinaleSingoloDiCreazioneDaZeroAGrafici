import random
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#GENERA DATI CASUALI DA AGGIUNGERE IN DATABASE

# Funzione per creare la tabella se non esiste
def crea_tabella():
    # Connessione al database (crea automaticamente il file se non esiste)
    conn = sqlite3.connect('cioccolato.db')  # Usa un percorso relativo o assoluto
    cursor = conn.cursor()
    
    # Creazione della tabella se non esiste
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cioccolato (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        cacao_percentuale REAL,
        peso REAL,
        prezzo REAL,
        unita_vendute INTEGER,
        valutazione REAL
    )
    """)
    
    # Commit e chiusura della connessione
    conn.commit()
    print("Tabella creata o già esistente.")
    conn.close()

# Funzione per creare dati randomici
def inserisci_dati_randomici():
    # Dati casuali
    tipi_cioccolato = ['Fondente', 'Latte', 'Bianco', 'Ruby']
    
    tipo = random.choice(tipi_cioccolato)  # Tipo di cioccolato
    cacao = random.randint(30, 90)  # Percentuale di cacao tra 30 e 90
    peso = random.choice([100, 150, 200, 250])  # Peso casuale della tavoletta (100g, 150g, 200g, 250g)
    prezzo = round(random.uniform(2.5, 6.5), 2)  # Prezzo casuale tra 2.5€ e 6.5€
    unita_vendute = random.randint(50, 500)  # Unità vendute casuali tra 50 e 500
    valutazione = random.randint(1, 5)  # Valutazione casuale tra 1 e 5
    
    # Connessione al database e inserimento dei dati casuali
    conn = sqlite3.connect('cioccolato.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO cioccolato (tipo, cacao_percentuale, peso, prezzo, unita_vendute, valutazione)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (tipo, cacao, peso, prezzo, unita_vendute, valutazione))
    
    conn.commit()
    print(f"Dati inseriti: {tipo}, {cacao}% cacao, {peso}g, €{prezzo}, {unita_vendute} unità, valutazione {valutazione}")
    conn.close()

# Funzione per inserire n dati casuali
def inserisci_n_dati_randomici(n):
    for _ in range(n):
        inserisci_dati_randomici()

# Crea la tabella (il database verrà creato automaticamente se non esiste)
crea_tabella()

# Inserisci 10 dati casuali
inserisci_n_dati_randomici(10)


#2. Visualizzazione dei dati nel DataFrame
#Dopo aver inserito i dati nel database, puoi esportarli in un file CSV e caricarli in un DataFrame Pandas per l'analisi.

# Carica i dati dal database in un DataFrame
def carica_dati():
    conn = sqlite3.connect('cioccolato.db')
    df = pd.read_sql_query("SELECT * FROM cioccolato", conn)
    conn.close()
    return df

# Carica e visualizza i primi 5 record
df = carica_dati()
print(df.head())


# 3.Analisi e grafici

# Analisi descrittiva
print(df.info())
print(df.describe())



# Grafico delle vendite per tipo di cioccolato
plt.figure(figsize=(10,6))
sns.barplot(x='tipo', y='unita_vendute', data=df)
plt.title('Vendite per tipo di cioccolato')
plt.show()
