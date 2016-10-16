window.get_or = function(value, or) {
    return is_set(value) ? value : or;
};

window.is_set = function(value) {
    return value !== null && value !== undefined;
};

window.is_not_set = function(value) {
    return !is_set(value);
};

window.is_empty = function(value) {
    return !is_set(value) || value.length === 0;
};


function lookup(target) {
    var $target = $(target);

    if (!is_set($target)) {
        console.log('No target found with id: ' + target);
    }

    return $target;
}

function toggle_class(target, classname) {
    var $target = lookup(target);

    if (is_set($target)) {
        if ($target.hasClass(classname)) {
            $target.removeClass(classname);
        } else {
            $target.addClass(classname);
        }
    }
}

function add_class(target, classname) {
    var $target = $(target);

    if (is_set($target)) {
        $target.addClass(classname);
    } else {
        console.log('No target found with id: ' + target);
    }
}

function remove_class(target, classname) {
    var $target = $(target);

    if (is_set($target)) {
        $target.removeClass(classname);
    } else {
        console.log('No target found with id: ' + target);
    }
}