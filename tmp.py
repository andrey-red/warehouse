from shapely import geometry, wkt, Point

poly1 = geometry.Polygon ([(1, 1), (1, 5), (5, 5), (5, 1)])
poly2 = geometry.Polygon ([(11, 11), (11, 15), (15, 15), (15, 11)])

line1 = geometry.LineString([(1, 1), (8, 4)])
line2 = geometry.LineString([(1, 1), (8, -4)])

tests = [
    ('line1, poly1', line1, poly1),
    ('line1, poly2', line1, poly2),
    ('line2, poly1', line2, poly1),
    ('line2, poly2', line2, poly2),
]

for name, l, p in tests:
    if not l.intersects(p):
        print(f'{name}: no-intersections')
        continue
    ips = l.intersection(p)
    match ips:
        case Point(): print(f'{name}: one point, OK')
        case _: print(f'{name}: multiple points, FAIL')


# for i in ips:
#     print(i.touches(poly.boundary))  # should touch but it doesnt!!!!
#     print(i.relate(poly.boundary))
