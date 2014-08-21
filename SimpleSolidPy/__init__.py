import SimpleSolidPy.container
import SimpleSolidPy.primitives

root_window = SimpleSolidPy.container.FreeCADContainer()

#root_window = SimpleSolidPy.container.EmbeddedContainer()

def preview():
    root_window.start()