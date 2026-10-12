import csv
from operator import attrgetter
class Strumento:
    def __init__(self, id_strumento, tipo, marca, anno_acquisto, valore):
        self.id_strumento = id_strumento
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno_acquisto)
        self.valore = float(valore)

    def __str__(self):
        return f"[{self.id_strumento}] {self.tipo} - {self.marca} ({self.anno_acquisto}) - {self.valore}"


class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"Prestito {self.id_prestito}: Strumento {self.id_strumento} {self.cognome_allievo} in data {self.data}"


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        # TODO
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = {}
        self.prestiti = {}
        self.strumenti_in_prestito = set()


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        # TODO
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for riga in reader:
                    if not riga:
                       continue
                    codice, tipo, marca, anno_acquisto, valore = riga
                    nuovo_strumento = Strumento(codice, tipo, marca, anno_acquisto, valore)
                    self.strumenti[codice] = nuovo_strumento
        except FileNotFoundError:
            raise FileNotFoundError(f"Errore: Il file '{file_path}' non è stato trovato.")

        except Exception as e:
            raise Exception(f"Errore durante la lettura del file: {e}")


    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        # TODO
        massimo = 0
        for codice in self.strumenti:
            if codice.startswith("S"):
                try:
                    num = int(codice[1:])
                    if num > massimo:
                        massimo = num
                except ValueError:
                    pass

        nuovo_codice = f"S{massimo + 1}"
        nuovo_strumento = Strumento(nuovo_codice, tipo, marca, anno_acquisto, valore)
        self.strumenti[nuovo_codice] = nuovo_strumento

        return nuovo_strumento



    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        # TODO
        return sorted(self.strumenti.values(), key=attrgetter('marca'))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # TODO
        if id_strumento not in self.strumenti:
            raise Exception(f"Errore: Lo strumento con ID '{id_strumento}' non esiste nel sistema.")
        if id_strumento in self.strumenti_in_prestito:
            raise Exception(f"Errore: Lo strumento con ID '{id_strumento}' risulta già in prestito.")

        codice_prestito = f"P{len(self.prestiti) + 1}"
        nuovo_p = Prestito(codice_prestito, data, id_strumento, cognome_allievo)
        self.prestiti[codice_prestito] = nuovo_p
        self.strumenti_in_prestito.add(id_strumento)
        return nuovo_p



    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        # TODO
        if id_prestito not in self.prestiti:
            raise Exception(f"Errore: Nessun prestito trovato con codice '{id_prestito}'.")

            # Rimuove il prestito e libera lo strumento dal set dei prestiti attivi
        prestito = self.prestiti.pop(id_prestito)
        if prestito.id_strumento in self.strumenti_in_prestito:
                self.strumenti_in_prestito.remove(prestito.id_strumento)