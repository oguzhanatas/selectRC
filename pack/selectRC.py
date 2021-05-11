# -*- coding: utf-8 -*-
#May 2021
#this code creates HR diagram from teff and logg. Also, using gaussian distrubution funcs the RC stars area is selected and copy a text file.***
#you can change the func (hess) what you need

import numpy as np
import pandas as pd
import matplotlib

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


def hess(data,teff,logg,outputname,figname):
    x=teff
    y=logg

    rect_scatter = [0.1, 0.15, 0.6, 0.65]
    rect_histx = [0.1, 0.83, 0.6, 0.1]
    rect_histy = [0.78, 0.15, 0.2, 0.65]


    fig=plt.figure()
    fig.set_figheight(7.5)
    fig.set_figwidth(5)

    #putting axes its locations
    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)

    #removing some tick labels
    axHistx.xaxis.set_ticklabels([])
    axHisty.yaxis.set_ticklabels([])

    #rotating some tick labels
    for label in axHisty.xaxis.get_ticklabels():
        label.set_rotation(270)

	# the scatter plot:
    H, xbins, ybins = np.histogram2d(x,y,bins=100)

    with np.errstate(divide='ignore'):
        #sc=axScatter.imshow(np.log10(H.T), origin='lower', extent=[xbins[0], xbins[-1], ybins[0], ybins[-1]],cmap=plt.cm.jet, interpolation="gaussian", aspect='auto',vmin=0,vmax=4)
        xe,ye=np.linspace(min(x),max(x),200),np.linspace(min(y),max(y),200)
        h,xe,ye=np.histogram2d(x,y,(xe,ye))
        xidx=np.clip(np.digitize(x,xe),0,h.shape[0]-1)
        yidx=np.clip(np.digitize(y,ye),0,h.shape[1]-1)
        c=h[xidx,yidx]
        sc=axScatter.scatter(x,y,c=c,norm=matplotlib.colors.LogNorm(vmin=10**0,vmax=10**4),cmap=plt.cm.get_cmap('RdYlBu_r'),ec=None,alpha=0.6,s=1)

    axScatter.set_xlabel(r"T$_{\rm eff}$ (K)",labelpad=10)
    axScatter.set_ylabel("$\log $g (cm/sn$^2$)",labelpad=3)
    axScatter.xaxis.label.set_fontsize(8)
    axScatter.yaxis.label.set_fontsize(8)
	
    axScatter.set_xlim([3000,8500])
    axScatter.set_ylim([0.,6.])

    #inverting axis
    axScatter.invert_xaxis()
    axScatter.invert_yaxis()


    #creating gaussian functions
    from scipy.optimize import curve_fit
    def gauss(x,mu,sigma,A):
        return A*np.exp(-(x-mu)**2/2/sigma**2)

    def bimodal(x,mu1,sigma1,A1,mu2,sigma2,A2):
        return gauss(x,mu1,sigma1,A1)+gauss(x,mu2,sigma2,A2)
    	
    def trimodal(x,mu1,sigma1,A1,mu2,sigma2,A2,mu3,sigma3,A3):
        return gauss(x,mu1,sigma1,A1)+gauss(x,mu2,sigma2,A2)+gauss(x,mu3,sigma3,A3)

    #teff histogram plot
    y1,x1,_=axHistx.hist(x, bins=np.arange(3000,8500,50), alpha=0.5,color='blue',ec='k',label=str(len(x)))
    x1=(x1[1:]+x1[:-1])/2
	
    #teff distribution funcs	
    expected_t=(4290,405,9500,4817,206,27000,5830,363,17600)
    params_t,cov_t=curve_fit(trimodal,x1,y1,expected_t)
    print("teff parameters (center, fwhm, amplitude): ",*params_t)
    axHistx.plot(x1,trimodal(x1,*params_t),c='red',lw=3)

    #logg histogram plot
    y2,x2,_=axHisty.hist(y, bins=np.arange(0.,6.,0.05), alpha=0.5,color='blue',ec='k', orientation='horizontal')
    x2=(x2[1:]+x2[:-1])/2
    
    #logg distribution funcs
    expected_l=(2.44,1.,7100,2.41,0.07,26100,4.25,0.3,26000)
    params_l,cov_l=curve_fit(trimodal,x2,y2,expected_l)
    print("logg parameters (center, fwhm, amplitude): ",*params_l)
    axHisty.plot(trimodal(x2,*params_l),x2,c='red',lw=3)

    #histogram plot gaussian distribution for every peak
    for ii in [0,3,6]:
        l1=np.linspace(0,6,10000)
        axHisty.plot(gauss(l1,*params_l[ii:ii+3]),l1,c='cyan',lw=1)
        t1=np.linspace(3000,9000,10000)
        axHistx.plot(t1,gauss(t1,*params_t[ii:ii+3]),c='cyan',lw=1)

    #generate 1sigma ellipse points....
    e_c=(4800,2.4)
    e_w=params_t[4]*2.35
    e_h=params_l[4]*2.35
    angle=0.

	#masking area in the ellipse
    xc=x-e_c[0]
    yc=y-e_c[1]
    cos_ang=np.cos(np.radians(180.-angle))
    sin_ang=np.sin(np.radians(180.+angle))
    xct=xc*cos_ang-yc*sin_ang
    yct=xc*sin_ang+yc*cos_ang
    rad_cc=((xct**2)/(e_w/2.)**2)+((yct)**2/((e_h)/2.)**2)
    print('in ellipse: ',len(np.where(rad_cc<=1.)[0]),' data points')
	
    #plotting the ellipse on figure
    import matplotlib.patches as patches
    g_ellipse = patches.Ellipse(e_c, e_w, e_h, angle=angle, fill=False, edgecolor='black',linestyle='--', linewidth=1,label=str(len(np.where(rad_cc<=1.)[0])))
    axScatter.add_patch(g_ellipse)

    ###############data in ellipse to csv#####################
    select_rc=data.loc[np.where(rad_cc<=1)]
    #print(select_rc)
    select_rc.to_csv('./data_outputs/'+outputname,sep=',',index=False)

    #generating minor and major ticks
    for ii in [axScatter,axHistx,axHisty]: 
        ii.xaxis.set_minor_locator(AutoMinorLocator(5))
        ii.yaxis.set_minor_locator(AutoMinorLocator(5))
        ii.tick_params(which='both', width=0.75)
        ii.tick_params(which='major', length=3.5, labelsize=5)
        ii.tick_params(which='minor', length=2)

    axHistx.set_xlim( axScatter.get_xlim() )
    axHisty.set_ylim( axScatter.get_ylim() )

    #creating color bar for number density scatter
    colorbar_ax = fig.add_axes([0.1, 0.07, 0.6, 0.01])
    fig.colorbar(sc, cax=colorbar_ax,orientation="horizontal")
    colorbar_ax.set_xlabel("log N")
    colorbar_ax.xaxis.label.set_fontsize(8)
    colorbar_ax.tick_params(which='major',labelsize=5)
	
    #setting some labels
    leg2=axHistx.legend(handlelength=0, handletextpad=0, fancybox=True,loc="upper left",prop={"size":7})
    for item2 in leg2.legendHandles:
        item2.set_visible(False)
    axScatter.legend(loc="upper left",prop={"size":7})
    
    #plt.show()
    plt.savefig('./fig_outputs/'+figname,dpi=300,bbox_inches='tight')

    return select_rc


#hess(merge_data,teff,logg,'HR_WithRCStars.png')
