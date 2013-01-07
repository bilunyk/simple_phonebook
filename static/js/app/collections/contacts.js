define([

    //libs
    'backbone',
    //deps
    '../models/contact'

], function(Backbone, Contact) {

    var Collection = Backbone.Collection.extend({
        model: Contact,
        url: '/contacts/',
        parse: function(response){
            return response.contacts;
        }
    });

    return Collection;

});
