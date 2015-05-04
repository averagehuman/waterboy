
import sys

from .application import UI, UIError

def main(argv=None):
    argv = argv or sys.argv[1:]
    ui = sys
    try:
        ui = UI()
        ui.run(argv)
    except Exception as e:
        ui.stderr.write("%s\n" % str(e))
        if '--debug' in argv:
            raise
        sys.exit(1)
        
if __name__ == '__main__':
    sys.exit(main())

