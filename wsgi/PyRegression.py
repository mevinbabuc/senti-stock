import cPickle as pickle

direct="/var/lib/openshift/512e12ac4382ec1abb000384/app-root/runtime/repo/data/"

def getY(x,name):
    theta=pickle.load(open(name,'rb'))
    return (theta[0][0]+theta[1][0]*x)

def getCompany(name,x):
    if(name =='aapl'):
        return getY(x,direct+'theta_Apple.p')

    if(name =='goog'):
       x = 90 
       return getY(x,direct+'theta_google.p')

    if(name =='bac'):
       x = 135
       return getY(x,direct+'theta_bac.p')

    return -1

