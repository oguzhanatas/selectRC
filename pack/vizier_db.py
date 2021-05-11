# -*- coding: utf-8 -*-
#May 2021
#this code calls the data from vizier database which selected catalog.***
#you can change the columns what you need

import numpy as np
import pandas as pd
from astroquery.vizier import Vizier
import astropy.units as u


def vizier_db(catalog):
    #getting datas from vizier
    apogee = Vizier(catalog=[catalog],columns=['Teff', 'logg', 'RAJ2000', 'DEJ2000'])
    apogee.ROW_LIMIT=-1
    result_apogee = apogee.query_constraints(Teff='>0', logg='>-2')

    teff=np.array(result_apogee[0]['Teff'])
    logg=np.array(result_apogee[0]['logg'])
    ra=np.array(result_apogee[0]['RAJ2000'])
    dec=np.array(result_apogee[0]['DEJ2000'])
    merge_data=pd.DataFrame({'Teff':teff,'logg':logg,'ra':ra,'dec':dec},index=None)
    return merge_data,teff,logg,ra,dec