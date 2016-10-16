function VDoc() {
    var Attribute = function(name, value) {
        this.name = name;
        this.value = value;
    };

    this.attribute = function(name, value) {
        return new Attribute(name, value);
    };
    
    this.unwrap_content = function(content) {
        if (content instanceof Function) {
            return content();
        } else {
            return content;
        }
    };

    this.format_contents = function(tag, contents) {
        var processed = this.join(contents);
        var opening_tag = '<' + tag;

        for (var attribute_name in processed.attributes) {
            opening_tag += ' ' + attribute_name + '="' + processed.attributes[attribute_name] + '"';
        }

        return opening_tag + '>' + processed.content + '</' + tag + '>';
    };

    this.transcribe_args = function(args_obj) {
        var args_array = [];

        // Skip the first arg - it's the options obj
        for (var i = 0; i < args_obj.length; i++) {
            args_array.push(args_obj[i]);
        }

        return args_array;
    };

    this.join = function(contents) {
        var attributes = {};
        var content = '';

        for (var i in contents) {
            var content_obj = this.unwrap_content(contents[i]);

            if (content_obj instanceof Attribute) {
                attributes[content_obj.name] = content_obj.value;
            } else {
                content += content_obj;
            }
        }

        return {
            'content': content,
            'attributes': attributes
        };
    };

    this.br = function() {
        return '<br />';
    };

    this.img = function() {
        return this.format_contents('img', this.transcribe_args(arguments));
    };

    this.a = function() {
        return this.format_contents('a', this.transcribe_args(arguments));
    };

    this.ol = function() {
        return this.format_contents('ol', this.transcribe_args(arguments));
    };

    this.li = function() {
        return this.format_contents('li', this.transcribe_args(arguments));
    };

    this.ul = function() {
        return this.format_contents('ul', this.transcribe_args(arguments));
    };

    this.h1 = function() {
        return this.format_contents('h1', this.transcribe_args(arguments));
    };

    this.h2 = function() {
        return this.format_contents('h2', this.transcribe_args(arguments));
    };

    this.h3 = function() {
        return this.format_contents('h3', this.transcribe_args(arguments));
    };

    this.h4 = function() {
        return this.format_contents('h4', this.transcribe_args(arguments));
    };

    this.h5 = function() {
        return this.format_contents('h5', this.transcribe_args(arguments));
    };

    this.p = function() {
        return this.format_contents('p', this.transcribe_args(arguments));
    };

    this.span = function() {
        return this.format_contents('span', this.transcribe_args(arguments));
    };

    this.div = function() {
        return this.format_contents('div', this.transcribe_args(arguments));
    };
}

var vdoc = new VDoc();