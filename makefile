play_count:
	py2applet --make-setup play_count_info.py \
  	&&python3 setup.py py2app
clear:
	rm -r build dist main.spec setup.py
