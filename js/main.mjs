import Perk from "./perk.mjs";
import Character from "./character.mjs";

const perks = {};
{
	const perk_data = await (await fetch("data/perks.json")).json();
	for(const [key, value] of Object.entries(perk_data)) {
		perks[key] = new Perk(key, value);
	}
}

const characters = {};
{
	const character_data = await (await fetch("data/characters.json")).json();
	for(const [key, value] of Object.entries(character_data)) {
		characters[key] = new Character(key, value);
	}
}

function getSortingFunction(dict) {
	return function(key_a, key_b) {
		const a = dict[key_a].name;
		const b = dict[key_b].name;

		if(a < b) {
			return -1;
		} else if(a > b) {
			return 1;
		}

		return 0;
	}
}

{
	for(const elem of document.body.children) {
		if(elem.id === "loading") {
			elem.classList.add("hidden");
		} else {
			elem.classList.remove("hidden");
		}
	}

	const elems = [];

	for(const key of Object.keys(perks).sort(getSortingFunction(perks))) {
		const data = perks[key];

		const container = document.createElement("div");
		container.classList.add("perk", data.role);

			const top = document.createElement("div");
			top.classList.add("top");

				const icon = document.createElement("div");
				icon.classList.add(data.image_class_prefix, data.image_class, "icon");

				const text_container = document.createElement("div");
				text_container.classList.add("text");

					const name = document.createElement("div");
					name.classList.add("name");
					name.innerText = data.name;

					const unique_to = document.createElement("div");
					unique_to.classList.add("unique_to");
					unique_to.innerText = (data.character === null) ? "Each Survivor" : characters[data.character].name;

				text_container.append(name, unique_to);

			top.append(icon, text_container);


		const description = document.createElement("div");
		description.classList.add("description");
		description.innerHTML = data.description;

		container.append(top, description);
		container._cached_innerText = container.innerText.toLowerCase();

		elems.push(container);
	}

	const perk_list = document.querySelector('#perk-list');
	perk_list.append(...elems);

	const search_bar = document.querySelector('#search-bar');
	function inputsChanged() {
		const search_string = (search_bar?.value || "").toLowerCase();
		const selected_type = document.querySelector('#type-row > input:checked')?.value || "all";

		for(const elem of perk_list.children) {
			if(selected_type !== "all") {
				if(elem.classList.contains(selected_type) === false) {
					elem.classList.add("hidden");
					continue;
				}
			}

			if(search_string === "") {
				elem.classList.remove("hidden");
				continue;
			}

			if(elem._cached_innerText.includes(search_string)) {
				elem.classList.remove("hidden");
			} else {
				elem.classList.add("hidden");
			}
		}
	}

	search_bar.oninput = inputsChanged;

	for(const radio_button of document.querySelector('#type-row').children) {
		radio_button.onchange = inputsChanged;
	}

	inputsChanged();
}
