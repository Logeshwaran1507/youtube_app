$(document).ready(function() {
    $('.bx-menu').click(function(){
        $(".sidebar").toggleClass("close");
    });
    $("#addRow").click(function () {
        var div = '<div class="d-flex inputFormRow">'+
        '<input type="text" class="form-control mt-2" placeholder="Keyword" name="kword" aria-label="Recipient" aria-describedby="button-addon2">'+
        '<button id="removeRow" type="button" class="btn btn-danger mt-2">Remove</button>'+
        '</div>';
        $('.keywords').append(div);
    });
    $('body').on("click","#button-remove",function(){
        $(this).parents(".d-flex").remove();
    });
    $(".action").click(function(){
        $(this).parent().removeClass("btn-dark").addClass("btn-primary");
        $(this).parent().siblings().removeClass("btn-primary").addClass("btn-dark");
        var href = "#"+$(".btn-primary").find(".action").attr("value");
        console.log(href)
        $(href).removeClass("d-none");
        $(href).siblings('div').addClass("d-none");
    })
    $(".keywordForDefault").click(function(){
        $(this).parent().removeClass("btn-dark").addClass("btn-primary");
        $(this).parent().siblings().removeClass("btn-primary").addClass("btn-dark");
        var val=$(this).parent().attr('value');
        console.log(val)
        $(this).parent().parent().siblings(".submit").attr("value",val)
    })
});
$(document).ready(function(){
    $("#search").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#keywords button").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
    $('.sidebar').hover(function(){
        $('.sidebar').removeClass('close');
    });
    $('.keywordTags').hover(function(){
        $('.sidebar').addClass('close');
    });
    $('.delgrp').click(function(){
        grpval=$(this).attr('value');
        $('[name="deleteGroup"]').attr('value',grpval);
    });
    $('.delkw').click(function(){
        kwval=$(this).attr('value');
        $('[name="deleteKeyword"]').attr('value',kwval);
    });
    $('p.title').click(function(){
        vid=$(this).attr('value');
        url=$(this).siblings('iframe').attr('src');
        $('.modal-body').children('iframe').attr('src',url);
        $('[name="bookmark"]').attr('value',vid);
    })
    $('[data-bs-dismiss="modal"]').click(function(){
        $('.modal-body').children('iframe').attr('src',' ');
    })
  });
$(document).on('click', '#removeRow', function () {
    $(this).closest('.inputFormRow').remove();
});
