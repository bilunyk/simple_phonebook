define([

    //libs
    'backbone'

], function(Backbone){

    var Contact = Backbone.Model.extend({

        validation: {
            first_name: {
                required: true,
                msg: 'Please provide first name'
            },
            last_name: {
                required: true,
                msg: 'Please provide last name'
            },
            phone_number: {
                required: true,
                pattern: 'digits',
                maxLength: 12,
                msg: 'Please provide correct phone number'
            }
        }

    });

    return Contact;

});