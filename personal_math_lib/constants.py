'''
pi, using bellard's formula
This is
pi = 1/(2^6)*
sigma(lower bound=0, upper=inf)of (
((-1)^n)/2^(10n))*(-(2^5)/(4n+1)-(1/(4n+3))+(2^8)/(10n+1)-(2^6)/(10n+3)-(2^2/(10n+5)
-(2^2)/10n+7)+(1/(10n+9))
https://en.wikipedia.org/wiki/Bellard%27s_formula
'''

x = 1 / 2**6
u = 9000 #upper bound
holder = 0

for n in range(10):
    holder += (((-1)**n) / (2**(10*n))) * ( (-1 * ((2**5)/((4*n) + 1))) - (1/((4*n) + 3))\
            + ((2**8)/((10*n) + 1)) - ((2**6)/((10*n) + 3)) - ((2**2)/((10*n) + 5))\
            - ((2**2)/((10*n) + 7)) + (1/((10*n) + 9)) )

PI = x * holder

print(PI)
