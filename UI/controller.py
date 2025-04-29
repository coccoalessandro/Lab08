import flet as ft
from model.nerc import Nerc



class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        self._view._txtOut.controls.clear()
        for nerc in self._model.loadNerc():
            if nerc.id == int(self._view._ddNerc.value):
                self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {self._model.worstCase(nerc, self._view._txtYears.value, self._view._txtHours.value)[1]}"))
                self._view._txtOut.controls.append(ft.Text(f"Tot hours of outage: {self._model.worstCase(nerc, self._view._txtYears.value, self._view._txtHours.value)[2]}"))
        for nerc in self._model.loadNerc():
            if nerc.id == int(self._view._ddNerc.value):
                for event in self._model.worstCase(nerc, self._view._txtYears.value, self._view._txtHours.value)[0]:
                    self._view._txtOut.controls.append(ft.Text(str(event)))

        self._view.update_page()


    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(key = n.id, text = n.value))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
