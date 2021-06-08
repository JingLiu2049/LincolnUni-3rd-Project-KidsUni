function move(obj, attr, target, speed, callback) {
	clearInterval(obj.timer);

	var current = parseInt(getStyle(obj, attr));

	if(current > target) {
		speed = -speed;
	}

	obj.timer = setInterval(function() {

		var oldValue = parseInt(getStyle(obj, attr));

		var newValue = oldValue + speed;

		if((speed < 0 && newValue < target) || (speed > 0 && newValue > target)) {
			newValue = target;
		}

		obj.style[attr] = newValue + "px";

		if(newValue == target) {
			clearInterval(obj.timer);
			callback && callback();
		}

	}, 30);
}

function getStyle(obj, name) {

	if(window.getComputedStyle) {
		return getComputedStyle(obj, null)[name];
	} else {
		return obj.currentStyle[name];
	}

}
function addClass(obj, cn) {

	if(!hasClass(obj, cn)) {
		obj.className += " " + cn;
	}

}

function hasClass(obj, cn) {

	var reg = new RegExp("\\b" + cn + "\\b");

	return reg.test(obj.className);

}

function removeClass(obj, cn) {
	var reg = new RegExp("\\b" + cn + "\\b");

	obj.className = obj.className.replace(reg, "");

}

function toggleClass(obj, cn) {

	if(hasClass(obj, cn)) {
		removeClass(obj, cn);
	} else {
		addClass(obj, cn);
	}

}


function test(text){
	console.log(text,typeof(text));
}
