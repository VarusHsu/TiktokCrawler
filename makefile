play_count:
	./set_default_path.sh \
	&&py2applet --make-setup play_count_info.py \
  	&&python3 setup.py py2app
clear:
	rm -r build dist setup.py generate_path.py
hashtag:
	./set_default_path.sh \
	&&py2applet --make-setup user_by_hashtag.py \
  	&&python3 setup.py py2app
run_play_count:
	./set_default_path.sh \
  	&&python3 ./play_count_info.py
run_hashtag:
	./set_default_path.sh \
	&&python3 ./user_by_hashtag.py
path:
	./set_default_path.sh