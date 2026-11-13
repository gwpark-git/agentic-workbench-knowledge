"""Hard-sphere contact and virtual-volume pressure estimators.

g_N is normalized using N*rho, with no N/(N-1) correction.
This convention yields the finite-N canonical pressure.
"""
import numpy as np

def cs(phi):
    return (1+phi+phi**2-phi**3)/(1-phi)**3

def mean_sem(x):
    return float(np.mean(x)),float(np.std(x,ddof=1)/np.sqrt(len(x)))

def block_means(x,size):
    n=len(x)//size
    return np.mean(x[:n*size].reshape((n,size)+x.shape[1:]),axis=1)

def contact_series(hist,n,box,width=.002,fit_range=.06,degree=2):
    bins=round(fit_range/width)
    assert bins>degree+1
    lo=np.arange(bins)*width
    hi=lo+width
    radial=((1+hi)**3-(1+lo)**3)/3
    columns=[]
    for power in range(degree+1):
        def integral(x):
            return x**(power+1)/(power+1)+2*x**(power+2)/(power+2)+x**(power+3)/(power+3)
        columns.append((integral(hi)-integral(lo))/radial)
    design=np.array(columns).T
    # Geometry-only weighted least squares: no EOS/theory value enters the fit.
    weight=radial/radial.mean()
    intercept=np.linalg.solve(design.T@(weight[:,None]*design),design.T*weight)[0]
    shell=4*np.pi*radial
    rho=n/box**3
    g_bins=hist[:,:bins]/(.5*n*rho*shell)
    contact=g_bins@intercept
    Z=1+2*np.pi*rho/3*contact
    return Z,contact

def compression_curves(minimum,n,epsilons):
    # e=-ln(V'/V). The compressed configuration is allowed iff
    # r_min*exp(-e/3)>=sigma. There is no trial evolution or force.
    survival=np.mean(minimum[:,None]>=np.exp(epsilons[None,:]/3),axis=0)
    return 1-np.log(survival)/(n*epsilons),survival
