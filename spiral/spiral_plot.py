import enaml
from enaml.qt.qt_application import QtApplication

from spiral_model import SpiralModel


def main():
    with enaml.imports():
        from spiral_plot import SpiralWindow

    app = QtApplication()
    model = SpiralModel()
    window = SpiralWindow(model=model)
    window.show()

    # Start the application event loop
    app.start()


if __name__ == '__main__':
    main()
