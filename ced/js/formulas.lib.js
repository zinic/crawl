var GM_ONLY = 'gm_only';

function Formulas() {
    this.get = function(name) {
        return this[name];
    };

    this.monetary_cost = function(value) {
        var sanitized = value.replace(/$/g, '');
        return Math.floor(parseInt(sanitized) / 120);
    };

    var damage_value_cost = function(value) {
        var ival = parseInt(value);
        return Math.floor((ival - 4) / 2);
    };
    this.damage_value_cost = damage_value_cost;

    this.damage_cost = function(value) {
        var die_parts = value.split('d');

        var num = parseInt(die_parts[0]);
        var die = parseInt(die_parts[1]);
        var damage_value = num * die;

        return Math.floor(num + damage_value_cost(damage_value));
    };

    this.damage_resistance_cost = function(value) {
        return value;
    };

    this.base_difficulty_cost = function(value) {
        if (value === GM_ONLY) {
            // The default base difficulty is currently 10, so
            // returning 2 for the cost is the same cost as 10
            return 2;
        }

        var ival = parseInt(value);
        return Math.floor(-1 * (ival - 8));
    };
}

window.formulas = new Formulas();