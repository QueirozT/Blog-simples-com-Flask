$(() => {
    var timer = null;
    var xhr = null;
    $('.user_popup').hover(
        (e) => {
            // Mouse In
            var elem = $(e.currentTarget);
            timer = setTimeout(() => {
                timer = null;
                hxr = $.ajax( 
                    '/user/' + elem.first().text().trim() + '/popup').done(
                        (data) => {
                            xhr = null;
                            elem.popover({
                                html: true,
                                trigger: 'manual',
                                animation: false,
                                container: elem,
                                content: data
                            }).popover('show', {})
                            elem.children()[1].children[1].innerHTML = data
                            flask_moment_render_all();
                        }
                    );
            }, 1000);
        },
        (e) => {
            // Mouse Out
            var elem = $(e.currentTarget);
            if (timer) {
                clearTimeout(timer);
                timer = null;
            }
            else if (xhr) {
                xhr.abort();
                xht = null
            }
            else {
                elem.popover('hide');
            }
        }
    )
});