import sys
import unittest
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from polygon_helpers.polygon_helpers import is_on_border, is_outside_polygon

inside_zone = {
    'point' : [-122.3631693841, 37.5804219281],
    'coordinates' : [[
        [-122.3561525345, 37.5873025984],
        [-122.3595428467, 37.5885948602],
        [-122.3616886139, 37.5899211055],
        [-122.3638343812, 37.5912813326],
        [-122.3688554764, 37.5875746554],
        [-122.3716449738, 37.5832556334],
        [-122.367181778, 37.5780860808],
        [-122.3595428467, 37.5750930179],
        [-122.3482131959, 37.5847520158],
        [-122.3503589631, 37.5869965331],
        [-122.3561525345, 37.5873025984]
    ]]
}

outside_zone = {
    'point' : [-121.9433529854, 37.3198692754],
    'coordinates' : [[
        [-121.9346809388, 37.3363162561],
        [-121.9624900818, 37.3361797698],
        [-121.9652366639, 37.3046448047],
        [-121.937084198, 37.3049178915],
        [-121.9377708436, 37.3176153316],
        [-121.9515037537, 37.3167962067],
        [-121.9521903992, 37.3260791003],
        [-121.937084198, 37.3264886133],
        [-121.9346809388, 37.3363162561]
    ]]
}

on_border = {
    'point' : [-122.0328712464, 37.3554063306],
    'coordinates' : [[
        [-122.0414543152, 37.3443685049],
        [-122.0328712464, 37.3443685049],
        [-122.0328712464, 37.3576050714],
        [-122.0414543152, 37.3576050714],
        [-122.0414543152,  37.3443685049]
    ]]
}
[]
multiple_zones_outside = {
    'point' : [-122.0328712464, 37.3554063306],
    'coordinates' : [[
        [-122.30946064, 37.5482180883], 
        [-122.3164558411, 37.5387585288], 
        [-122.2977018357, 37.5388265875], 
        [-122.30946064, 37.5482180883]
    ],
    [
        [-122.2871017457, 37.520005999], 
        [-122.2921657563, 37.5125172836], 
        [-122.2823810578, 37.5131300249], 
        [-122.2871017457, 37.520005999]
        ]]
}

multiple_zones_inside = {
    'point' : [-122.2869300843, 37.5148320577],
    'coordinates' : [[
        [-122.30946064, 37.5482180883], 
        [-122.3164558411, 37.5387585288], 
        [-122.2977018357, 37.5388265875], 
        [-122.30946064, 37.5482180883]
    ],
    [
        [-122.2871017457, 37.520005999], 
        [-122.2921657563, 37.5125172836], 
        [-122.2823810578, 37.5131300249], 
        [-122.2871017457, 37.520005999]
        ]]
}

class PolygonHelpersTest(unittest.TestCase):
    
    def test_inside_zone(self):
        res = is_outside_polygon(inside_zone['point'], inside_zone['coordinates'])
        self.assertFalse(res)

    def test_outside_zone(self):
        res = is_outside_polygon(outside_zone['point'], outside_zone['coordinates'])
        self.assertTrue(res)

    def test_on_border(self):
        res = is_outside_polygon(on_border['point'], on_border['coordinates'])
        self.assertFalse(res)
    
    def test_multiple_zones_outside(self):
        res = is_outside_polygon(multiple_zones_outside['point'], multiple_zones_inside['coordinates'])
        self.assertTrue(res)
    
    def test_multiple_zone_inside(self):
        res = is_outside_polygon(multiple_zones_inside['point'], multiple_zones_inside['coordinates'])
        self.assertFalse(res)
    
    def test_is_on_border_true(self):
        x,y = on_border['point']
        polygon = on_border['coordinates'][0]
        flag = False
        for i in range(len(polygon) - 1):
            polygon_x1, polygon_y1 = polygon[i]
            polygon_x2, polygon_y2 = polygon[i+1]
            
            if is_on_border(x, y, polygon_x1, polygon_y1, polygon_x2, polygon_y2):
                flag = True
        
        self.assertTrue(flag)

    def test_is_on_border_false_inside(self):
        x,y = inside_zone['point']
        polygon = inside_zone['coordinates'][0]
        flag = False
        for i in range(len(polygon) - 1):
            polygon_x1, polygon_y1 = polygon[i]
            polygon_x2, polygon_y2 = polygon[i+1]
            
            if is_on_border(x, y, polygon_x1, polygon_y1, polygon_x2, polygon_y2):
                flag = True
        
        self.assertFalse(flag)

    def test_is_on_border_false_outside(self):
        x,y = outside_zone['point']
        polygon = outside_zone['coordinates'][0]
        flag = False
        for i in range(len(polygon) - 1):
            polygon_x1, polygon_y1 = polygon[i]
            polygon_x2, polygon_y2 = polygon[i+1]
            
            if is_on_border(x, y, polygon_x1, polygon_y1, polygon_x2, polygon_y2):
                flag = True
        
        self.assertFalse(flag)

if __name__ == '__main__':
    unittest.main()
    