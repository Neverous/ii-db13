$(document).ready(function()
{

$('.garden-grid').each(function()
{
    var grid    = $(this);
    // dragging

    var clicked = false,
        clickX, clickY,
        startX, startY;

    grid.on({
        'mousemove': function(ev)
        {
            if(!clicked) return;
            grid.scrollTop(startY + (clickY - ev.pageY));
            grid.scrollLeft(startX + (clickX - ev.pageX));
        },

        'mousedown': function(ev)
        {
            clicked = true;
            startX = grid.scrollLeft();
            startY = grid.scrollTop();
            clickX = ev.pageX;
            clickY = ev.pageY;
        },
    });

    $(document).on({
        'mouseup': function(ev)
        {
            clicked = false;
        }
    });

    // selectable grid
    if(grid.hasClass('grid-select'))
    {
        var placements_sum = [];
        var events_sum = [];
        function updateShown()
        {
            placements_sum = [];
            events_sum = [];
            var cells = grid.find('.grass>.garden-cell.select');
            if(cells.length <= 0)
            {
                $('a[data-fields]').removeClass('text-muted');
                $('#selected_fields').val('');
                return;
            }

            cells.find('span[data-placement].plant').each(function()
            {
                placements_sum[$(this).data('placement')] = true;
            });

            var selected_fields = '';
            cells.each(function()
            {
                selected_fields += $(this).data('field-id') + ',';
                var events = $(this).data('events');
                if(typeof(events) == "number")
                    events = [events];

                else if(typeof(events) == "string")
                    events = events.split(',');

                else
                    events = [];

                for(key in events)
                {
                    events_sum[events[key]] = true;
                }
            });

            $('#selected_fields').val(selected_fields);

            $('a[data-fields]').addClass('text-muted');
            for(key in placements_sum)
            {
                $('a[data-fields]#placement_link_' + key).removeClass('text-muted');
            }

            for(key in events_sum)
            {
                $('a[data-fields]#event_link_' + key).removeClass('text-muted');
            }
        }

        $('a[data-toggle="toggle"]').click(function(ev)
        {
            $($(this).data('parent')).children('.tab-pane').hide();
            $($(this).attr('href')).show();
        });

        grid.find('.grass>.garden-cell').click(function(ev)
        {
            $(this).toggleClass('select');
            updateShown();
        }).hover(function(ev)
        {
            var placements = $(this).find('span[data-placement].plant');
            var events = $(this).data('events');
            if(typeof(events) == "number")
                events = [events];

            else if(typeof(events) == "string")
                events = events.split(',');

            else
                events = [];

            if(placements.length <= 0 && events.length <= 0)
                return;

            $('a[data-fields].text-danger').removeClass('text-danger');
            placements.each(function()
            {
                $('a[data-fields]#placement_link_' + $(this).data('placement')).addClass('text-danger');
            });

            if(events.length > 0)
            {
                for(key in events)
                {
                    $('a[data-fields]#event_link_' + events[key]).addClass('text-danger');
                }
            }
        },

        function(ev)
        {
            var placements = $(this).find('span[data-placement].plant');
            var events = $(this).data('events');
            if(typeof(events) == "number")
                events = [events];

            else if(typeof(events) == "string")
                events = events.split(',');

            else
                events = [];

            if(placements.length <= 0 && events.length <= 0)
                return;

            $('a[data-fields].text-danger').removeClass('text-danger');
        });

        $('a[data-fields]').click(function(ev)
        {
            grid.find('.grass>.garden-cell.select').removeClass('select');
            var fields = $(this).data('fields').split(';');
            for(key in fields)
            {
                var pt = fields[key].split(',');
                grid.find('.grass>.garden-cell#cell_' + pt[0] + '_' + pt[1]).addClass('select');
            }

            updateShown();
        }).hover(function(ev)
        {
            var fields = $(this).data('fields').split(';');
            if(fields.length <= 0)
                return;

            grid.find('.grass>.garden-cell.hover').removeClass('hover');
            for(key in fields)
            {
                var pt = fields[key].split(',');
                grid.find('.grass>.garden-cell#cell_' + pt[0] + '_' + pt[1]).addClass('hover');
            }
        },

        function(ev)
        {
            var fields = $(this).data('fields').split(';');
            if(fields.length <= 0)
                return;

            grid.find('.grass>.garden-cell.hover').removeClass('hover');
        });

    }

    // editable grid
    if(grid.hasClass('grid-edit'))
    {
        var _left   = 1048576;
        var _right  = -1048576;
        var _top    = -1048576;
        var _bottom = 1048576;

        function createCell(r, c)
        {
            var background  = $('<section>').addClass('garden-cell-background');
            var cell        = $('<article>').addClass('garden-cell').attr('id', 'cell_' + r + '_' + c).appendTo(background);
            var input       = $('<input type="checkbox" name="fields" value="' + r + ',' + c +'" />').hide().appendTo(cell);
            cell.click(checkGridClick);
            return background;
        }

        function createRow(r)
        {
            var row = $('<div>').addClass('garden-row').attr('id', 'row_' + r);
            for(c = _left; c <= _right; ++ c)
                row.append(createCell(r, c));

            return row;
        }

        function checkColumn(c)
        {
            for(r = _top; r >= _bottom; -- r)
                if(grid.children('#row_' + r).find('#cell_' + r + '_' + c).children('input').prop('checked'))
                    return true;

            return false;
        }

        function removeColumn(c)
        {
            for(r = _top; r >= _bottom; -- r)
                grid.children('#row_' + r).find('#cell_' + r + '_' + c).parent().remove();
        }

        function checkRow(r)
        {
            return grid.children('#row_' + r).find('input').filter(function(){return $(this).prop('checked');}).length > 0;
        }

        function removeRow(r)
        {
            grid.children('#row_' + r).remove();
        }

        function checkGridClick(ev)
        {
            var self    = $(this);
            var parent  = self.parent();
            var input   = self.children('input');
            var checked = input.prop('checked') ^ $(ev.target).is('input');
            var pos     = input.val().split(',');
            var y       = parseInt(pos[0]);
            var x       = parseInt(pos[1]);

            input.prop('checked', !checked).change();
            parent.toggleClass('grass');

            // add new row to the top
            if(y == _top && !checked)
                createRow(++ _top).insertBefore(grid.children('#row_' + y));

            // add new row to the bottom
            if(y == _bottom && !checked)
                createRow(-- _bottom).insertAfter(grid.children('#row_' + y));

            // add new column to the left
            if(x == _left && !checked)
            {
                -- _left;
                for(r = _top; r >= _bottom; -- r)
                    createCell(r, _left).insertBefore(grid.children('#row_' + r).find('#cell_' + r + '_' + x).parent());
            }

            // add new column to the right
            if(x == _right && !checked)
            {
                ++ _right;
                for(r = _top; r >= _bottom; -- r)
                    createCell(r, _right).insertAfter(grid.children('#row_' + r).find('#cell_' + r + '_' + x).parent());
            }

            // remove empty rows from the top
            while(_bottom + 4 < _top && !checkRow(_top) && !checkRow(_top - 1))
                removeRow(_top --);

            // remove empty rows from the bottom
            while(_bottom + 4 < _top && !checkRow(_bottom) && !checkRow(_bottom + 1))
                removeRow(_bottom ++);

            // remove empty columns from the left
            while(_left + 4 < _right && !checkColumn(_left) && !checkColumn(_left + 1))
                removeColumn(_left ++);

            // remove empty columns from the right
            while(_left + 4 < _right && !checkColumn(_right) && !checkColumn(_right - 1))
                removeColumn(_right --);
        }

        grid.find('input').each(function()
        {
            var self = $(this);
            var pos = self.val().split(',');
            var y   = parseInt(pos[0]);
            var x   = parseInt(pos[1]);
            _left   = Math.min(_left, x);
            _right  = Math.max(_right, x);
            _top    = Math.max(_top, y);
            _bottom = Math.min(_bottom, y);

            self.hide();
            self.parent().click(checkGridClick);
            if(self.is(':checked'))
                self.parent().parent().toggleClass('grass');
        });
    }
});

});
