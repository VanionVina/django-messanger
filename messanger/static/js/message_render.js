
    '{% if ' + data['message']['username'] + ' != user %}\n' +
    '<li class="left clearfix">\n' +
        '<span class="chat-img pull-left">\n' +
            '<a href="' + data['message']['absolute_url'] + '">\n' +
                '<img src="'+ data['message']['avatar_url'] + '" alt="User Avatar">\n' +
            '</a>\n' +
        '</span>\n' +
        '<div class="chat-body clearfix">\n' +
            '<div class="header">\n' +
                '<a href="'+ data['message']['absolute_url'] +'">\n' +
                    '<strong class="primary-font">\n' +
                        data['message']['username'] +
                    '</strong>\n' +
                '</a>\n' +
                '<small class="pull-right text-muted"><i class="fa fa-clock-o"></i>' + data['mesage'][sended] +  '</small>\n' +
            '</div>\n' +
            '<p>\n' +
                data['message']['text'] +
            '</p>\n' +
        '</div>\n' +
    '{% else %}\n' +
    '<li class="right clearfix">\n' +
        '<span class="chat-img pull-right">\n' +
            '<a href="'+ data['message']['absolute_url'] +'"><img src="'+ data['message']['avatar_url'] +'" alt="User Avatar"></a>\n' +
        '</span>\n' +
        '<div class="chat-body clearfix">\n' +
            '<div class="header">\n' +
                '<a href="'+ data['message']['absolute_url'] +'"><strong class="primary-font">'+ data['message']['username'] +'</strong></a>\n' +
                '<small class="pull-right text-muted"><i class="fa fa-clock-o"></i>'+ data['message']['sended'] + '</small>\n' +
            '</div>\n' +
            '<p>\n' +
                data['messgage']['text'] +
            '</p>\n' +
        '</div>\n' +
    '</li>\n' +
    '{% endif %}'