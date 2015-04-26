$('button[class=vote]').click(function(){ // on clicked of the vote element
    var postid;
    postid = $(this).attr("data-postid");
    // Encode the http request with parameters
    $.get('/reddit/vote_post/', {post_id: postid},
        function(data){ //Trigger this function in html
               $('.vote-count[data-postid="'+postid+'"]').html(data); //upload vote-count with the data returned by the request
               $('.vote[data-postid="'+postid+'"]').prop("disabled",true);
        }
    );
});

$('button[class=downvote]').click(function(){ // on clicked of the vote element
    var postid;
    postid = $(this).attr("data-postid");
    // Encode the http request with parameters
    $.get('/reddit/downvote_post/', {post_id: postid},
        function(data){ //Trigger this function in html
               $('.vote-count[data-postid="'+postid+'"]').html(data); //upload vote-count with the data returned by the request
               $('.downvote[data-postid="'+postid+'"]').prop("disabled",true);
        }
    );
});

$("#commenters").on("click", ".reply", function(event){
    event.preventDefault();
    var form = $("#postcomment").clone(true);
    form.find('.parent').val($(this).parent().parent().attr('id'));
    $(this).parent().append(form);
});