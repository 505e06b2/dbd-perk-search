const class_name_prefix = "img-character";

export default class Character {
	constructor(id, data) {
		this.id = id;
		this.name = data.name;
		this.role = data.role;
	}
}
