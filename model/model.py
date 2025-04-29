import copy
from functools import lru_cache

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self.nOpzioni = 0
        self.nClientiMax = 0
        self.soluzioneOttima = []
        self.nOreOttima = 0

    def worstCase(self, nerc, maxY, maxH):
        self.ricorsione([], maxY, maxH, nerc)
        return self.soluzioneOttima, self.nClientiMax, self.nOreOttima

    def calcolaMinimo(self, parziale):
        min = 9999
        for evento in parziale:
            if evento.date_event_began.year < min:
                min = evento.date_event_began.year
        return min

    def calcolaMassimo(self, parziale):
        max = 0
        for evento in parziale:
            if evento.date_event_began.year > max:
                max = evento.date_event_began.year
        return max

    def calcolaOre(self, parziale):
        n = 0
        for evento in parziale:
            n += evento.nOre
        return n

    def loadPossibili(self, parziale, maxH, maxY, nerc):
        sommaOre = 0
        possibili = []

        for evento in parziale:
            sommaOre += evento.nOre
        for event in self.loadEvents(nerc):
            if event not in parziale:
                if (event.nOre + sommaOre) < int(maxH):
                    minimo = self.calcolaMinimo(parziale)
                    massimo = self.calcolaMassimo(parziale)
                    if (event.date_event_began.year - minimo) <= int(maxY):
                        if (massimo - event.date_event_began.year) <= int(maxY):
                            possibili.append(event)

        return possibili

    def calcolaClienti(self, parziale):
        n = 0
        for evento in parziale:
            n += evento._customers_affected
        return n

    def ricorsione(self, parziale, maxY, maxH, nerc):
        if len(self.loadPossibili(parziale, maxH, maxY, nerc)) == 0:
            self.nOpzioni += 1
            numeroClienti = self.calcolaClienti(parziale)
            print(parziale)
            if numeroClienti > self.nClientiMax:
                self.nClientiMax = numeroClienti
                self.soluzioneOttima = copy.deepcopy(parziale)
                self.nOreOttima = self.calcolaOre(parziale)
                #print(self.soluzioneOttima, self.nClientiMax, self.nOreOttima)
        else:
            for event in self.loadPossibili(parziale, maxH, maxY, nerc):
                if len(parziale) != 0:
                    if event.id > parziale[-1].id:
                        parziale.append(event)
                        self.ricorsione(parziale, maxY, maxH, nerc)
                        parziale.pop()
                else:
                    parziale.append(event)
                    self.ricorsione(parziale, maxY, maxH, nerc)
                    parziale.pop()

        return self.soluzioneOttima, self.nClientiMax

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)
        return self._listEvents

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()
        return self._listNerc


    @property
    def listNerc(self):
        return self._listNerc