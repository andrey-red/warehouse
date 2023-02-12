from graphs.types import Polygons


def build_graph(disruptions: Polygons) -> None:
    for disruption in disruptions:
        for edge in disruption.exterior.coords:
            print(f'{edge}')
