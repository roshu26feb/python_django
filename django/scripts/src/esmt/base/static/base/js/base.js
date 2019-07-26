   $(document).on('click', '.accordion-toggle', function(e) {
        e.preventDefault();

        var $this = $(this);
        var openedClass = 'glyphicon-minus-sign';
        var closedClass = 'glyphicon-plus-sign';

        if ($this.next().hasClass('show')) {
            var icon = $(this).children().children().children('i:first');
            icon.toggleClass(openedClass + " " + closedClass);
            $(this).children().children().children().find('i:first').toggleClass(openedClass + " " + closedClass);
            $this.next().removeClass('show');
            $this.next().slideUp(350);
        } else {
            $this.parent().parent().find('.indicator').removeClass(openedClass).addClass(closedClass);
            var icon = $(this).children().children().children('i:first');
            icon.toggleClass(openedClass + " " + closedClass);
            $(this).children().children().children().find('i:first').toggleClass(openedClass + " " + closedClass);
            $this.parent().parent().find('li .inner').removeClass('show');
            $this.parent().parent().find('li .inner').slideUp(350);
            $this.next().toggleClass('show');
            $this.next().slideToggle(350);
        }
    });

$(function(){
    $('.collapse').on('shown.bs.collapse', function (e) {
      $('.collapse').not(this).removeClass('in');
    });

    $('[data-toggle=collapse]').click(function (e) {
      $('[data-toggle=collapse]').parent('li').removeClass('active');
      $(this).parent('li').toggleClass('active');
    });
    $('li a').click(function (e) {
        $('a').removeClass('active');
        $(this).addClass('active');
    });
});
