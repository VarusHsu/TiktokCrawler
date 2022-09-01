play_count:
	py2applet --make-setup play_count_info.py \
  	&&python3 setup.py py2app
clear:
	rm -r build dist setup.py
hashtag:
	py2applet --make-setup user_by_hashtag.py \
  	&&python3 setup.py py2app
run_play_count:
	python3 ./play_count_info.py
run_hashtag:
	python3 ./user_by_hashtag.py