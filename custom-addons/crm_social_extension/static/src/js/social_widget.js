odoo.define('crm_social_extension.social_widget', function (require) {
'use strict';

var AbstractField = require('web.AbstractField');
var core = require('web.core');
var field_registry = require('web.field_registry');

var QWeb = core.qweb;

/**
 * Social Media Widget for displaying social media links with icons
 */
var SocialMediaWidget = AbstractField.extend({
    className: 'o_field_social_media',
    
    init: function () {
        this._super.apply(this, arguments);
        this.socialPlatforms = {
            facebook: {
                icon: 'fa-facebook',
                color: '#1877f2',
                name: 'Facebook'
            },
            linkedin: {
                icon: 'fa-linkedin',
                color: '#0077b5',
                name: 'LinkedIn'
            },
            twitter: {
                icon: 'fa-twitter',
                color: '#1da1f2',
                name: 'Twitter'
            }
        };
    },

    _render: function () {
        var self = this;
        var $content = $('<div>');
        
        if (this.value) {
            var platform = this._detectPlatform(this.value);
            if (platform && this.socialPlatforms[platform]) {
                var platformData = this.socialPlatforms[platform];
                var $link = $('<a>')
                    .attr('href', this.value)
                    .attr('target', '_blank')
                    .addClass('social_media_link')
                    .css('color', platformData.color);
                
                var $icon = $('<i>')
                    .addClass('fa ' + platformData.icon)
                    .css('margin-right', '5px');
                
                $link.append($icon).append(platformData.name);
                $content.append($link);
            } else {
                // Fallback for unrecognized URLs
                var $link = $('<a>')
                    .attr('href', this.value)
                    .attr('target', '_blank')
                    .text(this.value);
                $content.append($link);
            }
        }
        
        this.$el.empty().append($content);
    },

    _detectPlatform: function (url) {
        if (!url) return null;
        
        if (url.match(/facebook\.com|fb\.com/i)) return 'facebook';
        if (url.match(/linkedin\.com/i)) return 'linkedin';
        if (url.match(/twitter\.com|x\.com/i)) return 'twitter';
        
        return null;
    }
});

field_registry.add('social_media', SocialMediaWidget);

/**
 * Social Profile Completion Widget
 */
var SocialProfileWidget = AbstractField.extend({
    className: 'o_field_social_profile',
    
    _render: function () {
        var self = this;
        var completion = this.value || 0;
        var $content = $('<div>');
        
        if (completion === 100) {
            var $badge = $('<span>')
                .addClass('badge badge-success')
                .html('<i class="fa fa-check-circle"></i> Complete Profile');
            $content.append($badge);
        } else if (completion > 0) {
            var $badge = $('<span>')
                .addClass('badge badge-warning')
                .html('<i class="fa fa-exclamation-circle"></i> ' + Math.round(completion) + '% Complete');
            $content.append($badge);
        } else {
            var $badge = $('<span>')
                .addClass('badge badge-secondary')
                .html('<i class="fa fa-minus-circle"></i> No Social Media');
            $content.append($badge);
        }
        
        this.$el.empty().append($content);
    }
});

field_registry.add('social_profile_completion', SocialProfileWidget);

return {
    SocialMediaWidget: SocialMediaWidget,
    SocialProfileWidget: SocialProfileWidget
};

});
