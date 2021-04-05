from ics import Calendar, Event
import pandas as pd
import numpy as np
from datetime import datetime


def generate_file(list_of_rows,table):
    
    c = Calendar()

    for event in list_of_rows:
        e = Event()
        if event == 0:
            continue
        
        e.name = table.iloc[event-1]['Holiday']
        e.begin = table.iloc[event-1]['Date']
        c.events.add(e)

    
    with open('./ics_files/your_custom.ics', 'w') as f:
        f.writelines(c)

