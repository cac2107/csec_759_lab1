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

EPSILON = 0.008

def read_all_files():
    # this function reads every file and returns
    # the result in a 2d list format
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

def read_ind_file(name):
    # this function reads individual files and returns
    # the result in a 2d list format
    all_coords = []
    with open(f"./csec_data/{name}") as f:
        lines = f.readlines()
    for line in lines:
        coords = line.split(',')
        coords[0] = float(coords[0])
        coords[1] = float(coords[1])
        all_coords.append(coords)
    return all_coords

def write_file(name, data):
    # This function writes the new data to a csv
    towrite = "longitude,latitude,perturbed_longitude,perturbed_latitude"
    for d in data:
        towrite += "\n" + ",".join(map(str, d))
    with open(f"./perturbed_data/{name}", "w") as f:
        f.write(towrite)

def convert_to_polar(long, lat):
    r = math.sqrt(long**2 + lat**2)
    theta = math.atan2(lat,long)
    return [r, theta]

def convert_to_cart(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    
    return [x, y]

def convert_to_cart_from_deg(long, lat):
    radius = 6371000
    x = radius * np.radians(long)
    y = radius * np.radians(lat)
    return x, y

def convert_to_deg_from_cart(x, y):
    radius = 6371000
    long = np.degrees(x / radius)
    lat = np.degrees(y / radius)

    return long,lat

def gen_p_r():
    # Generates r based on the paper provided
    p = random.uniform(0, 1)
    x = (p - 1) / np.exp(1)

    # End of 4.1 in paper states -1 branch of lambertw
    lambert = scipy.special.lambertw(x, -1)
    r = -(1 / EPSILON) * (lambert.real + 1)
    return r

def perturb(long, lat):
    # Generates random theta
    p_theta = random.uniform(0, 2*np.pi)
    # Generates r
    p_r = gen_p_r()

    # Convert r and theta to cartesian and 
    # then to degrees
    carts = convert_to_cart(p_r, p_theta)
    long2,lat2 = convert_to_deg_from_cart(carts[0], carts[1])

    # Add the generated r and theta to the original
    # coordinates and make sure they are within bounds
    p_long = long2 + long
    p_lat = lat2 + lat
    if (p_long < -90 or p_long > 90 or p_lat < -180 or p_lat > 180):
        return None
    return [long, lat, long2 + long, lat2 + lat]

def get_token():
    try:
        with open("secret.txt", "r") as f: txt = f.read()
        return txt
    except FileNotFoundError:
        print("secret.txt does not exist. Please create file and save API key.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def plot(coords):
    # Plotting using mapbox and plotly
    # In order for this to work, secret.txt must exist
    # with an API key in it.
    if len(coords) > 15:
        print("Too many coords to plot")
        return
    
    access_token = get_token()
    if access_token == None: return

    points = []
    lines = []
    for c in coords:
        p1 = [c[1], c[0]]
        p2 = [c[3], c[2]]
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
            zoom=30,
            style="open-street-map"
        ),
        title="Map of perturbed points"
    )

    fig.show()

def main():
    perturbed_coords_all = []
    for file in os.listdir("./csec_data"):
        ind_coords = read_ind_file(file)
        p_ind_coords = []
        for coord in ind_coords:
            p_coords = perturb(coord[0], coord[1])
            if p_coords == None: continue
            p_ind_coords.append(p_coords)

        write_file(f"perturbed_{file}", p_ind_coords)
        perturbed_coords_all += p_ind_coords

    plot(random.sample(perturbed_coords_all, k=5))

if __name__ == "__main__":
    main()