(function ($) {
    "use strict";
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    var $dropdownToggle = $('.dropdown-toggle', this);
                    if ($dropdownToggle.length) {
                        $dropdownToggle.trigger('click');
                    }
                }).on('mouseout', function () {
                    var $dropdownToggle = $('.dropdown-toggle', this);
                    if ($dropdownToggle.length) {
                        $dropdownToggle.trigger('click').blur();
                    }
                }); 
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }            
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });



    // Courses carousel
    $(".courses-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        loop: true,
        dots: false,
        nav : false,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:2
            },
            768:{
                items:3
            },
            992:{
                items:4
            }
        }
    });

    
})(jQuery);

