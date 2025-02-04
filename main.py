# Cole Cirillo
# Lab 1
import os
import math
import random
import scipy
import scipy.special
import numpy as np

EPSILON = 1

def read_all_files():
    all_coords = []
    for dir in os.listdir("./csec_data/"):
        with open(f"./csec_data/{dir}") as f:
            lines = f.readlines()
        for line in lines:
            coords = line.split(',')
            coords[0] = float(coords[0])
            coords[1] = float(coords[1])
            all_coords.append(coords)
    return all_coords

def convert_to_polar(long, lat):
    r = math.sqrt(long**2 + lat**2)
    theta = math.atan(lat/long)
    return [r, theta]

def convert_to_cart(r, theta):
    long = r * math.cos(theta)
    lat = r * math.sin(theta)
    
    return [long, lat]

def gen_p_r():
    p = random.uniform(0, 1)
    lambert = scipy.special.lambertw((p-1)/np.exp(1))
    r = (-(1/EPSILON)) * (lambert.real + 1)
    return r

def perturb(long, lat):
    r, theta = convert_to_polar(long, lat)
    p_theta = random.uniform(0, 2*np.pi)
    p_r = gen_p_r()

    new_theta = (theta + p_theta) % (2*np.pi)
    new_r = r + p_r

    #print(f"orig: {theta}, New: {new_theta}")

    carts = convert_to_cart(new_r, new_theta)

    return [long, lat, carts[0], carts[1]]

def main():
    coords = read_all_files()
    perturbed_coords = []
    for coord in coords:
        p_coord = perturb(coord[0], coord[1])
        perturbed_coords.append(p_coord)

    for p in perturbed_coords[:30]:
        print(p)

if __name__ == "__main__":
    main()