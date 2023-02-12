import matplotlib.pyplot as plot
from shapely import Polygon, Point
from graphs.types import Polygons, Line


class Presenter:
    def __init__(self,
                 draw_temp_lines: bool = False,
                 draw_base_lines: bool = False):
        self.draw_temp_lines = draw_temp_lines
        self.draw_base_lines = draw_base_lines
        self._fig, self._axs = plot.subplots()

    def add_disruptions(self, polygons: Polygons) -> None:
        for poly in polygons:
            self.add_disruption(poly)

    def add_disruption(self, polygon: Polygon) -> None:
        xs, ys = polygon.exterior.xy
        self._axs.fill(xs, ys, alpha=0.5, fc='#6666cc', ec='#333399')

    def add_temp_line(self, line: Line) -> None:
        if not self.draw_temp_lines:
            return

        self._axs.plot(
            (line.start.x, line.end.x),
            (line.start.y, line.end.y),
            color='gray',
            marker='o',
            linestyle='dashed',
            linewidth=1,
            markersize=5
        )

    def add_base_line(self, line: Line) -> None:
        if not self.draw_base_lines:
            return

        self._axs.plot(
            (line.start.x, line.end.x),
            (line.start.y, line.end.y),
            color='green',
            marker='o',
            linestyle='solid',
            linewidth=1,
            markersize=5
        )

    def add_base_point(self, point: Point) -> None:
        self._axs.scatter([point.x], [point.y], s=8, marker='^', color="red", zorder=2)

    @staticmethod
    def show() -> None:
        plot.show()
