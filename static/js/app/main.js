requirejs.config({

    deps: ['main'],

    paths: {
        'backbone': '../libs/backbone',
        'underscore': '../libs/underscore',
        'jquery': '../libs/jquery',
        'text': '../libs/rjs-text',
        'plugins': '../libs/plugins'
    },

    shim: {
        'backbone': {
            deps: ['jquery', 'underscore'],
            exports: 'Backbone'
        },
        'plugins/backbone-validation': ['backbone']
    }

});


require([

    // libs
    'jquery',

    //deps
    'collections/contacts',
    'views/list'

], function($, Collection, ListView){

    var collection = new Collection();
    var view = new ListView({collection: collection});
    collection.fetch();
});