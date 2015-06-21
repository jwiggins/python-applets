import enaml


def main():
    from spiral_canvas import SpiralCanvas
    SpiralCanvas.activate()

    with enaml.imports():
        from spiral_plot import SpiralWindow

    window = SpiralWindow()
    window.show()

if __name__ == '__main__':
    main()
