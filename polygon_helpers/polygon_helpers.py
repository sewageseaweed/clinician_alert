def is_on_border(x, y, polygon_x1, polygon_y1, polygon_x2, polygon_y2):
    
    #Check if point lies on the line that connects polygon_p1 and polygon_p2
    dxc = x - polygon_x1
    dyc = y - polygon_y1

    dxl = polygon_x2 - polygon_x1
    dyl = polygon_y2 - polygon_y1

    cross = dxc * dyl - dyc * dxl
    
    #Not on line if cross is not 0
    if cross != 0:
        return False
    
    #Check if point is between the two polygon points
    if abs(dxl) >= abs(dyl):
        if dxl > 0:
            return polygon_x1 <= x <= polygon_x2
        else:
            return polygon_x2 <= x <= polygon_x1
    else:
        if dyl > 0:
            return polygon_y1 <= y <= polygon_y2
        else:
            return polygon_y2 <= y <= polygon_y1


'''
TODO:
- have it processed in parallel ?
'''
#Ray casting: if inside a polygon, itll only have 1 intersection. Outside of polygon, itll have 2
def ray_casting(point, polygon):
    intersections = 0
    x, y = point

    for i in range(len(polygon) - 1):
        polygon_x1, polygon_y1 = polygon[i]
        polygon_x2, polygon_y2 = polygon[i+1]

        if is_on_border(x, y, polygon_x1, polygon_y1, polygon_x2, polygon_y2):
            return True
        
        if (y < polygon_y1) != (y < polygon_y2) and x < (polygon_x2 - polygon_x1) * (y - polygon_y1) / (polygon_y2 - polygon_y1) + polygon_x1:
            intersections += 1

    return intersections % 2 == 1

def is_outside_polygon(point, polygons):
    for polygon in polygons:
        if ray_casting(point, polygon):
            return False
    
    return True