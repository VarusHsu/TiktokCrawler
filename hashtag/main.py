import sys

sys.path.append(".")
import internal


def main():
    app = internal.Hashtag()
    app.render()
    pass


if __name__ == '__main__':
    main()
