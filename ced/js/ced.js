function Character() {
    var aspect_editor = null;

    this.id = null;
    this.rev = null;

    this.data = {
        aspects: {},
        type: 'character',
        ap_total: 0,
        name: '',
        age: '',
        gender: 'Undefined'
    };

    this.edit_aspect = function(name) {
        var $aspect = new Aspect(this.data.aspects[name]);
        aspect_editor = new AspectEditor($aspect);
    };

    this.ap_used = function() {
        var spent = 0;
        $.each(this.data.aspects, function(aspect_name, value) {
            var $aspect = new Aspect(value);
            spent += $aspect.cost();
        });

        return spent;
    };

    this.ap_avail = function() {
        return this.data.ap_total - this.ap_used();
    };

    this.update_from_ui = function() {
        this.data.name = $('#name_input').val();
        this.data.age = $('#age_input').val();
        this.data.gender = $('#gender_input option:selected').val();
        this.data.ap_total = $('#ap_total').val();

        this.save();
    };

    this.add_aspect = function($aspect) {
        this.data.aspects[$aspect.name()] = $aspect.serialize();
        this.save();
    };

    this.remove_aspect = function(name) {
        delete this.data.aspects[name];
        this.save();
    };

    this.load = function(character_name, callback) {
        var _this = this;

        couchdb.get(character_name, function(data) {
            _this.id = data.id;
            _this.rev = data.value._rev;
            _this.data = data.value;

            callback();
        });
    };

    this.save = function() {
        var _this = this;

        if (is_set(this.id)) {
            var doc = $.extend({}, this.data);
            doc._rev = this.rev;

            couchdb.update(this.id, doc, function(resp) {
                _this.rev = resp.rev;
            });
        } else {
            var character_name = this.data.name;
            if (character_name === '' || !is_set(character_name)) {
                alert('Please set a name for the character first then click save to begin.');
                return;
            }

            couchdb.get(character_name, function(data) {
                if (is_set(data)) {
                    alert('A character named "' + character_name + '" already exists. Please load the character before editing.');
                } else {
                    couchdb.save_new(this.data, function(resp) {
                        _this.id = resp.id;
                        _this.rev = resp.rev;
                    });
                }
            });
        }
    };
}

function AspectEditor($aspect) {
    this.render = function() {
        $("#ae_name_input").val($aspect.name());
        $("#ae_description_text").val($aspect.text());

        var list_html = '';
        $aspect.each_effect(function($effect) {
            list_html += vdoc.li(
                vdoc.span(
                vdoc.attribute('class', 'field_name'),
                $effect.descriptor()),
                vdoc.span(':'),
                vdoc.span($effect.value()));
        });

        $('#ae_effects_list').html(vdoc.ul(list_html));
    };

    this.render();
}

function Registry($doc) {
    this.$doc = $doc;
    this.db_login = {
        username: '',
        password: ''
    };
    this.character = new Character();
    this.selected_aspect = null;
    this.aspect_list_filter = null;

    this.set_aspect_list_filter = function(filter) {
        this.aspect_list_filter = filter.toLowerCase();
    };

    this.select_aspect = function(name) {
        // Select the new aspect
        if (is_set(this.selected_aspect) && name === this.selected_aspect) {
            this.selected_aspect = null;
        } else {
            this.selected_aspect = $doc.find_aspect(name);
        }
    };
}

function render() {
    console.log("Rendering...");

    render_aspect_list();
    render_character();
}

function render_character() {
    var character = registry.character;

    $('#ap_total').val(character.data.ap_total);
    $('#ap_avail').html(character.ap_avail());
    $('#ap_used').html(character.ap_used());

    $('#name_input').val(character.data.name);
    $('#age_input').val(character.data.age);
    $('#gender_input').val(character.data.gender);

    var list_html = '';
    $.each(character.data.aspects, function(aspect_name, value) {
        var $aspect = new Aspect(value);

        list_html += vdoc.li(
            vdoc.attribute('class', 'simple_list'),

        // Edit Icon
        vdoc.div(
            vdoc.attribute('class', 'icon_wrapper'),
            vdoc.img(
            vdoc.attribute('onclick', 'wc_edit_character_aspect(\'' + $aspect.name() + '\');'),
            vdoc.attribute('class', 'icon'),
            vdoc.attribute('src', 'images/edit_icon.jpg'),
            vdoc.attribute('height', '24'),
            vdoc.attribute('width', '24'))),

        // Delete Icon
        vdoc.div(
            vdoc.attribute('class', 'icon_wrapper'),
            vdoc.img(
            vdoc.attribute('onclick', 'wc_remove_character_aspect(\'' + $aspect.name() + '\');'),
            vdoc.attribute('class', 'icon'),
            vdoc.attribute('src', 'images/delete_icon.png'),
            vdoc.attribute('height', '24'),
            vdoc.attribute('width', '24'))),

        // Float clear
        vdoc.span(vdoc.attribute('style', 'float: none;')),

        // Character info
        format_character_aspect($aspect));
    });

    $('#character_aspect_list').html(list_html);
}

function wc_update_aspect_list_search() {
    var filter = $("#aspect_list_search_input").val();

    if (is_set(filter)) {
        registry.set_aspect_list_filter(filter);
    } else {
        registry.aspect_list_filter = null;
    }

    render_aspect_list();
}

function wc_select_aspect(name) {
    registry.select_aspect(name);
    render();
}

function wc_load_character() {
    registry.character.load($('#name_input').val(), render);
}

function wc_save_character() {
    registry.character.update_from_ui();
    render();
}

function wc_add_aspect() {
    registry.character.add_aspect(registry.selected_aspect);
    render();
}

function wc_edit_character_aspect(name) {
    $('#modal_pane').removeClass('hidden');
    $('#aspect_editor_pane').removeClass('hidden');
    $('#master_pane').addClass('hidden');

    registry.character.edit_aspect(name);
}

function wc_close_aspect_editor() {
    $('#modal_pane').addClass('hidden');
    $('#aspect_editor_pane').addClass('hidden');
    $('#master_pane').removeClass('hidden');
}

function wc_remove_character_aspect(name) {
    registry.character.remove_aspect(name);
    render();
}

function Requirement(xml) {
    var $requirement = $(xml);

    this.name = function() {
        return $requirement.attr('name');
    };
}

function Detail(xml) {
    var $detail = $(xml);

    this.type = function() {
        return $detail.attr('type');
    };

    this.value = function() {
        return $detail.attr('value');
    };
}

function Effect(xml) {
    var $effect = $(xml);

    this.each_detail = function(reciever) {
        $effect.find('detail').each(function(idx, detail_xml) {
            var $detail = new Detail(detail_xml);
            return reciever($detail);
        });
    };

    this.descriptor = function() {
        return $effect.attr('descriptor');
    };

    this.value = function() {
        return $effect.attr('value');
    };

    this.cost = function() {
        var $descriptor = registry.$doc.find_descriptor(this.descriptor());
        var formula = $descriptor.formula();
        var desc_cost = $descriptor.cost();

        if (is_set(formula)) {
            var formula_func = formulas.get(formula);
            return formula_func(this.value());
        }

        if (is_set(desc_cost)) {
            return parseInt(desc_cost);
        }

        var $desc_value = $descriptor.find_value(this.value());
        return parseInt($desc_value.cost());
    };
}

function Aspect(xml) {
    var $aspect = $(xml);

    this.serialize = function() {
        return $aspect[0].outerHTML;
    };

    this.cost = function() {
        var cost = 0;
        this.each_effect(function($effect) {
            cost += $effect.cost();
        });

        return cost;
    };

    this.id = function() {
        var name = $aspect.attr('name');
        var formated = name.toLowerCase().replace(/ /g, '_');

        return 'aspect_id_' + formated;
    };

    this.html_id = function() {
        return '#' + this.id();
    };

    this.name = function() {
        return $aspect.attr('name');
    };

    this.text = function() {
        return $aspect.find('text').text().trim();
    };

    this.each_effect = function(reciever) {
        $aspect.find('effect').each(function(idx, effect_xml) {
            var $effect = new Effect(effect_xml);
            return reciever($effect);
        });
    };

    this.each_requirement = function(reciever) {
        $aspect.find('requirement').each(function(idx, requirement_xml) {
            var $requirement = new Requirement(requirement_xml);
            return reciever($requirement);
        });
    };
}

function DescriptorValue(xml) {
    var $desc_value = $(xml);

    this.name = function() {
        return $desc_value.attr('name');
    };

    this.cost = function() {
        return $desc_value.attr('cost');
    };
}

function Descriptor(descriptor_xml) {
    var $descriptor = $(descriptor_xml);

    this.each_value = function(reciever) {
        $descriptor.find('value').each(function(idx, value_xml) {
            var $desc_value = new DescriptorValue(value_xml);
            return reciever($desc_value);
        });
    };

    this.find_value = function(name) {
        var found;
        this.each_value(function($desc_value) {
            if ($desc_value.name() === name) {
                found = $desc_value;
                return false;
            }

            return true;
        });
        return found;
    };

    this.cost = function() {
        return $descriptor.attr('cost');
    };

    this.formula = function() {
        return $descriptor.attr('formula');
    };

    this.name = function() {
        return $descriptor.attr('name');
    };
}

function CoreDocument(xml_data) {
    var $core_xml = $(xml_data);

    this.each_descriptor = function(reciever) {
        $core_xml.find('descriptor').each(function(idx, descriptor_xml) {
            var $descriptor = new Descriptor(descriptor_xml);
            return reciever($descriptor);
        });
    };

    this.find_descriptor = function(name) {
        var found;

        this.each_descriptor(function($descriptor) {
            if ($descriptor.name() === name) {
                found = $descriptor;
                return false;
            }

            return true;
        });

        return found;
    };

    this.each_aspect = function(reciever) {
        $core_xml.find('aspect').each(function(idx, aspect_xml) {
            var $aspect = new Aspect(aspect_xml);
            return reciever($aspect);
        });
    };

    this.find_aspect = function(name) {
        var found;

        this.each_aspect(function($aspect) {
            if ($aspect.name() === name) {
                found = $aspect;
                return false;
            }

            return true;
        });

        return found;
    };
}

function format_character_aspect($aspect) {
    return vdoc.div(
        vdoc.attribute('class', 'formatted_aspect'),
        vdoc.h3(
        vdoc.a(
        vdoc.attribute('href', $aspect.html_id()),
        $aspect.name())),
        vdoc.span('AP Cost: ' + $aspect.cost()),
        vdoc.ul(function() {
        var inner_html = '';

        $aspect.each_effect(function($effect) {
            inner_html += vdoc.li(
                vdoc.span(
                vdoc.attribute('class', 'field_name'),
                $effect.descriptor()),
                vdoc.span(':'),
                vdoc.span($effect.value()));
        });

        return inner_html;
    }));
}

function format_aspect($aspect) {
    return vdoc.div(
        vdoc.attribute('class', 'formatted_aspect'),
        vdoc.h3($aspect.name()),
        vdoc.div(
        vdoc.span('Aspect Point Cost: ' + $aspect.cost()),
        vdoc.br(),
        vdoc.br()),
        vdoc.ul(function() {
        var inner_html = '';

        $aspect.each_effect(function($effect) {
            inner_html += vdoc.li(
                vdoc.span(
                vdoc.attribute('class', 'field_name'),
                $effect.descriptor(), ' (' + $effect.cost() + 'AP): '),
                vdoc.span($effect.value()),
                vdoc.ul(function() {
                var list_html = '';

                $effect.each_detail(function($detail) {
                    var detail_text = $detail.type();

                    switch (detail_text) {
                        case 'inherits_from':
                            detail_text = 'Inherits Modifiers From';
                            break;

                        case 'limit':
                            detail_text = 'Limited';
                            break;
                    }

                    list_html += vdoc.li(
                        vdoc.span(
                        vdoc.attribute('class', 'field_name'),
                        detail_text, ': '),
                        vdoc.span($detail.value()));
                });

                return list_html;
            }));
        });

        return inner_html;
    }),
        vdoc.p($aspect.text()));
}

function render_aspect_list() {
    var $doc = registry.$doc;
    var list_html = '';

    $doc.each_aspect(function($aspect) {
        // Apply the filter before rendering this aspect
        if (is_set(registry.aspect_list_filter)) {
            var aspect_name = $aspect.name().toLowerCase();

            if (!aspect_name.includes(registry.aspect_list_filter)) {
                return;
            }
        }

        list_html += vdoc.li(
            vdoc.attribute('id', $aspect.id()), function() {
            if (is_set(registry.selected_aspect) && registry.selected_aspect.name() === $aspect.name()) {
                return vdoc.attribute('class', 'simple_list selected');
            }

            return vdoc.attribute('class', 'simple_list');
        },
            vdoc.attribute('onclick', 'wc_select_aspect(\'' + $aspect.name() + '\');'),
            format_aspect($aspect));
    });

    $('#aspect_list').html(list_html);
}

function wc_login() {
    couchdb.username = $('#db_login_username').val();
    couchdb.password = $('#db_login_password').val();

    $('#modal_pane').addClass('hidden');
    $('#db_login_pane').addClass('hidden');
    $('#master_pane').removeClass('hidden');

    render();
}

function on_xml_load(xml_data) {
    var registry = new Registry(new CoreDocument(xml_data));
    window.registry = registry;

    $('#modal_pane').removeClass('hidden');
    $('#db_login_pane').removeClass('hidden');
    $('#master_pane').addClass('hidden');
}

function main() {
    $.ajax({
        url: 'https://raw.githubusercontent.com/zinic/crawl/master/core.xml'
    }).done(on_xml_load);
}

$().ready(main);