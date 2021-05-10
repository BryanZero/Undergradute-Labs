import matplotlib
import LT_Fit.parameters as P
import LT_Fit.gen_fit as G
from matplotlib.ticker import FormatStrFormatter
from getData import *

l = 15.2  # length
w = 14.0  # width

d = 61.6  # separation of the plates

N = 10000  # number of rays to generate

# in degree
alpha = 90
factor = 1  # (np.cos(alpha*np.pi/180))**2
rate = 0.66 * factor

beans = 10


def Hit_by_Angle(N, ang):
    hit = 0;
    for i in range(N):

        cost = np.power(np.random.rand(), 1 / 3)

        # The phi distribution is thrown “flat”.

        phi = np.random.rand() * 2 * np.pi

        # place on the top where the ray is going to hit

        x_top = np.random.rand() * w
        y_top = np.random.rand() * l

        # We “know” that this one hits the top scintillator. Now see if it hits the bottom one.
        # Coordinate system: Z is up, B is wrt. Z-axis, 4 around it. X is in the “width” direction,
        # Y in the “length” direction. Given cos 0 and 0, see if the cosmic hits the panel at the bottom. For this to be true,
        # first calculate the direction tangents in x and y.

        sinp = np.sin(phi);
        cosp = np.cos(phi);

        sint = np.sqrt(1 - cost * cost)

        tant = sint / cost;

        tantx = tant * sinp;
        tanty = tant * cosp;
        # Extrapolate to the bottom counter

        xbot = x_top - tantx * d;
        ybot = y_top - tanty * d;

        # if the ray hit the bottom plate then the coodenates (x_bot ; y_bot) should be inside of the box [(0-w) ; (0-l)], which define the superfice of the bottom plate

        if xbot <= w * np.cos(ang) and xbot >= 0 and ybot <= l * np.cos(ang) and ybot >= 0:
            hit += 1;
    return hit;


x = np.linspace(-1 * np.pi / 2, np.pi / 2, 46)
y = [Hit_by_Angle(10000, k) for k in x]
dy = np.sqrt(y)/max(y)
y = y/np.max(y)

f,ax = B.pl.subplots(1,num='Cosmic_Ray_Simulation')
B.plot_exp(x, y, dy)

A = P.Parameter(250., 'A')
Bs = P.Parameter(1., 'B')
C = P.Parameter(1., 'C')
D = P.Parameter(1., 'D')


def cosf(x):
    return -1*A() * np.cos(Bs() * x + C()) ** 2 + D()


fit = G.genfit(cosf, [A, Bs, C, D], x=x, y=y)


ax.xaxis.set_major_formatter(FormatStrFormatter('%g $\pi$'))
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=0.5))
B.plot_line(fit.xpl,fit.ypl,color='red',label='$cos^2$ fit')
labels('Angles (radians)','Normalized Counts','Simulated Cosmic Rays',annotate='Fit: $A cos^2(Bx+C)+D$'+"\n"*4,fit=fit,xy=(0.05,.62))
B.pl.legend()
