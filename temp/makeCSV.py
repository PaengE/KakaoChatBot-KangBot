import pandas as pd
import inquire_all_station as ias
import inquire_all_route as iar

df = pd.DataFrame(iar.route_name_list)
df.to_csv("./res4.csv", header=False, index=False, sep='\n')