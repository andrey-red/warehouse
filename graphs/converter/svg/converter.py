from svg.path.path import Path
from shapely.geometry import Polygon
from xml.dom import minidom
from svg.path import parse_path, Move, Close, Line
from graphs.converter.types import Polygons


def _path_to_polygon(path_id: str, path: Path) -> Polygon:
    assert len(path) > 2, f'path {path_id}: too short'
    assert isinstance(path[0], Move), f'path {path_id}: expected the first segment of path is instance of {Move}'
    assert isinstance(path[-1], Close), f'path {path_id}: expected the last segment of path is instance of {Close}'

    points = []
    for segment in path:
        match segment:
            case Move(): points.append((segment.start.real, segment.start.imag))
            case Line(): points.append((segment.end.real, segment.end.imag))
            case Close(): pass
            case _: raise RuntimeError(f'Path {path_id}: Unexpected segment type: {type(segment)}')

    return Polygon(points)


def from_string(svg_as_string: str) -> Polygons:
    svg = minidom.parseString(svg_as_string)
    polygons: Polygons = []

    for path in svg.getElementsByTagName('path'):
        assert path.hasAttribute('id'), 'path does not have required `id` attribute'
        assert path.hasAttribute('d'), 'path does not have required `d` attribute'

        path_id = path.getAttribute('id')
        path = parse_path(path.getAttribute('d'))
        poly = _path_to_polygon(path_id, path)
        polygons.append(poly)

    return polygons


def from_file(svg_file: str) -> Polygons:
    with open(svg_file, 'r') as f:
        return from_string(f.read())
