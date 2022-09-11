import internalV2
import play_count_internal


def main():
    app = play_count_internal.PlayCountCrawler()
    app.render()
    pass


if __name__ == '__main__':
    main()
