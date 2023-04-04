import pandas as pd
from decouple import config
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt


class UtilsEDA:
    @staticmethod
    def create_datadict(dataframe: pd.DataFrame) -> dict:
        data = dict()
        for index, code in enumerate(dataframe["codCBO"].unique()):
            tmp_ = dict(
                round(
                    dataframe.loc[dataframe["codCBO"] == code]
                    .groupby("field")
                    .mean(numeric_only=True),
                    2,
                )["importance"]
            )
            data[code] = {
                dataframe.loc[dataframe["codCBO"] == code]["role"].iloc[0]: tmp_
            }

        return data

    @staticmethod
    def create_dataframe_to_dashboard(datadict: dict) -> pd.DataFrame:
        codes = list()
        roles = list()
        fields = list()
        importances = list()
        for code, first_dict_data in datadict.items():

            for role, second_dict_data in first_dict_data.items():

                for field_knowledge, importance in second_dict_data.items():

                    codes.append(code)
                    roles.append(role)
                    fields.append(field_knowledge.capitalize())
                    importances.append(importance)

        data_ = pd.DataFrame([codes, roles, fields, importances]).T
        data_.columns = ["codCBO", "role", "field_knowledge", "importance"]

        return data_

    @staticmethod
    def plotting_graph(dataframe: pd.DataFrame, code: int) -> sns:
        try:
            plt.figure(figsize=(15, 8))
            sns.barplot(
                data=dataframe.loc[dataframe["codCBO"] == code],
                x="importance",
                y="field_knowledge",
            )
            plt.title(
                label=dataframe.loc[dataframe["codCBO"] == code]["role"].iloc[0],
                fontdict={"weight": "bold", "fontsize": 15},
            )
            plt.xlabel(
                "Importância do Campo do Conhecimento",
                fontdict={"weight": "bold", "fontsize": 12},
            )
            plt.ylabel(
                "Campo do Conhecimento", fontdict={"weight": "bold", "fontsize": 12}
            )
            plt.show()
        except:
            print(
                "Esse código não existe na base de dados atual! Por favor tente outro código."
            )
