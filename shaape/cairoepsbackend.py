from cairobackend import CairoBackend
import cairo
import math
import os
import errno

class CairoEpsBackend(CairoBackend):
    def __init__(self, image_scale = 1.0, image_width = None, image_height = None):
        super(CairoEpsBackend, self).__init__(image_scale, image_width, image_height)
        return

    def blur_surface(self):
        pass

    def new_surface(self, name = None):
        surface = cairo.PSSurface(name, int(math.ceil(self.image_size()[0] + self.margin()[0] + self.margin()[1])), int(math.ceil(self.image_size()[1] + self.margin()[2] + self.margin()[3])))
        surface.set_eps(True)
        return surface

    def export_to_file(self, filename):
        path = os.path.dirname(filename)
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        surface = self.new_surface(filename)
        ctx = cairo.Context(surface)
        ctx.set_source_surface(self.surfaces()[-1])
        ctx.paint()
        surface.finish()
        return
