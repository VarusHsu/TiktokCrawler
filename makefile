generate-play-count:
	./script/set_default_path.sh \
	&&py2applet --make-setup ./play_count/main.py \
  	&&python3 setup.py py2app
clear:
	rm -r build dist setup.py ./generate/generate_path.py
generate-hashtag:
	./script/set_default_path.sh \
	&&py2applet --make-setup ./hashtag/main.py \
  	&&python3 setup.py py2app
run-play-count:
	./script/set_default_path.sh \
  	&&python3 ./play_count/main.py
run-hashtag:
	./script/set_default_path.sh \
	&&python3 ./hashtag/main.py
run-client:
	./script/set_default_path.sh \
	&&python3 ./client/main.py
path:
	./script/set_default_path.sh
generate-client:
	./script/set_default_path.sh \
	&&py2applet --make-setup ./client/main.py \
  	&&python3 setup.py py2app