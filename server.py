import json
import click
from geopy import distance
import math

@click.command()
@click.option('--rloc', prompt='remote (VPN) location', help='2-letter country code.')
def main(rloc):

    # Lat and Lon of Vancouver, BC; and other constants
    CURR_LOC = (49.2827, -123.1207)
    min_dist = math.inf
    best_dat = {'load':100, 'domain': 'nowhere'} # max server load = 50

    with open('server.json') as json_file:
        data = json.load(json_file)
        flag = []

        for dat in data:
            flag.append(dat['flag'])
            if (dat['flag'] == rloc):
                rlatlon = get_latlon(dat['location'])
                curr_dist = get_dist(CURR_LOC, rlatlon)

                if check_dat_valid(curr_dist, min_dist, dat):
                    min_dist = curr_dist
                    best_dat = get_lowest_load(dat, best_dat)

        if (best_dat['load'] == 100):
            print("WARNING: Country code used is likely wrong, please confirm")
            print(set(flag))
            print('Minimum distance (km) from VPN server to CURR_LOC = {:f}'.format(min_dist))
            print('Server load: {:d}'.format(best_dat['load']))
            print('Suggested server: {:s}'.format(best_dat['domain']))
        else:
            print('Minimum distance (km) from VPN server to CURR_LOC = {:f}'.format(min_dist))
            print('Server load: {:d}'.format(best_dat['load']))
            print('Suggested server: {:s}'.format(best_dat['domain']))

def get_latlon(dict):
    lat = dict['lat']
    lon = dict['long']
    return(lat,lon)

def get_dist(lloc, rloc):
    return(distance.distance(lloc, rloc).km) 

def check_dat_valid(curr_dist, min_dist, dat):
    return(curr_dist <= min_dist and check_features(dat['features']))

def check_features(features):
    std_features = {'ikev2': True, 
                    'openvpn_udp': True, 
                    'openvpn_tcp': True, 
                    'socks': False, 
                    'proxy': False, 
                    'pptp': False, 
                    'l2tp': False, 
                    'openvpn_xor_udp': False, 
                    'openvpn_xor_tcp': False, 
                    'proxy_cybersec': False, 
                    'proxy_ssl': True, 
                    'proxy_ssl_cybersec': True, 
                    'ikev2_v6': False, 
                    'openvpn_udp_v6': False, 
                    'openvpn_tcp_v6': False, 
                    'wireguard_udp': True, 
                    'openvpn_udp_tls_crypt': False, 
                    'openvpn_tcp_tls_crypt': False, 
                    'openvpn_dedicated_udp': False, 
                    'openvpn_dedicated_tcp': False, 
                    'skylark': False
                    }
    return(std_features == features)

def get_lowest_load(dat, best_dat):
    if (dat['load'] < best_dat['load']):
        best_dat = dat
    return(best_dat)

if __name__ == '__main__':
    main()
