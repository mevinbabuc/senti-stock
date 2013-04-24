#! /usr/bin/python

from numpy import array,zeros, ones
import cPickle as pickle
import web


direct="/var/lib/openshift/512e12ac4382ec1abb000384/app-root/runtime/repo/data/"

db = web.database(dbn='mysql', host="127.7.115.1", db='sentistock', port=3306, user='adminzQa3Yqe', pw='RDKC1VlNyLSg')


def compute_x(y):
    m=len(y)
    x=[]
    for i in range(0,m):
        x.append(i+1)

    # Aligning x for dot product computation with theta 
    aligned_x = ones(shape=(m, 2))
    aligned_x[:, 1] = x

    return aligned_x


# Alpha value set according to the learning
# rate of stocks.
alpha=0.00001

# Iterations set according to least j(theta) variation
iteration=1400000

 
#Initializing theta 
theta = zeros(shape=(2, 1))
 

 # Function for calculating the basic j(theta) equation
def cost_calc(x, y, theta):
    
    
    m = len(y)
 
    pre_val = x.dot(theta).flatten()
 
    square_errors = (pre_val - y) ** 2
 
    J_theta = (1.0 / (2 * m)) * square_errors.sum()
 
    return J_theta
 
 
 # Function for performing batch gradient descent
def batch_gradient_descent(x, y, theta, alpha, iteration):
  
    m = len(y)
    #print x
    J_hist = zeros(shape=(iteration, 1))
 
    for i in range(iteration):
 
        pre_val = x.dot(theta).flatten()

        
        errors_x1 = (pre_val - y) * x[:, 0]
        errors_x2 = (pre_val - y) * x[:, 1]
 
        theta[0][0] -=  alpha * (1.0 / m) * errors_x1.sum() # theta zero computation
        theta[1][0] -=  alpha * (1.0 / m) * errors_x2.sum() # theta one computation
 
        J_hist[i, 0] = cost_calc(x, y, theta)
 
    return theta

def start():
    # Extracting stock data from the input file
    print "Apple data Extraction."
    li=[]
    results = db.query("SELECT * FROM quotes_aapl order by time")
    for i in results:
        li.append(float(i.quote.encode("utf-8")))
    y = array(li)
    aligned_x=compute_x(y)
    pickle.dump(batch_gradient_descent(aligned_x, y, theta, alpha, iteration),open(direct+"theta_Apple.p",'wb'))
    print "Apple values computed."

    print "Google data Extraction."
    li=[]
    results = db.query("SELECT * FROM quotes_goog order by time")
    for i in results:
        li.append(float(i.quote.encode("utf-8")))
    y = array(li)
    aligned_x=compute_x(y)
    pickle.dump(batch_gradient_descent(aligned_x, y, theta, alpha, iteration),open(direct+"theta_google.p",'wb'))
    print "Google values computed."

    print "BAC data Extraction."
    li=[]
    results = db.query( "SELECT * FROM quotes_bac order by time")
    for i in results:
        li.append(float(i.quote.encode("utf-8")))
    y = array(li)
    aligned_x=compute_x(y)
    pickle.dump(batch_gradient_descent(aligned_x, y, theta, alpha, iteration),open(direct+"theta_bac.p",'wb'))
    print "BAC values computed."
    return "Training Finished..."
    
