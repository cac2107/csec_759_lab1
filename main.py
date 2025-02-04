# Cole Cirillo
# Lab 1
import os
import math
import random
import scipy
import scipy.special
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

EPSILON = 10000

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
    theta = math.atan2(lat,long)
    return [r, theta]

def convert_to_cart(r, theta):
    long = r * math.cos(theta)
    lat = r * math.sin(theta)
    
    return [long, lat]

def gen_p_r():
    p = random.uniform(0, 1)
    x = (p - 1) / np.exp(1)

    # End of 4.1 in paper states -1 branch of lambertw
    lambert = scipy.special.lambertw(x, -1)
    r = -(1 / EPSILON) * (lambert.real + 1)
    return r

def perturb(long, lat):
    r, theta = convert_to_polar(long, lat)
    p_theta = random.uniform(0, 2*np.pi)
    p_r = gen_p_r()

    new_theta = (theta + p_theta) # % (2*np.pi)
    new_r = r + p_r

    carts = convert_to_cart(new_r, new_theta)

    return [long, lat, carts[0], carts[1]]

def get_token():
    with open("secret.txt", "r") as f: txt = f.read()
    return txt

def plot(coords):
    if len(coords) > 15:
        print("Too many coords to plot")
        return
    
    access_token = get_token()

    points = []
    lines = []
    for c in coords:
        p1 = [c[0], c[1]]
        p2 = [c[2], c[3]]
        points.append(p1)
        points.append(p2)
        lines.append([p1, p2])

    latitudes = [line[0][0] for line in lines] + [line[1][0] for line in lines]
    longitudes = [line[0][1] for line in lines] + [line[1][1] for line in lines]

    center_lat = sum(latitudes) / len(latitudes)
    center_lon = sum(longitudes) / len(longitudes)

    lats, lons = zip(*points)

    text = []
    for i in range(len(points)): text.append(f"Point {i+1}")

    fig = go.Figure(go.Scattermap(
        lat=lats,
        lon=lons,
        mode='markers+text',
        marker=go.scattermap.Marker(size=8, color='blue'),
        text=text,
        textposition="bottom right"
    ))

    for line in lines:
        fig.add_trace(go.Scattermap(
            lat=[line[0][0], line[1][0]],
            lon=[line[0][1], line[1][1]],
            mode='lines',
            line=dict(width=2, color='green'),
        ))

    fig.update_layout(
        mapbox=dict(
            accesstoken=access_token,
            center=go.layout.mapbox.Center(lat=center_lat, lon=center_lon),
            zoom=2,
            style="open-street-map"
        ),
        title="Map of perturbed points"
    )

    fig.show()

def main():
    coords = read_all_files()
    perturbed_coords = []
    for coord in coords:
        p_coord = perturb(coord[1], coord[0])
        perturbed_coords.append(p_coord)

    plot(random.sample(perturbed_coords, k=5))

if __name__ == "__main__":
    main()