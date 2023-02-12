import dataclasses

from shapely import Polygon, LineString, Point


@dataclasses.dataclass
class Vertex:
    x: float
    y: float


Vertexes = list[Vertex]


@dataclasses.dataclass
class Line:
    start: Vertex
    end: Vertex

    def as_line_string(self):
        return LineString(((self.start.x, self.start.y), (self.end.x, self.end.y)))

    def midpoint(self) -> Point:
        return Point(
            (self.start.x + self.end.x) / 2,
            (self.start.y + self.end.y) / 2
        )


Polygons = list[Polygon]
