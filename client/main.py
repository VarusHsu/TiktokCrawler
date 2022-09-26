import sys

sys.path.append(".")
import internal


def main():
    play_count_client_internal = internal.PlayCountClient()
    play_count_client_internal.render()


if __name__ == '__main__':
    main()
