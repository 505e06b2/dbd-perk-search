#!/usr/bin/python3

import lupa #apt install python3-lupa / pip install lupa
lua_runtime = lupa.LuaRuntime()
lua_runtime.execute("_G.python = nil")

from pathlib import Path
import urllib.request, shutil

class CSSImageMap:
	def __init__(self):
		self.__css_sprite_size_template = """.img-%s {
	--scaling-factor: 1;
	background-size: calc(%dpx * var(--scaling-factor));
	width: calc(%dpx * var(--scaling-factor));
	height: calc(%dpx * var(--scaling-factor));
}"""
		self.__css_sprite_template = """.img-%s {
	background-image: url('%s');
	background-position-x: calc(%d * var(--scaling-factor) * -%dpx);
	background-position-y: calc(%d * var(--scaling-factor) * -%dpx);
}"""
		self.__buffer = []

	def __str__(self):
		return "\n".join(sorted(self.__buffer))

	def clearBuffer(self):
		self.__buffer = []
		return self

	def addSize(self, img_type, sheet_width, size):
		css_class = self.__css_sprite_size_template % (img_type, sheet_width, size, size)
		self.__buffer.append(css_class)
		return self

	def addEntry(self, id, image_path, x, y, size): #assuming each sprite is square
		css_class = self.__css_sprite_template % (id, image_path, x, size, y, size)
		self.__buffer.append(css_class)
		return self

def createHTTPRequest(url):
	return urllib.request.Request(url, headers={
		"User-Agent": "DBD Loadout Sprites"
	})

def getFandomSpriteModule(module_name):
	request = createHTTPRequest(f"https://deadbydaylight.fandom.com/wiki/Module:{module_name}?action=raw")
	with urllib.request.urlopen(request) as response:
		lua_script = response.read()

	def unrollLuaTables(d):
		py_obj = dict(d)
		for key in py_obj.keys():
			if lupa.lua_type(py_obj[key]) == "table":
				py_obj[key] = unrollLuaTables(py_obj[key])
		return py_obj

	return unrollLuaTables(lua_runtime.execute(lua_script))

def downloadFandomSpriteSheet(module, spritesheet_path):
	request = createHTTPRequest(module["settings"]["url"])
	with urllib.request.urlopen(request) as response:
		with open(spritesheet_path, "wb") as f:
			shutil.copyfileobj(response, f)

def addModuleToImageMap(image_map, module, spritesheet_path, class_prefix, classname_callback=lambda key: None):
	sprite_size = module["settings"]["size"]
	sprite_sheetsize = module["settings"]["sheetsize"]
	sprite_sheetimages = module["ids"]
	sprite_rowlen = sprite_sheetsize // sprite_size

	image_map.addSize(class_prefix, sprite_sheetsize, sprite_size)

	for key, data in sprite_sheetimages.items():
		i = data["pos"] - 1 #lua is not zero-indexed

		x = i % sprite_rowlen
		y = i // sprite_rowlen

		id = classname_callback(key)
		image_map.addEntry(f"{class_prefix}-{id}", spritesheet_path, x, y, sprite_size)

if __name__ == "__main__":
	root = Path(__file__).parent.resolve(strict=True)

	css_output_file = root / "image_map.css"

	def initSpriteModule(module_name, spritesheet_path, image_map, css_class_prefix, css_classname_callback):
		spritesheet_path = Path(spritesheet_path)

		print(f"Getting Module: {module_name}")
		module = getFandomSpriteModule(module_name)

		if not spritesheet_path.exists():
			print("Spritesheet does not exist on disk, downloading...")
			downloadFandomSpriteSheet(module, spritesheet_path)

		print("Generating CSS classes...")
		addModuleToImageMap(image_map, module, spritesheet_path.relative_to(css_output_file.parent), css_class_prefix, css_classname_callback)

		print("Done!")

	image_map = CSSImageMap()

	initSpriteModule(
		module_name="PerksSprite",
		spritesheet_path=root / "perks.png",
		image_map=image_map,
		css_class_prefix="perk",
		css_classname_callback=lambda key: key.split(" ")[-1].lower()
	)

	#character_spritesheet_settings = getFandomSpriteSettings("SurvivorPortraitsSprite")

	with css_output_file.open("w") as f:
		f.write(str(image_map))
