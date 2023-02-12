import matplotlib.pyplot as plot
import graphs.converter.svg as svg_converter


def main(svg_file_path: str) -> None:
    polygons = svg_converter.from_file(svg_file_path)
    for poly in polygons:
        plot.plot(*poly.exterior.xy)
    plot.show()


if __name__ == '__main__':
    main('resources/drawing-01.svg')
