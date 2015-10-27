from pylab import *

def AngMom(body):
    angmom = 0.
    #for y in range(len(body)):
    for i in range(len(body)-1):
        for j in range(i+1,len(body)):
            r = ((body[i].position[1,:]-body[j].position[1,:])**2).sum()
            angmom += ((body[i].mass*body[j].mass * (body[i].velocity[1,:]).sum())*r/(body[i].mass + body[j].mass))
        #angmom += body[y].mass*(-body[y].position[1,0]*body[y].velocity[1,1] + body[y].position[1,1]*body[y].velocity[1,0])
    return angmom

def VCOM(body):
    Vcom = zeros(3) 
    mTot = 0
    VcomTot = zeros(3)
    for x in range(len(body)):
        Vcom += body[x].mass * array(body[x].velocity[0,:])
        mTot += body[x].mass
    for x in range(len(Vcom)):
        VcomTot[x] = Vcom[x]/mTot
    return VcomTot

def Energy(body):
    PE = 0
    KE = 0
    G = (2*pi/365.25)**2
    #G=1
    for i in range(len(body)-1):
        KE += 0.5*(body[i].mass * (body[i].velocity[1,:]*body[i].velocity[1,:]).sum())
        for j in range(i+1,len(body)):
            r = sqrt(((body[j].position[1,:] - body[i].position[1,:])**2).sum())
            PE += - G*body[i].mass*body[j].mass/r
    TE = KE + PE
    return TE

def getplanets(body):
    datainput = []
    datainput = genfromtxt("horizons.txt",delimiter = ',',dtype = None) 
    x=0
    for rows in body:
        body[x].name = datainput[x][0]
        body[x].position[0,0] = datainput[x][1]
        body[x].position[0,1] = datainput[x][2]
        body[x].position[0,2] = datainput[x][3]
        body[x].velocity[0,0] = datainput[x][4]
        body[x].velocity[0,1] = datainput[x][5]
        body[x].velocity[0,2] = datainput[x][6]
        body[x].mass = datainput[x][7]
        x = x+1
        
        
def grav_accl(body):
    for i in range(len(body)):
        body[i].acceleration = [0,0,0]
    G = (2*pi/365.25)**2
    #G = 1
    for i in range(len(body)-1):
        for j in range(i+1,len(body)):
            Position = math.fabs(((body[j].position[1,:] - body[i].position[1,:])**2).sum())
            body[i].acceleration[:] += -(body[i].position[1,:]-body[j].position[1,:])*G*body[j].mass/(Position**1.5)   
            body[j].acceleration[:] += (body[i].position[1,:]-body[j].position[1,:])*G*body[i].mass/(Position**1.5)

class Bodies:
    #def __init__(self,mass, Position, Velocity,acceleration):
    def __init__(self):
        self.name = ' '
        self.mass = 0
        self.position = zeros((3,3))
        self.velocity = zeros((3,3))
        self.acceleration = zeros((3))
    
        
                
initialt = 0
finalt = 9625
N = 15.0*(finalt - initialt)
plotarrayx = []
plotarrayy = []

delt = (finalt - initialt)/(N)



Nbodies = input("input number of bodies")
body = []
plotbody = zeros(Nbodies)
for x in range(0,Nbodies):
    body.append(Bodies())  

getplanets(body)

for x in range(len(body)):
    body[x].position[1,:] = body[x].position[0,:]
    body[x].velocity[1,:] = body[x].velocity[0,:]
    plotarrayx.append([])
    plotarrayy.append([])   

for m in range(len(body)):
    plotarrayx[m].append(body[m].position[0,0])
    plotarrayy[m].append(body[m].position[0,1])
energy = []
steps = []
angMom = []
VelCom = zeros(3)
steps.append(initialt)
steps.append(initialt + delt)
steps.append(initialt + 2*delt)
for i in range(2,int(N)+1):
    steps.append(initialt + i*delt)
energy1 = Energy(body)
AngularM1 = AngMom(body)


energy.append(Energy(body)- energy1)
angMom.append(AngMom(body)- AngularM1)


#Euler in the first step
grav_accl(body)


for x in range(len(body)):
    body[x].position[1,:] = body[x].position[0,:] + delt*array(body[x].velocity[0,:])
    body[x].velocity[1,:] = body[x].velocity[0,:] + delt*array(body[x].acceleration[:]) - VCOM(body)
    plotarrayx[x].append(body[x].position[1,0])
    plotarrayy[x].append(body[x].position[1,1])


energy.append(Energy(body)- energy1)
angMom.append(AngMom(body) - AngularM1)

grav_accl(body)


#time loop starts now
for x in range(int(N)):    
    grav_accl(body)
    for y in range(len(body)):
        body[y].position[2,:] = body[y].position[0,:] + 2*delt*array(body[y].velocity[1,:])
        body[y].velocity[2,:] = body[y].velocity[0,:] + 2*delt*array(body[y].acceleration[:]) - VCOM(body)
    for m in range(len(body)):
        body[m].position[0,:] =  body[m].position[1,:] 
        body[m].position[1,:] =  body[m].position[2,:] 
        body[m].velocity[0,:] =  body[m].velocity[1,:] 
        body[m].velocity[1,:] =  body[m].velocity[2,:] 
        plotarrayx[m].append(body[m].position[1,0])
        plotarrayy[m].append(body[m].position[1,1])
    energyt = Energy(body)
    energy.append(energyt - energy1)
    momentum = AngMom(body)
    angMom.append(momentum - AngularM1)
    #body[:].acceleration = accel
names = []
plots = []
#marker= [',', '_', '-', '+', 's', '*','--','o','^']
figure(1)
for r in range(len(body)):
    plot(plotarrayx[r],plotarrayy[r])
    names.append(body[r].name)
    
    hold('on')
legend(names)
xlabel('X coordinate (AU)')
ylabel('Y coordinate (AU)')
#ylim([-6,6])
hold('off')
#xlim([-6,6])
figure(2)
plot(steps,energy)
ylabel('Change in Energy( E(t) - E(0)) (Nm) ')
xlabel('Time (days)')
figure(3)
plot(steps,angMom)
ylabel('Change in z component of Angular Momentum ( L(t) - L(0)) ')
xlabel('Time (days)')
show()  




'''def AngularMomentum(r,v,m):
    AM = 0.
    for i in range(len(r)):
        for j in range(len(r)):
            if (i != j):
                ra3 = ((r[i,:]-r[j,:])**2).sum() # dot product
        AM += ((m * (v[:,i])).sum())*ra3
    return AM'''
