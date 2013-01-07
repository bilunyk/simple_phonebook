define([

    //libs
    'backbone',
    //deps
    './item'

], function(Backbone, ContactView){

    var View = Backbone.View.extend({

        el: '#phonebookapp',

        events: {
            'click #add-contact': 'createNewContact',
            'focus .contact-input': 'unhighlightErrors'
        },

        initialize: function(){
            _.bindAll(this, 'createNewContact');
            this.first_name = this.$("#fname");
            this.last_name = this.$("#lname");
            this.phone_number = this.$("#pnumber");
            this.collection.on('add', this.addOne, this);
            this.collection.on('reset', this.render, this);
        },

        render: function(){
            this.collection.each(this.addOne, this);
            return this;
        },

        newAttributes: function(){
            return {"first_name": this.first_name.val(),
                    "last_name": this.last_name.val(),
                    "phone_number": this.phone_number.val()};
        },

        addOne: function(contact){
            var view = new ContactView({model: contact});
            $("#contact-list").append(view.render().el);
        },

        clearAttrs: function(){
            this.first_name.val('');
            this.last_name.val('');
            this.phone_number.val('');
        },

        unhighlightErrors: function(){
            var $elements = $(".control-group");
            $elements.each(function(){
                var $element = $(this);
                console.log($element);
                $element.removeClass("error");
                $(".help-inline", $element).text('');
            });
        },

        createNewContact: function(e){
            this.collection.create(this.newAttributes());
            this.clearAttrs();
        }
    });

    return View;

});