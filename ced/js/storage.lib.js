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
        console.log('Saving to localStorage: ' + 'gcm.' + key);
        window.localStorage.setItem('gcm.' + key, value);
    };

    this.get = function(key) {
        console.log('Loading from localStorage: ' + 'gcm.' + key);
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
        console.log('Removing from localStorage: ' + 'gcm.' + key);

        return window.localStorage.removeItem('gcm.' + key);
    };
}

var html5_localstore = new LocalStorage();


function CouchDBStorage() {
    this.username = '';
    this.password = '';
    
    this.save_new = function(object, receiver) {
        var auth_str = btoa(this.username + ':' + this.password);
        
        $.ajax({
            method: 'POST',
            url: '/db/ced',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(object),

            beforeSend: function(xhr) {
                xhr.setRequestHeader('Authorization', 'Basic ' + auth_str);
            },
            
            success: function (doc) {
                console.log('Saved okay...');
                
                if (is_set(receiver)) {
                    receiver(doc);
                }
            },
            error: function (err) {
                notifier.error('Failed to save. Check your credentials!');
                
                console.log('Errored out on save: ' + err);
            }
        });
    };
    
    this.update = function(id, object, receiver) {
        var auth_str = btoa(this.username + ':' + this.password);

        $.ajax({
            method: 'PUT',
            url: '/db/ced/' + id,
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(object),

            beforeSend: function(xhr) {
                xhr.setRequestHeader('Authorization', 'Basic ' + auth_str);
            },
            
            success: function (doc) {
                console.log('Saved okay...');
                
                if (is_set(receiver)) {
                    receiver(doc);
                }
            },
            error: function (err) {
                notifier.error('Failed to save. Check your credentials!');
                
                console.log('Error on update: ' + err);
            }
        });
    };

    this.get = function(key, receiver) {
        var auth_str = btoa(this.username + ':' + this.password);

        $.ajax({
            type: 'GET',
            url: '/db/ced/_design/ced/_view/character-name?key="' + key + '"',
            dataType: 'json',

            beforeSend: function(xhr) {
                xhr.setRequestHeader('Authorization', 'Basic ' + auth_str);
            },

            success: function (doc) {
                receiver(doc.rows[0]);
            },
            error: function (err) {
                notifier.error('Failed to load. Check your credentials!');

                console.log('Error on load: ' + err);
            }
        });
    };

    this.remove = function(key) {
        console.log('Removing from localStorage: ' + 'gcm.' + key);

        return window.localStorage.removeItem('gcm.' + key);
    };
}

var couchdb = new CouchDBStorage();