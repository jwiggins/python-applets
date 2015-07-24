import enaml
from enaml.qt.qt_application import QtApplication

from sound_model import SoundModel


def main():
    with enaml.imports():
        from playground_view import PlaygroundWindow

    app = QtApplication()
    model = SoundModel()
    window = PlaygroundWindow(model=model)
    window.show()

    # Start the application event loop
    app.start()


if __name__ == '__main__':
    main()
