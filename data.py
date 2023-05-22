import pandas as pd


class Data:

    def __init__(self):
        self.my_data = pd.DataFrame()

    def create_data(self):  # read the excel file
        self.my_data = pd.read_excel(r"C:\Users\Yoga\PycharmProjects\Flight_deals_pandas\Flights searcher.xlsx")
        return self.my_data

    def update_data(self):  # update the data in the excel
        self.my_data.to_excel(r"C:\Users\Yoga\PycharmProjects\Flight_deals_pandas\Flights searcher.xlsx", index=False)


