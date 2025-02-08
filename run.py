from doh.doh import run_dns
from vanilla.vanilla import run_tor_vanilla
from obfs4.obfs4 import run_tor_obfs4

if __name__ == '__main__':
    user_query = int(input('What do you want to parse and check?\n1) DOH servers\n2) TOR bridges (vanilla)\n3) TOR bridges (obfs4)\nChoose number: '))

    if user_query == 1:
        run_dns()
    elif user_query == 2:
        run_tor_vanilla()
    elif user_query == 3:
        run_tor_obfs4()