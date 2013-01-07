define([

    //libs
    'backbone',
    //deps
    'text!../templates/contacts.html',
    //plugins
    'plugins/backbone-validation'

], function(Backbone, contactsTemplate){

    var View = Backbone.View.extend({

        tagName: 'li',

        template: _.template(contactsTemplate),

        events: {
            'click .remove': 'removeItem',
            'click .edit': 'makeEditable',
            'keypress .editable': 'updateOnEnter'
        },

        initialize: function(){
            Backbone.Validation.bind(this);
            this.model.on('change', this.render, this);
            this.model.on('destroy', this.remove, this);
            this.model.on('validated:invalid', this.errorHandler, this);
        },

        render: function(){
            //this.unhighlightErrors();
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },

        makeEditable: function(e){
            e.preventDefault();
            this.$('.c-fname').removeAttr('disabled').addClass('editable');
            this.$('.c-lname').removeAttr('disabled').addClass('editable');
            this.$('.c-pnumber').removeAttr('disabled').addClass('editable');
        },

        updateOnEnter: function(e){
            if (e.keyCode === 13){
                this.model.set({'first_name': this.$('.c-fname').val(),
                                'last_name': this.$('.c-lname').val(),
                                'phone_number': this.$('.c-pnumber').val()});
                this.model.save();
            }
        },

        removeItem: function(e){
            e.preventDefault();
            this.model.destroy();
        },

        errorHandler: function(model, errors){
            _.each(errors, function(error_text, error_field){
                // highlight all errors
                var $error_el = $("#"+error_field);
                $error_el.addClass("error");
                $("input", $error_el).val('');
                $(".help-inline", $error_el).text(error_text);
            });
            this.model.destroy();
        }
    });

    return View;
});