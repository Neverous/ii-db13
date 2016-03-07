$(document).ready(function()
{
    var modal           = $('#modal');
    var modal_dialog    = modal.find('.modal-dialog');
    var modal_content   = modal_dialog.find('.modal-content');
    var modal_body      = modal_content.find('.modal-body');

    $('a.external').click(function(ev)
    {
        ev.preventDefault();
        var url = $(this).attr('href');
        modal_body.html('<iframe width="100%" height="100%" frameborder="0" scrolling="yes" allowtransparency="true" src="'+url+'"></iframe>');
        modal.modal({show: true});
    });

    modal.on('show.bs.modal', function(ev)
    {
        modal_dialog.css({
            'width':    '95%',
            'height':   '95%',
            'padding':  '0'
        });

        modal_content.css({
            'height':           '100%',
            'border-radius':    '0',
            'padding':          '0'
        });

        modal_body.css({
            'width':    'auto',
            'height':   '100%',
            'padding':  '0'
        });
    });
});
