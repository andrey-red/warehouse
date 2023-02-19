from itertools import permutations
from typing import Iterator

from shapely import Point, Polygon, MultiPoint, LineString
from shapely.ops import nearest_points

import graphs.converter.svg as svg_converter
from graphs.presentation.tk import Presenter
from graphs.types import Polygons, Vertex, Line


def _vertex_iterator(disruptions: Polygons) -> Iterator[Point]:
    for disruption in disruptions:
        for vertex in disruption.exterior.coords[1:]:
            yield Point(vertex)


def _vertex_to_disruption_pairs(disruptions: Polygons) -> Iterator[tuple[Point, Polygon]]:
    for (disruption1, disruption2) in permutations(disruptions, 2):
        for vertex_point in disruption1.exterior.coords[1:]:
            yield Point(vertex_point), disruption2


def _base_lines(disruptions: Polygons) -> Iterator[Line]:
    for (vertex_point, disruption_poly) in _vertex_to_disruption_pairs(disruptions):
        nearest_point, _ = nearest_points(disruption_poly, vertex_point)

        yield Line(
            Vertex(vertex_point.x, vertex_point.y),
            Vertex(nearest_point.x, nearest_point.y))


def _has_intersections(line: Line, polygons: Polygons) -> bool:
    line_string = line.as_line_string()
    for polygon in polygons:
        if not line_string.intersects(polygon):
            continue
        ips = line_string.intersection(polygon)
        match ips:
            case Point(): continue
            case _: return True

    return False


def main(svg_file_path: str) -> None:
    polygons = svg_converter.from_file(svg_file_path)

    presenter = Presenter()
    presenter.add_disruptions(polygons)

    base_points = []
    for line in _base_lines(polygons):
        presenter.add_temp_line(line)
        if not _has_intersections(line, polygons):
            base_points.append(line.midpoint())
            print(f'base: {line}')
            presenter.add_base_line(line)
            presenter.add_base_point(line.midpoint())
    presenter.show()


if __name__ == '__main__':
    main('resources/drawing-01.svg')
