import Image
import ImageChops
import math
import operator
import random
from shaape.node import Node
from shaape.polygon import Polygon
from shaape.opengraph import OpenGraph
import networkx as nx

class TestUtils(object):
    EXPORT_TEST_FILE = 'shaape/tests/generated_images/export_test.png'
    BLUR_INPUT = 'shaape/tests/input/lena.png'
    BLUR_GENERATED_IMAGE = 'shaape/tests/generated_images/blur.png'
    BLUR_EXPECTED_IMAGE = 'shaape/tests/expected_images/blur.png'
    EMPTY_INPUT = 'shaape/tests/input/empty.shaape'
    EMPTY_OUTPUT = 'shaape/tests/generated_images/empty.png'
    EMPTY_CANVAS_GENERATED_IMAGE = 'shaape/tests/generated_images/empty_canvas.png'
    EMPTY_CANVAS_EXPECTED_IMAGE = 'shaape/tests/expected_images/empty_canvas.png'
    POLYGON_GENERATED_IMAGE = 'shaape/tests/generated_images/polygon.png'
    POLYGON_EXPECTED_IMAGE = 'shaape/tests/expected_images/polygon.png'
    POLYGON_SHADOW_GENERATED_IMAGE = 'shaape/tests/generated_images/polygon_shadow.png'
    POLYGON_SHADOW_EXPECTED_IMAGE = 'shaape/tests/expected_images/polygon_shadow.png'
    OPEN_GRAPH_GENERATED_IMAGE = 'shaape/tests/generated_images/open_graph.png'
    OPEN_GRAPH_EXPECTED_IMAGE = 'shaape/tests/expected_images/open_graph.png'
    OPEN_GRAPH_EMPTY_GENERATED_IMAGE = 'shaape/tests/generated_images/open_graph_empty.png'
    OPEN_GRAPH_EMPTY_EXPECTED_IMAGE = 'shaape/tests/expected_images/open_graph_empty.png'
    OPEN_GRAPH_SHADOW_GENERATED_IMAGE = 'shaape/tests/generated_images/open_graph_shadow.png'
    OPEN_GRAPH_SHADOW_EXPECTED_IMAGE = 'shaape/tests/expected_images/open_graph_shadow.png'
    OPEN_GRAPH_SHADOW_EMPTY_GENERATED_IMAGE = 'shaape/tests/generated_images/open_graph_shadow_empty.png'
    OPEN_GRAPH_SHADOW_EMPTY_EXPECTED_IMAGE = 'shaape/tests/expected_images/open_graph_shadow_empty.png'
    TEXT_GENERATED_IMAGE = 'shaape/tests/generated_images/text.png'
    TEXT_EXPECTED_IMAGE = 'shaape/tests/expected_images/text.png'
    
    @staticmethod
    def images_equal(image1, image2, acceptable_rms = 30):
        try:
            img1 = Image.open(image1)
            img2 = Image.open(image2)
        except:
            return False
        diff = ImageChops.difference(img1, img2)
        h = ImageChops.difference(img1, img2).histogram()
        sq = (value*((idx%256)**2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares/float(img1.size[0] * img1.size[1]))
        return rms <= acceptable_rms
    
    @staticmethod
    def generate_test_polygon(seed = 0, points = 12, radius_range = (10, 50)):
        random.seed(seed)
        point_list = []
        for i in range(0, points):
            angle = math.radians(i * 360 / points - 180)
            radius = random.randint(*radius_range)
            point = (math.sin(angle) * radius, math.cos(angle) * radius)
            point_list.append(point)
        node_list = [Node(*p) for p in point_list]
        polygon = Polygon(node_list)
        return polygon

    @staticmethod
    def generate_test_opengraph(seed = 0, points = 12, radius_range = (10, 50)):
        random.seed(seed)
        point_list = []
        graph = nx.Graph()
        for i in range(0, points / 2):
            angle1 = math.radians(i * 360 / points - 180)
            angle2 = math.radians(-1 * (i * 360 / points - 180))
            radius = random.randint(*radius_range)
            point1 = (math.sin(angle1) * radius, math.cos(angle1) * radius)
            point2 = (math.sin(angle2) * radius, math.cos(angle2) * radius)
            graph.add_edge(Node(*point1), Node(0, 0))
            graph.add_edge(Node(*point2), Node(0, 0))
        opengraph = OpenGraph(graph)
        return opengraph

    @staticmethod
    def unordered_lists_equal(a, b):
        return len(a) == len(b) and all(a.count(x) == b.count(x) for x in a)

    __test__ = False
