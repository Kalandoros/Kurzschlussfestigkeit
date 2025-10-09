from collections import defaultdict
from pathlib import Path
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.precision', 3)

DIRECTORY_NAME = "data"
FILE_NAME = "Leiterseildaten.csv"

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def load_csv_to_df() -> pd.DataFrame:
    file = Path(get_project_root(), DIRECTORY_NAME, FILE_NAME)
    if file:
        raw_data = pd.read_csv(file, header=0, delimiter=";", na_filter=False)
        df = pd.DataFrame(raw_data)
    else:
        print(f"Datei {FILE_NAME} im Dateiordner {DIRECTORY_NAME} konnte nicht gefunden oder geladen werden. Prüfe "
              f"den Pfad {file}!")
        df = pd.DataFrame()
    return df

def convert_df_to_dict(df: pd.DataFrame) -> list[dict]:
    dictionary = df.to_dict(orient='records')
    return dictionary

if __name__ == "__main__":
    # Liefert alle Werte einer Spalte zurück
    print(load_csv_to_df()["Bezeichnung"])

    # Liefert die Bezeichnung eines speziellen Index zurück
    print(load_csv_to_df().at[2, "Bezeichnung"])

    # Liefert den Wert einer Spalte basierend auf dem Index zurück
    print(load_csv_to_df().iloc[2]["Querschnitt eines Teilleiters"])

    #print(load_csv_to_df())

    # list_dict_leiterseile = convert_df_to_dict(load_csv_to_df())
    # dict_leiterseile = list_dict_leiterseile[0]
    #print(list(dict_leiterseile.keys()))
    #print(list(dict_leiterseile.values()))
    #print(dict_leiterseile.get("Bezeichnung"))
    #print(dict_leiterseile["Bezeichnung"])
