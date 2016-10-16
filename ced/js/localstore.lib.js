function LocalStorage() {
    var LocalStorageError = function() {};

    this.is_supported = function() {
        try {
            return 'localStorage' in window && window.localStorage !== null;
        } catch (e) {
            return false;
        }
    };

    this.save = function(key, value) {
        console.log('Saving to localStorage: ' + "gcm." + key);
        window.localStorage.setItem('gcm.' + key, value);
    };

    this.get = function(key) {
        console.log('Loading from localStorage: ' + "gcm." + key);
        return window.localStorage.getItem('gcm.' + key);
    };

    this.save_obj = function(key, value) {
        this.save(key, JSON.stringify(value));
    };

    this.get_obj = function(key) {
        var json = this.get(key);
        if (is_set(json)) {
            try {
                return JSON.parse(json);
            } catch (exception) {
                console.log('Exception encountered trying to parse saved JSON data: ' + exception);
                throw new LocalStorageError();
            }
        }

        return null;
    };

    this.remove = function(key) {
        console.log('Removing from localStorage: ' + "gcm." + key);

        return window.localStorage.removeItem('gcm.' + key);
    };
}

var html5_localstore = new LocalStorage();