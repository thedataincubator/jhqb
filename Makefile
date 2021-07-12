.PHONY: svelte wheel

svelte: server/jhqb/*.dir

wheel: svelte
	python -m build

# Deep magic to make this search all subfolders.  See
# https://stackoverflow.com/a/21950971
.SECONDEXPANSION:

server/jhqb/%.dir: $$(shell find client/$$* -type f)
	cp -r client/$*/* $@
	touch $@

client/public/build/bundle.js: client/src/*.js client/src/*.svelte client/node_modules
	cd client && npm run build

client/node_modules: client/package.json
	cd client && npm install
