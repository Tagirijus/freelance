"""The main programm is executed here."""

import npyscreen
# from offer.entries import SimpleEntry


class OfferApp(npyscreen.NPSApp):
    """Main app for the programm."""
    def main(self):
        F  = npyscreen.Form(name = "Welcome to Npyscreen",)
        t  = F.add(npyscreen.TitleText, name = "Text:",)

        F.edit()
