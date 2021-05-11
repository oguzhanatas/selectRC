#call the funcs
from pack import selectRC
from pack import gaia_match
from pack import vizier_db

#run the funcs

#you can call a catalog from vizier database
merge_data,teff,logg,ra,dec=vizier_db.vizier_db("III/284/allstars")

##you can match all catalog to gaia and bailer-jones
#gaia_match.gaia_match(ra,dec,'sampleGaia.csv')

#you can select RC stars on HR diagram and save the RC data to csv
select_rc=selectRC.hess(merge_data,teff,logg,'sample.csv','sample.png')

#you can match only RC stars to gaia and bailer-jones and save the data
gaia_match.gaia_match(select_rc['ra'],select_rc['dec'],'sampleRCGaia.csv')

#you can use your data when you want to select RC stars in your data
#select_rc=select_rc.hess('yourdata.csv',yourdataTeff,yourdataLogg,'yourOutputName.csv','yourFigure.png')

#you can use your data when you want to match your data to Gaia
#gaia_match.gaia_match(yourdataRA,yourdataDEC,'yourdataCGaia.csv')



