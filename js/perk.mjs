const class_name_prefix = "img-perk";

export default class Perk {
	constructor(id, data) {
		this.id = id;
		this.name = data.name;
		this.role = data.role;
		this.character = data.character;

		let description = data.description;
		for(const i in data.tunables) {
			const x = data.tunables[i];

			const key = `{${i}}`;
			const value = x[x.length - 1];

			description = description.replaceAll(key, `<b class="tunable">${value}</b>`);
		}
		this.description = description;

		this.image_class_prefix = class_name_prefix;

		const image_class_match = data.image.match(/(?<=icons?Perks_)[^\.]+/i);
		if(image_class_match === null) {
			throw `${data.image} is invalid`;
		}
		this.image_class = class_name_prefix + "-" + image_class_match[0].toLowerCase();
	}
}
