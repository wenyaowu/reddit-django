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

$("#commenters").on("click", ".reply", function(event){ //Place a listener on 'ul', applies to all 'li'
    event.preventDefault(); //Prevent default behavior of the event. (Here, prevent <a> change pages)
    var form = $("#postcomment").clone(true); // Get and clone the form with id=postcomment
    form.find('.parent').val($(this).parent().parent().attr('id'));
    //Find all the element within current selection that match the selector, which is
    //<input class=parent...>, and set that value to id of 'li'
    //which is also the id of the post
    var boo = $(this).parent().find("#postcomment").length
    if (boo!=0){
        $(this).parent().find('form').remove()
    }
    else{
    $(this).parent().append(form);     //append this form with new id to <p> of the link <a class=reply>
    }


    // 'this' represent 'a' element which contains the link
    // this.parrent().parrent() is 'li'
    // this.parent() is 'p'
});

$('.span-shrink').on("click", function(event){
    event.preventDefault();
    var id = this.id
    if (id == 'shrink'){
    $(this).parent().next('#comment-text').hide()
    $(this).text('[+]')
    $(this).attr('id','expend')
    }
    if (id == 'expend'){
    $(this).parent().next('#comment-text').show()
    $(this).text('[-]')
    $(this).attr('id','shrink')
    }
})