# -*- coding: utf-8 -*-
#May 2021
#this code matchs the input data which contains ra and dec to gaia edr3 and bailer-jones distances.***

from pandas import read_csv
import numpy as np
import os
import warnings
import pandas as pd
warnings.simplefilter('ignore', np.RankWarning)
from progress.bar import Bar

#read the data which is planned to match
#match_data=pd.read_csv('../data_outputs/'+'radec.csv',sep=',',low_memory=True)


#https://dc.zah.uni-heidelberg.de/__system__/dc_tables/list/form JOIN tables
#https://dc.zah.uni-heidelberg.de/tableinfo/gedr3dist.main
#https://gea.esac.esa.int/archive/ sol menude gaiaedr3.gaia_source sekmesini buyutunce kolon isimleri cikiyor
#https://gea.esac.esa.int/archive/documentation/GEDR3/Gaia_archive/chap_datamodel/sec_dm_main_tables/ssec_dm_gaia_source.html#gaia_source-l gaiaedr3 kolon isimleri
import pyvo as vo

def gaia_match(ra_in,dec_in,outputname):
    print('writing gaia edr3 data....')
    gaia_output=open('./data_outputs/'+outputname,'w')
    gaia_output.write('source_id,ra_gaia,dec_gaia,parallax,parallax_error,radial_velocity,radial_velocity_error,pmra,pmra_error,pmdec,pmdec_error,dist_circ,r_med_geo,r_lo_geo,r_hi_geo,phot_g_mean_mag,phot_bp_mean_mag,phot_rp_mean_mag,bp_rp,qg_geo\n')
    service = vo.dal.TAPService("http://dc.zah.uni-heidelberg.de/__system__/tap/run/tap")

    bar = Bar('Processing', max=len(ra_in))
    for ra_in,dec_in in zip(ra_in,dec_in):
        if ra_in>0:
            sql="""SELECT
                source_id, ra, dec, parallax, parallax_error,dr2_radial_velocity,dr2_radial_velocity_error,pmra,pmra_error,pmdec,pmdec_error, SQRT(POWER(ra-{ra:.5f},2)+POWER(dec-({dec:.5f}),2)) AS dist,
                r_med_geo, r_lo_geo, r_hi_geo,
            
                phot_g_mean_mag, phot_bp_mean_mag,phot_rp_mean_mag,
                phot_bp_mean_mag-phot_rp_mean_mag AS bp_rp,
                phot_g_mean_mag-5*LOG10(r_med_geo)+5 AS qg_geo
            
                FROM gedr3dist.main
                JOIN gaia.edr3lite USING (source_id)
                WHERE  1=CONTAINS(
                POINT('ICRS', {ra:.5f}, {dec:.5f}),
                CIRCLE('ICRS',ra, dec, 0.00139))
                ORDER BY dist ASC
                """.format(ra=float(ra_in),dec=float(dec_in))
        #print(sql)
        resultset = service.search(sql)
        if len(resultset)<1:
            resultset=np.repeat('nan',20)
        else:
            resultset=[*resultset[0].values()]

        gaia_output.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(*resultset))
        bar.next()
    print('***completed***')
    bar.finish()