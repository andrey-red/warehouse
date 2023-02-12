import sys
import matplotlib.pyplot as plot
from typing import Iterable
from xml.dom.minidom import Element
from svg.path.path import Path
from shapely.geometry import Polygon
from xml.dom import minidom
from svg.path import parse_path, Move, Close, Line


def read_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()


def find_paths(file_path: str) -> Iterable[Element]:
    """ Finds all <path/> elements """
    svg = minidom.parse(file_path)
    return svg.getElementsByTagName('path')


def path_to_polygon(path_id: str, path: Path) -> Polygon:
    assert len(path) > 2, f'path {path_id}: too short'
    assert isinstance(path[0], Move), f'path {path_id}: expected the first segment of path is instance of {Move}'
    assert isinstance(path[-1], Close), f'path {path_id}: expected the last segment of path is instance of {Close}'

    points = []
    for segment in path:
        match segment:
            case Move(): points.append((segment.start.real, segment.start.imag))
            case Line(): points.append((segment.end.real, segment.end.imag))
            case Close(): pass
            case _: raise RuntimeError(f'Unexpected segment type: {type(segment)}')

    return Polygon(points)


def svg_to_shapely(svg_file_path: str) -> list[Polygon]:
    polygons = []
    for path in find_paths(svg_file_path):
        if not path.hasAttribute('id'):
            raise RuntimeError('path does not have required `id` attribute')
        if not path.hasAttribute('d'):
            raise RuntimeError('path does not have required `d` attribute')

        path_id = path.getAttribute('id')
        path = parse_path(path.getAttribute('d'))
        poly = path_to_polygon(path_id, path)
        polygons.append(poly)

    return polygons


def main(svg_file_path: str) -> None:
    polygons = svg_to_shapely(svg_file_path)
    for poly in polygons:
        plot.plot(*poly.exterior.xy)
    plot.show()


if __name__ == '__main__':
    main('resources/drawing-01.svg')
