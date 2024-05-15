import geopandas as gpd
import random
from shapely.geometry import Point


def generate_random_points_in_polygon(poly, num_points):
    minx, miny, maxx, maxy = poly.bounds
    points = []
    while len(points) < num_points:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if poly.contains(p):
            points.append(p)
    return points


def main():
    melbourne_area = gpd.read_file("melbourne.geojson")
    melbourne_polygon = melbourne_area.geometry.unary_union

    point = generate_random_points_in_polygon(melbourne_polygon, 1)
    return point[0].x, point[0].y
